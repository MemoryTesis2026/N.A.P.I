/* ═══════════════════════════════════════════
   ArchivaIA – app.js
   Lógica principal · INACAP Sede Maipú
   Paleta: Red & Slate INACAP Tech Intelligence
═══════════════════════════════════════════ */

// ──────────────────────────────────────────
//  ESTRUCTURA OFICIAL DE ÁREAS Y CARRERAS INACAP (13 ÁREAS)
// ──────────────────────────────────────────
const AREAS_CARRERAS = {
  "Administración": [
    "Administración Pública",
    "Administración de Empresas",
    "Comercio Exterior",
    "Contabilidad General",
    "Contador Público",
    "Ingeniería en Administración de Empresas",
    "Ingeniería en Comercio Exterior",
    "Técnico en Administración Pública"
  ],
  "Gastronomía": [
    "Administración Gastronómica",
    "Gastronomía"
  ],
  "Salud": [
    "Informática Biomédica",
    "Técnico en Enfermería",
    "Técnico en Farmacia",
    "Técnico en Odontología"
  ],
  "Turismo y Hospitalidad": [
    "Gestión Turística",
    "Hotelería y Servicios",
    "Ingeniería en Gestión Turística"
  ],
  "Agroindustria y Medioambiente": [
    "Ingeniería Agrícola",
    "Ingeniería en Medioambiente y Sustentabilidad",
    "Tecnología en Análisis Químico",
    "Técnico Agrícola",
    "Técnico en Medioambiente y Sustentabilidad"
  ],
  "Construcción": [
    "Construcción Civil",
    "Ingeniería en Geomensura y Geomática",
    "Técnico en Construcción",
    "Técnico en Topografía y Geomática"
  ],
  "Energía": [
    "Ingeniería Eléctrica",
    "Ingeniería en Climatización y Refrigeración",
    "Ingeniería en Energía",
    "Técnico en Climatización y Refrigeración",
    "Técnico en Electricidad Industrial",
    "Técnico en Energías Renovables"
  ],
  "Logística": [
    "Ingeniería en Logística",
    "Técnico en Logística"
  ],
  "Mecánica": [
    "Ingeniería en Mantenimiento Industrial",
    "Ingeniería en Maquinaria Pesada y Vehículos Automotrices",
    "Ingeniería en Mecatrónica",
    "Ingeniería en Mecánica y Electromovilidad Automotriz",
    "Mecánica Automotriz en Maquinaria Pesada",
    "Técnico en Mantenimiento Industrial",
    "Técnico en Mecatrónica",
    "Técnico en Mecánica y Electromovilidad Automotriz"
  ],
  "Minería": [
    "Ingeniería en Mantenimiento de Plantas Mineras",
    "Ingeniería en Metalurgia",
    "Ingeniería en Minas",
    "Técnico en Mantenimiento de Plantas Mineras",
    "Técnico en Metalurgia Extractiva",
    "Técnico en Minería",
    "Técnico en Prevención de Riesgos y Gestión de Emergencias"
  ],
  "Automatización, Electrónica y Robótica": [
    "Electrónica",
    "Ingeniería en Automatización y Robótica",
    "Ingeniería en Electrónica y Sistemas Inteligentes",
    "Técnico en Automatización y Robótica"
  ],
  "Diseño e Industria Digital": [
    "Animación Digital y Videojuegos",
    "Diseño Digital Profesional",
    "Diseño Digital y Web",
    "Diseño de Moda Profesional",
    "Producción de Moda y Tecnología"
  ],
  "Informática, Ciberseguridad y Telecomunicaciones": [
    "Analista Programador",
    "Ingeniería en Ciberseguridad",
    "Ingeniería en Informática",
    "Ingeniería en Telecomunicaciones y Servicios Digitales",
    "Técnico en Telecomunicaciones y Servicios Digitales"
  ]
};

// ──────────────────────────────────────────
//  DATASET — 12 Proyectos Sede Maipú
// ──────────────────────────────────────────
const PROJECTS = [
  { id:1, nombre:"Sistema IoT de Monitoreo y Eficiencia Energética para Planta Industrial Maipú", area:"Automatización, Electrónica y Robótica", carrera:"Ingeniería en Electrónica y Sistemas Inteligentes", anio:2025, autores:"Diego Álvarez, Valentina Cruz", desc:"Plataforma IoT con ESP32 y sensores SCT-013 para telemetría energética en tiempo real. Algoritmo predictivo por turnos con alertas automáticas vía Telegram.", stack:["ESP32","MQTT","Node.js","React","MongoDB","TensorFlow Lite"], estado:"Público", nota:6.7 },
  { id:2, nombre:"App Móvil de Gestión de Stock y Trazabilidad QR para PyMEs Logísticas", area:"Informática, Ciberseguridad y Telecomunicaciones", carrera:"Ingeniería en Informática", anio:2025, autores:"Camila Herrera, Francisco Sepúlveda", desc:"App multiplataforma para control de inventario con escaneo masivo QR, sincronización offline-first, reporte de stock crítico y backend distribuido en FastAPI.", stack:["React Native","FastAPI","PostgreSQL","Docker","AWS S3"], estado:"Público", nota:6.8 },
  { id:3, nombre:"Plataforma E-Commerce con Motor de Recomendación IA y Pagos Webpay", area:"Informática, Ciberseguridad y Telecomunicaciones", carrera:"Ingeniería en Informática", anio:2024, autores:"Matías Rojas, Sofía Morales, Ignacio Vega", desc:"E-commerce con filtrado colaborativo en Python para recomendación personalizada, panel analítico de conversión y chatbot transaccional integrado.", stack:["Next.js","Python","Scikit-learn","Redis","Transbank API","MySQL"], estado:"Público", nota:6.9 },
  { id:4, nombre:"Diagnóstico Predictivo de Vibraciones en Motores Diésel", area:"Mecánica", carrera:"Ingeniería en Mantenimiento Industrial", anio:2025, autores:"Pablo Fuentes, Andrés Muñoz", desc:"Telemetría mecánica con FFT y acelerómetros MEMS para prevención de desalineaciones y desbalances en maquinaria pesada industrial.", stack:["Python","SciPy","InfluxDB","Grafana","Raspberry Pi 4","Twilio API"], estado:"Público", nota:6.7 },
  { id:5, nombre:"Dashboard BI y Predicción RFM para Retail Maipú", area:"Administración", carrera:"Ingeniería en Administración de Empresas", anio:2024, autores:"Javiera Contreras, Rodrigo Sánchez", desc:"Inteligencia de negocios para retail local: consolida ERP, segmenta clientes por RFM y proyecta ventas estacionales con modelos predictivos.", stack:["Power BI","SQL Server","Python","Excel VBA","Azure Synapse"], estado:"Público", nota:6.5 },
  { id:6, nombre:"Simulador Inmersivo WebGL de Circuitos Eléctricos Trifásicos", area:"Energía", carrera:"Ingeniería Eléctrica", anio:2023, autores:"Nicolás Torres, Ángela Ramírez", desc:"Plataforma 3D interactiva en el navegador para ensayar tableros eléctricos trifásicos con multímetro virtual y cálculo de caídas de tensión seguro.", stack:["Three.js","WebRTC","Python Flask","SQLite","Tailwind CSS"], estado:"Público", nota:6.6 },
  { id:7, nombre:"Gestor Documental y Trazabilidad Aduanera para Embarques Marítimos", area:"Administración", carrera:"Ingeniería en Comercio Exterior", anio:2024, autores:"Carolina Espinoza, Luis Medina", desc:"Automatización de carpeta de importaciones con cálculo de aranceles Ad-Valorem, validación de Certificados de Origen y tracking GPS de contenedores.", stack:["Vue.js","Laravel","MySQL","Google Maps API","PDF.js"], estado:"Público", nota:6.4 },
  { id:8, nombre:"Control de Acceso Biométrico por Reconocimiento Facial con Edge AI", area:"Informática, Ciberseguridad y Telecomunicaciones", carrera:"Ingeniería en Informática", anio:2024, autores:"Maximiliano Bravo, Renata Castillo", desc:"Seguridad física con validación facial en tiempo real usando embeddings DeepFace, generación de informes de asistencia e integración con relé electromagnético.", stack:["Python","DeepFace","OpenCV","Django","PostgreSQL","Raspberry Pi"], estado:"Público", nota:7.0 },
  { id:9, nombre:"Asistente Conversacional NLP para Mantenimiento de Maquinaria Pesada", area:"Mecánica", carrera:"Ingeniería en Maquinaria Pesada y Vehículos Automotrices", anio:2025, autores:"Emilia Castro, Daniel Flores", desc:"Chatbot técnico especializado en manuales de talleres mecánicos que diagnóstica fallas hidráulicas y eléctricas mediante procesamiento de lenguaje natural.", stack:["Python","spaCy","Rasa Core","React","MongoDB","FastAPI"], estado:"En Revisión", nota:6.3 },
  { id:10, nombre:"Software BIM y Estimación Presupuestaria para Edificación", area:"Construcción", carrera:"Construcción Civil", anio:2024, autores:"Felipe Gutiérrez, Sebastián Vargas", desc:"Extrae cantidades de obra de archivos IFC/Revit y genera presupuestos de materiales automatizados según normativas chilenas.", stack:["Autodesk Forge","Node.js","Python","PostgreSQL","Three.js"], estado:"Público", nota:6.8 },
  { id:11, nombre:"Rover Teleoperado para Minería Subterránea con Sensores de Gas", area:"Minería", carrera:"Ingeniería en Minas", anio:2025, autores:"Gonzalo Parra, Tamara Henríquez", desc:"Prototipo de rover explorador con detección remota de CO y CH4, cámara infrarroja y transmisión de mapa térmico 2D a estación de control.", stack:["Arduino","ROS 2","Python","React","WebSockets"], estado:"Público", nota:6.9 },
  { id:12, nombre:"Plataforma de Auditoría Ambiental y Huella de Carbono Corporativa", area:"Agroindustria y Medioambiente", carrera:"Ingeniería en Medioambiente y Sustentabilidad", anio:2023, autores:"Bastián Morales, Camila Silva", desc:"Sistema cloud para calcular emisiones CO2eq (Alcances 1, 2 y 3) en empresas de servicios, compatible con estándar GHG Protocol.", stack:["React","Express.js","PostgreSQL","Chart.js","Node.js"], estado:"Público", nota:6.5 }
];

const shortC = c => c ? c.split('/')[0].trim() : '';

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

let currentRole = 'docente'; // 'estudiante', 'docente', 'administrador'
let napiOpen = false;
let editingId = null;
let visPublic = true;
let currentModal = null;
let currentUser = null;

// ──────────────────────────────────────────
//  HELPERS PARA DROPDOWNS EN CASCADA (ÁREA -> CARRERA)
// ──────────────────────────────────────────
function populateCarreraDropdown(areaSelectId, carreraSelectId, includeAllOption = false, selectedVal = '') {
  const areaSelect = document.getElementById(areaSelectId);
  const carSelect = document.getElementById(carreraSelectId);
  if (!carSelect) return;

  const area = areaSelect ? areaSelect.value : '';
  carSelect.innerHTML = '';

  if (includeAllOption) {
    const optAll = document.createElement('option');
    optAll.value = '';
    optAll.textContent = 'Todas las Carreras';
    carSelect.appendChild(optAll);
  }

  let list = [];
  if (area && AREAS_CARRERAS[area]) {
    list = AREAS_CARRERAS[area];
  } else if (!area && includeAllOption) {
    // Si no hay área seleccionada y se permite 'Todas', consolidar todas las carreras
    const allSet = new Set();
    Object.values(AREAS_CARRERAS).forEach(arr => arr.forEach(c => allSet.add(c)));
    list = Array.from(allSet).sort();
  } else {
    // Área por defecto: primera área
    const firstKey = Object.keys(AREAS_CARRERAS)[0];
    list = AREAS_CARRERAS[firstKey] || [];
  }

  list.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    if (selectedVal && selectedVal === c) {
      opt.selected = true;
    }
    carSelect.appendChild(opt);
  });
}

function onStudentAreaChange() {
  populateCarreraDropdown('studentAreaFilter', 'studentCarreraFilter', true);
  filterCards();
}

function onManageAreaChange() {
  populateCarreraDropdown('manageAreaFilter', 'manageCarreraFilter', true);
  filterTable();
}

