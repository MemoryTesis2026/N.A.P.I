/* ═══════════════════════════════════════════
   ArchivaIA – app.js
   Lógica principal · INACAP Sede Maipú
   Paleta: Blue & Cyan Tech Intelligence
═══════════════════════════════════════════ */

// ──────────────────────────────────────────
//  DATASET — 12 Proyectos Sede Maipú
// ──────────────────────────────────────────
const PROJECTS = [
  { id:1, nombre:"Sistema IoT de Monitoreo y Eficiencia Energética para Planta Industrial Maipú", carrera:"Electricidad y Electrónica", anio:2025, autores:"Diego Álvarez, Valentina Cruz", desc:"Plataforma IoT con ESP32 y sensores SCT-013 para telemetría energética en tiempo real. Algoritmo predictivo por turnos con alertas automáticas vía Telegram.", stack:["ESP32","MQTT","Node.js","React","MongoDB","TensorFlow Lite"], estado:"Público", nota:6.7 },
  { id:2, nombre:"App Móvil de Gestión de Stock y Trazabilidad QR para PyMEs Logísticas", carrera:"Informática / Ing. en Computación", anio:2025, autores:"Camila Herrera, Francisco Sepúlveda", desc:"App multiplataforma para control de inventario con escaneo masivo QR, sincronización offline-first, reporte de stock crítico y backend distribuido en FastAPI.", stack:["React Native","FastAPI","PostgreSQL","Docker","AWS S3"], estado:"Público", nota:6.8 },
  { id:3, nombre:"Plataforma E-Commerce con Motor de Recomendación IA y Pagos Webpay", carrera:"Informática / Ing. en Computación", anio:2024, autores:"Matías Rojas, Sofía Morales, Ignacio Vega", desc:"E-commerce con filtrado colaborativo en Python para recomendación personalizada, panel analítico de conversión y chatbot transaccional integrado.", stack:["Next.js","Python","Scikit-learn","Redis","Transbank API","MySQL"], estado:"Público", nota:6.9 },
  { id:4, nombre:"Diagnóstico Predictivo de Vibraciones en Motores Diésel", carrera:"Mecánica Automotriz e Industrial", anio:2025, autores:"Pablo Fuentes, Andrés Muñoz", desc:"Telemetría mecánica con FFT y acelerómetros MEMS para prevención de desalineaciones y desbalances en maquinaria pesada industrial.", stack:["Python","SciPy","InfluxDB","Grafana","Raspberry Pi 4","Twilio API"], estado:"Público", nota:6.7 },
  { id:5, nombre:"Dashboard BI y Predicción RFM para Retail Maipú", carrera:"Administración de Empresas", anio:2024, autores:"Javiera Contreras, Rodrigo Sánchez", desc:"Inteligencia de negocios para retail local: consolida ERP, segmenta clientes por RFM y proyecta ventas estacionales con modelos predictivos.", stack:["Power BI","SQL Server","Python","Excel VBA","Azure Synapse"], estado:"Público", nota:6.5 },
  { id:6, nombre:"Simulador Inmersivo WebGL de Circuitos Eléctricos Trifásicos", carrera:"Electricidad y Electrónica", anio:2023, autores:"Nicolás Torres, Ángela Ramírez", desc:"Plataforma 3D interactiva en el navegador para ensayar tableros eléctricos trifásicos con multímetro virtual y cálculo de caídas de tensión seguro.", stack:["Three.js","WebRTC","Python Flask","SQLite","Tailwind CSS"], estado:"Público", nota:6.6 },
  { id:7, nombre:"Gestor Documental y Trazabilidad Aduanera para Embarques Marítimos", carrera:"Comercio Internacional", anio:2024, autores:"Carolina Espinoza, Luis Medina", desc:"Automatización de carpeta de importaciones con cálculo de aranceles Ad-Valorem, validación de Certificados de Origen y tracking GPS de contenedores.", stack:["Vue.js","Laravel","MySQL","Google Maps API","PDF.js"], estado:"Público", nota:6.4 },
  { id:8, nombre:"Control de Acceso Biométrico por Reconocimiento Facial con Edge AI", carrera:"Informática / Ing. en Computación", anio:2024, autores:"Maximiliano Bravo, Renata Castillo", desc:"Seguridad física con validación facial en tiempo real usando embeddings DeepFace, generación de informes de asistencia e integración con relé electromagnético.", stack:["Python","DeepFace","OpenCV","Django","PostgreSQL","Raspberry Pi"], estado:"Público", nota:7.0 },
  { id:9, nombre:"Asistente Conversacional NLP para Mantenimiento de Maquinaria Pesada", carrera:"Mecánica Automotriz e Industrial", anio:2025, autores:"Emilia Castro, Daniel Flores", desc:"Chatbot técnico especializado en manuales de talleres mecánicos que diagnóstica fallas hidráulicas y eléctricas mediante procesamiento de lenguaje natural.", stack:["Python","spaCy","Rasa Core","React","MongoDB","FastAPI"], estado:"En Revisión", nota:6.3 },
  { id:10, nombre:"Software BIM y Estimación Presupuestaria para Edificación", carrera:"Edificación y Construcción", anio:2024, autores:"Felipe Gutiérrez, Sebastián Vargas", desc:"Extrae cantidades de obra de archivos IFC/Revit y genera presupuestos de materiales automatizados según normativas chilenas.", stack:["Autodesk Forge","Node.js","Python","PostgreSQL","Three.js"], estado:"Público", nota:6.8 },
  { id:11, nombre:"Rover Teleoperado para Minería Subterránea con Sensores de Gas", carrera:"Minería y Metalurgia", anio:2025, autores:"Gonzalo Parra, Tamara Henríquez", desc:"Prototipo de rover explorador con detección remota de CO y CH4, cámara infrarroja y transmisión de mapa térmico 2D a estación de control.", stack:["Arduino","ROS 2","Python","React","WebSockets"], estado:"Público", nota:6.9 },
  { id:12, nombre:"Plataforma de Auditoría Ambiental y Huella de Carbono Corporativa", carrera:"Administración de Empresas", anio:2023, autores:"Bastián Morales, Camila Silva", desc:"Sistema cloud para calcular emisiones CO2eq (Alcances 1, 2 y 3) en empresas de servicios, compatible con estándar GHG Protocol.", stack:["React","Express.js","PostgreSQL","Chart.js","Node.js"], estado:"Público", nota:6.5 }
];

const CARRERAS = [
  "Informática / Ing. en Computación","Mecánica Automotriz e Industrial",
  "Electricidad y Electrónica","Administración de Empresas",
  "Comercio Internacional","Edificación y Construcción","Minería y Metalurgia"
];

const shortC = c => c.split('/')[0].trim();

