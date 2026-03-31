# PROPAI Firebase 최종판

이 패키지는 업로드하신 기존 HTML에 들어 있던 Firebase 설정값을 반영한 최종판입니다.

## 포함 파일
- `index.html` : 모바일 웹앱
- `style.css` : 스타일
- `app.js` : Firebase/localStorage 동작 로직
- `app.py` : Streamlit 운영 대시보드
- `.env.example` : Streamlit용 환경변수 예시

## 이미 반영된 Firebase 웹 설정
- Project ID: `propai-dad54`
- Realtime DB: `https://propai-dad54-default-rtdb.firebaseio.com`

## 웹앱 실행
1. 같은 폴더에서 `index.html`을 엽니다.
2. Firebase Realtime Database 규칙이 웹 읽기/쓰기를 허용하면 바로 저장됩니다.
3. 규칙이 막혀 있으면 브라우저에서 데모 모드처럼 보일 수 있습니다.

## Streamlit 실행
```bash
pip install streamlit pandas requests
streamlit run app.py
```

## Streamlit에서 Firebase 연결
Windows PowerShell:
```powershell
$env:FIREBASE_DB_URL="https://propai-dad54-default-rtdb.firebaseio.com"
streamlit run app.py
```

## 주의
- 현재 웹앱은 Firebase **Realtime Database** 기준입니다.
- 파일 업로드(사진/영상)는 아직 Storage 실연동 전 단계입니다.
- Realtime Database Rules가 너무 넓게 열려 있으면 보안 위험이 있습니다.