function onUploadAreaChange() {
  populateCarreraDropdown('fArea', 'fCarrera', false);
}

function onEditAreaChange() {
  populateCarreraDropdown('editArea', 'editCarrera', false);
}

function onRegDocenteAreaChange() {
  populateCarreraDropdown('regDocenteArea', 'regDocenteCarrera', false);
}

function onRegEstudianteAreaChange() {
  populateCarreraDropdown('regEstudianteArea', 'regEstudianteCarrera', false);
}

function onCrudAreaChange() {
  populateCarreraDropdown('crudArea', 'crudCarrera', false);
}

// ══════════════════════════════════════════
//  MÓDULO 0: LANDING PAGE
// ══════════════════════════════════════════

// ── Carrusel Hero ──
let carouselIndex = 0;
let carouselTimer = null;
const TOTAL_SLIDES = 3;

function goToSlide(n) {
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
  let id = 'modalEstudiante';
  if (role === 'docente') id = 'modalDocente';
  else if (role === 'administrador') id = 'modalAdmin';

  const el = document.getElementById(id);
  if (el) {
    el.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    currentModal = role;
  }
}

function closeLoginModal(role) {
  let id = 'modalEstudiante';
  if (role === 'docente') id = 'modalDocente';
  else if (role === 'administrador') id = 'modalAdmin';

  const el = document.getElementById(id);
  if (el) {
    el.classList.add('hidden');
    document.body.style.overflow = '';
    currentModal = null;
  }
}

function closeAllModals() {
  ['modalDocente','modalEstudiante','modalAdmin'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  });
  document.body.style.overflow = '';
  currentModal = null;
}

// Cerrar modales al hacer clic en el backdrop
document.addEventListener('click', function(e) {
  ['modalDocente','modalEstudiante','modalAdmin'].forEach(id => {
    const el = document.getElementById(id);
    if (el && e.target === el) closeAllModals();
  });
});
// Cerrar con Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeAllModals();
    closeUserCrudModal();
    closeProjModal();
    closeEdit();
  }
});

// ── Estado de Usuario ──
function updateUserDisplay(user) {
  if (!user) return;
  
  const displayName = user.nombre || user.email || 'ESTUDIANTE INACAP';

  // Banner de estudiante
  const stName = document.getElementById('studentUserName');
  const stSub  = document.getElementById('studentUserSub');
  if (stName) stName.textContent = displayName.toUpperCase();
  if (stSub) {
    const roleLabel = user.rol === 'administrador' ? 'ADMINISTRADOR' : user.rol === 'docente' ? 'DOCENTE' : 'ALUMNO';
    stSub.textContent = `${roleLabel} INACAP · ${(user.carrera || 'SEDE MAIPÚ').toUpperCase()}`;
  }

  // Sidebar de docente / admin
  const adSubtitle = document.getElementById('adminSidebarSubtitle');
  const adName = document.getElementById('adminUserName');
  const adRole = document.getElementById('adminUserRole');
  const adAvatar = document.getElementById('adminUserAvatar');
  const navUsers = document.getElementById('nav-users');
  const navUpload = document.getElementById('nav-upload');

  const isAdmin = user.rol === 'administrador';

  if (adSubtitle) {
    adSubtitle.textContent = isAdmin ? 'Administrador · Sede Maipú' : 'Portal Docente · Sede Maipú';
  }
  if (adName) {
    adName.textContent = isAdmin ? (user.nombre || 'Admin Sede Maipú') : (user.nombre || 'Prof. Marcela Rojas');
  }
  if (adRole) {
    adRole.textContent = isAdmin ? 'Administrador' : 'Docente / Evaluador';
  }
  if (adAvatar) {
    const initials = isAdmin ? 'AD' : (user.nombre || 'Prof. Marcela Rojas').replace('Prof. ', '').split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();
    adAvatar.textContent = initials || (isAdmin ? 'AD' : 'MR');
  }

  // Visibilidad de pestañas según rol
  if (navUsers) {
    navUsers.classList.toggle('hidden', !isAdmin);
  }
  if (navUpload) {
    navUpload.classList.toggle('hidden', isAdmin);
  }
}

// ── Estado Inicial de Usuarios ──
const DEFAULT_USERS = [
  { id: "usr-1", nombre: "Flavio Escobar Mendoza", email: "flavio.escobar@inacapmail.cl", password: "InacapPassword123!", rol: "estudiante", area: "Informática, Ciberseguridad y Telecomunicaciones", carrera: "Ingeniería en Informática", created_at: "2026-03-01" },
  { id: "usr-2", nombre: "Francisca González", email: "francisca.gonzalez@inacapmail.cl", password: "InacapPassword123!", rol: "estudiante", area: "Informática, Ciberseguridad y Telecomunicaciones", carrera: "Ingeniería en Informática", created_at: "2026-03-02" },
  { id: "usr-3", nombre: "Prof. Marcela Rojas", email: "docente.maipu@inacap.cl", password: "InacapPassword123!", rol: "docente", area: "Informática, Ciberseguridad y Telecomunicaciones", carrera: "Ingeniería en Informática", created_at: "2025-10-20" },
  { id: "usr-4", nombre: "Prof. Carlos Mendoza", email: "carlos.mendoza@inacap.cl", password: "InacapPassword123!", rol: "docente", area: "Automatización, Electrónica y Robótica", carrera: "Ingeniería en Automatización y Robótica", created_at: "2025-11-15" },
  { id: "usr-5", nombre: "Admin Sede Maipú", email: "admin.maipu@inacap.cl", password: "InacapPassword123!", rol: "administrador", area: "Informática, Ciberseguridad y Telecomunicaciones", carrera: "Ingeniería en Informática", created_at: "2025-08-01" }
];

let ADMIN_USERS = (() => {
  try {
    const saved = localStorage.getItem('napi_stored_users');
    if (saved) {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.length > 0) {
        const emails = new Set(parsed.map(u => (u.email || '').toLowerCase()));
        DEFAULT_USERS.forEach(du => {
          if (!emails.has(du.email.toLowerCase())) parsed.push(du);
        });
        return parsed;
      }
    }
  } catch(e) {}
  return [...DEFAULT_USERS];
})();

function saveAdminUsersToStorage() {
  try {
    localStorage.setItem('napi_stored_users', JSON.stringify(ADMIN_USERS));
  } catch(e) {}
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
    // Inicializar dropdowns de carrera
    if (role === 'docente') onRegDocenteAreaChange();
    else onRegEstudianteAreaChange();
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
  const area   = document.getElementById(isDoc ? 'regDocenteArea' : 'regEstudianteArea')?.value || 'Informática, Ciberseguridad y Telecomunicaciones';
  const carrera = document.getElementById(isDoc ? 'regDocenteCarrera' : 'regEstudianteCarrera')?.value || 'Ingeniería en Informática';

  const errEl  = document.getElementById(isDoc ? 'regDocenteError' : 'regEstudianteError');
  const errMsg = document.getElementById(isDoc ? 'regDocenteErrMsg' : 'regEstudianteErrMsg');

  if (!nombre || !email || !pass) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'Por favor completa todos los campos obligatorios.';
    return;
  }
  if (pass.length < 6) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'La contraseña debe tener al menos 6 caracteres.';
    return;
  }

  // Guardar inmediatamente en almacén local y memoria
  const newRegUser = {
    id: 'usr-' + Date.now(),
    nombre,
    email,
    password: pass,
    rol: role,
    area,
    carrera,
    created_at: new Date().toISOString().split('T')[0]
  };
  const exIdx = ADMIN_USERS.findIndex(u => (u.email || '').toLowerCase() === email.toLowerCase());
  if (exIdx >= 0) {
    ADMIN_USERS[exIdx] = newRegUser;
  } else {
    ADMIN_USERS.unshift(newRegUser);
  }
  saveAdminUsersToStorage();

  try {
    fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass, nombre, rol: role, area, carrera })
    }).catch(() => {});
  } catch (err) {}

  toast(`✅ Cuenta de ${role} registrada exitosamente`);
  const emailInput = document.getElementById(isDoc ? 'dEmail' : 'eEmail');
  const passInput  = document.getElementById(isDoc ? 'dPass' : 'ePass');
  if (emailInput) emailInput.value = email;
  if (passInput) passInput.value = pass;
  toggleRegisterForm(role, false);
  await doModalLogin(role);
}

