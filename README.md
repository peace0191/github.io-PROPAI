# PROPAI Rebuild

재구성 파일 구성:

- `index.html` : 정적 웹 버전 메인 화면
- `style.css` : 공통 스타일
- `app.js` : 로그인, 탭 전환, 문의 폼, 토스트 동작
- `app.py` : Streamlit 대시보드 버전

## 정적 웹 실행
브라우저에서 `index.html`을 열면 됩니다.

## Streamlit 실행
```bash
pip install streamlit
streamlit run app.py
```

## 다음 연결 추천
1. Firebase Auth 로그인 연결
2. Firestore/Realtime DB 저장
3. 숏츠 업로드 및 이메일/카카오 공유 API 연결
4. 관리자 권한 분리
