// 검증 전용 entrypoint — DAY 제품 코드가 아니다(app/ 밖 profile 증거 폴더). 자격증명 · Keychain · 로그인 · 업무 쓰기 없음.
// 같은 iPhone 시뮬레이터의 앱 프로세스(같은 번들 · 같은 Info.plist · ATS 예외 0)에서 public health 하나만 GET 한다.
// 앱 HTTP 와 같은 package:http Client(DayApi 가 쓰는 것) + dart:io HttpClient 두 길로 한 번씩 · 리다이렉트 안 따라감.
//   fvm flutter run -t <이 파일> --no-resident -d <UDID> --dart-define=PROBE_ORIGIN=http://127.0.0.1:11040
// 결과 = 화면 글자 + 앱 sandbox tmp/day-health-probe.txt(상태 코드 · 바이트 수 · 오류 종류만).
import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const _origin = String.fromEnvironment('PROBE_ORIGIN');

Future<String> _viaHttpPackage(Uri uri) async {
  final client = http.Client();
  try {
    final req = http.Request('GET', uri)..followRedirects = false;
    final res = await client.send(req).timeout(const Duration(seconds: 10));
    final body = await res.stream.toBytes().timeout(const Duration(seconds: 10));
    return 'package:http status=${res.statusCode} bytes=${body.length}';
  } catch (e) {
    return 'package:http error=${e.runtimeType}: $e';
  } finally {
    client.close();
  }
}

Future<String> _viaHttpClient(Uri uri) async {
  final client = HttpClient()..connectionTimeout = const Duration(seconds: 10);
  try {
    final req = await client.getUrl(uri);
    req.followRedirects = false;
    final res = await req.close().timeout(const Duration(seconds: 10));
    var n = 0;
    await for (final chunk in res) {
      n += chunk.length;
    }
    return 'dart:io HttpClient status=${res.statusCode} bytes=$n';
  } catch (e) {
    return 'dart:io HttpClient error=${e.runtimeType}: $e';
  } finally {
    client.close(force: true);
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final lines = <String>['probe at ${DateTime.now().toUtc().toIso8601String()}', 'origin=$_origin'];
  if (_origin.isEmpty) {
    lines.add('PROBE_ORIGIN missing');
  } else {
    final uri = Uri.parse('$_origin/health/ready');
    lines.add('GET $uri');
    lines.add(await _viaHttpPackage(uri));
    lines.add(await _viaHttpClient(uri));
  }
  final text = lines.join('\n');
  // ignore: avoid_print
  print('DAY_HEALTH_PROBE\n$text');
  try {
    File('${Directory.systemTemp.path}/day-health-probe.txt').writeAsStringSync('$text\n');
  } catch (_) {}
  runApp(MaterialApp(home: Scaffold(body: SafeArea(child: Padding(padding: const EdgeInsets.all(16), child: Text(text))))));
}
