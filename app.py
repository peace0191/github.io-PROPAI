from pathlib import Path
from datetime import datetime
import urllib.parse

import pandas as pd
import streamlit as st

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="PROPAI — 투명 부동산 AI 플랫폼",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = Path("data")
LEADS_FILE = DATA_DIR / "leads.csv"

ADMIN_ID = "sangsu"
ADMIN_PW = "propai2026"
KAKAO_OPENCHAT_URL = "https://open.kakao.com/o/sangsu"

DATA_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 상태
# --------------------------------------------------
def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "admin_login" not in st.session_state:
        st.session_state.admin_login = False


def go(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


# --------------------------------------------------
# 데이터
# --------------------------------------------------
def ensure_leads_file() -> None:
    if not LEADS_FILE.exists():
        df = pd.DataFrame(
            columns=[
                "접수시각",
                "이름",
                "연락처",
                "관심권역",
                "희망유형",
                "예산",
                "문의내용",
                "상담채널",
            ]
        )
        df.to_csv(LEADS_FILE, index=False, encoding="utf-8-sig")


def load_leads() -> pd.DataFrame:
    ensure_leads_file()
    return pd.read_csv(LEADS_FILE)


def save_lead(row: dict) -> None:
    df = load_leads()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(LEADS_FILE, index=False, encoding="utf-8-sig")


# --------------------------------------------------
# 유틸
# --------------------------------------------------
def kakao_message_link(message: str) -> str:
    return f"{KAKAO_OPENCHAT_URL}?text={urllib.parse.quote(message)}"


def render_home_button(key: str) -> None:
    st.markdown("<div class='back-wrap'>", unsafe_allow_html=True)
    if st.button("홈으로", key=key, use_container_width=True):
        go("home")
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# 스타일
# --------------------------------------------------
def apply_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Noto Sans KR', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top center, rgba(30, 45, 84, 0.32), transparent 30%),
                linear-gradient(180deg, #030b1a 0%, #031022 48%, #041226 100%);
        }

        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {display:none !important;}
        [data-testid="stDecoration"] {display:none !important;}
        [data-testid="stStatusWidget"] {display:none !important;}

        .block-container {
            max-width: 760px !important;
            padding-top: 0.75rem !important;
            padding-bottom: 2.8rem !important;
        }

        .top-title {
            color: rgba(255,255,255,0.88);
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            margin-top: 4px;
        }

        .hero-wrap {
            width: 100%;
            max-width: 430px;
            margin: 18px auto 0 auto;
            text-align: center;
        }

        .logo-box {
            width: 82px;
            height: 82px;
            margin: 0 auto 20px auto;
            border-radius: 24px;
            background: linear-gradient(180deg, #c9ac59 0%, #a28131 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 16px 38px rgba(0,0,0,0.30);
        }

        .logo-letter {
            color: #111827;
            font-size: 2.15rem;
            font-weight: 700;
            font-family: Georgia, 'Times New Roman', serif;
        }

        .hero-title {
            color: #ffffff;
            font-size: 2.15rem;
            line-height: 1.16;
            font-family: Georgia, 'Times New Roman', serif;
            font-weight: 500;
            margin-bottom: 10px;
            letter-spacing: -0.02em;
        }

        .hero-sub {
            color: rgba(255,255,255,0.77);
            font-size: 0.98rem;
            line-height: 1.75;
            margin-bottom: 18px;
        }

        .zone-card {
            background: rgba(9, 17, 34, 0.92);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 17px;
            padding: 15px 17px;
            margin-bottom: 11px;
            box-shadow: 0 10px 22px rgba(0,0,0,0.18);
        }

        .zone-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
        }

        .zone-left {
            flex: 1.15;
            color: #ffffff;
            font-size: 0.98rem;
            font-weight: 800;
            line-height: 1.45;
            text-align: left;
        }

        .zone-right {
            flex: 1;
            color: rgba(255,255,255,0.42);
            font-size: 0.86rem;
            line-height: 1.6;
            text-align: right;
        }

        .chip-wrap {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin: 18px auto 8px auto;
            max-width: 460px;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
            padding: 8px 13px;
            border-radius: 999px;
            background: rgba(10, 18, 35, 0.92);
            border: 1px solid rgba(255,255,255,0.07);
            color: rgba(255,255,255,0.84);
            font-size: 0.83rem;
            font-weight: 700;
            min-height: 38px;
        }

        .yellow-btn button {
            background: #eadb4f !important;
            color: #172033 !important;
            border: 0 !important;
            border-radius: 18px !important;
            min-height: 74px !important;
            font-size: 1.52rem !important;
            font-weight: 900 !important;
            box-shadow: 0 18px 34px rgba(0,0,0,0.24) !important;
        }

        .menu-btn button,
        .admin-btn button,
        .back-wrap button,
        .stDownloadButton > button,
        .plain-btn button {
            background: rgba(10, 18, 35, 0.94) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
            font-weight: 800 !important;
            min-height: 44px !important;
        }

        .note-text {
            color: rgba(255,255,255,0.40);
            font-size: 0.79rem;
            line-height: 1.65;
            text-align: center;
            margin-top: 13px;
        }

        .sub-card {
            background: rgba(9, 17, 34, 0.92);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 22px;
            padding: 22px;
            margin-top: 16px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.18);
        }

        .sub-title {
            color: #ffffff;
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .sub-text {
            color: rgba(255,255,255,0.82);
            font-size: 0.97rem;
            line-height: 1.9;
        }

        .minor-box {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 15px;
            margin-top: 14px;
        }

        .metric-line {
            color: #ffffff;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stRadio label {
            color: rgba(255,255,255,0.92) !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            background: rgba(255,255,255,0.98) !important;
            color: #111827 !important;
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] > div {
            background: rgba(255,255,255,0.98) !important;
            color: #111827 !important;
            border-radius: 12px !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }

        [data-testid="stMetricLabel"] {
            color: rgba(255,255,255,0.72) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# 상단바
# --------------------------------------------------
def render_top_bar(show_admin: bool = True) -> None:
    c1, c2, c3 = st.columns([2, 5, 1.3])
    with c1:
        st.markdown("<div class='top-title'>PROPAI</div>", unsafe_allow_html=True)
    with c3:
        if show_admin:
            st.markdown("<div class='admin-btn'>", unsafe_allow_html=True)
            if st.button("관리자", key="admin_top_btn", use_container_width=True):
                go("admin")
            st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# 홈
# --------------------------------------------------
def render_home() -> None:
    render_top_bar(show_admin=True)

    st.markdown(
        """
        <div class="hero-wrap">
            <div class="logo-box">
                <div class="logo-letter">P</div>
            </div>

            <div class="hero-title">PROPAI<br>투명 부동산 플랫폼</div>

            <div class="hero-sub">
                광고 없음 · 중개보수만으로 수익<br>
                수요·공급·공동중개 3자 AI 자동매칭
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cards = [
        ("🪙 학군 배후 주거 권역", "대치 · 도곡 · 역삼 · 개포 · 압구정"),
        ("🌊 한강 벨트 럭셔리 권역", "강남 · 반포 · 송파 · 용산 · 성수 · 마포"),
        ("📈 한강변 재건축·재개발<br>투자 권역", "삼성동 · 압구정 · 여의도 · 목동 · 성수 · 한남 · 흑석"),
    ]

    for left, right in cards:
        st.markdown(
            f"""
            <div class="zone-card">
                <div class="zone-row">
                    <div class="zone-left">{left}</div>
                    <div class="zone-right">{right}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="chip-wrap">
            <div class="chip">✅ 광고비 0원</div>
            <div class="chip">🤖 AI 자동매칭</div>
            <div class="chip">🔒 법정 중개보수</div>
            <div class="chip">🎬 숏츠 자동제작</div>
            <div class="chip">🤝 공동중개</div>
            <div class="chip">📊 포털 실시간비교</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='yellow-btn'>", unsafe_allow_html=True)
    if st.button("💬 카카오 로그인으로 시작하기", key="main_kakao_start", use_container_width=True):
        go("consult")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="note-text">
            본 플랫폼 이용 시 서비스 이용약관, 개인정보 처리방침,<br>
            플랫폼 규약(데이터 3차 검수 정책 포함)에 동의하게 됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(3)
    with row1[0]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("이용약관", key="home_terms", use_container_width=True):
            go("terms")
        st.markdown("</div>", unsafe_allow_html=True)
    with row1[1]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("공동중개", key="home_cowork", use_container_width=True):
            go("cowork")
        st.markdown("</div>", unsafe_allow_html=True)
    with row1[2]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("수익모델", key="home_revenue", use_container_width=True):
            go("revenue")
        st.markdown("</div>", unsafe_allow_html=True)

    row2 = st.columns(3)
    with row2[0]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("광고비 0원", key="home_ad_zero", use_container_width=True):
            go("ad_zero")
        st.markdown("</div>", unsafe_allow_html=True)
    with row2[1]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("AI 자동매칭", key="home_matching", use_container_width=True):
            go("matching")
        st.markdown("</div>", unsafe_allow_html=True)
    with row2[2]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("법정 중개보수", key="home_legal", use_container_width=True):
            go("legal_fee")
        st.markdown("</div>", unsafe_allow_html=True)

    row3 = st.columns(3)
    with row3[0]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("숏츠 자동제작", key="home_shorts", use_container_width=True):
            go("shorts")
        st.markdown("</div>", unsafe_allow_html=True)
    with row3[1]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("포털 실시간비교", key="home_portal", use_container_width=True):
            go("portal")
        st.markdown("</div>", unsafe_allow_html=True)
    with row3[2]:
        st.markdown("<div class='menu-btn'>", unsafe_allow_html=True)
        if st.button("빠른 상담접수", key="home_consult", use_container_width=True):
            go("consult")
        st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# 상담 페이지
# --------------------------------------------------
def render_consult() -> None:
    render_top_bar(show_admin=True)

    st.markdown(
        """
        <div class="sub-card">
            <div class="sub-title">빠른 상담 접수</div>
            <div class="sub-text">
                상담 접수 후 카카오 상담으로 바로 연결됩니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("consult_form", clear_on_submit=False):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("이름")
            phone = st.text_input("연락처")
            region = st.selectbox(
                "관심 권역",
                ["🎓 학군 배후 주거", "🌊 한강 벨트 럭셔리", "📈 한강변 재건축"],
            )

        with c2:
            property_type = st.selectbox(
                "희망 유형",
                ["아파트", "고급주거", "오피스텔", "빌딩", "재건축", "기타"],
            )
            budget = st.selectbox(
                "예산대",
                ["1억 미만", "1~5억", "5~10억", "10~30억", "30억 이상", "문의"],
            )
            channel = st.radio("상담 방식", ["카카오톡", "전화상담"], horizontal=True)

        memo = st.text_area("문의 내용", placeholder="희망 지역, 입주 시기, 투자 목적 등을 입력하세요.")
        submitted = st.form_submit_button("상담 접수 저장", use_container_width=True)

    st.markdown("<div class='minor-box'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-line'>상담 흐름</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sub-text">
            1. 고객 접수<br>
            2. 권역/예산 분류<br>
            3. 카카오 상담 연결<br>
            4. 관리자 리드 관리
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not name.strip() or not phone.strip():
            st.warning("이름과 연락처를 입력해주세요.")
        else:
            row = {
                "접수시각": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "이름": name.strip(),
                "연락처": phone.strip(),
                "관심권역": region,
                "희망유형": property_type,
                "예산": budget,
                "문의내용": memo.strip(),
                "상담채널": channel,
            }
            save_lead(row)
            st.success("상담 접수가 저장되었습니다.")

            msg = f"""안녕하세요. PROPAI 상담 요청드립니다.

이름: {name}
연락처: {phone}
관심 권역: {region}
희망 유형: {property_type}
예산: {budget}
문의 내용: {memo if memo else '없음'}

맞춤 상담 부탁드립니다.
"""
            st.link_button(
                "카카오 상담으로 이동",
                kakao_message_link(msg),
                use_container_width=True,
            )

    render_home_button("consult_home_btn")


# --------------------------------------------------
# 관리자
# --------------------------------------------------
def render_admin() -> None:
    render_top_bar(show_admin=False)

    if not st.session_state.admin_login:
        st.markdown(
            """
            <div class="sub-card">
                <div class="sub-title">관리자 로그인</div>
                <div class="sub-text">
                    접수된 리드 확인 및 CSV 다운로드를 위한 관리자 화면입니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        admin_id = st.text_input("아이디")
        admin_pw = st.text_input("비밀번호", type="password")

        if st.button("로그인", key="admin_login_btn_main", use_container_width=True):
            if admin_id == ADMIN_ID and admin_pw == ADMIN_PW:
                st.session_state.admin_login = True
                st.success("로그인되었습니다.")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        render_home_button("admin_login_home_btn")
        return

    leads = load_leads()

    st.markdown(
        """
        <div class="sub-card">
            <div class="sub-title">관리자 리드 대시보드</div>
            <div class="sub-text">
                접수된 고객 문의를 확인하고 CSV로 다운로드할 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("전체 리드", len(leads))
    c2.metric("카카오 상담", int((leads["상담채널"] == "카카오톡").sum()) if not leads.empty else 0)
    c3.metric("전화 상담", int((leads["상담채널"] == "전화상담").sum()) if not leads.empty else 0)

    if leads.empty:
        st.info("아직 접수된 리드가 없습니다.")
    else:
        st.dataframe(leads, use_container_width=True, hide_index=True)
        csv_bytes = leads.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            data=csv_bytes,
            file_name="propai_leads.csv",
            mime="text/csv",
            use_container_width=True,
        )

    row = st.columns(2)
    with row[0]:
        if st.button("로그아웃", key="admin_logout_btn", use_container_width=True):
            st.session_state.admin_login = False
            st.rerun()
    with row[1]:
        if st.button("홈으로", key="admin_home_btn", use_container_width=True):
            go("home")


# --------------------------------------------------
# 정보 페이지
# --------------------------------------------------
def render_info_page(title: str, content: str) -> None:
    render_top_bar(show_admin=True)

    st.markdown(
        f"""
        <div class="sub-card">
            <div class="sub-title">{title}</div>
            <div class="sub-text">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_home_button(f"{title}_home_btn")


# --------------------------------------------------
# 메인
# --------------------------------------------------
def main() -> None:
    init_state()
    ensure_leads_file()
    apply_style()

    page = st.session_state.page

    if page == "home":
        render_home()
    elif page == "consult":
        render_consult()
    elif page == "admin":
        render_admin()
    elif page == "terms":
        render_info_page(
            "이용약관",
            """
            PROPAI는 투명한 중개 구조와 정보 제공을 목표로 하는 플랫폼입니다.<br><br>
            - 허위 매물 등록 금지<br>
            - 법정 범위 내 중개보수 준수<br>
            - 개인정보 보호 원칙 준수<br>
            - 플랫폼 운영 규약 준수
            """,
        )
    elif page == "cowork":
        render_info_page(
            "공동중개",
            """
            공동중개 네트워크를 통해 수요자·공급자·중개 파트너를 연결합니다.<br><br>
            - 지역별 협업 구조<br>
            - 공동중개 조건 투명화<br>
            - 실수요자 중심 연결<br>
            - AI 기반 우선 매칭
            """,
        )
    elif page == "revenue":
        render_info_page(
            "수익모델",
            """
            광고 중심이 아니라 실제 중개 전환 중심 구조를 지향합니다.<br><br>
            - 광고비 최소화<br>
            - 법정 중개보수 기반 수익<br>
            - 공동중개 확장 수익<br>
            - AI 자동매칭 기반 상담 효율화
            """,
        )
    elif page == "ad_zero":
        render_info_page(
            "광고비 0원",
            """
            무분별한 광고 지출보다 실제 수요 연결과 상담 전환을 우선합니다.<br><br>
            - 광고 의존도 축소<br>
            - 실수요자 중심 상담 구조<br>
            - AI 자동매칭 기반 효율화
            """,
        )
    elif page == "matching":
        render_info_page(
            "AI 자동매칭",
            """
            고객의 관심 권역, 예산, 희망 유형을 기준으로 상담 흐름을 정리합니다.<br><br>
            - 3대 권역 자동 분류<br>
            - 니즈 기반 연결<br>
            - 상담 우선순위 정리<br>
            - 관리자 리드 관리 연동
            """,
        )
    elif page == "legal_fee":
        render_info_page(
            "법정 중개보수",
            """
            PROPAI는 법정 범위 내 중개보수를 원칙으로 합니다.<br><br>
            - 중개보수 기준 준수<br>
            - 사전 안내 원칙<br>
            - 과도한 추가 비용 지양
            """,
        )
    elif page == "shorts":
        render_info_page(
            "숏츠 자동제작",
            """
            매물 특징과 권역 특성을 바탕으로 숏폼 소개 문구와 스크립트를 정리하는 기능입니다.<br><br>
            - 랜딩 유입 강화<br>
            - 반복 제작 시간 절감<br>
            - 관심 고객 전환 유도
            """,
        )
    elif page == "portal":
        render_info_page(
            "포털 실시간비교",
            """
            포털별 반응과 노출 흐름을 비교해 상담 전략을 정리합니다.<br><br>
            - 매물 반응 비교<br>
            - 상담 전환 경로 분석<br>
            - 노출 대비 효율 점검
            """,
        )
    else:
        go("home")


if __name__ == "__main__":
    main()