// ──────────────────────────────────────────
//  CONFIGURACIÓN DE API Y ESTADO GLOBAL
// ──────────────────────────────────────────
const API_BASE_URL = (() => {
  if (typeof window !== 'undefined') {
    if (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' || window.location.protocol === 'file:') {
      if (window.location.port !== '8000') {
        return 'http://127.0.0.1:8000/api';
      }
    }
  }
  return '/api';
})();

let currentRole = 'docente';
let napiOpen = false;
let editingId = null;
let visPublic = true;
let currentModal = null;

// ══════════════════════════════════════════
//  MÓDULO 0: LANDING PAGE
// ══════════════════════════════════════════

// ── Carrusel Hero ──
let carouselIndex = 0;
let carouselTimer = null;
const TOTAL_SLIDES = 3;

function goToSlide(n) {
  // Quitar clase active del slide actual
  const prev = document.getElementById('slide-' + carouselIndex);
  const prevDot = document.querySelectorAll('.carousel-dot')[carouselIndex];
  if (prev) prev.classList.remove('active');
  if (prevDot) prevDot.classList.remove('active');

  carouselIndex = (n + TOTAL_SLIDES) % TOTAL_SLIDES;

  const curr = document.getElementById('slide-' + carouselIndex);
  const currDot = document.querySelectorAll('.carousel-dot')[carouselIndex];
  if (curr) curr.classList.add('active');
  if (currDot) currDot.classList.add('active');
}

function nextSlide() { goToSlide(carouselIndex + 1); resetCarouselTimer(); }
function prevSlide() { goToSlide(carouselIndex - 1); resetCarouselTimer(); }

function startCarouselTimer() {
  carouselTimer = setInterval(() => goToSlide(carouselIndex + 1), 5000);
}
function resetCarouselTimer() {
  clearInterval(carouselTimer);
  startCarouselTimer();
}

// ── Modales de Login (desde Landing) ──
function openLoginModal(role) {
  closeAllModals();
  const id = role === 'docente' ? 'modalDocente' : 'modalEstudiante';
  const el = document.getElementById(id);
  if (el) {
    el.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    currentModal = role;
  }
}

function closeLoginModal(role) {
  const id = role === 'docente' ? 'modalDocente' : 'modalEstudiante';
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('hidden');
    document.body.style.overflow = '';
    currentModal = null;
  }
}

function closeAllModals() {
  ['modalDocente','modalEstudiante'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });
  document.body.style.overflow = '';
  currentModal = null;
}

// Cerrar modales al hacer clic en el backdrop
document.addEventListener('click', function(e) {
  ['modalDocente','modalEstudiante'].forEach(id => {
    const el = document.getElementById(id);
    if (el && e.target === el) closeAllModals();
  });
});
// Cerrar con Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeAllModals();
});

// ── Estado de Usuario ──
let currentUser = null;

function updateUserDisplay(user) {
  if (!user) return;
  // Banner de estudiante
  const stName = document.getElementById('studentUserName');
  const stSub  = document.getElementById('studentUserSub');
  if (stName) stName.textContent = user.nombre || user.email;
  if (stSub) stSub.textContent = `${user.rol === 'docente' ? 'DOCENTE' : 'ALUMNO'} INACAP · ${user.carrera || 'SEDE MAIPÚ'}`;

  // Sidebar de admin
  const adName = document.getElementById('adminUserName');
  const adRole = document.getElementById('adminUserRole');
  const adAvatar = document.getElementById('adminUserAvatar');
  if (adName) adName.textContent = user.nombre || user.email;
  if (adRole) adRole.textContent = user.rol === 'docente' ? 'Docente / Admin' : 'Estudiante';
  if (adAvatar && user.nombre) {
    const initials = user.nombre.split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();
    adAvatar.textContent = initials || 'IN';
  }
}

// ── Modales de Login & Registro ──
function toggleRegisterForm(role, show = null) {
  const regId = role === 'docente' ? 'regFormDocente' : 'regFormEstudiante';
  const logId = role === 'docente' ? 'loginFormDocente' : 'loginFormEstudiante';
  const regEl = document.getElementById(regId);
  const logEl = document.getElementById(logId);
  if (!regEl || !logEl) return;

  const shouldShow = show !== null ? show : regEl.classList.contains('hidden');
  if (shouldShow) {
    regEl.classList.remove('hidden');
    logEl.classList.add('hidden');
  } else {
    regEl.classList.add('hidden');
    logEl.classList.remove('hidden');
  }
}

async function doModalRegister(role) {
  const isDoc = role === 'docente';
  const nombre = document.getElementById(isDoc ? 'regDocenteNombre' : 'regEstudianteNombre')?.value.trim();
  const email  = document.getElementById(isDoc ? 'regDocenteEmail' : 'regEstudianteEmail')?.value.trim();
  const pass   = document.getElementById(isDoc ? 'regDocentePass' : 'regEstudiantePass')?.value.trim();
  const carrera = isDoc
    ? 'Informática / Ing. en Computación'
    : (document.getElementById('regEstudianteCarrera')?.value || 'Informática / Ing. en Computación');

  const errEl  = document.getElementById(isDoc ? 'regDocenteError' : 'regEstudianteError');
  const errMsg = document.getElementById(isDoc ? 'regDocenteErrMsg' : 'regEstudianteErrMsg');

  if (!nombre || !email || !pass) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'Por favor completa todos los campos.';
    return;
  }
  if (pass.length < 6) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'La contraseña debe tener al menos 6 caracteres.';
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass, nombre, rol: role, carrera })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      toast(`✅ Cuenta de ${role} registrada exitosamente en Supabase`);
      // Llenar datos en el login y acceder automáticamente
      const emailInput = document.getElementById(isDoc ? 'dEmail' : 'eEmail');
      const passInput  = document.getElementById(isDoc ? 'dPass' : 'ePass');
      if (emailInput) emailInput.value = email;
      if (passInput) passInput.value = pass;
      toggleRegisterForm(role, false);
      await doModalLogin(role);
    } else {
      errEl?.classList.remove('hidden');
      if (errMsg) errMsg.textContent = data.detail || 'Error al crear la cuenta.';
    }
  } catch (err) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'Error de conexión: ' + err.message;
  }
}

