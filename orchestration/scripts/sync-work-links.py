#!/usr/bin/env python3
"""프로젝트 ↔ 작업 ↔ 회고·근거 문서의 탐색 목차를 현재 체크아웃에서 재생성한다."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- work-links:start -->'
END = '<!-- work-links:end -->'


def link(path: str, label: str) -> str:
    return f'[[{path.removesuffix(".md")}|{label}]]'


def table_link(path: str, label: str) -> str:
    return link(path, label).replace('|', r'\|')


def block(text: str, body: str) -> str:
    replacement = f'{START}\n{body.rstrip()}\n{END}'
    if START in text:
        if END not in text:
            raise ValueError('작업 링크 블록 종료 마커 없음')
        return re.sub(re.escape(START) + r'.*?' + re.escape(END),
                      lambda _: replacement, text, flags=re.S)
    return text.rstrip() + '\n\n' + replacement + '\n'


def render(root: Path, template: str, **values: str) -> str:
    text = (root / 'templates/orchestration' / template).read_text()
    return re.sub(r'<([A-Z_]+)>', lambda m: values[m[1]], text)


def build(root: Path) -> tuple[dict[str, str], list[str]]:
    files = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
        cwd=root, text=True).splitlines()
    docs = sorted({p for p in files if p.endswith('.md') and (root / p).is_file()})
    configs = {}
    for p in sorted((root / 'orchestration/config/projects').glob('*.json')):
        cfg = json.loads(p.read_text())
        document_root = cfg.get('document_root')
        if not document_root or not (root / document_root / 'README.md').is_file():
            raise ValueError(f'{p.name}: 유효한 document_root/README.md가 필요하다')
        configs[p.stem] = document_root

    tasks: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for p in docs:
        parts = Path(p).parts
        if parts[:3] == ('orchestration', 'work', '_archive') and len(parts) >= 6:
            project, slug = parts[3:5]
            folder = '/'.join(parts[:5])
            item = (slug, folder, '아카이브')
            if item not in tasks[project]:
                tasks[project].append(item)
    for p in docs:
        parts = Path(p).parts
        if len(parts) == 4 and parts[:2] == ('orchestration', 'work') and parts[-1] == '_RESUME.md':
            m = re.search(r'^# 재개 노트 — .* \(([^)]+)\)', (root / p).read_text(), re.M)
            if not m:
                raise ValueError(f'{p}: 소속 프로젝트를 읽을 수 없다')
            tasks[m[1]].append((parts[2], str(Path(p).parent), '진행 폴더'))

    outputs: dict[str, str] = {}
    retrospective_tasks: dict[str, list[str]] = defaultdict(list)
    warnings = []
    overview = []
    for project, items in sorted(tasks.items()):
        if project not in configs:
            raise ValueError(f'{project}: 프로젝트 config 없음')
        document_root = configs[project]
        project_readme = f'{document_root}/README.md'
        project_index = f'{document_root}/work-index.md'
        rows = []
        overview.append(f'| {table_link(project_readme, project)} | {table_link(project_index, "작업 목록")} | '
                        f'{sum(s == "진행 폴더" for _, _, s in items)} | '
                        f'{sum(s == "아카이브" for _, _, s in items)} |')
        for slug, folder, state in sorted(items):
            index = f'{folder}/README.md'
            summary = f'{folder}/SUMMARY.md'
            task_docs = [p for p in docs if p.startswith(folder + '/') and p != index]
            retrospective = None
            if summary in task_docs:
                content = (root / summary).read_text()
                pointer = re.match(r'원본:\s*(.+)', content)
                if pointer:
                    original = pointer[1].strip()
                    candidate = original[original.index('para/'):] if 'para/' in original else ''
                    if candidate and (root / candidate).is_file():
                        retrospective = candidate
                    else:
                        warnings.append(f'{folder}: 회고 원본 없음 — {original}')
                else:
                    retrospective = summary
            elif state == '아카이브':
                warnings.append(f'{folder}: SUMMARY.md 없음')
            retro_cell = link(retrospective, '회고') if retrospective else '회고 미확인'
            retro_table = retro_cell.replace('|', r'\|')
            rows.append(f'| {table_link(index, slug)} | {state} | {retro_table} |')
            retro_text = retro_cell
            if not retrospective:
                retro_text += '\n\n회고 원본을 현재 체크아웃에서 확인하지 못했다. '
                retro_text += '아래 당시 기록에서 복구 근거를 확인한다. 완료 여부를 추측하지 않는다.'
            outputs[index] = render(root, 'task-record.md', SLUG=slug,
                                    PROJECT_LINK=link(project_readme, project),
                                    INDEX_LINK=link(project_index, '작업 목록'), STATE=state,
                                    RETROSPECTIVE=retro_text,
                                    DOCUMENTS='\n'.join('- ' + link(p, p[len(folder) + 1:]) for p in task_docs))
            if retrospective and retrospective != summary:
                retrospective_tasks[retrospective].append(link(index, slug))
        outputs[project_index] = render(root, 'work-index.md', PROJECT=project,
                                        PROJECT_LINK=link(project_readme, '프로젝트'), ROWS='\n'.join(rows))
        outputs[project_readme] = block((root / project_readme).read_text(),
                                       render(root, 'project-work-links.md',
                                              INDEX_LINK=link(project_index, '진행 중·완료된 작업 목록')))
    outputs['orchestration/work/README.md'] = render(root, 'work-overview.md', ROWS='\n'.join(overview))
    for retrospective, links in retrospective_tasks.items():
        outputs[retrospective] = block((root / retrospective).read_text(),
            render(root, 'retrospective-work-links.md',
                   TASK_LINKS='\n'.join('- ' + value for value in sorted(set(links)))))
    return outputs, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='파일을 쓰지 않고 목차의 최신 여부 검사')
    parser.add_argument('--paths', action='store_true', help='관리하는 파일 경로만 출력')
    args = parser.parse_args()
    outputs, warnings = build(ROOT)
    if args.paths:
        print('\n'.join(sorted(outputs)))
        return 0
    changed = []
    for path, content in outputs.items():
        p = ROOT / path
        if not p.exists() or p.read_text() != content:
            changed.append(path)
            if not args.check:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
    print(f'작업 연결: 관리 {len(outputs)}개, {"차이" if args.check else "갱신"} {len(changed)}개')
    for warning in warnings:
        print('미확인: ' + warning)
    return int(args.check and bool(changed))


if __name__ == '__main__':
    raise SystemExit(main())
