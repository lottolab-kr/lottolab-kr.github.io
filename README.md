# 로또 넘버랩

번호별 출현 빈도에 가중치를 두어 중복 없는 10게임을 만들어 주는 로또 6/45 번호 생성기입니다. 정적 사이트라 별도 서버 없이 GitHub Pages로 배포됩니다.

## 구조

```
index.html        공개 생성기 (누구나 접근)
data.json          현재 배포된 통계 (build_data.py가 생성)
data/draws.csv      검증된 당첨 결과 원본 (버전 관리 대상)
tools/build_data.py  draws.csv -> data.json 빌드 스크립트
admin/index.html    새 회차 검증·병합용 로컬 도구 (검색엔진 비노출)
manifest.webmanifest, sw.js, icons/   PWA(홈 화면에 설치) 설정
```

## 새 회차 추가하기

1. `admin/index.html`(배포 후에는 `/admin/` 경로)을 열어 공식 결과를 붙여넣거나 "회차 하나 빠르게 추가" 폼을 씁니다.
2. 검증을 통과하면 `draws.csv`, `data.json` 두 파일을 다운로드합니다.
3. 이 저장소의 `data/draws.csv`를 다운로드한 파일로 덮어쓰고 커밋 · 푸시합니다.
   - 또는 두 파일을 Claude와의 대화에 첨부해 반영을 요청하면 커밋까지 대신 처리합니다.
4. `data/draws.csv`만 바꿨다면 `python3 tools/build_data.py`로 `data.json`을 다시 생성한 뒤 커밋하세요.

## 검증 규칙

- 회차는 1 이상의 정수, 추첨일은 실제 달력 날짜(YYYY-MM-DD)
- 본번호 6개는 1~45 사이 서로 다른 정수, 보너스는 1~45 사이이며 본번호와 중복 불가
- 저장하려는 구간(최소~최대 회차) 안에 빠진 회차가 있으면 저장 거부
- 1회부터 채워지기 전까지는 "부분 구간"으로 표시되며, 그래도 정상적으로 사용할 수 있습니다

## 배포 (GitHub Pages)

저장소 **Settings → Pages**에서 Source를 "Deploy from a branch", Branch를 `main` / `(root)`로 설정하면 `https://<계정>.github.io/lotto-number-lab/`에서 서비스됩니다.

## 광고 배너

`data.json`의 `ads.top` / `ads.bottom`에 `{ enabled, image, link }`를 채우면 공개 화면 상하단에 배너가 노출됩니다. 이미지 파일은 저장소에 올려 상대 경로로 연결하세요(예: `ads/top.png`).

## 앱스토어 배포로 가는 다음 단계

1. 지금 이 정적 사이트를 GitHub Pages(또는 Vercel/Netlify)로 배포 — **완료 후 다음 단계**
2. PWA로 설치 확인 (모바일 브라우저에서 "홈 화면에 추가") — manifest/서비스 워커는 이미 포함되어 있습니다
3. Android: PWA를 TWA(Trusted Web Activity)로 감싸 Google Play Console(1회 25달러)에 등록
4. iOS: Capacitor 등으로 감싸 Apple Developer Program(연 99달러) 계정으로 App Store Connect에 제출

3~4단계는 각 스토어 개발자 계정 개설과 최종 제출을 직접 진행해야 하며, 그 전 단계(코드 패키징, 아이콘/스플래시, 스토어 등록 정보 초안)는 도와드릴 수 있습니다.

## 면책

과거 출현 빈도를 반영한 무작위 조합을 만들 뿐이며, 당첨을 예측하거나 보장하지 않습니다. 매 추첨은 이전 결과와 무관하게 독립적으로 진행됩니다.