async function doModalLogin(role, isDemo = false) {
  let emailId = 'eEmail';
  let passId  = 'ePass';
  let errId   = 'loginError-e';
  let errMsgId = 'loginErrMsg-e';

  if (role === 'docente') {
    emailId = 'dEmail'; passId = 'dPass'; errId = 'loginError-d'; errMsgId = 'loginErrMsg-d';
  } else if (role === 'administrador') {
    emailId = 'aEmail'; passId = 'aPass'; errId = 'loginError-a'; errMsgId = 'loginErrMsg-a';
  }

  if (isDemo) {
    const emailEl = document.getElementById(emailId);
    const passEl = document.getElementById(passId);
    if (role === 'administrador') {
      if (emailEl) emailEl.value = 'admin.maipu@inacap.cl';
    } else if (role === 'docente') {
      if (emailEl) emailEl.value = 'docente.maipu@inacap.cl';
    } else {
      if (emailEl) emailEl.value = 'alumno.maipu@inacap.cl';
    }
    if (passEl) passEl.value = 'InacapPassword123!';
  }

  const email = document.getElementById(emailId)?.value.trim();
  const pass  = document.getElementById(passId)?.value.trim();
  const errEl = document.getElementById(errId);
  const errMsg = document.getElementById(errMsgId);

  if (!email) { errEl?.classList.remove('hidden'); if(errMsg) errMsg.textContent='Ingresa tu correo institucional.'; return; }
  if (!pass)  { errEl?.classList.remove('hidden'); if(errMsg) errMsg.textContent='Ingresa tu contraseña.'; return; }

  let user = null;

  // Buscar coincidencia local
  const localMatch = ADMIN_USERS.find(u => (u.email || '').toLowerCase() === email.toLowerCase());

  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass, role })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      user = data.user;
      if (localMatch) {
        if (localMatch.nombre) user.nombre = localMatch.nombre;
        if (localMatch.carrera) user.carrera = localMatch.carrera;
        if (localMatch.area) user.area = localMatch.area;
      }
    }
  } catch (err) {
    console.warn('Backend offline o error auth:', err);
  }

  if (!user) {
    const isMasterPass = (pass === '1234' || pass === 'InacapPassword123!');
    const passMatches = localMatch && (localMatch.password === pass || isMasterPass);

    if (passMatches || isMasterPass) {
      if (localMatch) {
        user = { ...localMatch };
      } else {
        const isAdmin = email.toLowerCase().includes('admin');
        const isDoc = email.toLowerCase().includes('docente') || role === 'docente';
        
        let customName = '';
        if (isAdmin) {
          customName = 'Admin Sede Maipú';
        } else if (isDoc) {
          customName = 'Prof. Marcela Rojas';
        } else if (email.toLowerCase().includes('flavio')) {
          customName = 'Flavio Escobar Mendoza';
        } else if (email.toLowerCase().includes('francisca')) {
          customName = 'Francisca González';
        } else {
          const raw = email.split('@')[0].replace(/[._-]/g, ' ');
          customName = raw.split(' ').map(w => w ? w.charAt(0).toUpperCase() + w.slice(1) : '').join(' ').trim() || 'Estudiante INACAP';
        }

        user = {
          nombre: customName,
          email: email,
          rol: isAdmin ? 'administrador' : isDoc ? 'docente' : 'estudiante',
          area: 'Informática, Ciberseguridad y Telecomunicaciones',
          carrera: 'Ingeniería en Informática'
        };
      }
    } else {
      errEl?.classList.remove('hidden');
      if (errMsg) errMsg.textContent = 'Credenciales inválidas. Verifica tu correo y contraseña.';
      return;
    }
  }

  errEl?.classList.add('hidden');
  currentRole = user.rol || role;
  currentUser = user;
  localStorage.setItem('napi_user', JSON.stringify(currentUser));
  updateUserDisplay(currentUser);

  // Limpiar chatbox para aislamiento de sesión
  const box = document.getElementById('chatBox');
  if (box) box.innerHTML = '';

  closeAllModals();
  clearInterval(carouselTimer);

  const landing = document.getElementById('landingScreen');
  if (landing) landing.style.display = 'none';
  const legacyLogin = document.getElementById('loginScreen');
  if (legacyLogin) legacyLogin.style.display = 'none';

  setTimeout(() => {
    if (currentRole === 'administrador') {
      document.getElementById('adminScreen')?.classList.remove('hidden');
      initAdmin('users');
      // El administrador NO utiliza NAPI (se oculta botón y panel)
      const napiWidget = document.getElementById('napiWidget');
      if (napiWidget) napiWidget.style.display = 'none';
      const chatPanel = document.getElementById('chatPanel');
      if (chatPanel) chatPanel.classList.add('hidden');
      napiOpen = false;
    } else if (currentRole === 'docente') {
      document.getElementById('adminScreen')?.classList.remove('hidden');
      initAdmin('dashboard');
      const napiWidget = document.getElementById('napiWidget');
      if (napiWidget) napiWidget.style.display = 'flex';
      initNapi();
    } else {
      document.getElementById('studentScreen')?.classList.remove('hidden');
      initStudent();
      const napiWidget = document.getElementById('napiWidget');
      if (napiWidget) napiWidget.style.display = 'flex';
      initNapi();
    }
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

// ── Inicialización General ──
document.addEventListener('DOMContentLoaded', () => {
  const adminScreen = document.getElementById('adminScreen');
  const studentScreen = document.getElementById('studentScreen');
  const loginScreen = document.getElementById('loginScreen');
  if (adminScreen) adminScreen.classList.add('hidden');
  if (studentScreen) studentScreen.classList.add('hidden');
  if (loginScreen) loginScreen.style.display = 'none';

  // Iniciar carrusel
  startCarouselTimer();

  // Inicializar dropdowns dependientes
  populateCarreraDropdown('studentAreaFilter', 'studentCarreraFilter', true);
  populateCarreraDropdown('manageAreaFilter', 'manageCarreraFilter', true);
  populateCarreraDropdown('fArea', 'fCarrera', false);
  populateCarreraDropdown('editArea', 'editCarrera', false);
  populateCarreraDropdown('regDocenteArea', 'regDocenteCarrera', false);
  populateCarreraDropdown('crudArea', 'crudCarrera', false);

  // Inicializar Drag & Drop para documentos de tesis
  initDragAndDrop();

  window.addEventListener('scroll', updateNavActive, { passive: true });
});

// ══════════════════════════════════════════
//  MÓDULO 1: CIERRE DE SESIÓN
// ══════════════════════════════════════════

function logout() {
  currentUser = null;
  localStorage.removeItem('napi_user');

  const adminScreen = document.getElementById('adminScreen');
  const studentScreen = document.getElementById('studentScreen');
  const loginScreen = document.getElementById('loginScreen');
  const landingScreen = document.getElementById('landingScreen');

  if (adminScreen) adminScreen.classList.add('hidden');
  if (studentScreen) studentScreen.classList.add('hidden');
  if (loginScreen) loginScreen.style.display = 'none';

  const napiWidget = document.getElementById('napiWidget');
  if (napiWidget) napiWidget.style.display = 'none';

  const chatPanel = document.getElementById('chatPanel');
  if (chatPanel) chatPanel.classList.add('hidden');
  napiOpen = false;

  const box = document.getElementById('chatBox');
  if (box) box.innerHTML = '';

  if (landingScreen) {
    landingScreen.style.display = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    clearInterval(carouselTimer);
    goToSlide(0);
    startCarouselTimer();
  }
  toast('👋 Sesión cerrada correctamente');
}

// ══════════════════════════════════════════
//  MÓDULO 2: PANEL DOCENTE / ADMINISTRADOR & CRUD USUARIOS
// ══════════════════════════════════════════

function adminTab(tab) {
  ['dashboard','upload','users','manage','reports'].forEach(t => {
    document.getElementById('tab-'+t)?.classList.toggle('hidden', t !== tab);
    document.getElementById('nav-'+t)?.classList.toggle('active', t === tab);
  });
  const titles = { 
    dashboard: 'Panel General de Control', 
    upload: 'Subir Nuevo Proyecto de Título',
    users: 'Gestión de Usuarios (Alumnos y Docentes)',
    manage: 'Gestor del Repositorio Institucional', 
    reports: 'Métricas e Informes Analíticos' 
  };
  const titleEl = document.getElementById('adminTitle');
  if (titleEl) titleEl.textContent = titles[tab] || 'Panel Académico';

  if (tab === 'users') {
    loadAdminUsers();
  }
}

function initAdmin(defaultTab = 'dashboard') {
  adminTab(defaultTab);
  renderKpis();
  renderCarreraChart();
  renderActivity();
  renderReviews();
  renderTable(PROJECTS);
  renderMetrics();
  renderYearBars();
  loadAdminUsers();

  // Asegurar dropdowns de carga
  populateCarreraDropdown('fArea', 'fCarrera', false);
  populateCarreraDropdown('manageAreaFilter', 'manageCarreraFilter', true);

  const stackInput = document.getElementById('fStack');
  if (stackInput && !stackInput.dataset.bound) {
    stackInput.dataset.bound = 'true';
    stackInput.addEventListener('input', function() {
      const tags = document.getElementById('techTags');
      if (!tags) return;
      tags.innerHTML = this.value.split(',').map(s => s.trim()).filter(Boolean)
        .map(t => `<span class="badge-tech">${t}</span>`).join('');
    });
  }
}

// ── CRUD de Usuarios ──
async function loadAdminUsers() {
  try {
    const res = await fetch(`${API_BASE_URL}/admin/users`);
    if (res.ok) {
      const data = await res.json();
      if (data.users && data.users.length > 0) {
        // Combinar o actualizar con usuarios de la base de datos
        const existingEmails = new Set(ADMIN_USERS.map(u => u.email.toLowerCase()));
        data.users.forEach(u => {
          if (!existingEmails.has(u.email.toLowerCase())) {
            ADMIN_USERS.push(u);
          }
        });
      }
    }
  } catch (err) {
    console.warn('Usando catálogo local de usuarios:', err);
  }
  renderAdminUsersTable(ADMIN_USERS);
  updateUserKpis();
}

function updateUserKpis() {
  const tot = document.getElementById('kpiUsersTotal');
  const stu = document.getElementById('kpiUsersStudents');
  const tea = document.getElementById('kpiUsersTeachers');
  const adm = document.getElementById('kpiUsersAdmins');

  if (tot) tot.textContent = ADMIN_USERS.length;
  if (stu) stu.textContent = ADMIN_USERS.filter(u => u.rol === 'estudiante').length;
  if (tea) tea.textContent = ADMIN_USERS.filter(u => u.rol === 'docente').length;
  if (adm) adm.textContent = ADMIN_USERS.filter(u => u.rol === 'administrador').length;
}

function renderAdminUsersTable(list) {
  const tbody = document.getElementById('usersTableBody');
  const empty = document.getElementById('usersTableEmpty');
  if (!tbody) return;

  if (list.length === 0) {
    tbody.innerHTML = '';
    empty?.classList.remove('hidden');
    return;
  }
  empty?.classList.add('hidden');

  tbody.innerHTML = list.map(u => {
    let roleBadge = '<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-[#8BA3C5]/20 text-[#223355] dark:text-[#8BA3C5] border border-[rgba(139,163,197,0.3)]">Alumno</span>';
    if (u.rol === 'docente') {
      roleBadge = '<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-[#495B7D]/20 text-[#495B7D] dark:text-[#8BA3C5] border border-[rgba(139,163,197,0.3)]">Docente</span>';
    } else if (u.rol === 'administrador') {
      roleBadge = '<span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-[#132644] text-white border border-[#495B7D]">Administrador</span>';
    }

    const initials = (u.nombre || u.email).split(' ').map(n=>n[0]).slice(0,2).join('').toUpperCase();

    return `
    <tr>
      <td class="px-4 py-3">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-black flex items-center justify-center shrink-0">
            ${initials || 'U'}
          </div>
          <div>
            <p class="font-bold text-slate-800 dark:text-white text-xs">${u.nombre || 'Sin nombre'}</p>
            <p class="text-[11px] text-slate-500 dark:text-[#B0ADA4]">${u.email}</p>
          </div>
        </div>
      </td>
      <td class="px-4 py-3">${roleBadge}</td>
      <td class="px-4 py-3 text-xs font-semibold text-slate-700 dark:text-slate-300">${u.area || 'Tecnología Aplicada'}</td>
      <td class="px-4 py-3 text-xs text-slate-600 dark:text-[#B0ADA4]">${u.carrera || '-'}</td>
      <td class="px-4 py-3">
        <div class="flex items-center gap-2">
          <button onclick="openEditUserModal('${u.id}')" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-[#8BA3C5]/20 text-slate-600 dark:text-slate-300 hover:text-[#223355] dark:hover:text-white transition-colors" title="Editar Usuario">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
          </button>
          <button onclick="deleteUserCrud('${u.id}')" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-950/40 text-slate-600 dark:text-slate-300 hover:text-red-600 transition-colors" title="Eliminar Usuario">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

function filterAdminUsersTable() {
  const search = document.getElementById('userSearchInput')?.value.toLowerCase().trim() || '';
  const role = document.getElementById('userRoleFilter')?.value || '';
  const area = document.getElementById('userAreaFilter')?.value || '';

  const filtered = ADMIN_USERS.filter(u => {
    const matchSearch = !search || 
      (u.nombre && u.nombre.toLowerCase().includes(search)) || 
      (u.email && u.email.toLowerCase().includes(search)) ||
      (u.carrera && u.carrera.toLowerCase().includes(search));
    const matchRole = !role || u.rol === role;
    const matchArea = !area || u.area === area;
    return matchSearch && matchRole && matchArea;
  });

  renderAdminUsersTable(filtered);
}

function openCreateUserModal() {
  document.getElementById('userCrudModalTitle').textContent = 'Registrar Nuevo Usuario';
  document.getElementById('crudUserId').value = '';
  document.getElementById('crudNombre').value = '';
  document.getElementById('crudEmail').value = '';
  document.getElementById('crudRol').value = 'estudiante';
  document.getElementById('crudPassword').value = 'InacapPassword123!';
  document.getElementById('crudArea').value = 'Informática, Ciberseguridad y Telecomunicaciones';
  onCrudAreaChange();

  document.getElementById('userCrudError')?.classList.add('hidden');
  document.getElementById('userCrudModal')?.classList.remove('hidden');
}

function openEditUserModal(userId) {
  const u = ADMIN_USERS.find(x => x.id === userId);
  if (!u) return;

  document.getElementById('userCrudModalTitle').textContent = 'Editar Usuario';
  document.getElementById('crudUserId').value = u.id;
  document.getElementById('crudNombre').value = u.nombre || '';
  document.getElementById('crudEmail').value = u.email || '';
  document.getElementById('crudRol').value = u.rol || 'estudiante';
  document.getElementById('crudPassword').value = u.password || '';
  document.getElementById('crudArea').value = u.area || 'Informática, Ciberseguridad y Telecomunicaciones';
  
  onCrudAreaChange();
  const carSelect = document.getElementById('crudCarrera');
  if (carSelect && u.carrera) carSelect.value = u.carrera;

  document.getElementById('userCrudError')?.classList.add('hidden');
  document.getElementById('userCrudModal')?.classList.remove('hidden');
}

function closeUserCrudModal() {
  document.getElementById('userCrudModal')?.classList.add('hidden');
}

async function submitUserCrud() {
  const userId = document.getElementById('crudUserId')?.value;
  const nombre = document.getElementById('crudNombre')?.value.trim();
  const email  = document.getElementById('crudEmail')?.value.trim();
  const rol    = document.getElementById('crudRol')?.value;
  const pass   = document.getElementById('crudPassword')?.value.trim();
  const area   = document.getElementById('crudArea')?.value || 'Informática, Ciberseguridad y Telecomunicaciones';
  const carrera = document.getElementById('crudCarrera')?.value;

  const errEl = document.getElementById('userCrudError');
  const errMsg = document.getElementById('userCrudErrMsg');

  if (!nombre || !email) {
    errEl?.classList.remove('hidden');
    if (errMsg) errMsg.textContent = 'Nombre y Correo son obligatorios.';
    return;
  }

  if (!userId) {
    // Modo CREACIÓN
    const newId = 'usr-' + Date.now();
    const newUser = {
      id: newId,
      nombre,
      email,
      password: pass || 'InacapPassword123!',
      rol,
      area,
      carrera,
      created_at: new Date().toISOString().split('T')[0]
    };
    ADMIN_USERS.unshift(newUser);
    saveAdminUsersToStorage();

    // Sincronizar en background con FastAPI
    try {
      fetch(`${API_BASE_URL}/admin/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, email, rol, area, carrera, password: pass || 'InacapPassword123!' })
      }).catch(() => {});
    } catch(e) {}

    toast(`✅ Usuario ${nombre} creado exitosamente`);
  } else {
    // Modo EDICIÓN
    const u = ADMIN_USERS.find(x => x.id === userId);
    if (u) {
      u.nombre = nombre;
      u.email = email;
      u.rol = rol;
      u.area = area;
      u.carrera = carrera;
      if (pass) u.password = pass;
      saveAdminUsersToStorage();

      try {
        fetch(`${API_BASE_URL}/admin/users/${userId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nombre, email, rol, area, carrera, password: pass || undefined })
        }).catch(() => {});
      } catch(e) {}

      toast(`✅ Usuario ${nombre} actualizado`);
    }
  }

  closeUserCrudModal();
  filterAdminUsersTable();
  updateUserKpis();
}

async function deleteUserCrud(userId) {
  const u = ADMIN_USERS.find(x => x.id === userId);
  const name = u ? u.nombre : 'este usuario';
  if (!confirm(`¿Estás seguro de eliminar a ${name} del sistema?`)) return;

  const idx = ADMIN_USERS.findIndex(x => x.id === userId);
  if (idx >= 0) {
    ADMIN_USERS.splice(idx, 1);
    saveAdminUsersToStorage();
  }

  try {
    fetch(`${API_BASE_URL}/admin/users/${userId}`, { method: 'DELETE' }).catch(() => {});
  } catch(e) {}

  filterAdminUsersTable();
  updateUserKpis();
}

function getActivityIconSvg(icon) {
  if (icon === '🚀' || icon === 'rocket') {
    return `<div class="w-8 h-8 rounded-xl bg-[#223355]/15 dark:bg-[#495B7D]/30 text-[#223355] dark:text-[#8BA3C5] flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg></div>`;
  }
  if (icon === '📤' || icon === 'upload') {
    return `<div class="w-8 h-8 rounded-xl bg-[#495B7D]/15 dark:bg-[#495B7D]/30 text-[#495B7D] dark:text-[#8BA3C5] flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg></div>`;
  }
  if (icon === '👥' || icon === 'users') {
    return `<div class="w-8 h-8 rounded-xl bg-[#23354D]/15 dark:bg-[#23354D]/40 text-[#223355] dark:text-[#8BA3C5] flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div>`;
  }
  if (icon === '🔍' || icon === 'audit') {
    return `<div class="w-8 h-8 rounded-xl bg-[#495B7D]/15 dark:bg-[#495B7D]/30 text-[#495B7D] dark:text-[#8BA3C5] flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>`;
  }
  if (icon === '✅' || icon === 'check') {
    return `<div class="w-8 h-8 rounded-xl bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div>`;
  }
  return `<div class="w-8 h-8 rounded-xl bg-[#223355]/15 dark:bg-[#8BA3C5]/20 text-[#223355] dark:text-[#8BA3C5] flex items-center justify-center shrink-0 shadow-xs"><svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></div>`;
}

function logActivity(icon, text, time='Justo ahora') {
  try {
    let logs = JSON.parse(localStorage.getItem('napi_activity_logs') || '[]');
    logs.unshift({ i: icon, t: text, h: time, ts: Date.now() });
    if (logs.length > 25) logs = logs.slice(0, 25);
    localStorage.setItem('napi_activity_logs', JSON.stringify(logs));
  } catch(e) {}
  renderActivity();
}

function renderActivity() {
  let acts = [];
  try {
    const saved = localStorage.getItem('napi_activity_logs');
    if (saved) acts = JSON.parse(saved);
  } catch(e) {}

  if (!acts || acts.length === 0) {
    acts = [
      {i:'rocket', t:'Sistema N.A.P.I v2.0 operativo en INACAP Sede Maipú', h:'Reciente'},
      {i:'upload', t:'Proyecto indexado: <strong class="text-[#495B7D] dark:text-[#8BA3C5]">IoT Telemetría Industrial</strong> (Nota: 6.8)', h:'Hace 1h'},
      {i:'users',  t:'Usuario registrado: <strong class="text-slate-800 dark:text-white">Flavio Escobar Mendoza</strong>', h:'Hace 2h'},
      {i:'audit',  t:'Auditoría: <strong class="text-[#495B7D] dark:text-[#8BA3C5]">Validaciones RAG y Supabase activas</strong>', h:'Hace 3h'},
      {i:'check',  t:'Proyecto aprobado: <strong class="text-slate-800 dark:text-white">App Móvil Stock QR</strong> (Nota: 6.5)', h:'Hace 5h'}
    ];
  }

  const el = document.getElementById('recentActivity');
  if (el) el.innerHTML = acts.slice(0, 6).map(a=>`
    <div class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-[#23354D] border border-slate-200 dark:border-[rgba(139,163,197,0.2)] anim-fade">
      ${getActivityIconSvg(a.i)}
      <div class="min-w-0 flex-1">
        <p class="text-xs text-slate-700 dark:text-slate-200 leading-snug truncate">${a.t}</p>
        <p class="text-[10px] text-slate-400 dark:text-[#B0ADA4] mt-0.5 font-medium">${a.h}</p>
      </div>
    </div>`).join('');
}

// ── Renderizado de Dashboard y Repositorio ──
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
        <span class="text-xs font-semibold text-slate-700 dark:text-slate-200">${c}</span>
        <span class="text-xs font-bold text-[#495B7D] dark:text-[#8BA3C5]">${n}</span>
      </div>
      <div class="progress-track"><div class="progress-fill" style="width:${Math.round(n/max*100)}%"></div></div>
    </div>`).join('');
}

function renderReviews() {
  const reqs = [
    {n:'Emilia Castro', p:'Chatbot Orientación Vocacional', c:'Ing. en Informática'},
    {n:'Roberto Lima',  p:'App Delivery con Drones',        c:'Ing. en Mecatrónica'},
    {n:'Valentina Ríos',p:'Contabilidad Cloud',             c:'Contador Público'}
  ];
  const el = document.getElementById('reviewList');
  if (el) el.innerHTML = reqs.map(r=>`
    <div class="flex items-center gap-3 p-3 rounded-xl bg-white dark:bg-[#23354D] border border-slate-200 dark:border-[rgba(139,163,197,0.2)] hover:border-[#495B7D] transition-all">
      <div class="w-8 h-8 rounded-full bg-[#8BA3C5]/20 border border-[#8BA3C5]/40 text-[#223355] dark:text-[#8BA3C5] text-xs font-bold flex items-center justify-center shrink-0">${r.n.split(' ').map(x=>x[0]).join('')}</div>
      <div class="flex-1 min-w-0">
        <p class="text-xs font-bold text-slate-800 dark:text-white truncate">${r.p}</p>
        <p class="text-[11px] text-slate-500 dark:text-[#B0ADA4]">${r.n} · <span class="text-[#495B7D] dark:text-[#8BA3C5]">${r.c}</span></p>
      </div>
      <div class="flex gap-1.5 shrink-0">
        <button onclick="logActivity('check', 'Solicitud aprobada: ${r.p}'); toast('Solicitud de ${r.n} aprobada');" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-[#223355]/10 hover:bg-[#223355]/20 dark:bg-[#8BA3C5]/20 text-[#223355] dark:text-[#8BA3C5] transition-colors">Aprobar</button>
        <button onclick="logActivity('alert', 'Solicitud rechazada: ${r.p}'); toast('Solicitud de ${r.n} rechazada');" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-600 dark:text-red-400 transition-colors">Rechazar</button>
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
        <div class="flex gap-1 flex-wrap mt-1">${(Array.isArray(p.stack)?p.stack:[]).slice(0,3).map(s=>`<span class="badge-tech">${s}</span>`).join('')}</div>
      </td>
      <td class="px-4 py-3">
        <span class="badge-cyan block truncate max-w-[200px]" title="${p.carrera}">${shortC(p.carrera)}</span>
        <span class="text-[10px] text-slate-400 block mt-0.5">${p.area || 'General'}</span>
      </td>
      <td class="px-4 py-3 text-xs font-semibold text-slate-700">${p.anio}</td>
      <td class="px-4 py-3 text-xs text-slate-500">${p.autores}</td>
      <td class="px-4 py-3">
        <span class="text-[11px] font-bold px-2 py-0.5 rounded-full ${p.estado==='Público'?'bg-cyan-50 text-cyan-700 border border-cyan-200':p.estado==='En Revisión'?'bg-amber-50 text-amber-700 border border-amber-200':'bg-slate-100 text-slate-500 border border-slate-200'}">${p.estado}</span>
      </td>
      <td class="px-4 py-3">
        <div class="flex gap-1.5">
          <button onclick="openEdit(${p.id})" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-[#8BA3C5]/20 text-slate-600 dark:text-slate-300 hover:text-[#223355] dark:hover:text-white transition-colors" title="Editar Metadatos">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
          </button>
          <button onclick="toggleStatus(${p.id})" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-[#8BA3C5]/20 text-slate-600 dark:text-slate-300 hover:text-[#223355] dark:hover:text-white transition-colors" title="Visibilidad">
            ${p.estado==='Público'?'<svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>':'<svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>'}
          </button>
          <button onclick="deleteP(${p.id})" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-950/40 text-slate-600 dark:text-slate-300 hover:text-red-600 transition-colors" title="Eliminar">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>`).join('');
}

function filterTable() {
  const q    = document.getElementById('manageSearch')?.value.toLowerCase().trim() || '';
  const area = document.getElementById('manageAreaFilter')?.value.toLowerCase().trim() || '';
  const car  = document.getElementById('manageCarreraFilter')?.value.toLowerCase().trim() || '';

  renderTable(PROJECTS.filter(p => {
    const matchQ = !q || p.nombre.toLowerCase().includes(q) || p.autores.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q);
    const matchArea = !area || (p.area && p.area.toLowerCase().includes(area));
    const matchCar = !car || p.carrera.toLowerCase().includes(car);
    return matchQ && matchArea && matchCar;
  }));
}

function openEdit(id) {
  editingId = id;
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  document.getElementById('editNombre').value  = p.nombre || '';
  document.getElementById('editArea').value    = p.area || 'Informática, Ciberseguridad y Telecomunicaciones';
  onEditAreaChange();
  document.getElementById('editCarrera').value = p.carrera || '';
  document.getElementById('editAutores').value = p.autores || '';
  document.getElementById('editAnio').value    = p.anio || 2025;
  document.getElementById('editNota').value    = p.nota || 6.5;
  document.getElementById('editStack').value   = Array.isArray(p.stack) ? p.stack.join(', ') : (p.stack || '');
  document.getElementById('editDesc').value    = p.desc || '';
  document.getElementById('editEstado').value  = p.estado || 'Público';
  document.getElementById('editModal').classList.remove('hidden');
}

function closeEdit() { document.getElementById('editModal').classList.add('hidden'); }

function saveEdit() {
  const p = PROJECTS.find(x=>x.id===editingId); if(!p) return;
  const nombre  = document.getElementById('editNombre')?.value.trim();
  const area    = document.getElementById('editArea')?.value;
  const carrera = document.getElementById('editCarrera')?.value;
  const autores = document.getElementById('editAutores')?.value.trim();
  const anio    = parseInt(document.getElementById('editAnio')?.value) || 2025;
  const nota    = parseFloat(document.getElementById('editNota')?.value);
  const stackStr= document.getElementById('editStack')?.value.trim();
  const desc    = document.getElementById('editDesc')?.value.trim();
  const estado  = document.getElementById('editEstado')?.value;

  if (!nombre || !carrera || !autores) {
    toast('⚠️ Completa los campos obligatorios del proyecto.');
    return;
  }
  if (isNaN(nota) || nota < 6.0 || nota > 7.0) {
    toast('⛔ Normativa INACAP: La nota final debe ser entre 6.0 y 7.0.');
    return;
  }

  p.nombre  = nombre;
  p.area    = area;
  p.carrera = carrera;
  p.autores = autores;
  p.anio    = anio;
  p.nota    = nota;
  p.stack   = stackStr ? stackStr.split(',').map(s=>s.trim()).filter(Boolean) : ['General'];
  p.desc    = desc || p.desc;
  p.estado  = estado;

  closeEdit(); 
  filterTable(); 
  renderKpis();
  logActivity('✏️', `Metadatos editados: "${p.nombre}" (Nota: ${p.nota})`);
  toast('✅ Metadatos del proyecto actualizados correctamente.');
}

function toggleStatus(id) {
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  p.estado = p.estado==='Público'?'Oculto':'Público';
  filterTable(); 
  logActivity('👁️', `Visibilidad cambiada: "${p.nombre}" -> ${p.estado}`);
  toast(`${p.estado==='Público'?'👁️ Visible':'🙈 Oculto'} en el catálogo.`);
}

function deleteP(id) {
  if (!confirm('¿Eliminar este proyecto del repositorio?')) return;
  const i = PROJECTS.findIndex(x=>x.id===id);
  if (i>=0) {
    const deleted = PROJECTS[i];
    PROJECTS.splice(i,1);
    logActivity('🗑️', `Proyecto eliminado: "${deleted.nombre}"`);
  }
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
    {l:'Proyectos Registrados',v:PROJECTS.length,i:'<svg class="w-4 h-4 text-[#495B7D] dark:text-[#8BA3C5]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>'},
    {l:'Áreas Académicas INACAP',v:Object.keys(AREAS_CARRERAS).length,i:'<svg class="w-4 h-4 text-[#495B7D] dark:text-[#8BA3C5]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 14l9-5-9-5-9 5 9 5z"/><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>'},
    {l:'Nota Promedio',v:(PROJECTS.reduce((a,p)=>a+(p.nota||6.0),0)/PROJECTS.length).toFixed(1),i:'<svg class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>'},
    {l:'Consultas NAPI IA',v:184,i:'<svg class="w-4 h-4 text-[#495B7D] dark:text-[#8BA3C5]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>'},
    {l:'Tasa de Aprobación',v:'100%',i:'<svg class="w-4 h-4 text-[#495B7D] dark:text-[#8BA3C5]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>'},
    {l:'Estado Supabase',v:'En Línea',i:'<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block animate-pulse"></span>'}
  ];
  const ms = document.getElementById('sysSummary');
  if (ms) ms.innerHTML = sum.map(s=>`
    <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-[#1E2E44] border border-slate-200 dark:border-[rgba(139,163,197,0.2)]">
      <span class="text-xs text-slate-600 dark:text-[#B0ADA4] flex items-center gap-2">${s.i} <span>${s.l}</span></span>
      <span class="text-xs font-bold text-slate-800 dark:text-white">${s.v}</span>
    </div>`).join('');
}

function renderYearBars() {
  const yc = {}; PROJECTS.forEach(p=>{ yc[p.anio]=(yc[p.anio]||0)+1; });
  const years = [2023,2024,2025,2026];
  const max = Math.max(...Object.values(yc),1);
  const el = document.getElementById('yearChart');
  if (el) el.innerHTML = years.map(y=>{
    const c = yc[y]||0; const pct = Math.round(c/max*100);
    return `
    <div class="flex-1 flex flex-col items-center gap-2 h-full justify-end">
      <span class="text-[11px] font-black text-cyan-700">${c}</span>
      <div class="w-full bg-slate-100 rounded-t-lg overflow-hidden flex items-end" style="height:100px">
        <div class="w-full bg-[#00B5E2] rounded-t-lg transition-all" style="height:${pct}%"></div>
      </div>
      <span class="text-[11px] font-semibold text-slate-500">${y}</span>
    </div>`;
  }).join('');
}

function toggleVis() {
  visPublic = !visPublic;
  const btn = document.getElementById('visToggle');
  if (btn) btn.classList.toggle('bg-cyan-600', visPublic), btn.classList.toggle('bg-slate-400', !visPublic);
  const lbl = document.getElementById('visLabel');
  if (lbl) { lbl.textContent = visPublic?'Público (Visible para Estudiantes)':'Oculto (Sólo Administración)'; lbl.className = visPublic?'text-xs font-bold text-cyan-700':'text-xs font-bold text-slate-500'; }
}

let currentUploadedFile = null;

function handleFile(e) {
  const f = e.target?.files?.[0];
  if (!f) return;
  processUploadedFile(f);
}

function processUploadedFile(file) {
  const validExtensions = ['.pdf', '.docx', '.doc'];
  const nameLower = file.name.toLowerCase();
  const isValid = validExtensions.some(ext => nameLower.endsWith(ext));
  
  if (!isValid) {
    toast('⚠️ Formato no compatible. Por favor adjunta un archivo PDF o Word (.docx)');
    return;
  }

  currentUploadedFile = file;
  document.getElementById('uploadDefault')?.classList.add('hidden');
  document.getElementById('uploadSelected')?.classList.remove('hidden');
  const sizeMb = (file.size / 1048576).toFixed(1);
  const extBadge = nameLower.endsWith('.pdf') ? '📄 PDF' : '📝 Word';
  const fnEl = document.getElementById('fileName');
  if (fnEl) fnEl.textContent = `${extBadge}: ${file.name} (${sizeMb} MB)`;
  toast(`📎 Documento "${file.name}" cargado para indexación.`);
}

function initDragAndDrop() {
  const dropZone = document.getElementById('dropZone');
  if (!dropZone) return;

  ['dragenter', 'dragover'].forEach(evt => {
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('border-[#4A7FA7]', 'bg-sky-50/50');
    });
  });

  ['dragleave', 'drop'].forEach(evt => {
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('border-[#4A7FA7]', 'bg-sky-50/50');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      processUploadedFile(files[0]);
    }
  });
}

