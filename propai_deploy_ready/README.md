# PROPAI 배포 준비판

이 패키지는 다음까지 포함한 실사용 준비판입니다.
- 웹앱 `index.html`
- 스타일 `style.css`
- 동작 로직 `app.js`
- Streamlit 운영판 `app.py`
- Firebase Hosting 설정 `firebase.json`
- Realtime Database Rules `database.rules.json`
- Firebase 프로젝트 예시 `.firebaserc.example`

## 1) 웹앱 바로 실행
같은 폴더에서 `index.html`을 열면 됩니다.

## 2) Firebase Realtime Database Rules 적용
Firebase CLI 설치 후 아래 순서로 진행하세요.

```bash
npm install -g firebase-tools
firebase login
firebase use propai-dad54
firebase deploy --only database
```

규칙 파일은 `database.rules.json`입니다.

## 3) Hosting 배포
```bash
firebase deploy --only hosting
```

배포 전 확인:
- `index.html`, `style.css`, `app.js`가 루트 폴더에 있어야 함
- `firebase.json`이 같은 폴더에 있어야 함

## 4) Streamlit 운영판 실행
```bash
pip install streamlit pandas requests
streamlit run app.py
```

PowerShell 예시:
```powershell
$env:FIREBASE_DB_URL="https://propai-dad54-default-rtdb.firebaseio.com"
streamlit run app.py
```

## 5) 주의
현재 규칙은 "앱이 바로 동작하도록" 만든 기본 공개형 규칙입니다.
즉, 인증 없이도 `inquiries`, `shorts_requests` 경로의 읽기/쓰기가 가능합니다.
실서비스에서 외부 오남용을 막으려면 다음 단계가 필요합니다.
- Firebase Authentication 도입
- 관리자 쓰기만 허용하는 규칙 분리
- Storage 업로드 분리
- 관리자 승인 워크플로 추가

## 6) 추천 다음 단계
- 카카오 로그인 실연동
- Firebase Auth 연결
- Storage 업로드 연결
- 관리자 승인 후 공개되는 구조로 변경
