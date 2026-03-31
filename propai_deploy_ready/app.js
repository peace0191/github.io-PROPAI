import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getDatabase,
  ref,
  push,
  set,
  get,
  update,
  serverTimestamp,
  query,
  orderByChild,
  limitToLast,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

const state = {
  loggedIn: false,
  currentTab: 'dashboard',
  profile: { name: '방문자', role: '수요자' },
  dbMode: 'local',
  firebaseReady: false,
  db: null,
  feed: { demand: [], supply: [], shorts: [], admin: [] },
};

const defaultSeed = {
  inquiries: {
    a1: { kind: '매수 문의', customerName: '수요자 #001', area: '대치동', budget: '30억대', memo: '학군 우선', category: 'demand', status: 'matching', createdAt: Date.now() - 86400000 },
    a2: { kind: '전세 문의', customerName: '수요자 #002', area: '반포동', budget: '20억대', memo: '한강벨트', category: 'demand', status: 'ai', createdAt: Date.now() - 54000000 },
    a3: { kind: '임대 의뢰', customerName: '공급자 #001', area: '잠실', budget: '보증금 3억 / 월 1800', memo: '시그니엘 95평', category: 'supply', status: 'done', createdAt: Date.now() - 24000000 },
  },
  shorts_requests: {
    s1: { property: '시그니엘 레지던스 95평', plan: 'paid', channel: '유튜브 + 카카오', requester: '010-8985-8945', memo: '한강뷰 강조', status: 'shorts', createdAt: Date.now() - 3600000 },
  },
};