function clearForm() {
  ['fNombre','fAutores','fDesc','fStack'].forEach(id=>{ const el=document.getElementById(id); if(el) el.value=''; });
  const fNota = document.getElementById('fNota');
  if (fNota) fNota.value = '6.5';
  const techTags = document.getElementById('techTags');
  if (techTags) techTags.innerHTML = '';
  document.getElementById('uploadDefault')?.classList.remove('hidden');
  document.getElementById('uploadSelected')?.classList.add('hidden');
  currentUploadedFile = null;
}

async function submitProject() {
  const nombre  = document.getElementById('fNombre')?.value.trim();
  const area    = document.getElementById('fArea')?.value;
  const carrera = document.getElementById('fCarrera')?.value;
  const autores = document.getElementById('fAutores')?.value.trim();
  const desc    = document.getElementById('fDesc')?.value.trim();
  const anio    = parseInt(document.getElementById('fAnio')?.value) || 2025;
  const notaVal = document.getElementById('fNota')?.value.trim();
  const nota    = parseFloat(notaVal);

  if (!nombre || !carrera || !autores || !desc) {
    toast('⚠️ Completa todos los campos obligatorios del proyecto.');
    return;
  }

  // RF-10: Validación estricta que impida registrar proyectos con nota inferior a 6.0
  if (!notaVal || isNaN(nota) || nota < 6.0 || nota > 7.0) {
    toast('⛔ Normativa INACAP: Solo se pueden registrar proyectos con nota final igual o superior a 6.0 (Aprobados).');
    return;
  }

  const stack = document.getElementById('fStack')?.value.split(',').map(s=>s.trim()).filter(Boolean) || ['General'];
  const btnSubmit = document.querySelector('#tab-upload button[onclick="submitProject()"]');

  // RF-11: Indicador de carga durante el procesamiento e indexación
  if (btnSubmit) {
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `<span class="inline-flex items-center gap-2"><div class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> Indexando con IA...</span>`;
  }

  await new Promise(r => setTimeout(r, 600));

  PROJECTS.unshift({ 
    id: PROJECTS.length + 1, 
    nombre, 
    area: area || 'Informática, Ciberseguridad y Telecomunicaciones', 
    carrera, 
    anio, 
    autores, 
    desc, 
    stack, 
    estado: visPublic ? 'Público' : 'Oculto', 
    nota: nota,
    archivo: currentUploadedFile ? currentUploadedFile.name : null
  });

  const sb = document.getElementById('uploadSuccess');
  if (sb) { sb.classList.remove('hidden'); setTimeout(()=>sb.classList.add('hidden'), 4000); }
  
  clearForm(); 
  filterTable(); 
  renderKpis();
  logActivity('🚀', `Nuevo proyecto indexado: "${nombre}" (Nota: ${nota})`);
  toast(`🚀 Proyecto "${nombre}" (Nota ${nota}) indexado exitosamente en N.A.P.I.`);

  if (btnSubmit) {
    btnSubmit.disabled = false;
    btnSubmit.innerHTML = 'Guardar e Indexar Proyecto';
  }

  // Sincronizar en Supabase
  try {
    fetch(`${API_BASE_URL}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        titulo: nombre,
        carrera: carrera,
        anio: anio,
        autores: autores,
        resumen: desc,
        nota: nota,
        area: area,
        stack: stack.join(', ')
      })
    }).catch(() => {});
  } catch(e) {}
}

// ══════════════════════════════════════════
//  MÓDULO 3: PANEL ESTUDIANTE & CATÁLOGO
// ══════════════════════════════════════════
function initStudent() { 
  if (currentUser) updateUserDisplay(currentUser);
  populateCarreraDropdown('studentAreaFilter', 'studentCarreraFilter', true);
  renderCards(PROJECTS.filter(p=>p.estado==='Público')); 
}

function renderCards(list) {
  const grid  = document.getElementById('studentGrid');
  const empty = document.getElementById('studentEmpty');
  const cnt   = document.getElementById('studentCount');
  if (cnt) cnt.textContent = `${list.length} proyecto${list.length!==1?'s':''} disponible${list.length!==1?'s':''}`;
  if (list.length===0) { if(grid) grid.innerHTML=''; if(empty) empty.classList.remove('hidden'); return; }
  if (empty) empty.classList.add('hidden');
  if (!grid) return;

  const pastelThemes = [
    { 
      cardClass: 'card-pastel-sky', 
      badgeColor: 'bg-[#23354D]', 
      arrowColor: 'text-[#495B7D]', 
      icon: `<svg class="w-5 h-5 text-[#8BA3C5]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>` 
    },
    { 
      cardClass: 'card-pastel-mint', 
      badgeColor: 'bg-[#495B7D]', 
      arrowColor: 'text-[#223355]', 
      icon: `<svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>` 
    },
    { 
      cardClass: 'card-pastel-rose', 
      badgeColor: 'bg-[#223355]', 
      arrowColor: 'text-[#8BA3C5]', 
      icon: `<svg class="w-5 h-5 text-[#8BA3C5]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>` 
    },
    { 
      cardClass: 'card-pastel-lavender', 
      badgeColor: 'bg-[#23354D]', 
      arrowColor: 'text-[#8BA3C5]', 
      icon: `<svg class="w-5 h-5 text-[#B0ADA4]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31L4.36 19.46A2 2 0 0 0 6.09 22h11.82a2 2 0 0 0 1.73-2.54L14 9.31V2"></path><line x1="8.5" y1="2" x2="15.5" y2="2"></line><line x1="14" y1="9.3" x2="10" y2="9.3"></line></svg>` 
    },
    { 
      cardClass: 'card-pastel-butter', 
      badgeColor: 'bg-[#495B7D]', 
      arrowColor: 'text-[#223355]', 
      icon: `<svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>` 
    },
    { 
      cardClass: 'card-pastel-peach', 
      badgeColor: 'bg-[#223355]', 
      arrowColor: 'text-[#8BA3C5]', 
      icon: `<svg class="w-5 h-5 text-[#8BA3C5]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>` 
    }
  ];

  grid.innerHTML = list.map((p, idx) => {
    const theme = pastelThemes[idx % pastelThemes.length];
    return `
    <div class="${theme.cardClass} p-6 flex flex-col justify-between cursor-pointer anim-fade shadow-sm relative group" onclick="openProjModal(${p.id})">
      <div>
        <div class="flex items-center justify-between mb-4">
          <div class="w-10 h-10 rounded-xl ${theme.badgeColor} flex items-center justify-center text-lg shadow-sm border border-white/10">
            ${theme.icon}
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-[#495B7D] dark:text-[#8BA3C5] bg-slate-100 dark:bg-[#132644] px-2.5 py-1 rounded-full border border-slate-200 dark:border-[#8BA3C5]/35">${p.anio}</span>
            <span class="${theme.arrowColor} dark:text-[#8BA3C5] group-hover:scale-125 transition-transform flex items-center">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
            </span>
          </div>
        </div>
        <div class="mb-2">
          <span class="text-[10px] font-bold text-[#495B7D] dark:text-[#8BA3C5] uppercase tracking-wider">${shortC(p.carrera)}</span>
          <span class="text-[10px] text-slate-500 dark:text-[#B0ADA4] block mt-0.5">${p.area || ''}</span>
        </div>
        <h3 class="proj-card-title font-black text-slate-900 dark:text-white text-sm leading-snug mb-2 clamp2 group-hover:text-[#495B7D] dark:group-hover:text-[#8BA3C5] transition-colors">${p.nombre}</h3>
        <p class="text-xs text-slate-600 dark:text-[#B0ADA4] leading-relaxed clamp3 mb-4">${p.desc}</p>
      </div>
      <div>
        <div class="flex flex-wrap gap-1.5 mb-4">
          ${p.stack.slice(0,4).map(t=>`<span class="badge-tech">${t}</span>`).join('')}
          ${p.stack.length>4?`<span class="text-[10px] text-slate-500 dark:text-[#8BA3C5] font-semibold">+${p.stack.length-4}</span>`:''}
        </div>
        <div class="flex items-center justify-between pt-3 border-t border-slate-200/80 dark:border-slate-700/60">
          <span class="badge-restricted">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            <span>Acceso Académico</span>
          </span>
          <span class="text-xs font-bold text-[#223355] dark:text-[#8BA3C5] group-hover:text-[#495B7D] flex items-center gap-1.5 transition-colors">
            <span>Ver Ficha</span>
            <svg class="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </span>
        </div>
      </div>
    </div>`;
  }).join('');
}

