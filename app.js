const state = {
  loggedIn: false,
  currentTab: 'dashboard',
  profile: { name: '방문자', role: '수요자' },
  stats: {
    demand: 189,
    supply: 247,
    shorts: 22,
    contracts: 14,
  },
  feed: {
    demand: [
      { title: '수요자 #001', sub: '학군지역 · 매수 · 30억대 · 대치동', state: 'matching', label: '매칭대기' },
      { title: '수요자 #002', sub: '한강벨트 · 전세 · 20억대 · 반포동', state: 'ai', label: 'AI매칭중' },
      { title: '수요자 #003', sub: '학군지역 · 단기임대 · 역삼동', state: 'contract', label: '계약진행' }
    ],
    supply: [
      { title: '대치 SK뷰 33평 급매', sub: '24.5억 · 즉시입주 · AI저평가 ▼8.2%', state: 'contract', label: '숏츠대기' },
      { title: '반포 레미안퍼스티지 59평', sub: '82억 · 한강뷰 · ▼6.1%', state: 'matching', label: '매칭완료' },
      { title: '시그니엘 레지던스 95평', sub: '보증금 3억 / 월 1,800만', state: 'ai', label: '추천노출' }
    ]
  }
};

function qs(sel) { return document.querySelector(sel); }
function qsa(sel) { return [...document.querySelectorAll(sel)]; }

function toast(message) {
  const wrap = qs('.toast-wrap');
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = message;
  wrap.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function login(role) {
  state.loggedIn = true;
  state.profile = {
    name: role === 'admin' ? '이상수 대표' : role === 'partner' ? '공동중개 파트너' : '카카오 회원',
    role: role === 'admin' ? '관리자' : role === 'partner' ? '공동중개' : '수요자'
  };
  qs('#loginScreen').classList.add('hidden');
  qs('#mainScreen').classList.remove('hidden');
  qs('#profileName').textContent = state.profile.name;
  qs('#profileRole').textContent = state.profile.role;
  toast(`${state.profile.role} 로그인 완료`);
}

function setTab(tab) {
  state.currentTab = tab;
  qsa('.tab').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
  qsa('.nav-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
  qsa('.screen').forEach(screen => screen.classList.toggle('active', screen.id === `screen-${tab}`));
}

function renderFeeds() {
  const render = (items, target) => {
    const html = items.map(item => `
      <div class="feed-card">
        <div class="feed-head">
          <div>
            <div class="feed-title">${item.title}</div>
            <div class="feed-sub">${item.sub}</div>
          </div>
          <span class="state ${item.state}">${item.label}</span>
        </div>
      </div>
    `).join('');
    qs(target).innerHTML = html;
  };
  render(state.feed.demand, '#recentDemand');
  render(state.feed.supply, '#recentSupply');
}

function submitInquiry(e) {
  e.preventDefault();
  const form = e.target;
  const kind = form.kind.value;
  const area = form.area.value;
  const budget = form.budget.value;
  toast(`${kind} 문의가 접수되었습니다 (${area || '지역미정'} / ${budget || '예산미정'})`);
  form.reset();
  setTab('dashboard');
}

function bindEvents() {
  qsa('[data-login]').forEach(btn => btn.addEventListener('click', () => login(btn.dataset.login)));
  qsa('.tab').forEach(btn => btn.addEventListener('click', () => setTab(btn.dataset.tab)));
  qsa('.nav-btn').forEach(btn => btn.addEventListener('click', () => setTab(btn.dataset.tab)));
  qs('#inquiryForm').addEventListener('submit', submitInquiry);
  qs('#logoutBtn').addEventListener('click', () => {
    state.loggedIn = false;
    qs('#mainScreen').classList.add('hidden');
    qs('#loginScreen').classList.remove('hidden');
    toast('로그아웃되었습니다');
  });
}

function bootstrap() {
  renderFeeds();
  bindEvents();
  setTab('dashboard');
}

document.addEventListener('DOMContentLoaded', bootstrap);
