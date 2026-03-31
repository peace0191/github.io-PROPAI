from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="PROPAI Firebase", page_icon="🏙️", layout="wide")

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
.block-container { max-width: 1220px; padding-top: 1.2rem; padding-bottom: 4rem; }
.card {
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.015));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px;
}
.small { color: var(--muted); font-size: .9rem; line-height: 1.7; }
.badge {
  display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: .72rem; font-weight: 700;
  background: rgba(212,175,87,.12); border: 1px solid rgba(212,175,87,.25); color: #f7deb0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@dataclass
class Inquiry:
    kind: str
    customer_name: str
    contact: str
    area: str
    budget: str
    memo: str
    category: str
    status: str
    role: str
    created_at: int


@dataclass
class ShortsRequest:
    property: str
    plan: str
    channel: str
    requester: str
    memo: str
    status: str
    created_at: int


DEFAULT_DATA = {
    "inquiries": {
        "a1": {
            "kind": "매수 문의",
            "customer_name": "수요자 #001",
            "contact": "010-1111-1111",
            "area": "대치동",
            "budget": "30억대",
            "memo": "학군 우선",
            "category": "demand",
            "status": "matching",
            "role": "수요자",
            "created_at": 1719800000000,
        },
        "a2": {
            "kind": "임대 의뢰",
            "customer_name": "공급자 #001",
            "contact": "010-2222-2222",
            "area": "잠실",
            "budget": "보증금 3억 / 월 1800",
            "memo": "시그니엘 95평",
            "category": "supply",
            "status": "ai",
            "role": "관리자",
            "created_at": 1719900000000,
        },
    },
    "shorts_requests": {
        "s1": {
            "property": "시그니엘 레지던스 95평",
            "plan": "paid",
            "channel": "유튜브 + 카카오",
            "requester": "010-8985-8945",
            "memo": "한강뷰 강조",
            "status": "shorts",
            "created_at": 1720000000000,
        }
    },
}


def now_ms() -> int:
    return int(datetime.now().timestamp() * 1000)


def get_firebase_db_url() -> str | None:
    return st.secrets.get("FIREBASE_DB_URL") if hasattr(st, "secrets") and "FIREBASE_DB_URL" in st.secrets else os.getenv("FIREBASE_DB_URL")


def get_firebase_db_secret() -> str | None:
    return st.secrets.get("FIREBASE_DB_SECRET") if hasattr(st, "secrets") and "FIREBASE_DB_SECRET" in st.secrets else os.getenv("FIREBASE_DB_SECRET")


def firebase_enabled() -> bool:
    return bool(get_firebase_db_url())


def fb_url(path: str) -> str:
    base = get_firebase_db_url().rstrip("/")
    secret = get_firebase_db_secret()
    suffix = f"?auth={secret}" if secret else ""
    return f"{base}/{path}.json{suffix}"


def load_path(path: str) -> dict[str, Any]:
    if not firebase_enabled():
        return DEFAULT_DATA.get(path, {})
    try:
        resp = requests.get(fb_url(path), timeout=10)
        resp.raise_for_status()
        return resp.json() or {}
    except Exception as exc:
        st.warning(f"Firebase 읽기 실패로 데모 데이터로 표시합니다: {exc}")
        return DEFAULT_DATA.get(path, {})


def push_path(path: str, payload: dict[str, Any]) -> bool:
    if not firebase_enabled():
        demo_key = f"demo_{now_ms()}"
        DEFAULT_DATA.setdefault(path, {})[demo_key] = payload
        return True
    try:
        resp = requests.post(fb_url(path), json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as exc:
        st.error(f"Firebase 저장 실패: {exc}")
        return False


def patch_path(path: str, doc_id: str, payload: dict[str, Any]) -> bool:
    if not firebase_enabled():
        if doc_id in DEFAULT_DATA.get(path, {}):
            DEFAULT_DATA[path][doc_id].update(payload)
        return True
    try:
        url = fb_url(f"{path}/{doc_id}")
        resp = requests.patch(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as exc:
        st.error(f"Firebase 업데이트 실패: {exc}")
        return False


def to_df(records: dict[str, Any]) -> pd.DataFrame:
    rows = [{"id": k, **v} for k, v in (records or {}).items()]
    df = pd.DataFrame(rows)
    if not df.empty and "created_at" in df.columns:
        df = df.sort_values("created_at", ascending=False)
    return df


def format_time(ms: Any) -> str:
    try:
        return datetime.fromtimestamp(int(ms) / 1000).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "-"


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


if st.session_state.role is None:
    st.markdown("<div class='badge'>PROPAI Firebase 연결판</div>", unsafe_allow_html=True)
    st.title("PROPAI")
    st.caption("웹앱과 같은 데이터 구조를 사용하는 Streamlit 운영판입니다.")

    left, right = st.columns(2)
    left.markdown("<div class='card'><strong>시그니엘 레지던스 95평</strong><div class='small'>서울 전경뷰 · 최고층 · 보증금 3억</div><h3 style='color:#34d399;'>월 1,800만원</h3></div>", unsafe_allow_html=True)
    right.markdown("<div class='card'><strong>역삼 래전드힐스 9평</strong><div class='small'>학원가 랜트 · 럭셔리 원룸 · 즉시입주</div><h3 style='color:#d4af57;'>월 130만원</h3></div>", unsafe_allow_html=True)

    a, b, c = st.columns(3)
    if a.button("카카오 회원 로그인", use_container_width=True):
        login_as("수요자", "카카오 회원")
        st.rerun()
    if b.button("공동중개 파트너", use_container_width=True):
        login_as("공동중개", "파트너 계정")
        st.rerun()
    if c.button("관리자 로그인", use_container_width=True):
        login_as("관리자", "이상수 대표")
        st.rerun()

    st.stop()

inquiries_df = to_df(load_path("inquiries"))
shorts_df = to_df(load_path("shorts_requests"))

demand_df = inquiries_df[inquiries_df.get("category", pd.Series(dtype=str)) == "demand"] if not inquiries_df.empty else pd.DataFrame()
supply_df = inquiries_df[inquiries_df.get("category", pd.Series(dtype=str)) == "supply"] if not inquiries_df.empty else pd.DataFrame()

head_left, head_right = st.columns([0.75, 0.25])
with head_left:
    st.title("PROPAI 운영 대시보드")
    st.caption(f"현재 로그인: {st.session_state.user_name} · {st.session_state.role} · {'Firebase 연결' if firebase_enabled() else '데모 모드'}")
with head_right:
    st.button("로그아웃", on_click=logout, use_container_width=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("매수·임차 수요", str(len(demand_df)))
m2.metric("매도·임대 공급", str(len(supply_df)))
m3.metric("숏츠 제작대기", str(len(shorts_df[shorts_df.get("status", pd.Series(dtype=str)) != "done"])) if not shorts_df.empty else "0")
m4.metric("계약 진행중", "14")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["대시보드", "등록/문의", "AI 매칭", "숏츠 광고", "관리"])

with tab1:
    st.markdown("<div class='card'><strong>자동화 파이프라인</strong><div class='small'>문의 등록과 숏츠 접수가 Firebase 같은 경로로 저장됩니다.</div></div>", unsafe_allow_html=True)
    st.subheader("수요자 최근 등록")
    if demand_df.empty:
        st.info("아직 수요 데이터가 없습니다.")
    else:
        for _, row in demand_df.head(5).iterrows():
            st.markdown(
                f"<div class='card'><strong>{row.get('customer_name', '수요자')}</strong>"
                f"<div class='small'>{row.get('kind', '-') } · {row.get('area', '-')} · {row.get('budget', '-')}</div>"
                f"<div class='small'>{format_time(row.get('created_at'))}</div></div>",
                unsafe_allow_html=True,
            )
    st.subheader("공급자 최근 등록")
    if supply_df.empty:
        st.info("아직 공급 데이터가 없습니다.")
    else:
        for _, row in supply_df.head(5).iterrows():
            st.markdown(
                f"<div class='card'><strong>{row.get('customer_name', '공급자')}</strong>"
                f"<div class='small'>{row.get('kind', '-') } · {row.get('area', '-')} · {row.get('budget', '-')}</div>"
                f"<div class='small'>{format_time(row.get('created_at'))}</div></div>",
                unsafe_allow_html=True,
            )

with tab2:
    st.markdown("<div class='card'><strong>문의 등록</strong><div class='small'>이 폼은 inquiries 경로에 저장됩니다.</div></div>", unsafe_allow_html=True)
    with st.form("inquiry_form"):
        kind = st.selectbox("유형", ["매수 문의", "전세 문의", "월세 문의", "매도 의뢰", "임대 의뢰"])
        customer_name = st.text_input("이름", placeholder="예: 홍길동")
        contact = st.text_input("연락처", placeholder="010-0000-0000")
        area = st.text_input("희망 지역", placeholder="예: 대치동, 잠실, 반포")
        budget = st.text_input("예산 / 조건", placeholder="예: 30억대 / 보증금 1억 + 월세 800")
        memo = st.text_area("추가 메모", placeholder="입주시기, 학군, 뷰 등")
        submitted = st.form_submit_button("등록 요청 보내기", use_container_width=True)
        if submitted:
            category = "supply" if kind in ["매도 의뢰", "임대 의뢰"] else "demand"
            status = "ai" if category == "supply" else "matching"
            payload = asdict(Inquiry(kind, customer_name or st.session_state.user_name, contact, area, budget, memo, category, status, st.session_state.role, now_ms()))
            if push_path("inquiries", payload):
                st.success("문의가 저장되었습니다.")
                st.rerun()

with tab3:
    st.markdown("<div class='card'><strong>AI 자동 매칭 기준</strong><div class='small'>현재는 규칙 기반 안내, 이후 OpenAI / 벡터 검색 연동 포인트로 확장 가능</div></div>", unsafe_allow_html=True)
    st.write("- 지역/생활권 우선")
    st.write("- 가격 적합도 ±10%")
    st.write("- 즉시입주, 뷰, 학군, 숏츠 적합도 반영")
    if not demand_df.empty and not supply_df.empty:
        pairs = min(3, len(demand_df), len(supply_df))
        for i in range(pairs):
            d = demand_df.iloc[i]
            s = supply_df.iloc[i]
            st.markdown(
                f"<div class='card'><strong>{d.get('customer_name')} ↔ {s.get('customer_name')}</strong>"
                f"<div class='small'>{d.get('area', '-')} / {d.get('budget', '-')} ↔ {s.get('area', '-')} / {s.get('budget', '-')}</div>"
                f"<div class='small'>추천 점수: {92 - i * 7}점</div></div>",
                unsafe_allow_html=True,
            )

with tab4:
    st.markdown("<div class='card'><strong>숏츠 광고 접수</strong><div class='small'>shorts_requests 경로에 저장되며, 상태 변경은 관리 탭에서 처리합니다.</div></div>", unsafe_allow_html=True)
    with st.form("shorts_form"):
        property_name = st.text_input("매물명", placeholder="예: 시그니엘 95평 임대")
        plan = st.selectbox("요금제", ["free", "paid"])
        channel = st.selectbox("발송 채널", ["유튜브", "카카오", "유튜브 + 카카오"])
        requester = st.text_input("신청자 연락처", placeholder="010-0000-0000")
        memo = st.text_area("요청사항", placeholder="강조 포인트, 희망 업로드 채널")
        submit_shorts = st.form_submit_button("숏츠 광고 접수 저장", use_container_width=True)
        if submit_shorts:
            payload = asdict(ShortsRequest(property_name, plan, channel, requester, memo, "shorts", now_ms()))
            if push_path("shorts_requests", payload):
                st.success("숏츠 요청이 저장되었습니다.")
                st.rerun()
    if not shorts_df.empty:
        st.dataframe(shorts_df.assign(created_at=shorts_df["created_at"].map(format_time)), use_container_width=True)

with tab5:
    st.markdown("<div class='card'><strong>운영 관리</strong><div class='small'>최근 등록 데이터를 확인하고 상태를 done으로 바꿀 수 있습니다.</div></div>", unsafe_allow_html=True)
    st.subheader("문의 현황")
    if inquiries_df.empty:
        st.info("문의 데이터가 없습니다.")
    else:
        display_df = inquiries_df.copy()
        display_df["created_at"] = display_df["created_at"].map(format_time)
        st.dataframe(display_df, use_container_width=True)
        selected_inquiry = st.selectbox("완료 처리할 문의 ID", options=display_df["id"].tolist())
        if st.button("선택 문의 완료 처리", use_container_width=True):
            if patch_path("inquiries", selected_inquiry, {"status": "done"}):
                st.success("문의 상태를 완료로 변경했습니다.")
                st.rerun()

    st.subheader("숏츠 현황")
    if shorts_df.empty:
        st.info("숏츠 요청이 없습니다.")
    else:
        display_shorts_df = shorts_df.copy()
        display_shorts_df["created_at"] = display_shorts_df["created_at"].map(format_time)
        st.dataframe(display_shorts_df, use_container_width=True)
        selected_shorts = st.selectbox("완료 처리할 숏츠 ID", options=display_shorts_df["id"].tolist())
        if st.button("선택 숏츠 완료 처리", use_container_width=True):
            if patch_path("shorts_requests", selected_shorts, {"status": "done"}):
                st.success("숏츠 상태를 완료로 변경했습니다.")
                st.rerun()

st.caption("환경 변수: FIREBASE_DB_URL, FIREBASE_DB_SECRET(선택). URL이 없으면 데모 모드로 동작합니다.")