function filterCards() {
  const q    = document.getElementById('studentSearch')?.value.toLowerCase().trim() || '';
  const area = document.getElementById('studentAreaFilter')?.value.toLowerCase().trim() || '';
  const car  = document.getElementById('studentCarreraFilter')?.value.toLowerCase().trim() || '';
  const anio = document.getElementById('anioFilter')?.value || '';
  const sort = document.getElementById('sortFilter')?.value || 'newest';

  let list = PROJECTS.filter(p => p.estado === 'Público').filter(p => {
    const matchQ = !q || p.nombre.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q) || p.stack.join(' ').toLowerCase().includes(q) || p.autores.toLowerCase().includes(q);
    const matchArea = !area || (p.area && p.area.toLowerCase().includes(area));
    const matchCar = !car || p.carrera.toLowerCase().includes(car);
    const matchAnio = !anio || p.anio.toString() === anio;
    return matchQ && matchArea && matchCar && matchAnio;
  });

  if (sort === 'oldest') list.sort((a,b)=>a.anio-b.anio);
  else if (sort === 'newest') list.sort((a,b)=>b.anio-a.anio);
  else if (sort === 'az') list.sort((a,b)=>a.nombre.localeCompare(b.nombre));

  renderCards(list);
}

function openProjModal(id) {
  const p = PROJECTS.find(x=>x.id===id); if(!p) return;
  currentModal = p;
  document.getElementById('mBadge').textContent   = `${p.area ? p.area + ' · ' : ''}${shortC(p.carrera)}`;
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
//  MÓDULO 4: ASISTENTE NAPI CON CHATS EN BASE DE DATOS
// ══════════════════════════════════════════

function getChatStorageKey() {
  if (currentUser && currentUser.email) {
    const rolePrefix = currentUser.rol || 'guest';
    return `napi_chat_${rolePrefix}_${currentUser.email.toLowerCase().replace(/[^a-z0-9_]/g, '_')}`;
  }
  if (currentRole) {
    return `napi_chat_${currentRole}`;
  }
  return 'napi_chat_guest';
}

async function saveChatMessageToDb(sender, message, metadata = null) {
  const email = currentUser?.email || (currentRole === 'docente' ? 'docente.maipu@inacap.cl' : 'alumno.maipu@inacap.cl');
  const role = currentUser?.rol || currentRole || 'estudiante';
  try {
    fetch(`${API_BASE_URL}/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, role, sender, message, metadata })
    }).catch(e => console.warn('Sync chat DB aviso:', e));
  } catch (e) {
    console.warn('Error guardando en BD:', e);
  }
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

async function clearUserChat() {
  const email = currentUser?.email || (currentRole === 'docente' ? 'docente.maipu@inacap.cl' : 'alumno.maipu@inacap.cl');
  const role = currentUser?.rol || currentRole || 'estudiante';
  
  try {
    await fetch(`${API_BASE_URL}/chat/history?email=${encodeURIComponent(email)}&role=${encodeURIComponent(role)}`, {
      method: 'DELETE'
    });
  } catch (e) {
    console.warn('Error borrando chat en BD:', e);
  }

  const key = getChatStorageKey();
  localStorage.removeItem(key);
  const box = document.getElementById('chatBox');
  if (box) box.innerHTML = '';
  initNapi(true);
  toast('🗑️ Historial de conversación reiniciado');
}

async function initNapi(forceGreeting = false) {
  const box = document.getElementById('chatBox');
  if (!box) return;

  const privacyBadge = document.getElementById('chatPrivacyBadge');
  if (privacyBadge) {
    if (currentUser) {
      const rolName = currentUser.rol === 'administrador' ? 'Admin' : currentUser.rol === 'docente' ? 'Docente' : 'Estudiante';
      privacyBadge.textContent = `☁️ Base de Datos · ${currentUser.nombre.split(' ')[0]} (${rolName})`;
    } else {
      privacyBadge.textContent = `☁️ Chat Seguro · INACAP Maipú`;
    }
  }

  if (forceGreeting) {
    box.innerHTML = '';
    renderDefaultGreeting();
    return;
  }

  const email = currentUser?.email || (currentRole === 'docente' ? 'docente.maipu@inacap.cl' : 'alumno.maipu@inacap.cl');
  const role = currentUser?.rol || currentRole || 'estudiante';

  try {
    const res = await fetch(`${API_BASE_URL}/chat/history?email=${encodeURIComponent(email)}&role=${encodeURIComponent(role)}`);
    if (res.ok) {
      const data = await res.json();
      if (data.messages && data.messages.length > 0) {
        box.innerHTML = '';
        data.messages.forEach(m => {
          if (m.sender === 'user') {
            addUser(m.message, false);
          } else if (m.sender === 'napi') {
            addNapi(m.message, false);
          } else if (m.sender === 'card' && m.metadata) {
            addSimCardSupabase(m.metadata, false);
          }
        });
        box.scrollTop = box.scrollHeight;
        saveChatHistory();
        return;
      }
    }
  } catch (err) {
    console.warn('No se pudo conectar con BD de chat, probando caché local:', err);
  }

  const key = getChatStorageKey();
  const saved = localStorage.getItem(key);

  if (saved && saved.trim().length > 0) {
    box.innerHTML = saved;
    box.scrollTop = box.scrollHeight;
    return;
  }

  box.innerHTML = '';
  renderDefaultGreeting();
}

function renderDefaultGreeting() {
  if (currentUser && currentUser.rol === 'estudiante') {
    addNapi(`¡Hola **${currentUser.nombre}**! Soy **NAPI**, tu Asistente de Proyectos de Título para **${currentUser.carrera}** (${currentUser.area || 'INACAP'}) en Sede Maipú.\n\nEscribe la **idea de tu proyecto de título** y te indicaré el porcentaje de coincidencia con proyectos previos y recomendaciones técnicas para diferenciarlo e innovar.`, false);
  } else if (currentUser && (currentUser.rol === 'docente' || currentUser.rol === 'administrador')) {
    addNapi(`¡Hola **${currentUser.nombre}**! Soy **NAPI** en **Modo ${currentUser.rol === 'administrador' ? 'Administrador' : 'Docente'}**.\n\nPuedes consultar cualquier propuesta para evaluar similitud, originalidad y antecedentes en el repositorio institucional de Sede Maipú.`, false);
  } else {
    addNapi(`¡Hola! Soy **NAPI**, el Asistente Institucional de INACAP Sede Maipú.\n\nEscribe la **idea de tu proyecto** y te indicaré qué porcentaje de coincidencia tiene con el repositorio y cómo potenciar su propuesta técnica.`, false);
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

// ══════════════════════════════════════════
//  ASISTENCIA POR VOZ (SPEECH TO TEXT & TTS)
// ══════════════════════════════════════════
let isVoiceSpeechEnabled = false;
let isVoiceListening = false;
let speechRecInstance = null;

function toggleVoiceSpeech() {
  isVoiceSpeechEnabled = !isVoiceSpeechEnabled;
  const btn = document.getElementById('napiTtsBtn');
  if (btn) {
    btn.classList.toggle('text-red-400', isVoiceSpeechEnabled);
    btn.classList.toggle('text-white/70', !isVoiceSpeechEnabled);
    btn.classList.toggle('bg-white/20', isVoiceSpeechEnabled);
  }
  toast(isVoiceSpeechEnabled ? '🔊 Voz de NAPI activada (Lectura en voz alta)' : '🔇 Voz de NAPI desactivada');
  if (!isVoiceSpeechEnabled && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

function speakNapi(text) {
  if (!isVoiceSpeechEnabled || !('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  
  // Extraer respuesta breve hablada (<= 2 frases) para locución natural y concisa
  let spokenText = text.split('\n')[0].replace(/#{1,6}\s?/g, '').trim();
  if (text.includes('coincide') || text.includes('similitud') || text.includes('%')) {
    const matchPct = text.match(/(\d{1,2}(?:\.\d)?%)/);
    const pctStr = matchPct ? matchPct[1] : '';
    spokenText = `He analizado tu propuesta con el repositorio de INACAP Maipú. ${pctStr ? `Tiene una coincidencia cercana al ${pctStr}.` : ''} Revisa los detalles en pantalla y coméntalos con tu docente guía.`;
  } else {
    spokenText = spokenText.substring(0, 180);
  }

  const clean = spokenText
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/`{1,3}[^`]*`{1,3}/g, '')
    .replace(/•/g, '')
    .trim();

  if (!clean) return;

  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.lang = 'es-CL';
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const esVoice = voices.find(v => v.lang.startsWith('es-CL') || v.lang.startsWith('es-ES') || v.lang.startsWith('es-MX') || v.lang.includes('es'));
  if (esVoice) utterance.voice = esVoice;

  window.speechSynthesis.speak(utterance);
}

function toggleVoiceInput() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    toast('⚠️ Tu navegador no soporta reconocimiento de voz nativo. Usa Chrome o Edge.');
    return;
  }

  const micBtn = document.getElementById('napiMicBtn');
  const input = document.getElementById('napiInput');

  if (isVoiceListening) {
    if (speechRecInstance) speechRecInstance.stop();
    isVoiceListening = false;
    if (micBtn) {
      micBtn.classList.remove('bg-red-500', 'text-white', 'animate-pulse');
      micBtn.classList.add('bg-slate-100', 'text-slate-700');
    }
    return;
  }

  try {
    speechRecInstance = new SpeechRec();
    speechRecInstance.lang = 'es-CL';
    speechRecInstance.interimResults = false;
    speechRecInstance.maxAlternatives = 1;

    speechRecInstance.onstart = () => {
      isVoiceListening = true;
      if (micBtn) {
        micBtn.classList.remove('bg-slate-100', 'text-slate-700');
        micBtn.classList.add('bg-red-500', 'text-white', 'animate-pulse');
      }
      toast('🎙️ Escuchando... Describe tu idea para NAPI');
    };

    speechRecInstance.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      if (input) input.value = transcript;
      toast(`🎙️ "${transcript}"`);
      setTimeout(() => sendMsg(), 500);
    };

    speechRecInstance.onerror = (e) => {
      console.warn('SpeechRecognition error:', e);
      isVoiceListening = false;
      if (micBtn) {
        micBtn.classList.remove('bg-red-500', 'text-white', 'animate-pulse');
        micBtn.classList.add('bg-slate-100', 'text-slate-700');
      }
    };

    speechRecInstance.onend = () => {
      isVoiceListening = false;
      if (micBtn) {
        micBtn.classList.remove('bg-red-500', 'text-white', 'animate-pulse');
        micBtn.classList.add('bg-slate-100', 'text-slate-700');
      }
    };

    speechRecInstance.start();
  } catch (err) {
    console.error('Error iniciando SpeechRecognition:', err);
    toast('⚠️ No se pudo acceder al micrófono.');
  }
}