async function doModalLogin(role, isDemo = false) {
  const emailId = role === 'docente' ? 'dEmail' : 'eEmail';
  const passId  = role === 'docente' ? 'dPass'  : 'ePass';
  const errId   = role === 'docente' ? 'loginError-d' : 'loginError-e';
  const errMsgId = role === 'docente' ? 'loginErrMsg-d' : 'loginErrMsg-e';

  if (isDemo) {
    document.getElementById(emailId).value = role === 'docente'
      ? 'docente.maipu@inacap.cl' : 'alumno.maipu@inacap.cl';
    document.getElementById(passId).value = 'InacapPassword123!';
  }

  const email = document.getElementById(emailId)?.value.trim();
  const pass  = document.getElementById(passId)?.value.trim();

  const errEl = document.getElementById(errId);
  const errMsg = document.getElementById(errMsgId);

  if (!email) { errEl?.classList.remove('hidden'); if(errMsg) errMsg.textContent='Ingresa tu correo institucional.'; return; }
  if (!pass)  { errEl?.classList.remove('hidden'); if(errMsg) errMsg.textContent='Ingresa tu contraseña.'; return; }

  // Autenticación con Backend / Supabase Auth
  let user = null;
  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass, role })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      user = data.user;
    } else {
      // Si la contraseña ingresada es 1234, admitir como demo
      if (pass === '1234') {
        user = {
          nombre: role === 'docente' ? 'Prof. Carlos Mendoza' : 'Francisca González',
          email: email,
          rol: role,
          carrera: 'Informática / Ing. en Computación'
        };
      } else {
        errEl?.classList.remove('hidden');
        if (errMsg) errMsg.textContent = data.detail || 'Credenciales inválidas.';
        return;
      }
    }
  } catch (err) {
    console.warn('Backend offline, usando fallback de sesión:', err);
    if (pass === '1234' || pass === 'InacapPassword123!') {
      user = {
        nombre: role === 'docente' ? 'Prof. Carlos Mendoza' : 'Francisca González',
        email: email,
        rol: role,
        carrera: 'Informática / Ing. en Computación'
      };
    } else {
      errEl?.classList.remove('hidden');
      if (errMsg) errMsg.textContent = 'Servidor inaccesible. Puedes usar la demo rápida o verificar el backend.';
      return;
    }
  }

  errEl?.classList.add('hidden');
  currentRole = user.rol || role;
  currentUser = user;
  localStorage.setItem('napi_user', JSON.stringify(currentUser));
  updateUserDisplay(currentUser);

  // Ocultar landing + modal, mostrar panel correspondiente
  closeAllModals();
  clearInterval(carouselTimer);

  const landing = document.getElementById('landingScreen');
  if (landing) landing.style.display = 'none';
  const legacyLogin = document.getElementById('loginScreen');
  if (legacyLogin) legacyLogin.style.display = 'none';

  setTimeout(() => {
    if (currentRole === 'docente') {
      document.getElementById('adminScreen').classList.remove('hidden');
      initAdmin();
    } else {
      document.getElementById('studentScreen').classList.remove('hidden');
      initStudent();
    }
    document.getElementById('napiWidget').style.display = 'flex';
    initNapi();
    toast(`🔑 Sesión iniciada: ${currentUser.nombre}`);
  }, 300);
}

// ── Navegación suave ──
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Menú Mobile ──
function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  if (menu) menu.classList.toggle('hidden');
}

// ── Navbar activo al scroll ──
function updateNavActive() {
  const sections = ['inicio','sobre-nosotros','origen','napi'];
  const links = document.querySelectorAll('.nav-landing-link');
  let current = '';
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el && window.scrollY >= el.offsetTop - 100) current = id;
  });
  links.forEach(link => {
    const href = link.getAttribute('href');
    link.style.color = href === '#' + current ? '#FFFFFF' : '';
    link.style.background = href === '#' + current ? 'rgba(255,255,255,0.08)' : '';
  });
}

// ── Init Landing (se ejecuta al cargar) ──
document.addEventListener('DOMContentLoaded', function() {
  // Ocultar pantallas de plataforma, mostrar landing por defecto
  const loginScreen = document.getElementById('loginScreen');
  if (loginScreen) loginScreen.style.display = 'none';

  // Iniciar carrusel automático
  startCarouselTimer();

  // Scroll activo en navbar
  window.addEventListener('scroll', updateNavActive, { passive: true });
});

// ══════════════════════════════════════════
//  MÓDULO 1: AUTENTICACIÓN
// ══════════════════════════════════════════

function selectRole(role) {
  currentRole = role;
  currentUser = {
    nombre: role === 'docente' ? 'Prof. Carlos Mendoza' : 'Francisca González',
    email: role === 'docente' ? 'docente.maipu@inacap.cl' : 'estudiante.maipu@inacapmail.cl',
    rol: role,
    carrera: 'Informática / Ing. en Computación'
  };
  localStorage.setItem('napi_user', JSON.stringify(currentUser));
  initNapi();
  document.getElementById('roleDocente')?.classList.toggle('active', role === 'docente');
  document.getElementById('roleEstudiante')?.classList.toggle('active', role === 'estudiante');
  const emailInput = document.getElementById('loginEmail');
  if (emailInput) {
    emailInput.value = role === 'docente' ? 'docente.maipu@inacap.cl' : 'estudiante.maipu@inacapmail.cl';
  }
}

function demoLogin(role) { selectRole(role); document.getElementById('loginPass').value='1234'; handleLogin(); }

function togglePass() {
  const i = document.getElementById('loginPass');
  i.type = i.type === 'password' ? 'text' : 'password';
}

function handleLogin() {
  const email = document.getElementById('loginEmail')?.value.trim() || (currentRole === 'docente' ? 'docente.maipu@inacap.cl' : 'estudiante.maipu@inacapmail.cl');
  const pass  = document.getElementById('loginPass')?.value.trim();
  if (!pass)  { showError('Ingresa tu contraseña.'); return; }
  if (pass !== '1234') { showError('Contraseña inválida. Usa "1234" para la demo.'); return; }

  currentUser = {
    nombre: currentRole === 'docente' ? 'Prof. Carlos Mendoza' : 'Francisca González',
    email: email,
    rol: currentRole,
    carrera: 'Informática / Ing. en Computación'
  };
  localStorage.setItem('napi_user', JSON.stringify(currentUser));

  document.getElementById('loginError')?.classList.add('hidden');
  document.getElementById('loginBtnTxt')?.classList.add('invisible');
  document.getElementById('loginSpinner')?.classList.remove('hidden');
  setTimeout(() => {
    document.getElementById('loginScreen')?.classList.add('hidden');
    if (currentRole === 'docente') {
      document.getElementById('adminScreen')?.classList.remove('hidden');
      initAdmin();
    } else {
      document.getElementById('studentScreen')?.classList.remove('hidden');
      initStudent();
    }
    document.getElementById('napiWidget').style.display = 'flex';
    initNapi();
    toast(`🔑 Sesión iniciada: ${currentUser.nombre}`);
  }, 400);
}

function showError(msg) {
  document.getElementById('loginErrMsg').textContent = msg;
  document.getElementById('loginError')?.classList.remove('hidden');
}

function logout() {
  // Resetear sesión del usuario
  currentUser = null;
  localStorage.removeItem('napi_user');

  // Ocultar pantallas de plataforma
  document.getElementById('adminScreen')?.classList.add('hidden');
  document.getElementById('studentScreen')?.classList.add('hidden');
  document.getElementById('napiWidget').style.display = 'flex';
  
  // Cerrar panel de chat y re-iniciar contexto de invitado
  napiOpen = false;
  document.getElementById('chatPanel')?.classList.add('hidden');
  initNapi();

  // Mostrar landing
  const landing = document.getElementById('landingScreen');
  if (landing) {
    landing.style.display = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // Reiniciar carrusel
    clearInterval(carouselTimer);
    goToSlide(0);
    startCarouselTimer();
  }
  toast('👋 Sesión cerrada correctamente');
}


