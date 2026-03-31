from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="PROPAI", page_icon="🏙️", layout="wide")

# ---------- Theme helpers ----------
CUSTOM_CSS = """
<style>
:root {
  --bg: #08101c;
  --card: #132238;
  --line: rgba(255,255,255,.08);
  --text: #eef4fb;
  --muted: #94a3b8;
  --gold: #d4af57;
  --jade: #34d399;
  --blue: #60a5fa;
}
.stApp {
  background: linear-gradient(180deg, #050a13, #08101c 18%, #08101c 100%);
  color: var(--text);
}
.block-container {
  max-width: 1200px;
  padding-top: 1.2rem;
  padding-bottom: 5rem;
}
div[data-testid="stMetric"] {
  background: #122033;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 12px 16px;
}
div[data-testid="stMetric"] label {
  color: var(--muted) !important;
}
.card {
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.015));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px;
}
.small { color: var(--muted); font-size: .9rem; line-height: 1.7; }
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: .72rem;
  font-weight: 700;
  background: rgba(212,175,87,.12);
  border: 1px solid rgba(212,175,87,.25);
  color: #f7deb0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- Session ----------
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = "방문자"


def login_as(role: str, name: str) -> None:
    st.session_state.role = role
    st.session_state.user_name = name


def logout() -> None:
    st.session_state.role = None
    st.session_state.user_name = "방문자"


# ---------- Mock data ----------
recent_demand = [
    ("수요자 #001", "학군지역 · 매수 · 30억대 · 대치동", "매칭대기"),
    ("수요자 #002", "한강벨트 · 전세 · 20억대 · 반포동", "AI매칭중"),
    ("수요자 #003", "학군지역 · 단기임대 · 역삼동", "계약진행"),
]
recent_supply = [
    ("대치 SK뷰 33평 급매", "24.5억 · 즉시입주 · AI저평가 ▼8.2%", "숏츠대기"),
    ("반포 레미안퍼스티지 59평", "82억 · 한강뷰 · ▼6.1%", "매칭완료"),
    ("시그니엘 레지던스 95평", "보증금 3억 / 월 1,800만", "추천노출"),
]

# ---------- Login screen ----------
if st.session_state.role is None:
    st.markdown("<div class='badge'>PROPAI 재구성본</div>", unsafe_allow_html=True)
    st.title("PROPAI")
    st.caption("롯데타워&강남빌딩 부동산 중개(주) · 시그니엘 레지던스 · 대치동 학군 랜트 전문")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'><strong>시그니엘 레지던스 95평</strong><div class='small'>서울 전경뷰 · 최고층 · 보증금 3억</div><h3 style='color:#34d399;'>월 1,800만원</h3></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><strong>역삼 래전드힐스 9평</strong><div class='small'>학원가 랜트 · 럭셔리 원룸 · 즉시입주</div><h3 style='color:#d4af57;'>월 130만원</h3></div>", unsafe_allow_html=True)

    st.subheader("로그인 선택")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("카카오 회원 로그인", use_container_width=True):
            login_as("수요자", "카카오 회원")
            st.rerun()
    with b2:
        if st.button("공동중개 파트너", use_container_width=True):
            login_as("공동중개", "파트너 계정")
            st.rerun()
    with b3:
        if st.button("관리자 로그인", use_container_width=True):
            login_as("관리자", "이상수 대표")
            st.rerun()

    st.subheader("직통 연락")
    c1, c2 = st.columns(2)
    c1.markdown("<div class='card'><strong>이상수 대표</strong><div class='small'>010-8985-8945</div></div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'><strong>김은경 이사</strong><div class='small'>010-2482-2460</div></div>", unsafe_allow_html=True)

    st.stop()

# ---------- Main dashboard ----------
left, right = st.columns([0.78, 0.22])
with left:
    st.title("PROPAI 운영 대시보드")
    st.caption(f"현재 로그인: {st.session_state.user_name} · {st.session_state.role}")
with right:
    st.button("로그아웃", on_click=logout, use_container_width=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("매수·임차 수요", "189")
m2.metric("매도·임대 공급", "247")
m3.metric("숏츠 제작대기", "22")
m4.metric("계약 진행중", "14")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["대시보드", "등록/문의", "AI 매칭", "숏츠 광고", "관리"])

with tab1:
    st.markdown("<div class='card'><strong>자동화 파이프라인</strong><div class='small'>등록 → AI분류 → 매칭 → 숏츠 → 계약완료 흐름을 기준으로 구조를 단순화했습니다.</div></div>", unsafe_allow_html=True)
    st.subheader("수요자 최근 등록")
    for title, sub, label in recent_demand:
        st.markdown(f"<div class='card'><strong>{title}</strong><div class='small'>{sub}</div><div class='badge' style='margin-top:8px'>{label}</div></div>", unsafe_allow_html=True)
    st.subheader("공급자 최근 등록")
    for title, sub, label in recent_supply:
        st.markdown(f"<div class='card'><strong>{title}</strong><div class='small'>{sub}</div><div class='badge' style='margin-top:8px'>{label}</div></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card'><strong>수요/공급 등록 폼</strong><div class='small'>예산, 지역, 유형을 남기면 AI 분류 및 관리자 전달 흐름으로 연결됩니다.</div></div>", unsafe_allow_html=True)
    with st.form("inquiry_form"):
        kind = st.selectbox("유형", ["매수 문의", "전세 문의", "월세 문의", "매도 의뢰", "임대 의뢰"])
        area = st.text_input("희망 지역", placeholder="예: 대치동, 잠실, 반포")
        budget = st.text_input("예산 / 조건", placeholder="예: 30억대 / 보증금 1억 + 월세 800")
        memo = st.text_area("추가 메모", placeholder="입주시기, 평형, 학군, 뷰 등")
        submitted = st.form_submit_button("등록 요청 보내기", use_container_width=True)
        if submitted:
            st.success(f"{kind} 문의가 접수되었습니다. ({area or '지역미정'} / {budget or '예산미정'})")

with tab3:
    st.markdown("<div class='card'><strong>AI 자동 매칭 기준</strong><div class='small'>지역, 예산, 입주시기, 학군, 상품성, 공동중개 가능 여부를 점수화합니다.</div></div>", unsafe_allow_html=True)
    st.write("- 지역/생활권 우선")
    st.write("- 가격 적합도 ±10% 반영")
    st.write("- 즉시입주, 뷰, 숏츠 적합도 반영")

with tab4:
    st.markdown("<div class='card'><strong>숏츠 광고 패키지</strong><div class='small'>무료 1건 또는 유료 단건으로 접수하고, 유튜브/카카오 공유 흐름으로 연결할 수 있습니다.</div></div>", unsafe_allow_html=True)
    a, b = st.columns(2)
    a.markdown("<div class='card'><strong>무료 1건</strong><div class='small'>AI 저평가 판정 매물 · 당사 연락처 노출</div><h3 style='color:#34d399;'>₩0</h3></div>", unsafe_allow_html=True)
    b.markdown("<div class='card'><strong>유료 단건</strong><div class='small'>신청자 연락처 삽입 · 우선 제작</div><h3 style='color:#d4af57;'>₩30,000</h3></div>", unsafe_allow_html=True)
    st.info("이 단계에서 이메일 전송, 파일 업로드, 카카오 공유 API를 실제로 연결하면 됩니다.")

with tab5:
    st.markdown("<div class='card'><strong>실서비스 연결 포인트</strong><div class='small'>Firebase 저장, 역할별 권한 분리, GitHub Pages 또는 Streamlit 배포 구조를 기준으로 다시 정리했습니다.</div></div>", unsafe_allow_html=True)
    st.write("1. customers / listings / shorts_requests / contracts 컬렉션 분리")
    st.write("2. 관리자만 수정 가능한 운영 메뉴 분리")
    st.write("3. 정적 웹과 Streamlit 앱의 역할 분리")