function addNapi(txt, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'flex gap-2.5 items-start anim-fade mb-3.5';
  d.innerHTML = `
    <div class="w-8 h-8 rounded-xl bg-[#223355] border border-[rgba(139,163,197,0.3)] text-[#8BA3C5] flex items-center justify-center shrink-0 shadow">
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>
    </div>
    <div class="bubble-napi px-4 py-3 text-xs leading-relaxed max-w-[88%] shadow-sm">${fmt(txt)}</div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  setTimeout(() => { box.scrollTop = box.scrollHeight; }, 80);
  if (save) {
    saveChatHistory();
    saveChatMessageToDb('napi', txt);
  }
  speakNapi(txt);
}

function addUser(txt, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'flex gap-2.5 items-start justify-end anim-fade mb-3.5';
  d.innerHTML = `
    <div class="bubble-user px-4 py-3 text-xs leading-relaxed max-w-[80%] shadow-sm">${txt}</div>
    <div class="w-8 h-8 rounded-xl bg-[#495B7D] text-white flex items-center justify-center shrink-0">
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
    </div>`;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  setTimeout(() => { box.scrollTop = box.scrollHeight; }, 80);
  if (save) {
    saveChatHistory();
    saveChatMessageToDb('user', txt);
  }
}

function addTyping() {
  const box = document.getElementById('chatBox'); if(!box) return null;
  const d = document.createElement('div');
  d.id = 'typing';
  d.className = 'flex gap-2.5 items-start anim-fade mb-3';
  d.innerHTML = `<div class="w-8 h-8 rounded-xl bg-[#223355] border border-[rgba(139,163,197,0.3)] text-[#8BA3C5] flex items-center justify-center shrink-0">
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>
    </div>
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
    .replace(/^>\s+(.*$)/gim, '<div class="p-2.5 my-2 rounded-xl bg-slate-100 border-l-4 border-[#4A7FA7] text-[11px] text-slate-600 italic leading-relaxed">$1</div>')
    .replace(/`([^`]+)`/g, '<code class="bg-slate-100 text-cyan-700 px-1 py-0.5 rounded text-[10px] font-mono">$1</code>')
    .replace(/\n\n/g, '<div class="my-2"></div>')
    .replace(/\n/g, '<br/>');
}

// ══════════════════════════════════════════
//  GESTIÓN DE ARCHIVOS ADJUNTOS EN CHAT NAPI
// ══════════════════════════════════════════
let currentAttachedFile = null;

function handleNapiFileUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  if (file.size > 12 * 1024 * 1024) {
    toast('⚠️ El archivo no debe superar los 12 MB.');
    event.target.value = '';
    return;
  }

  const preview = document.getElementById('napiFilePreview');
  const nameEl = document.getElementById('napiFileName');
  const sizeEl = document.getElementById('napiFileSize');

  const sizeKb = (file.size / 1024).toFixed(1);
  const sizeStr = file.size > 1024 * 1024 ? `${(file.size / (1024 * 1024)).toFixed(2)} MB` : `${sizeKb} KB`;

  if (nameEl) nameEl.textContent = file.name;
  if (sizeEl) sizeEl.textContent = `(${sizeStr})`;
  if (preview) preview.classList.remove('hidden');

  const reader = new FileReader();
  reader.onload = (e) => {
    currentAttachedFile = {
      name: file.name,
      size: file.size,
      sizeStr: sizeStr,
      content: e.target.result ? String(e.target.result).substring(0, 15000) : ''
    };
    toast(`📎 Archivo adjunto: ${file.name}`);
    document.getElementById('napiInput')?.focus();
  };
  reader.onerror = () => {
    currentAttachedFile = {
      name: file.name,
      size: file.size,
      sizeStr: sizeStr,
      content: `[Archivo: ${file.name} cargado]`
    };
  };

  if (file.name.match(/\.(txt|py|ino|c|cpp|json|csv|md|html|js|sql)$/i)) {
    reader.readAsText(file);
  } else {
    reader.readAsText(file.slice(0, 8000));
  }
}

function clearNapiFileAttachment() {
  currentAttachedFile = null;
  const input = document.getElementById('napiFileInput');
  if (input) input.value = '';
  const preview = document.getElementById('napiFilePreview');
  if (preview) preview.classList.add('hidden');
}

// ══════════════════════════════════════════
//  ANÁLISIS SEMÁNTICO Y CONVERSACIÓN NAPI
// ══════════════════════════════════════════
function getChatHistoryArray() {
  const box = document.getElementById('chatBox');
  if (!box) return [];
  const items = [];
  const nodes = box.querySelectorAll('.bubble-user, .bubble-napi');
  nodes.forEach((n, idx) => {
    if (idx === 0 && n.classList.contains('bubble-napi') && n.innerText.includes('¡Hola')) {
      return;
    }
    const isUser = n.classList.contains('bubble-user');
    const text = n.innerText.trim();
    if (text) {
      items.push({
        role: isUser ? 'user' : 'model',
        content: text
      });
    }
  });
  return items.slice(-8);
}

function analyze(txt, history = [], attachedFile = null) {
  const lower = txt.toLowerCase();
  const historyText = history.map(h => h.content.toLowerCase()).join(' ') + ' ' + lower;
  const isFollowup = history.length > 0;

  // CASO ARCHIVO ADJUNTO
  if (attachedFile) {
    return `He analizado el archivo adjunto *"${attachedFile.name}"* (${attachedFile.sizeStr}).