// ══════════════════════════════════════════
//  MÓDULO 2: PANEL DOCENTE / ADMINISTRADOR
// ══════════════════════════════════════════
function adminTab(tab) {
  ['dashboard','upload','manage','reports'].forEach(t => {
    document.getElementById('tab-'+t)?.classList.toggle('hidden', t !== tab);
    document.getElementById('nav-'+t)?.classList.toggle('active', t === tab);
  });
  const titles = { dashboard:'Panel General de Control', upload:'Cargar Nuevo Proyecto', manage:'Gestor del Repositorio', reports:'Métricas e Informes Analíticos' };
  document.getElementById('adminTitle').textContent = titles[tab] || '';
}

function initAdmin() {
  adminTab('dashboard');
  renderKpis();
  renderCarreraChart();
  renderActivity();
  renderReviews();
  renderTable(PROJECTS);
  renderMetrics();
  renderYearBars();
  document.getElementById('fStack')?.addEventListener('input', function() {
    const tags = document.getElementById('techTags');
    if (!tags) return;
    tags.innerHTML = this.value.split(',').map(s => s.trim()).filter(Boolean)
      .map(t => `<span class="badge-tech">${t}</span>`).join('');
  });
}

function renderKpis() {
  const totEl = document.getElementById('kpiTotal');
  if (totEl) totEl.textContent = PROJECTS.length;
}

function renderCarreraChart() {
  const counts = {};
  PROJECTS.forEach(p => { const k = shortC(p.carrera); counts[k] = (counts[k]||0)+1; });
  const max = Math.max(...Object.values(counts));
  const el = document.getElementById('carreraChart');
  if (!el) return;
  el.innerHTML = Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([c,n]) => `
    <div>
      <div class="flex justify-between mb-1">
        <span class="text-xs font-semibold text-slate-700">${c}</span>
        <span class="text-xs font-bold text-cyan-700">${n}</span>
      </div>
      <div class="progress-track"><div class="progress-fill" style="width:${Math.round(n/max*100)}%"></div></div>
    </div>`).join('');
}

function renderActivity() {
  const acts = [
    {i:'📤', t:'Proyecto cargado: <strong class="text-cyan-700">IoT Telemetría Industrial</strong>', h:'Hace 1h'},
    {i:'🔍', t:'NAPI realizó <strong class="text-cyan-700">14 análisis</strong> hoy', h:'Hace 3h'},
    {i:'✅', t:'Aprobado: <strong class="text-slate-800">App Móvil Stock QR</strong>', h:'Hace 5h'},
    {i:'🔒', t:'Solicitud de acceso: <strong class="text-slate-700">Carlos Pérez</strong>', h:'Hace 8h'}
  ];
  const el = document.getElementById('recentActivity');
  if (el) el.innerHTML = acts.map(a=>`
    <div class="flex gap-3 p-2.5 rounded-xl bg-slate-50 border border-slate-200">
      <span class="shrink-0 text-base">${a.i}</span>
      <div>
        <p class="text-xs text-slate-700 leading-snug">${a.t}</p>
        <p class="text-[10px] text-slate-400 mt-0.5 font-medium">${a.h}</p>
      </div>
    </div>`).join('');
}

function renderReviews() {
  const reqs = [
    {n:'Emilia Castro', p:'Chatbot Orientación Vocacional', c:'Informática'},
    {n:'Roberto Lima',  p:'App Delivery con Drones',        c:'Mecánica'},
    {n:'Valentina Ríos',p:'Contabilidad Cloud',             c:'Administración'}
  ];
  const el = document.getElementById('reviewList');
  if (el) el.innerHTML = reqs.map(r=>`
    <div class="flex items-center gap-3 p-3 rounded-xl bg-white border border-slate-200 hover:border-cyan-400 transition-all">
      <div class="w-8 h-8 rounded-full bg-cyan-100 border border-cyan-300 text-cyan-800 text-xs font-bold flex items-center justify-center shrink-0">${r.n.split(' ').map(x=>x[0]).join('')}</div>
      <div class="flex-1 min-w-0">
        <p class="text-xs font-bold text-slate-800 truncate">${r.p}</p>
        <p class="text-[11px] text-slate-500">${r.n} · <span class="text-cyan-700">${r.c}</span></p>
      </div>
      <div class="flex gap-1.5 shrink-0">
        <button onclick="toast('✅ Solicitud aprobada')" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-blue-50 border border-blue-200 text-blue-700 hover:bg-blue-100 transition-colors">Aprobar</button>
        <button onclick="toast('❌ Solicitud rechazada')" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-red-50 border border-red-200 text-red-600 hover:bg-red-100 transition-colors">Rechazar</button>
      </div>
    </div>`).join('');
}

function renderTable(list) {
  const tbody = document.getElementById('projectBody');
  if (!tbody) return;
  document.getElementById('showCount').textContent  = list.length;
  document.getElementById('totalCount').textContent = PROJECTS.length;
  document.getElementById('manageEmpty')?.classList.toggle('hidden', list.length > 0);
  tbody.innerHTML = list.map(p => `
    <tr>
      <td class="px-4 py-3">
        <p class="font-bold text-slate-800 text-xs leading-snug" style="max-width:260px">${p.nombre}</p>
        <div class="flex gap-1 flex-wrap mt-1">${p.stack.slice(0,3).map(s=>`<span class="badge-tech">${s}</span>`).join('')}</div>
      </td>
      <td class="px-4 py-3"><span class="badge-cyan">${shortC(p.carrera)}</span></td>
      <td class="px-4 py-3 text-xs font-semibold text-slate-700">${p.anio}</td>
      <td class="px-4 py-3 text-xs text-slate-500">${p.autores}</td>
      <td class="px-4 py-3">
        <span class="text-[11px] font-bold px-2 py-0.5 rounded-full ${p.estado==='Público'?'bg-cyan-50 text-cyan-700 border border-cyan-200':'bg-slate-100 text-slate-500 border border-slate-200'}">${p.estado}</span>
      </td>
      <td class="px-4 py-3">
        <div class="flex gap-1.5">
          <button onclick="openEdit(${p.id})" class="p-1.5 rounded-lg bg-slate-100 hover:bg-cyan-50 text-slate-600 hover:text-cyan-700 transition-colors" title="Editar">✏️</button>
          <button onclick="toggleStatus(${p.id})" class="p-1.5 rounded-lg bg-slate-100 hover:bg-amber-50 text-slate-600 hover:text-amber-600 transition-colors" title="Visibilidad">${p.estado==='Público'?'👁️':'🙈'}</button>
          <button onclick="deleteP(${p.id})" class="p-1.5 rounded-lg bg-slate-100 hover:bg-red-50 text-slate-600 hover:text-red-600 transition-colors" title="Eliminar">🗑️</button>
        </div>
      </td>
    </tr>`).join('');
}

