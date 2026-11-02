import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import sharp from 'sharp';
import {parseBlogList,matchBlogKeyword,imageHash,hashDistance,mapConcurrent} from '../server/blog.mjs';
const card = (title,url) => `<div data-template-id="ugcItem"><a href="${url}"><span class="sds-comps-text-type-headline1">${title}</span></a><a href="${url}"><span class="sds-comps-text-type-body1">후기 내용</span></a><a href="${url}"><img src="https://search.pstatic.net/common/?src=abc"/></a></div>`;
test('글 카드 순서로 순위 계산; 썸네일 링크 중복은 순위에서 제외', () => {
 const rows=parseBlogList('<title>키워드 : 네이버 블로그검색</title>'+card('다른 병원','https://blog.naver.com/a/1')+card('썸 블리 의원 후기','https://blog.naver.com/b/2'));
 assert.equal(rows.length,2);assert.equal(matchBlogKeyword(rows,'썸블리의원').rank,2);assert.equal(rows[1].thumbnailUrls.length,1);assert.equal(matchBlogKeyword(rows,'없는 병원').status,'not_found');
});
test('같은 이미지의 축소 JPEG는 pHash 일치; 다른 이미지 배치는 구분',async()=>{
 const original=readFileSync(new URL('../1.png',import.meta.url));const hash=await imageHash(original);
 const resized=await sharp(original).resize(180).jpeg({quality:60}).toBuffer();
 assert.ok(hashDistance(hash,await imageHash(resized))<=6);
 const mirrored=await sharp(original).flop().png().toBuffer();assert.ok(hashDistance(hash,await imageHash(mirrored))>6);
});
test('병렬 비교는 제한을 지키고 입력 순서를 보존',async()=>{
 let active=0,max=0;
 const result=await mapConcurrent([1,2,3,4,5,6,7,8,9],3,async x=>{active++;max=Math.max(max,active);await new Promise(r=>setImmediate(r));active--;return x*2;});
 assert.equal(max,3);assert.deepEqual(result,[2,4,6,8,10,12,14,16,18]);
});