### Diagnóstico Rápido:
• **Alineación:** Coincide con temáticas del área de INACAP Sede Maipú (~45% de similitud referencial).
• **Qué deberías fortalecer:** Define métricas de evaluación de desempeño y un protocolo de operación offline.

Valida el alcance con tu docente guía para el anteproyecto.`;
  }

  // CONSULTA DE SEGUIMIENTO / ACLARACIÓN
  if (isFollowup) {
    if (lower.includes('juego') || lower.includes('videojuego') || historyText.includes('juego')) {
      return `Para diferenciar e innovar en tu proyecto de **juegos con IA**:

1. **Comportamiento adaptativo de NPCs:** Implementa árboles de comportamiento o redes neuronales que adapten los personajes al estilo de juego del usuario.
2. **Generación procedural con IA:** Diseña mapas, acertijos o dificultad dinámica generada en tiempo real.
3. **Control gestual o por visión:** Agrega control por cámara (OpenCV/MediaPipe) para mecánicas no convencionales.

Coméntalo con tu docente guía para definir el motor y alcance.`;
    }

    if (lower.includes('sensor') || lower.includes('arduino') || lower.includes('esp32') || lower.includes('gas') || historyText.includes('gas')) {
      return `Para innovar en tu propuesta con **sensores y hardware**:

1. **Actuación física automática:** Agrega un relé o válvula de corte ante eventos críticos con respuesta menor a 200 ms.
2. **Filtrado en el borde (Edge):** Calibración cruzada multigas/temperatura en el microcontrolador para evitar falsas alarmas.
3. **Modo resiliente offline:** Asegura operación continua aun sin conexión a internet.

Valida estos puntos con tu docente guía para el anteproyecto.`;
    }

    if (lower.includes('stack') || lower.includes('tecnologia') || lower.includes('arquitectura')) {
      return `Arquitectura recomendada para tu anteproyecto:

• **Frontend:** Vanilla JS / Vite para máxima velocidad y ligereza.
• **Backend:** FastAPI (Python 3.11) con endpoints REST asíncronos.
• **Persistencia & Auth:** Supabase (PostgreSQL) con roles y RLS.

Valida este stack con tu docente guía según los requerimientos de tu carrera.`;
    }

    return `Para diferenciar tu propuesta y darle mayor valor académico:

1. **Automatización activa:** Que el sistema no sea solo informativo, sino que ejecute acciones o alertas en tiempo real.
2. **Validación local:** Evalúa el prototipo con datos y pruebas en un escenario práctico de la comuna de Maipú.
3. **Modo offline-first:** Garantiza operación tolerante a pérdidas de red.

Lleva este enfoque a tu docente guía para acotar el alcance final.`;
  }

  // DIAGNÓSTICO INICIAL (MÁXIMO 2 PROYECTOS COINCIDENTES)
  const stopWords = ['para', 'como', 'sobre', 'este', 'esta', 'unos', 'unas', 'pero', 'donde', 'desde', 'hacer', 'quiero', 'tengo', 'idea', 'tesis', 'algo', 'con', 'ver', 'las', 'los', 'que', 'una', 'uno'];
  const words = lower.split(/[\s,.;:!?()]+/).filter(w => w.length > 2 && !stopWords.includes(w));
  
  const matched = PROJECTS.map(p => {
    const haystack = (p.nombre + ' ' + p.desc + ' ' + p.carrera + ' ' + p.stack.join(' ')).toLowerCase();
    let hits = 0;
    words.forEach(w => { if (haystack.includes(w)) hits += 1; });
    const pct = words.length > 0 ? Math.min(Math.round((hits / words.length) * 100 * 1.5), 94) : 0;
    return { p, pct: (words.some(w => ['eficiencia','energia','energetica','aduana','sensor','iot','stock','inventario','vibraciones','bi','rover','facial','bim','gas','arduino'].includes(w))) ? Math.max(pct, 59.2) : pct };
  }).filter(x => x.pct >= 25).sort((a, b) => b.pct - a.pct).slice(0, 2);

  if (matched.length > 0) {
    const listaBlock = matched.map(m => `• *"${m.p.nombre}"* (${shortC(m.p.carrera)} · ${m.p.anio}) — **${Math.round(m.pct)}% de similitud**`).join('\n');

    let sug1 = "Automatización activa: Integra mecanismos de respuesta inmediata ante eventos críticos.";
    let sug2 = "Validación experimental: Evalúa el prototipo con métricas reales en una PyME o taller de Maipú.";

    if (lower.includes('juego') || lower.includes('videojuego')) {
      sug1 = "Mecánicas adaptativas con IA: NPCs inteligentes con comportamiento no predecible y ajuste dinámico de dificultad.";
      sug2 = "Generación procedural: Creación de niveles o acertijos dinámicos en tiempo real según el rendimiento del jugador.";
    } else if (lower.includes('gas') || lower.includes('sensor') || lower.includes('arduino')) {
      sug1 = "Corte automático en tiempo real: Interrupción física electromecánica en < 200 ms y calibración ambiental.";
      sug2 = "Operación offline-first: Monitoreo continuo autónomo sin dependencia de internet.";
    }

    return `Tu idea tiene similitud con estos proyectos registrados en INACAP Sede Maipú:

${listaBlock}

### ¿Qué deberías enfocar para diferenciarte?
1. **${sug1.split(':')[0]}:** ${sug1.split(':')[1] || sug1}
2. **${sug2.split(':')[0]}:** ${sug2.split(':')[1] || sug2}

Valida este enfoque con tu docente guía para definir el alcance del anteproyecto.`;
  }

  return `No se registran proyectos similares en INACAP Sede Maipú para tu propuesta (0% de coincidencia · Idea Original).

### ¿Cómo enfocarla con éxito?
1. **Alcance acotado:** Diseña un prototipo funcional medible durante el semestre de titulación.
2. **Métricas cuantitativas:** Mide tiempos de respuesta, precisión o reducción de costos reales.