function filterTable() {
  const q = document.getElementById('manageSearch')?.value.toLowerCase()||'';
  const cat = document.getElementById('manageFilter')?.value.toLowerCase()||'';
  renderTable(PROJECTS.filter(p=>
    (!q||p.nombre.toLowerCase().includes(q)||p.autores.toLowerCase().includes(q))&&
    (!cat||p.carrera.toLowerCase().includes(cat))
  ));
}

function openEdit(id) {
  editingId = id;
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  document.getElementById('editNombre').value  = p.nombre;
  document.getElementById('editCarrera').value = p.carrera;
  document.getElementById('editEstado').value  = p.estado;
  document.getElementById('editModal').classList.remove('hidden');
}
function closeEdit() { document.getElementById('editModal').classList.add('hidden'); }
function saveEdit() {
  const p = PROJECTS.find(x=>x.id===editingId); if(!p) return;
  p.nombre  = document.getElementById('editNombre').value;
  p.carrera = document.getElementById('editCarrera').value;
  p.estado  = document.getElementById('editEstado').value;
  closeEdit(); filterTable(); toast('✅ Proyecto actualizado.');
}
function toggleStatus(id) {
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  p.estado = p.estado==='Público'?'Oculto':'Público';
  filterTable(); toast(`${p.estado==='Público'?'👁️ Visible':'🙈 Oculto'} en el catálogo.`);
}
function deleteP(id) {
  if (!confirm('¿Eliminar este proyecto del repositorio?')) return;
  const i = PROJECTS.findIndex(x=>x.id===id);
  if (i>=0) PROJECTS.splice(i,1);
  filterTable(); renderKpis(); toast('🗑️ Proyecto eliminado.');
}

function renderMetrics() {
  const counts = {}; PROJECTS.forEach(p=>{ const k=shortC(p.carrera); counts[k]=(counts[k]||0)+1; });
  const total = PROJECTS.length;
  const mc = document.getElementById('metCarrera');
  if (mc) mc.innerHTML = Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([c,n])=>`
    <div class="flex items-center gap-3">
      <span class="text-xs text-slate-700 w-36 truncate">${c}</span>
      <div class="flex-1 progress-track"><div class="progress-fill" style="width:${Math.round(n/total*100)}%"></div></div>
      <span class="text-xs font-bold text-cyan-700 w-14 text-right">${n} (${Math.round(n/total*100)}%)</span>
    </div>`).join('');

  const techC = {}; PROJECTS.forEach(p=>p.stack.forEach(t=>{ techC[t]=(techC[t]||0)+1; }));
  const topT = Object.entries(techC).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const maxT = topT[0]?.[1]||1;
  const mt = document.getElementById('metTech');
  if (mt) mt.innerHTML = topT.map(([t,n])=>`
    <div class="flex items-center gap-2">
      <span class="text-xs text-slate-700 w-24 truncate">${t}</span>
      <div class="flex-1 progress-track"><div class="progress-fill" style="width:${Math.round(n/maxT*100)}%"></div></div>
      <span class="text-xs font-bold text-cyan-700">${n}</span>
    </div>`).join('');

  const sum = [
    {l:'Proyectos Registrados',v:PROJECTS.length,i:'📁'},
    {l:'Carreras Sede Maipú',v:CARRERAS.length,i:'🎓'},
    {l:'Nota Promedio',v:(PROJECTS.reduce((a,p)=>a+p.nota,0)/PROJECTS.length).toFixed(1),i:'⭐'},
    {l:'Consultas NAPI IA',v:184,i:'🤖'},
    {l:'Estudiantes Activos',v:342,i:'👥'}
  ];
  const ss = document.getElementById('sysSummary');
  if (ss) ss.innerHTML = sum.map(s=>`
    <div class="flex justify-between py-2 border-b border-slate-100 last:border-0">
      <span class="text-xs text-slate-500">${s.i} ${s.l}</span>
      <span class="text-xs font-bold text-slate-800">${s.v}</span>
    </div>`).join('');
}

function renderYearBars() {
  const data = [{y:'2023',n:4},{y:'2024',n:5},{y:'2025',n:8}];
  const max = Math.max(...data.map(d=>d.n));
  const el = document.getElementById('yearChart');
  if (el) el.innerHTML = data.map(d=>`
    <div class="flex flex-col items-center gap-1 flex-1">
      <span class="text-xs font-bold text-cyan-700">${d.n}</span>
      <div class="w-full rounded-t-lg bg-cyan-600" style="height:${Math.round(d.n/max*100)}px"></div>
      <span class="text-xs text-slate-500">${d.y}</span>
    </div>`).join('');
}