function qs(sel) { return document.querySelector(sel); }
function qsa(sel) { return [...document.querySelectorAll(sel)]; }
function formatDate(ts) {
  if (!ts) return '방금';
  const d = new Date(ts);
  return `${d.getMonth() + 1}.${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}
function toast(message) {
  const wrap = qs('.toast-wrap');
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = message;
  wrap.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function getLocalData() {
  const raw = localStorage.getItem('propai_demo_db');
  if (raw) return JSON.parse(raw);
  localStorage.setItem('propai_demo_db', JSON.stringify(defaultSeed));
  return structuredClone(defaultSeed);
}
function saveLocalData(data) {
  localStorage.setItem('propai_demo_db', JSON.stringify(data));
}

function isFirebaseConfigValid(config) {
  return !!config && !!config.apiKey && config.apiKey !== 'REPLACE_ME' && !!config.databaseURL && !config.databaseURL.includes('REPLACE_ME');
}

async function initFirebase() {
  try {
    const config = window.FIREBASE_CONFIG;
    if (!isFirebaseConfigValid(config)) throw new Error('Firebase config placeholder');
    const app = initializeApp(config);
    state.db = getDatabase(app);
    state.firebaseReady = true;
    state.dbMode = 'firebase';
    qs('#dbModeBadge').textContent = 'Firebase 연결됨';
    qs('#dbModeBadge').className = 'badge jade';
  } catch (err) {
    state.firebaseReady = false;
    state.dbMode = 'local';
    qs('#dbModeBadge').textContent = '데모 저장 모드';
    qs('#dbModeBadge').className = 'badge blue';
    console.warn('Firebase 미연결, localStorage 모드로 실행합니다.', err?.message || err);
  }
}

function inferCategory(kind) {
  return ['매도 의뢰', '임대 의뢰'].includes(kind) ? 'supply' : 'demand';
}
function inferState(status) {
  switch (status) {
    case 'ai': return 'AI매칭중';
    case 'done': return '완료';
    case 'shorts': return '숏츠대기';
    default: return '매칭대기';
  }
}

async function listRecords(path) {
  if (state.firebaseReady) {
    const snapshot = await get(query(ref(state.db, path), orderByChild('createdAt'), limitToLast(30)));
    return snapshot.exists() ? Object.entries(snapshot.val()).map(([id, value]) => ({ id, ...value })) : [];
  }
  const data = getLocalData();
  return Object.entries(data[path] || {}).map(([id, value]) => ({ id, ...value }));
}

async function createRecord(path, payload) {
  if (state.firebaseReady) {
    const newRef = push(ref(state.db, path));
    await set(newRef, { ...payload, createdAt: Date.now(), serverTime: serverTimestamp() });
    return newRef.key;
  }
  const data = getLocalData();
  const id = `${path}_${Date.now()}`;
  data[path] = data[path] || {};
  data[path][id] = { ...payload, createdAt: Date.now() };
  saveLocalData(data);
  return id;
}

async function updateRecord(path, id, payload) {
  if (state.firebaseReady) {
    await update(ref(state.db, `${path}/${id}`), payload);
    return;
  }
  const data = getLocalData();
  if (!data[path]?.[id]) return;
  data[path][id] = { ...data[path][id], ...payload };
  saveLocalData(data);
}

function renderFeed(items, target) {
  qs(target).innerHTML = items.map(item => `
    <div class="feed-card">
      <div class="feed-head">
        <div>
          <div class="feed-title">${item.title}</div>
          <div class="feed-sub">${item.sub}</div>
          <div class="feed-sub">${item.time}</div>
        </div>
        <span class="state ${item.state}">${item.label}</span>
      </div>
    </div>
  `).join('') || `<div class="feed-card"><div class="feed-sub">아직 데이터가 없습니다.</div></div>`;
}

function renderAdmin(items) {
  qs('#adminFeed').innerHTML = items.map(item => `
    <div class="feed-card">
      <div class="feed-head">
        <div>
          <div class="feed-title">${item.title}</div>
          <div class="feed-sub">${item.sub}</div>
          <div class="feed-sub">${item.time}</div>
        </div>
        <div class="action-row">
          <span class="state ${item.state}">${item.label}</span>
          <button class="btn line small-btn admin-status-btn" data-path="${item.path}" data-id="${item.id}" data-next="done">완료</button>
        </div>
      </div>
    </div>
  `).join('') || `<div class="feed-card"><div class="feed-sub">운영 피드가 비어 있습니다.</div></div>`;

  qsa('.admin-status-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      await updateRecord(btn.dataset.path, btn.dataset.id, { status: btn.dataset.next });
      toast('상태를 완료로 변경했습니다');
      await refreshAll();
    });
  });
}

function updateMetrics(demand, supply, shorts) {
  qs('#metricDemand').textContent = demand.length;
  qs('#metricSupply').textContent = supply.length;
  qs('#metricShorts').textContent = shorts.filter(x => x.status !== 'done').length;
  qs('#pipeRegistered').textContent = demand.length + supply.length;
  qs('#pipeAI').textContent = [...demand, ...supply].filter(x => x.status === 'ai').length;
  qs('#pipeMatched').textContent = [...demand, ...supply].filter(x => x.status === 'matching').length;
  qs('#pipeShorts').textContent = shorts.length;
  qs('#pipeDone').textContent = [...demand, ...supply, ...shorts].filter(x => x.status === 'done').length;
}

function buildMatchResults(demand, supply) {
  const demandSample = demand.slice(0, 3);
  const supplySample = supply.slice(0, 3);
  const html = demandSample.map((d, idx) => {
    const s = supplySample[idx] || supplySample[0];
    if (!s) return null;
    return `
      <div class="feed-card">
        <div class="feed-title">${d.customerName || d.title} ↔ ${s.customerName || s.title}</div>
        <div class="feed-sub">${d.area || '-'} · ${d.budget || '-'} / ${s.area || '-'} · ${s.budget || '-'}</div>
        <div class="feed-sub">추천 점수: ${92 - idx * 7}점</div>
      </div>
    `;
  }).filter(Boolean).join('');
  qs('#matchResults').innerHTML = html || `<div class="feed-card"><div class="feed-sub">매칭 결과가 아직 없습니다.</div></div>`;
}

async function refreshAll() {
  const inquiries = await listRecords('inquiries');
  const shorts = await listRecords('shorts_requests');
  inquiries.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
  shorts.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));

  const demand = inquiries.filter(x => x.category === 'demand').map(x => ({
    ...x,
    title: x.customerName || '수요자',
    sub: `${x.kind} · ${x.area || '지역미정'} · ${x.budget || '예산미정'}`,
    time: formatDate(x.createdAt),
    state: x.status || 'matching',
    label: inferState(x.status),
  }));
  const supply = inquiries.filter(x => x.category === 'supply').map(x => ({
    ...x,
    title: x.customerName || '공급자',
    sub: `${x.kind} · ${x.area || '지역미정'} · ${x.budget || '조건미정'}`,
    time: formatDate(x.createdAt),
    state: x.status || 'ai',
    label: inferState(x.status),
  }));
  const shortsView = shorts.map(x => ({
    ...x,
    title: x.property,
    sub: `${x.channel} · ${x.plan === 'paid' ? '유료 단건' : '무료 1건'} · ${x.requester || '연락처 미입력'}`,
    time: formatDate(x.createdAt),
    state: x.status || 'shorts',
    label: x.status === 'done' ? '완료' : '숏츠대기',
  }));

  renderFeed(demand.slice(0, 8), '#recentDemand');
  renderFeed(supply.slice(0, 8), '#recentSupply');
  renderFeed(shortsView.slice(0, 8), '#shortsRequests');
  renderAdmin([
    ...demand.slice(0, 5).map(x => ({ ...x, path: 'inquiries' })),
    ...supply.slice(0, 5).map(x => ({ ...x, path: 'inquiries' })),
    ...shortsView.slice(0, 5).map(x => ({ ...x, path: 'shorts_requests' })),
  ].sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0)).slice(0, 10));
  updateMetrics(demand, supply, shortsView);
  buildMatchResults(demand, supply);
}

function login(role) {
  state.loggedIn = true;
  state.profile = {
    name: role === 'admin' ? '이상수 대표' : role === 'partner' ? '공동중개 파트너' : '카카오 회원',
    role: role === 'admin' ? '관리자' : role === 'partner' ? '공동중개' : '수요자',
  };
  qs('#loginScreen').classList.add('hidden');
  qs('#mainScreen').classList.remove('hidden');
  qs('#profileName').textContent = state.profile.name;
  qs('#profileRole').textContent = state.profile.role;
  toast(`${state.profile.role} 로그인 완료`);
  refreshAll();
}

function setTab(tab) {
  state.currentTab = tab;
  qsa('.tab').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
  qsa('.nav-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
  qsa('.screen').forEach(screen => screen.classList.toggle('active', screen.id === `screen-${tab}`));
}

async function submitInquiry(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    kind: form.kind.value,
    customerName: form.customerName.value || state.profile.name,
    contact: form.contact.value,
    area: form.area.value,
    budget: form.budget.value,
    memo: form.memo.value,
    category: inferCategory(form.kind.value),
    status: inferCategory(form.kind.value) === 'supply' ? 'ai' : 'matching',
    role: state.profile.role,
  };
  await createRecord('inquiries', payload);
  toast('문의가 저장되었습니다');
  form.reset();
  await refreshAll();
  setTab('dashboard');
}

async function submitShorts(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    property: form.shortsProperty.value,
    plan: form.shortsPlan.value,
    channel: form.shortsChannel.value,
    requester: form.shortsRequester.value,
    memo: form.shortsMemo.value,
    status: 'shorts',
  };
  await createRecord('shorts_requests', payload);
  toast('숏츠 광고 요청이 저장되었습니다');
  form.reset();
  await refreshAll();
}

function bindEvents() {
  qsa('[data-login]').forEach(btn => btn.addEventListener('click', () => login(btn.dataset.login)));
  qsa('.tab').forEach(btn => btn.addEventListener('click', () => setTab(btn.dataset.tab)));
  qsa('.nav-btn').forEach(btn => btn.addEventListener('click', () => setTab(btn.dataset.tab)));
  qs('#inquiryForm').addEventListener('submit', submitInquiry);
  qs('#shortsForm').addEventListener('submit', submitShorts);
  qs('#logoutBtn').addEventListener('click', () => {
    state.loggedIn = false;
    qs('#mainScreen').classList.add('hidden');
    qs('#loginScreen').classList.remove('hidden');
    toast('로그아웃되었습니다');
  });
  qs('#refreshBtn').addEventListener('click', refreshAll);
}

async function bootstrap() {
  await initFirebase();
  bindEvents();
  setTab('dashboard');
}

document.addEventListener('DOMContentLoaded', bootstrap);