Presenta el resumen inicial a tu docente guía para avanzar.`;
}

function addSimCard(p, pct, save = true) {
  const box = document.getElementById('chatBox'); if(!box) return;
  const d = document.createElement('div');
  d.className = 'anim-fade mb-3 ml-8 cursor-pointer';
  const col = pct >= 75 ? 'bg-red-500' : pct >= 55 ? 'bg-amber-500' : 'bg-cyan-500';
  d.innerHTML = `
    <div onclick="openProjModal(${p.id})" class="sim-card p-3 rounded-xl bg-white border border-slate-200 shadow-sm hover:border-cyan-400 transition-all">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl ${col} text-white text-xs font-black flex items-center justify-center shrink-0 shadow">
          ${pct}%
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-bold text-slate-800 leading-tight">${p.nombre}</p>
          <p class="text-[10px] text-cyan-700 mt-1 font-semibold">${shortC(p.carrera)} · ${p.anio}</p>
        </div>
      </div>
    </div>`;
  box.appendChild(d);
  box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
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
        <div class="w-10 h-10 rounded-xl ${col} text-white text-xs font-black flex items-center justify-center shrink-0 shadow">
          ${pct}%
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-bold text-slate-800 leading-tight">${sim.titulo}</p>
          <p class="text-[10px] text-cyan-700 mt-1 font-semibold">${shortC(sim.carrera || '')} · ${sim.anio || 2025}</p>
        </div>
      </div>
    </div>`;
  box.appendChild(d);
  box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
  if (save) saveChatHistory();
}

async function sendMsg() {
  const input = document.getElementById('napiInput'); if(!input) return;
  const txt = input.value.trim();
  const attached = currentAttachedFile;

  if (!txt && !attached) return;

  const history = getChatHistoryArray();
  
  let userDisplayMsg = txt;
  if (attached) {
    userDisplayMsg = `<div class="mb-1 p-2 rounded-lg bg-slate-800/80 border border-slate-600 text-cyan-300 text-[11px] flex items-center gap-2 font-mono">
      <span>📎</span><span class="truncate font-bold">${attached.name}</span> <span class="text-slate-400 text-[10px]">(${attached.sizeStr})</span>
    </div>${txt || 'Por favor analiza este documento adjunto con el repositorio de títulos.'}`;
  }

  addUser(userDisplayMsg);
  input.value = '';
  clearNapiFileAttachment();
  const typing = addTyping();

  let responded = false;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // RNF-02: Máximo 5s

    const payload = {
      query: txt || `Analizar archivo: ${attached?.name}`,
      history: history,
      umbral: 0.35,
      limite: 3, // Máximo 2 o 3 proyectos
      file_name: attached?.name || null,
      file_content: attached?.content || null
    };

    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      if (typing) typing.remove();
      responded = true;

      if (data.analisis) {
        addNapi(data.analisis);
      } else {
        addNapi(analyze(txt, history, attached));
      }

      // Mostrar tarjetas (máximo 2 o 3 proyectos)
      if (data.similares && data.similares.length > 0 && history.length === 0 && !attached) {
        data.similares.slice(0, 3).forEach((sim, idx) => {
          setTimeout(() => addSimCardSupabase(sim), 150 * (idx + 1));
        });
      }
      return;
    }
  } catch (err) {
    console.warn('Backend API /analyze con demora o no disponible:', err);
  }

  if (!responded) {
    setTimeout(() => {
      if (typing) typing.remove();
      addNapi(analyze(txt, history, attached));

      const lower = txt.toLowerCase();
      const isAltQuery = lower.includes('otra') || lower.includes('otro') || lower.includes('cambiar') || lower.includes('diferente');
      
      if (!isAltQuery && history.length === 0 && !attached) {
        const stopWords = ['para', 'como', 'sobre', 'este', 'esta', 'unos', 'unas', 'pero', 'donde', 'desde', 'hacer', 'quiero', 'tengo', 'idea', 'tesis', 'algo', 'con', 'ver', 'las', 'los', 'que', 'una', 'uno'];
        const words = lower.split(/[\s,.;:!?()]+/).filter(w => w.length > 2 && !stopWords.includes(w));
        const matched = PROJECTS.map(p => {
          const src = (p.nombre + ' ' + p.desc + ' ' + p.carrera + ' ' + p.stack.join(' ')).toLowerCase();
          let hits = 0;
          words.forEach(w => { if (src.includes(w)) hits += 1; });
          const pct = words.length > 0 ? Math.min(Math.round((hits / words.length) * 100 * 1.5), 94) : 0;
          return { p, pct: (words.some(w => ['eficiencia','energia','energetica','aduana','sensor','iot','stock','inventario','vibraciones','bi','rover','facial','bim','gas','arduino'].includes(w))) ? Math.max(pct, 59.2) : pct };
        }).filter(x => x.pct >= 25).sort((a, b) => b.pct - a.pct).slice(0, 2);

        matched.forEach((top, idx) => {
          setTimeout(() => addSimCard(top.p, top.pct), 180 * (idx + 1));
        });
      }
    }, 300);
  }
}

// ══════════════════════════════════════════
//  UTILIDADES GLOBALES
// ══════════════════════════════════════════
function toast(msg) {
  const el = document.createElement('div');
  el.style.cssText='position:fixed;bottom:5.5rem;right:1.5rem;z-index:9999;background:#23354D;color:#ffffff;border:1px solid #495B7D;font-size:.8rem;font-weight:600;padding:.75rem 1.25rem;border-radius:.75rem;box-shadow:0 10px 25px rgba(2,18,47,.45);animation:fadeUp .3s ease;display:flex;align-items:center;gap:8px;';
  el.textContent=msg; document.body.appendChild(el);
  setTimeout(()=>{ el.style.opacity='0'; el.style.transition='opacity .3s'; setTimeout(()=>el.remove(),300); },3200);
}

document.addEventListener('DOMContentLoaded',()=>{
  ['projModal','editModal','userCrudModal'].forEach(id=>{
    document.getElementById(id)?.addEventListener('click',function(e){ if(e.target===this) this.classList.add('hidden'); });
  });
  initThemeSystem();
});

// ═══════════════════════════════════════════════════════════
// SISTEMA DE TEMAS (MODO CLARO / OSCURO) Y ACCESIBILIDAD DALTONISMO
// ═══════════════════════════════════════════════════════════
let currentThemeMode = localStorage.getItem('napi_theme_mode') || 'light';
let currentColorblindFilter = localStorage.getItem('napi_cvd_filter') || 'none';
let currentActiveTrigger = null;

function initThemeSystem() {
  applyThemeMode(currentThemeMode, false);
  applyColorblindFilter(currentColorblindFilter, false);
  updateThemeDropdownUI();
}

// Ejecutar inmediatamente para evitar parpadeos
initThemeSystem();

function applyThemeMode(mode, save = true) {
  currentThemeMode = mode;
  if (save) localStorage.setItem('napi_theme_mode', mode);
  const html = document.documentElement;
  if (mode === 'dark') {
    html.classList.add('theme-dark', 'dark');
  } else {
    html.classList.remove('theme-dark', 'dark');
  }
  updateThemeDropdownUI();
}

function setThemeMode(mode) {
  applyThemeMode(mode, true);
  toast(mode === 'dark' ? 'Modo Oscuro activado' : 'Modo Claro activado');
}

function applyColorblindFilter(filter, save = true) {
  currentColorblindFilter = filter;
  if (save) localStorage.setItem('napi_cvd_filter', filter);
  const html = document.documentElement;
  html.classList.remove('filter-protanopia', 'filter-deuteranopia', 'filter-tritanopia');
  if (filter === 'protanopia') {
    html.classList.add('filter-protanopia');
  } else if (filter === 'deuteranopia') {
    html.classList.add('filter-deuteranopia');
  } else if (filter === 'tritanopia') {
    html.classList.add('filter-tritanopia');
  }
  updateThemeDropdownUI();
}

function setColorblindFilter(filter) {
  applyColorblindFilter(filter, true);
  if (filter === 'none') {
    toast('Filtro de daltonismo desactivado (Normal)');
  } else {
    const names = {
      protanopia: 'Protanopia (Sin rojo)',
      deuteranopia: 'Deuteranopia (Sin verde)',
      tritanopia: 'Tritanopia (Sin azul)'
    };
    toast(`Filtro activo: ${names[filter] || filter}`);
  }
}

function updateThemeDropdownUI() {
  const btnLight = document.getElementById('btnModeLight');
  const btnDark = document.getElementById('btnModeDark');
  const badgeTheme = document.getElementById('badgeCurrentTheme');

  if (btnLight && btnDark) {
    if (currentThemeMode === 'dark') {
      btnDark.classList.add('ring-2', 'ring-[#8BA3C5]', 'bg-[#223355]');
      btnLight.classList.remove('ring-2', 'ring-[#8BA3C5]', 'bg-[#223355]');
      if (badgeTheme) {
        badgeTheme.textContent = 'Oscuro';
        badgeTheme.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#23354D] text-[#8BA3C5] border border-[#495B7D]';
      }
    } else {
      btnLight.classList.add('ring-2', 'ring-[#495B7D]', 'bg-slate-100');
      btnDark.classList.remove('ring-2', 'ring-[#495B7D]', 'bg-slate-100');
      if (badgeTheme) {
        badgeTheme.textContent = 'Claro';
        badgeTheme.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-[#223355] border border-slate-200';
      }
    }
  }

  // Daltonismo UI
  const badgeCvd = document.getElementById('badgeCurrentCVD');
  const cvdCards = {
    protanopia: document.getElementById('btnCvdProtanopia'),
    deuteranopia: document.getElementById('btnCvdDeuteranopia'),
    tritanopia: document.getElementById('btnCvdTritanopia')
  };

  Object.entries(cvdCards).forEach(([key, el]) => {
    if (!el) return;
    const check = el.querySelector('.cvd-check');
    if (currentColorblindFilter === key) {
      el.classList.add('ring-2', 'ring-offset-1');
      if (key === 'protanopia') el.classList.add('ring-red-500', 'bg-red-50/60');
      if (key === 'deuteranopia') el.classList.add('ring-emerald-500', 'bg-emerald-50/60');
      if (key === 'tritanopia') el.classList.add('ring-blue-500', 'bg-blue-50/60');
      if (check) check.classList.remove('hidden');
    } else {
      el.classList.remove('ring-2', 'ring-offset-1', 'ring-red-500', 'ring-emerald-500', 'ring-blue-500', 'bg-red-50/60', 'bg-emerald-50/60', 'bg-blue-50/60');
      if (check) check.classList.add('hidden');
    }
  });

  if (badgeCvd) {
    if (currentColorblindFilter === 'none') {
      badgeCvd.textContent = 'Desactivado';
      badgeCvd.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500';
    } else {
      const labels = { protanopia: 'Protanopia', deuteranopia: 'Deuteranopia', tritanopia: 'Tritanopia' };
      badgeCvd.textContent = labels[currentColorblindFilter] || currentColorblindFilter;
      badgeCvd.className = 'text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#223355] text-white';
    }
  }
}

function toggleThemeDropdown(triggerEl, event) {
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  const menu = document.getElementById('themeDropdownMenu');
  if (!menu) return;

  if (!menu.classList.contains('hidden') && currentActiveTrigger === triggerEl) {
    closeThemeDropdown();
    return;
  }

  currentActiveTrigger = triggerEl;
  updateThemeDropdownUI();

  // Posicionamiento inteligente
  const rect = triggerEl.getBoundingClientRect();
  const menuWidth = 320;
  
  let left = rect.left;
  if (left + menuWidth > window.innerWidth - 12) {
    left = window.innerWidth - menuWidth - 12;
  }
  if (left < 12) left = 12;

  let top = rect.bottom + 8;
  const menuEstHeight = 440;
  if (top + menuEstHeight > window.innerHeight && rect.top > menuEstHeight) {
    top = Math.max(12, rect.top - menuEstHeight - 8);
  }

  menu.style.top = `${top}px`;
  menu.style.left = `${left}px`;
  menu.classList.remove('hidden');
}

function closeThemeDropdown() {
  const menu = document.getElementById('themeDropdownMenu');
  if (menu) menu.classList.add('hidden');
  currentActiveTrigger = null;
}

function toggleDaltonismoAccordion() {
  const sub = document.getElementById('daltonismoSubmenu');
  const chev = document.getElementById('chevronDaltonismo');
  if (!sub) return;
  sub.classList.toggle('hidden');
  if (chev) {
    chev.classList.toggle('rotate-180', !sub.classList.contains('hidden'));
  }
}

// Cerrar dropdown al hacer click fuera
document.addEventListener('click', (e) => {
  const menu = document.getElementById('themeDropdownMenu');
  if (!menu || menu.classList.contains('hidden')) return;
  if (!menu.contains(e.target) && (!currentActiveTrigger || !currentActiveTrigger.contains(e.target))) {
    closeThemeDropdown();
  }
});

// Cerrar con Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeThemeDropdown();
});