function toggleVis() {
  visPublic = !visPublic;
  const btn = document.getElementById('visToggle');
  if (btn) btn.classList.toggle('bg-cyan-600', visPublic), btn.classList.toggle('bg-slate-400', !visPublic);
  const lbl = document.getElementById('visLabel');
  if (lbl) { lbl.textContent = visPublic?'Público (Visible para Estudiantes)':'Oculto (Sólo Administración)'; lbl.className = visPublic?'text-xs font-bold text-cyan-700':'text-xs font-bold text-slate-500'; }
}
function handleFile(e) {
  const f = e.target.files[0]; if(!f) return;
  document.getElementById('uploadDefault').classList.add('hidden');
  document.getElementById('uploadSelected').classList.remove('hidden');
  document.getElementById('fileName').textContent = `${f.name} (${(f.size/1048576).toFixed(1)} MB)`;
}
function clearForm() {
  ['fNombre','fCarrera','fAutores','fDesc','fStack'].forEach(id=>{ const el=document.getElementById(id); if(el) el.value=''; });
  document.getElementById('techTags').innerHTML='';
  document.getElementById('uploadDefault').classList.remove('hidden');
  document.getElementById('uploadSelected').classList.add('hidden');
}
function submitProject() {
  const nombre  = document.getElementById('fNombre')?.value.trim();
  const carrera = document.getElementById('fCarrera')?.value;
  const autores = document.getElementById('fAutores')?.value.trim();
  const desc    = document.getElementById('fDesc')?.value.trim();
  if (!nombre||!carrera||!autores||!desc) { toast('⚠️ Completa todos los campos obligatorios.'); return; }
  const stack = document.getElementById('fStack')?.value.split(',').map(s=>s.trim()).filter(Boolean)||['General'];
  const anio  = parseInt(document.getElementById('fAnio')?.value)||2025;
  PROJECTS.unshift({ id:PROJECTS.length+1, nombre, carrera, anio, autores, desc, stack, estado:visPublic?'Público':'Oculto', nota:6.5 });
  const sb = document.getElementById('uploadSuccess');
  if (sb) { sb.classList.remove('hidden'); setTimeout(()=>sb.classList.add('hidden'),4000); }
  clearForm(); filterTable(); renderKpis();
  toast('🚀 Proyecto registrado en el repositorio N.A.P.I.');

  // Sincronizar con Supabase y generar embedding en segundo plano
  fetch(`${API_BASE_URL}/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      titulo: nombre,
      carrera: carrera,
      anio: anio,
      autores: autores,
      resumen: desc
    })
  }).then(r => r.json()).then(res => {
    if (res.success) toast('⚡ Vectorizado y sincronizado en Supabase.');
  }).catch(() => {});
}

// ══════════════════════════════════════════
//  MÓDULO 3: PANEL ESTUDIANTE
// ══════════════════════════════════════════
function initStudent() { renderCards(PROJECTS.filter(p=>p.estado==='Público')); }

function renderCards(list) {
  const grid  = document.getElementById('studentGrid');
  const empty = document.getElementById('studentEmpty');
  const cnt   = document.getElementById('studentCount');
  if (cnt) cnt.textContent = `${list.length} proyecto${list.length!==1?'s':''} disponible${list.length!==1?'s':''}`;
  if (list.length===0) { if(grid) grid.innerHTML=''; if(empty) empty.classList.remove('hidden'); return; }
  if (empty) empty.classList.add('hidden');
  if (!grid) return;

  const pastelThemes = [
    { cardClass: 'card-pastel-rose', badgeColor: 'bg-rose-500', arrowColor: 'text-rose-600', icon: '📕' },
    { cardClass: 'card-pastel-peach', badgeColor: 'bg-amber-500', arrowColor: 'text-amber-600', icon: '🏛️' },
    { cardClass: 'card-pastel-mint', badgeColor: 'bg-emerald-500', arrowColor: 'text-emerald-600', icon: '💻' },
    { cardClass: 'card-pastel-sky', badgeColor: 'bg-sky-500', arrowColor: 'text-sky-600', icon: '🔬' },
    { cardClass: 'card-pastel-lavender', badgeColor: 'bg-purple-500', arrowColor: 'text-purple-600', icon: '📊' },
    { cardClass: 'card-pastel-butter', badgeColor: 'bg-yellow-500', arrowColor: 'text-yellow-700', icon: '⚡' }
  ];

  grid.innerHTML = list.map((p, idx) => {
    const theme = pastelThemes[idx % pastelThemes.length];
    return `
    <div class="${theme.cardClass} p-6 flex flex-col justify-between cursor-pointer anim-fade shadow-sm relative group" onclick="openProjModal(${p.id})">
      <div>
        <div class="flex items-center justify-between mb-4">
          <div class="w-10 h-10 rounded-xl ${theme.badgeColor} text-white flex items-center justify-center text-lg shadow-sm">
            ${theme.icon}
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-slate-500 bg-white/80 px-2.5 py-1 rounded-full border border-slate-200/60">${p.anio}</span>
            <span class="${theme.arrowColor} group-hover:scale-125 transition-transform text-lg font-bold">↗</span>
          </div>
        </div>
        <div class="mb-2">
          <span class="text-[10px] font-bold text-[#ED1C24] uppercase tracking-wider">${shortC(p.carrera)}</span>
        </div>
        <h3 class="font-black text-slate-800 text-sm leading-snug mb-2 clamp2 group-hover:text-[#ED1C24] transition-colors">${p.nombre}</h3>
        <p class="text-xs text-slate-600 leading-relaxed clamp3 mb-4">${p.desc}</p>
      </div>
      <div>
        <div class="flex flex-wrap gap-1.5 mb-4">
          ${p.stack.slice(0,4).map(t=>`<span class="badge-tech bg-white/90 border-slate-200">${t}</span>`).join('')}
          ${p.stack.length>4?`<span class="text-[10px] text-slate-500 font-semibold">+${p.stack.length-4}</span>`:''}
        </div>
        <div class="flex items-center justify-between pt-3 border-t border-slate-200/70">
          <span class="badge-restricted">🔒 Acceso Académico</span>
          <span class="text-xs font-bold text-[#ED1C24] hover:text-[#C41219] flex items-center gap-1 transition-colors">
            Ver Ficha <span>→</span>
          </span>
        </div>
      </div>
    </div>`;
  }).join('');
}

function filterCards() {
  const q    = document.getElementById('studentSearch')?.value.toLowerCase()||'';
  const car  = document.getElementById('carFilter')?.value.toLowerCase()||'';
  const anio = document.getElementById('anioFilter')?.value||'';
  const sort = document.getElementById('sortFilter')?.value||'newest';
  let list   = PROJECTS.filter(p=>p.estado==='Público').filter(p=>
    (!q||p.nombre.toLowerCase().includes(q)||p.desc.toLowerCase().includes(q)||p.stack.join(' ').toLowerCase().includes(q))&&
    (!car||p.carrera.toLowerCase().includes(car))&&
    (!anio||p.anio.toString()===anio)
  );
  if (sort==='oldest') list.sort((a,b)=>a.anio-b.anio);
  else if (sort==='newest') list.sort((a,b)=>b.anio-a.anio);
  else if (sort==='az') list.sort((a,b)=>a.nombre.localeCompare(b.nombre));
  renderCards(list);
}

function openProjModal(id) {
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  currentModal = p;
  document.getElementById('mBadge').textContent   = shortC(p.carrera);
  document.getElementById('mTitle').textContent   = p.nombre;
  document.getElementById('mAnio').textContent    = p.anio;
  document.getElementById('mAutores').textContent = p.autores;
  document.getElementById('mDesc').textContent    = p.desc;
  document.getElementById('mTechs').innerHTML     = p.stack.map(t=>`<span class="badge-cyan px-2.5 py-1 text-xs">${t}</span>`).join('');
  document.getElementById('projModal').classList.remove('hidden');
}
function closeProjModal() { document.getElementById('projModal').classList.add('hidden'); }
function requestAccess() { closeProjModal(); toast(`🔒 Solicitud enviada al docente para: "${currentModal?.nombre?.substring(0,35)}..."`); }
function sendToNapi() {
  closeProjModal(); if(!napiOpen) toggleChat();
  if(currentModal) setTimeout(()=>{ document.getElementById('napiInput').value=`Quiero hacer un proyecto similar a: "${currentModal.nombre}"`; sendMsg(); },300);
}

// ══════════════════════════════════════════
//  MÓDULO 4: ASISTENTE NAPI CON CHATS INDIVIDUALES
// ══════════════════════════════════════════

function getChatStorageKey() {
  if (currentUser && currentUser.email) {
    const rolePrefix = currentUser.rol === 'docente' ? 'docente' : 'estudiante';
    return `napi_chat_${rolePrefix}_${currentUser.email.toLowerCase().replace(/[^a-z0-9_]/g, '_')}`;
  }
  if (currentRole) {
    return `napi_chat_${currentRole}`;
  }
  return 'napi_chat_guest';
}

function saveChatHistory() {
  const box = document.getElementById('chatBox');
  if (!box) return;
  const key = getChatStorageKey();
  try {
    localStorage.setItem(key, box.innerHTML);
  } catch (e) {
    console.warn('No se pudo guardar historial local:', e);
  }
}

function clearUserChat() {
  const key = getChatStorageKey();
  localStorage.removeItem(key);
  const box = document.getElementById('chatBox');
  if (box) box.innerHTML = '';
  initNapi(true);
  toast('🗑️ Historial de conversación reiniciado');
}

function initNapi(forceGreeting = false) {
  const box = document.getElementById('chatBox');
  if (!box) return;

  // Actualizar indicador de privacidad en el header del chat
  const privacyBadge = document.getElementById('chatPrivacyBadge');
  if (privacyBadge) {
    if (currentUser) {
      const rolName = currentUser.rol === 'docente' ? 'Docente' : 'Estudiante';
      privacyBadge.textContent = `🔒 Chat de ${currentUser.nombre.split(' ')[0]} (${rolName})`;
    } else {
      privacyBadge.textContent = `🔒 Chat Individual · INACAP Maipú`;
    }
  }

  const key = getChatStorageKey();
  const saved = localStorage.getItem(key);

  if (!forceGreeting && saved && saved.trim().length > 0) {
    box.innerHTML = saved;
    box.scrollTop = box.scrollHeight;
    return;
  }

  box.innerHTML = '';
  if (currentUser && currentUser.rol === 'estudiante') {
    addNapi(`¡Hola **${currentUser.nombre}**! 👋 Soy **NAPI**, tu Asistente Inteligente para **${currentUser.carrera}** en INACAP Sede Maipú.\n\nEscribe la **idea de tu proyecto de título** y te diré qué porcentaje de coincidencia tiene con proyectos anteriores y cómo innovar para que sea único. 🚀`, false);
  } else if (currentUser && currentUser.rol === 'docente') {
    addNapi(`¡Hola **${currentUser.nombre}**! 👋 Soy **NAPI** en **Modo Docente**.\n\nPuedes consultar cualquier propuesta para evaluar similitud, originalidad y antecedentes en el repositorio institucional. 🎓`, false);
  } else {
    addNapi(`¡Hola! 👋 Soy **NAPI**, el Asistente Inteligente de INACAP Sede Maipú.\n\nEscribe la **idea de tu proyecto** y te diré qué porcentaje de coincidencia tiene con otros proyectos y cómo diferenciarte. 🚀`, false);
  }
}

function toggleChat() {
  napiOpen = !napiOpen;
  document.getElementById('chatPanel')?.classList.toggle('hidden', !napiOpen);
  document.getElementById('napiDot')?.classList.toggle('hidden', napiOpen);
  if (napiOpen) {
    initNapi();
    document.getElementById('napiInput')?.focus();
  }
}

function sendPreset(txt) {
  const input = document.getElementById('napiInput');
  if (input) input.value = txt;
  sendMsg();
}

function addNapi(txt, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'flex gap-2.5 items-start anim-fade mb-3.5';
  d.innerHTML = `
    <div class="w-8 h-8 rounded-full bg-cyan-500 border border-cyan-300 text-white text-sm font-bold flex items-center justify-center shrink-0 shadow">🤖</div>
    <div class="bubble-napi px-4 py-3 text-xs leading-relaxed max-w-[88%] shadow-sm">${fmt(txt)}</div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  if (save) saveChatHistory();
}

function addUser(txt, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'flex gap-2.5 items-start justify-end anim-fade mb-3.5';
  d.innerHTML = `
    <div class="bubble-user px-4 py-3 text-xs leading-relaxed max-w-[80%] shadow-sm">${txt}</div>
    <div class="w-8 h-8 rounded-full bg-slate-700 text-white text-sm font-bold flex items-center justify-center shrink-0">👤</div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  if (save) saveChatHistory();
}

function addTyping() {
  const box = document.getElementById('chatBox'); if(!box) return null;
  const d = document.createElement('div');
  d.id = 'typing';
  d.className = 'flex gap-2.5 items-start anim-fade mb-3';
  d.innerHTML = `<div class="w-8 h-8 rounded-full bg-cyan-500 border border-cyan-300 text-white text-sm font-bold flex items-center justify-center shrink-0">🤖</div>
    <div class="bubble-napi px-4 py-3"><div class="flex gap-1.5"><div class="dot-typing"></div><div class="dot-typing"></div><div class="dot-typing"></div></div></div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  return d;
}

function fmt(t) {
  if (!t) return '';
  return t
    .replace(/^### (.*$)/gim, '<h4 class="font-bold text-slate-800 text-xs mt-3 mb-1.5">$1</h4>')
    .replace(/^## (.*$)/gim, '<h3 class="font-bold text-cyan-800 text-sm mt-3.5 mb-1.5 pb-1 border-b border-cyan-100">$1</h3>')
    .replace(/^# (.*$)/gim, '<h2 class="font-black text-slate-900 text-sm mt-3.5 mb-1.5">$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-800 font-bold">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em class="text-slate-600">$1</em>')
    .replace(/^\d+\.\s+(.*$)/gim, '<div class="flex items-start gap-1.5 my-1 text-slate-700"><span class="text-cyan-600 font-bold">•</span><span>$1</span></div>')
    .replace(/^[-\*•]\s+(.*$)/gim, '<div class="flex items-start gap-1.5 my-1 text-slate-700"><span class="text-cyan-500 font-bold">•</span><span>$1</span></div>')
    .replace(/`([^`]+)`/g, '<code class="bg-slate-100 text-cyan-700 px-1 py-0.5 rounded text-[10px] font-mono">$1</code>')
    .replace(/\n\n/g, '<div class="my-2"></div>')
    .replace(/\n/g, '<br/>');
}

// Motor de análisis semántico local con lenguaje simple y motivador
function analyze(txt) {
  const lower = txt.toLowerCase();
  const words = lower.split(/[\s,.;:!?()]+/).filter(w => w.length > 3 && !['para', 'como', 'sobre', 'este', 'esta', 'unos', 'unas', 'pero', 'donde', 'desde', 'hacer', 'quiero', 'tengo', 'idea'].includes(w));
  
  let bestMatch = null;
  let maxScore = 0;

  PROJECTS.forEach(p => {
    const haystack = (p.nombre + ' ' + p.desc + ' ' + p.carrera + ' ' + p.stack.join(' ')).toLowerCase();
    let hits = 0;
    words.forEach(w => {
      if (haystack.includes(w)) hits += 1;
    });
    const score = words.length > 0 ? Math.min(Math.round((hits / words.length) * 100 * 1.6), 94) : 0;
    if (score > maxScore) {
      maxScore = score;
      bestMatch = p;
    }
  });

  if (bestMatch && maxScore >= 35) {
    return `## 💡 Diagnóstico de tu Idea

Tu idea tiene un **${maxScore}% de similitud** con un proyecto anterior en INACAP Sede Maipú:

* **Proyecto más parecido:** *"${bestMatch.nombre}"* (${bestMatch.anio})

## 🔍 ¿En qué se parece?
Tu propuesta comparte el enfoque de **${bestMatch.stack.slice(0, 3).join(', ')}** y el tipo de solución que aborda.

## 🚀 ¿Cómo puedes innovar y diferenciarte?
Para que tu proyecto sea único y destaque en tu titulación, puedes hacer lo siguiente:
1. **Agregar alertas automáticas:** Envío de notificaciones inmediatas al celular (por WhatsApp o Telegram) ante cualquier evento.
2. **Usar predicción simple con IA:** En vez de solo medir variables, programa un modelo que anticipe fallas antes de que ocurran.
3. **Aplicarlo a un caso real en Maipú:** Enfoca las pruebas directamente en un taller, empresa o comercio de la comuna.

## 🎯 Tu próximo paso
Revisa la ficha del proyecto coincidente y enfoca tu anteproyecto en una propuesta de valor única.`;
  }

  return `## 💡 Diagnóstico de tu Idea

* **Nivel de coincidencia:** **0% (Idea Original)**
* **Propuesta:** "${txt.substring(0, 60)}${txt.length > 60 ? '...' : ''}"

🎉 **¡Excelente propuesta!** No se detectaron proyectos con alta similitud en el repositorio de INACAP Sede Maipú.

## 🚀 ¿Cómo asegurar el éxito de tu proyecto?
1. **Tecnologías modernas:** Usa herramientas fáciles y escalables como FastAPI, Supabase y React/Next.js.
2. **Prototipo funcional:** Construye primero una prueba pequeña y medible.

## 🎯 Tu próximo paso
Empieza a redactar el alcance técnico y preséntalo con confianza a tu docente guía.`;
}

function addSimCard(p, pct, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'anim-fade mb-3 ml-8 cursor-pointer';
  const col = pct >= 75 ? 'bg-red-500' : pct >= 55 ? 'bg-amber-500' : 'bg-cyan-500';
  d.innerHTML = `
    <div onclick="openProjModal(${p.id})" class="sim-card p-3 rounded-xl bg-white border border-slate-200 shadow-sm hover:border-cyan-400 transition-all">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 rounded-xl ${col} text-white text-xs font-black flex items-center justify-center shrink-0 shadow">
          ${pct}%
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-bold text-slate-800 leading-tight">${p.nombre}</p>
          <p class="text-[10px] text-cyan-700 mt-1 font-semibold">${shortC(p.carrera)} · ${p.anio} · <span class="text-slate-500">${p.autores}</span></p>
        </div>
      </div>
      <p class="text-[11px] text-slate-500 mt-2 line-clamp-2">${p.desc}</p>
    </div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  if (save) saveChatHistory();
}

function addSimCardSupabase(sim, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'anim-fade mb-3 ml-8';
  const pct = Math.round(sim.porcentaje_similitud || 60);
  const col = pct >= 75 ? 'bg-red-500' : pct >= 55 ? 'bg-amber-500' : 'bg-cyan-500';
  d.innerHTML = `
    <div class="sim-card p-3 rounded-xl bg-white border border-slate-200 shadow-sm hover:border-cyan-400 transition-all">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 rounded-xl ${col} text-white text-xs font-black flex items-center justify-center shrink-0 shadow">
          ${pct}%
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-bold text-slate-800 leading-tight">${sim.titulo}</p>
          <p class="text-[10px] text-cyan-700 mt-1 font-semibold">${shortC(sim.carrera || '')} · ${sim.anio || 2025} · <span class="text-slate-500">${sim.autores || 'Autores INACAP'}</span></p>
        </div>
      </div>
      <p class="text-[11px] text-slate-500 mt-2 line-clamp-2">${sim.resumen || ''}</p>
    </div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  if (save) saveChatHistory();
}

async function sendMsg() {
  const input = document.getElementById('napiInput'); if(!input) return;
  const txt = input.value.trim(); if(!txt) return;
  addUser(txt);
  input.value = '';
  const typing = addTyping();

  // 1. Intentar llamar a la API FastAPI + Supabase + Gemini
  let responded = false;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000); // 4s timeout

    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: txt, umbral: 0.35, limite: 4 }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      if (typing) typing.remove();
      responded = true;

      // Renderizar análisis de NAPI
      if (data.analisis) {
        addNapi(data.analisis);
      } else {
        addNapi(analyze(txt));
      }

      // Renderizar cards de proyectos de Supabase
      if (data.similares && data.similares.length > 0) {
        data.similares.forEach((sim, idx) => {
          setTimeout(() => addSimCardSupabase(sim), 150 * (idx + 1));
        });
      }
      return;
    }
  } catch (err) {
    console.warn('Backend API /analyze con demora o no disponible:', err);
  }

  // 2. Respaldo directo en frontend (Garantizado 100% sin importar el estado del servidor)
  if (!responded) {
    setTimeout(() => {
      if (typing) typing.remove();
      addNapi(analyze(txt));

      const lower = txt.toLowerCase();
      const words = lower.split(/[\s,.;:!?()]+/).filter(w => w.length > 3);
      const top = PROJECTS.map(p => {
        const src = (p.nombre + ' ' + p.desc + ' ' + p.stack.join(' ')).toLowerCase();
        const cnt = words.filter(w => src.includes(w)).length;
        return { p, pct: Math.min(Math.round(cnt / Math.max(words.length, 1) * 100 * 1.65), 92) };
      }).filter(x => x.pct >= 35).sort((a, b) => b.pct - a.pct)[0];

      if (top) {
        setTimeout(() => addSimCard(top.p, top.pct), 200);
      }
    }, 300);
  }
}

// ══════════════════════════════════════════
//  UTILIDADES GLOBALES
// ══════════════════════════════════════════
function toast(msg) {
  const el = document.createElement('div');
  el.style.cssText='position:fixed;bottom:5.5rem;right:1.5rem;z-index:9999;background:#121826;color:#ffffff;border:1px solid #00B5E2;font-size:.8rem;font-weight:600;padding:.75rem 1.25rem;border-radius:.75rem;box-shadow:0 10px 25px rgba(0,0,0,.25);animation:fadeUp .3s ease';
  el.textContent=msg; document.body.appendChild(el);
  setTimeout(()=>{ el.style.opacity='0'; el.style.transition='opacity .3s'; setTimeout(()=>el.remove(),300); },3200);
}

document.addEventListener('DOMContentLoaded',()=>{
  ['projModal','editModal'].forEach(id=>{
    document.getElementById(id)?.addEventListener('click',function(e){ if(e.target===this) this.classList.add('hidden'); });
  });
});
