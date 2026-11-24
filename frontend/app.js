/**
 * MACTOR PROSP Frontend Application
 * Handles state, interactive matrices, live territorial news mining,
 * Vis.js Network graph, Chart.js visualizations, scenario simulation, and report generation.
 */

// Application State
const state = {
  currentCaseId: "manual_caballos_monteria",
  variant: "softprosp",
  territory: "Coliseo de Ferias Miguel Villamil Muñoz, Montería",
  actors: [],
  objectives: [],
  mid: [],
  mao2: [],
  results: null,
  territoryAnalysis: null,
  quadrantChart: null,
  mobilizationChart: null,
  networkInstance: null,
  treeMode: "convergence",
  selectedChannelFilter: "all",
  balanceScale: {
    mode: "single", // "single" | "gallery" | "actor"
    objIndex: 0,
    actorIndex: 0,
    weighted: true
  }
};

// DOM Loaded Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupTabNavigation();
  setupEventListeners();
  setupBalanceScaleHandlers();
  loadCase("manual_caballos_monteria"); // Default benchmark from attached manual
});

// Guided Process Metadata (9 Steps across 4 Prospective Phases)
const PROCESS_STEPS = [
  {
    id: "tab-territory",
    num: 1,
    phase: "Fase I • Preparación y Mapeo",
    shortPhase: "Fase I: Preparación",
    title: "1. Inteligencia Territorial: Selecciona o rastrea un caso",
    shortTitle: "Inteligencia Territorial",
    instruction: "<b>Qué hacer aquí:</b> Elige uno de los 11 casos preconfigurados o ingresa un territorio y sector para extraer actores reales y evidencias desde 9 canales de fuentes."
  },
  {
    id: "tab-config",
    num: 2,
    phase: "Fase I • Preparación y Mapeo",
    shortPhase: "Fase I: Preparación",
    title: "2. Actores y Objetivos: Valida el tablero del sistema",
    shortTitle: "Actores & Objetivos",
    instruction: "<b>Qué hacer aquí:</b> Revisa, edita o agrega actores estratégicos y ajusta los pesos de los objetivos (deben sumar 100%)."
  },
  {
    id: "tab-mid",
    num: 3,
    phase: "Fase II • Modelación de Poder",
    shortPhase: "Fase II: Modelación",
    title: "3. Matriz MID & Cuadrantes: Califica quién influye sobre quién",
    shortTitle: "Matriz MID & Cuadrantes",
    instruction: "<b>Qué hacer aquí:</b> Asigna la influencia directa entre actores (escala 0 a 4) y observa en el gráfico qué actores son Dominantes, de Enlace o Dominados."
  },
  {
    id: "tab-mao",
    num: 4,
    phase: "Fase II • Modelación de Poder",
    shortPhase: "Fase II: Modelación",
    title: "4. Posiciones & Balanzas LIPSOR: Mide el pulso de fuerzas",
    shortTitle: "Posiciones & Balanzas",
    instruction: "<b>Qué hacer aquí:</b> Registra la postura de cada actor (-4 a +4) frente a cada objetivo y revisa hacia qué platillo se inclina la Balanza de Poder."
  },
  {
    id: "tab-alliances",
    num: 5,
    phase: "Fase III • Alianzas y Simulación",
    shortPhase: "Fase III: Alianzas",
    title: "5. Red de Alianzas & Conflictos: Identifica aliados y rivales",
    shortTitle: "Alianzas & Conflictos",
    instruction: "<b>Qué hacer aquí:</b> Analiza el grafo de relaciones y las matrices de Convergencia (CAA3) y Divergencia (DAA3) para detectar coaliciones naturales y tensiones."
  },
  {
    id: "tab-trees",
    num: 6,
    phase: "Fase III • Alianzas y Simulación",
    shortPhase: "Fase III: Alianzas",
    title: "6. Árboles de Convergencia: Agrupa bloques por afinidad",
    shortTitle: "Árboles de Convergencia",
    instruction: "<b>Qué hacer aquí:</b> Explora los dendrogramas jerárquicos para visualizar qué grupos de actores forman bloques homogéneos."
  },
  {
    id: "tab-mobilization",
    num: 7,
    phase: "Fase III • Alianzas y Simulación",
    shortPhase: "Fase III: Alianzas",
    title: "7. Movilización de Objetivos: Evalúa viabilidad y bloqueos",
    shortTitle: "Movilización Objetivos",
    instruction: "<b>Qué hacer aquí:</b> Compara el nivel de movilización, balance neto e índice de disputa para priorizar qué objetivos son viables o requieren mediación."
  },
  {
    id: "tab-scenarios",
    num: 8,
    phase: "Fase III • Alianzas y Simulación",
    shortPhase: "Fase III: Alianzas",
    title: "8. Simulación \"¿Qué pasa si...?\": Prueba escenarios tácticos",
    shortTitle: "Simulación Escenarios",
    instruction: "<b>Qué hacer aquí:</b> Modifica hipotéticamente el poder o la postura de un actor clave para anticipar si cambia el actor hegemónico o se destraba un conflicto."
  },
  {
    id: "tab-report",
    num: 9,
    phase: "Fase IV • Decisión y Entrega",
    shortPhase: "Fase IV: Entrega",
    title: "9. Informe Ejecutivo: Revisa conclusiones y descarga Word/Excel",
    shortTitle: "Informe Ejecutivo",
    instruction: "<b>Qué hacer aquí:</b> Revisa el resumen estratégico completo y descarga el <b>Informe Integral en Word (.docx)</b> o el libro de <b>Excel (.xlsx)</b>."
  }
];

let currentStepIndex = 0;

function navigateToStep(targetPaneId, shouldScroll = true) {
  const stepIdx = PROCESS_STEPS.findIndex(s => s.id === targetPaneId);
  if (stepIdx === -1) return;
  currentStepIndex = stepIdx;
  const step = PROCESS_STEPS[stepIdx];

  // Update top nav tabs
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(t => {
    if (t.getAttribute("data-tab") === targetPaneId) {
      t.classList.add("active");
    } else {
      t.classList.remove("active");
    }
  });

  // Hide all panes & show target
  document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.add("hidden"));
  const targetPane = document.getElementById(targetPaneId);
  if (targetPane) targetPane.classList.remove("hidden");

  // Update progress bar
  const progressEl = document.getElementById("process-progress-bar");
  if (progressEl) {
    const pct = ((stepIdx + 1) / PROCESS_STEPS.length) * 100;
    progressEl.style.width = `${pct.toFixed(1)}%`;
  }

  // Update Top Guidance Banner
  const numEl = document.getElementById("step-banner-number");
  const phaseEl = document.getElementById("step-banner-phase");
  const countEl = document.getElementById("step-banner-counter");
  const titleEl = document.getElementById("step-banner-title");
  const instEl = document.getElementById("step-banner-instruction");

  if (numEl) numEl.textContent = step.num;
  if (phaseEl) phaseEl.textContent = step.phase;
  if (countEl) countEl.textContent = `Paso ${step.num} de ${PROCESS_STEPS.length}`;
  if (titleEl) titleEl.textContent = step.title;
  if (instEl) instEl.innerHTML = step.instruction;

  // Update Top & Bottom Prev/Next Buttons
  const prevStep = stepIdx > 0 ? PROCESS_STEPS[stepIdx - 1] : null;
  const nextStep = stepIdx < PROCESS_STEPS.length - 1 ? PROCESS_STEPS[stepIdx + 1] : null;

  const btnPrevTop = document.getElementById("btn-step-prev-top");
  const btnNextTop = document.getElementById("btn-step-next-top");
  const lblNextTop = document.getElementById("btn-step-next-top-label");
  const btnPrevBot = document.getElementById("btn-step-prev-bottom");
  const lblPrevBot = document.getElementById("btn-step-prev-bottom-label");
  const btnNextBot = document.getElementById("btn-step-next-bottom");
  const lblNextBot = document.getElementById("btn-step-next-bottom-label");
  const footerInd = document.getElementById("footer-step-indicator");

  if (btnPrevTop) btnPrevTop.disabled = !prevStep;
  if (btnPrevBot) btnPrevBot.disabled = !prevStep;
  if (lblPrevBot) lblPrevBot.textContent = prevStep ? `Anterior: ${prevStep.shortTitle}` : "Inicio del Proceso";

  if (nextStep) {
    if (btnNextTop) {
      btnNextTop.disabled = false;
      btnNextTop.className = "px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center space-x-1.5 shadow transition-all cursor-pointer";
    }
    if (lblNextTop) lblNextTop.textContent = `Siguiente: ${nextStep.shortTitle}`;
    if (btnNextBot) {
      btnNextBot.className = "w-full sm:w-auto px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center justify-center space-x-2 shadow-md transition-all cursor-pointer";
    }
    if (lblNextBot) lblNextBot.textContent = `Continuar al Paso ${nextStep.num}: ${nextStep.shortTitle}`;
  } else {
    // Step 9: Final Delivery Action
    if (btnNextTop) {
      btnNextTop.disabled = false;
      btnNextTop.className = "px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center space-x-1.5 shadow transition-all cursor-pointer";
    }
    if (lblNextTop) lblNextTop.textContent = "Descargar Informe Word (.docx)";
    if (btnNextBot) {
      btnNextBot.className = "w-full sm:w-auto px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold flex items-center justify-center space-x-2 shadow-md transition-all cursor-pointer";
    }
    if (lblNextBot) lblNextBot.textContent = "Descargar Informe Completo en Word (.docx)";
  }

  if (footerInd) {
    footerInd.textContent = `Paso ${step.num} de ${PROCESS_STEPS.length} • ${step.shortPhase}`;
  }

  // Re-render charts or networks if tab became visible
  if (targetPaneId === "tab-mid" && state.results) {
    renderQuadrantChart();
  } else if (targetPaneId === "tab-mao") {
    populateBalanceDropdowns();
    renderBalanceScaleView();
  } else if (targetPaneId === "tab-alliances" && state.results) {
    renderAllianceNetwork();
  } else if (targetPaneId === "tab-trees" && state.results) {
    renderDendrogram(state.treeMode);
  } else if (targetPaneId === "tab-mobilization" && state.results) {
    renderMobilizationChart();
  } else if (targetPaneId === "tab-report" && state.results) {
    renderExecutiveReport();
  }

  if (shouldScroll) {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

// Setup tab switches & process step navigation
function setupTabNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetPaneId = tab.getAttribute("data-tab");
      navigateToStep(targetPaneId, false);
    });
  });

  const goPrev = () => {
    if (currentStepIndex > 0) {
      navigateToStep(PROCESS_STEPS[currentStepIndex - 1].id, true);
    }
  };
  const goNext = () => {
    if (currentStepIndex < PROCESS_STEPS.length - 1) {
      navigateToStep(PROCESS_STEPS[currentStepIndex + 1].id, true);
    } else {
      exportWordDocx();
    }
  };

  const btnPrevTop = document.getElementById("btn-step-prev-top");
  const btnNextTop = document.getElementById("btn-step-next-top");
  const btnPrevBot = document.getElementById("btn-step-prev-bottom");
  const btnNextBot = document.getElementById("btn-step-next-bottom");
  const btnToggleMap = document.getElementById("btn-toggle-process-map");
  const mapDrawer = document.getElementById("process-map-drawer");

  if (btnPrevTop) btnPrevTop.addEventListener("click", goPrev);
  if (btnNextTop) btnNextTop.addEventListener("click", goNext);
  if (btnPrevBot) btnPrevBot.addEventListener("click", goPrev);
  if (btnNextBot) btnNextBot.addEventListener("click", goNext);
  if (btnToggleMap && mapDrawer) {
    btnToggleMap.addEventListener("click", () => {
      mapDrawer.classList.toggle("hidden");
    });
  }

  // Initialize banner on step 1
  navigateToStep("tab-territory", false);
}

// Real-time two-way synchronization: Territory & Sector inputs <--> Top Active Context Bar (Global Scope)
function syncTopContextBar() {
  const inputTerr = document.getElementById("input-territory");
  const inputSect = document.getElementById("input-sector");
  const inputCountry = document.getElementById("input-country");

  const terr = inputTerr ? inputTerr.value.trim() : "";
  const country = inputCountry ? inputCountry.value : "Colombia";
  const sect = inputSect ? inputSect.value.trim() : "";

  // 1:1 exact match with user input
  if (document.getElementById("banner-title")) {
    document.getElementById("banner-title").textContent = terr || "Sin definir";
  }
  // Flag & country badge
  if (document.getElementById("banner-country-badge")) {
    const countryFlags = {
      "Colombia": "🇨🇴 Colombia",
      "Chile": "🇨🇱 Chile",
      "Argentina": "🇦🇷 Argentina",
      "México": "🇲🇽 México",
      "Perú": "🇵🇪 Perú",
      "España": "🇪🇸 España",
      "Internacional": "🌐 Internacional"
    };
    document.getElementById("banner-country-badge").textContent = countryFlags[country] || country || "";
  }
  if (document.getElementById("active-sector-tag")) {
    document.getElementById("active-sector-tag").textContent = sect || "General / En Disputa";
  }
  state.territory = terr;
  state.country = country;
  state.sector = sect;
}

// Setup Event Listeners
function setupEventListeners() {
  const inputTerr = document.getElementById("input-territory");
  const inputSect = document.getElementById("input-sector");
  const inputCountry = document.getElementById("input-country");

  if (inputTerr) {
    inputTerr.addEventListener("input", syncTopContextBar);
    inputTerr.addEventListener("change", syncTopContextBar);
  }
  if (inputSect) {
    inputSect.addEventListener("input", syncTopContextBar);
    inputSect.addEventListener("change", syncTopContextBar);
  }
  if (inputCountry) {
    inputCountry.addEventListener("change", syncTopContextBar);
  }

  // Initial call to guarantee top bar and inputs are 100% synchronized
  syncTopContextBar();

  // Live Search Dock Handlers (Bottom Window)
  const btnCloseDock = document.getElementById("btn-close-search-dock");
  if (btnCloseDock) {
    btnCloseDock.addEventListener("click", () => {
      document.getElementById("live-search-dock").classList.add("hidden");
    });
  }

  const btnToggleDock = document.getElementById("btn-toggle-search-dock");
  if (btnToggleDock) {
    btnToggleDock.addEventListener("click", () => {
      const body = document.getElementById("search-dock-body");
      if (body) {
        body.classList.toggle("hidden");
        const icon = btnToggleDock.querySelector("i");
        if (icon) {
          icon.classList.toggle("fa-chevron-down");
          icon.classList.toggle("fa-chevron-up");
        }
      }
    });
  }

  const btnScrollResults = document.getElementById("btn-scroll-to-results");
  if (btnScrollResults) {
    btnScrollResults.addEventListener("click", () => {
      const container = document.getElementById("territory-results");
      if (container) {
        container.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  // Case switcher
  document.getElementById("case-select").addEventListener("change", (e) => {
    loadCase(e.target.value);
  });

  // Variant switcher
  document.getElementById("variant-select").addEventListener("change", (e) => {
    setMethodVariant(e.target.value);
  });

  // Method selector cards (4 Methods Panel)
  const methodCards = document.querySelectorAll(".method-card");
  methodCards.forEach(card => {
    card.addEventListener("click", (e) => {
      // If clicked on info button, don't just select, open modal
      if (e.target.closest(".btn-method-info")) return;
      const method = card.getAttribute("data-method");
      setMethodVariant(method);
    });
  });

  // Info buttons on method cards
  const infoButtons = document.querySelectorAll(".btn-method-info");
  infoButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const methodKey = btn.getAttribute("data-method-key");
      openInterpretationModal(methodKey);
    });
  });

  // Modal tab buttons inside interpretation popup
  const modalTabBtns = document.querySelectorAll(".modal-tab-btn");
  modalTabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabTarget = btn.getAttribute("data-interp-tab");
      switchInterpretationTab(tabTarget);
    });
  });

  // Activate method button from inside modal
  const btnActivateFromModal = document.querySelectorAll(".btn-activate-method");
  btnActivateFromModal.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetMethod = btn.getAttribute("data-target-method");
      setMethodVariant(targetMethod);
      document.getElementById("modal-method-interpretation").classList.add("hidden");
    });
  });

  // Close interpretation modal
  const btnCloseInterp = document.getElementById("btn-close-interpretation-modal");
  if (btnCloseInterp) {
    btnCloseInterp.addEventListener("click", () => {
      document.getElementById("modal-method-interpretation").classList.add("hidden");
    });
  }
  const btnCloseInterpFooter = document.getElementById("btn-modal-close-footer");
  if (btnCloseInterpFooter) {
    btnCloseInterpFooter.addEventListener("click", () => {
      document.getElementById("modal-method-interpretation").classList.add("hidden");
    });
  }

  // Main Big Detonator: Start AI Analysis
  const btnStartAi = document.getElementById("btn-start-ai-analysis");
  if (btnStartAi) {
    btnStartAi.addEventListener("click", () => {
      analyzeTerritoryLive();
    });
  }

  // Quick method help button beside method options
  const btnQuickHelp = document.getElementById("btn-quick-method-help");
  if (btnQuickHelp) {
    btnQuickHelp.addEventListener("click", () => {
      openInterpretationModal(state.variant || "softprosp");
    });
  }

  // Method radio inputs inside Step 1
  const methodRadios = document.querySelectorAll('input[name="method-radio"]');
  methodRadios.forEach(radio => {
    radio.addEventListener("change", (e) => {
      if (e.target.checked) {
        setMethodVariant(e.target.value);
      }
    });
  });

  // Export Word (.docx) buttons
  const btnExportDocx = document.getElementById("btn-export-docx");
  if (btnExportDocx) btnExportDocx.addEventListener("click", exportWordDocx);
  const btnExportDocx2 = document.getElementById("btn-export-docx-2");
  if (btnExportDocx2) btnExportDocx2.addEventListener("click", exportWordDocx);

  // Export Excel buttons
  const btnExport = document.getElementById("btn-export-excel");
  if (btnExport) btnExport.addEventListener("click", exportExcel);
  const btnExport2 = document.getElementById("btn-export-excel-2");
  if (btnExport2) btnExport2.addEventListener("click", exportExcel);

  // Apply territory to workspace
  const btnApplyTerritory = document.getElementById("btn-apply-territory-to-mactor");
  if (btnApplyTerritory) btnApplyTerritory.addEventListener("click", applyTerritoryToWorkspace);

  // Add actor/objective buttons
  const btnAddActor = document.getElementById("btn-add-actor");
  if (btnAddActor) btnAddActor.addEventListener("click", addNewActor);
  const btnAddObj = document.getElementById("btn-add-objective");
  if (btnAddObj) btnAddObj.addEventListener("click", addNewObjective);

  // Network threshold slider
  const slider = document.getElementById("network-filter-threshold");
  slider.addEventListener("input", (e) => {
    document.getElementById("threshold-val").textContent = e.target.value;
    renderAllianceNetwork();
  });

  // Reset physics
  document.getElementById("btn-reset-physics").addEventListener("click", () => {
    if (state.networkInstance) {
      state.networkInstance.stabilize();
      state.networkInstance.fit();
    }
  });

  // Channel filter buttons
  const channelFilterBtns = document.querySelectorAll(".channel-filter-btn");
  channelFilterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const channel = btn.getAttribute("data-channel");
      state.selectedChannelFilter = channel;

      // Update button styles
      channelFilterBtns.forEach(b => {
        b.classList.remove("bg-slate-900", "text-white");
        b.classList.add("bg-slate-100", "text-slate-700");
      });
      btn.classList.add("bg-slate-900", "text-white");
      btn.classList.remove("bg-slate-100", "text-slate-700");

      // Filter news cards
      filterNewsCardsByChannel(channel);
    });
  });

  // Tree Mode Switchers
  const btnTreeConv = document.getElementById("btn-tree-mode-conv");
  const btnTreeDiv = document.getElementById("btn-tree-mode-div");
  if (btnTreeConv && btnTreeDiv) {
    btnTreeConv.addEventListener("click", () => {
      state.treeMode = "convergence";
      btnTreeConv.classList.add("bg-emerald-600", "text-white");
      btnTreeConv.classList.remove("text-slate-600");
      btnTreeDiv.classList.remove("bg-rose-600", "text-white");
      btnTreeDiv.classList.add("text-slate-600");
      renderDendrogram("convergence");
    });

    btnTreeDiv.addEventListener("click", () => {
      state.treeMode = "divergence";
      btnTreeDiv.classList.add("bg-rose-600", "text-white");
      btnTreeDiv.classList.remove("text-slate-600");
      btnTreeConv.classList.remove("bg-emerald-600", "text-white");
      btnTreeConv.classList.add("text-slate-600");
      renderDendrogram("divergence");
    });
  }

  // Method guide modal
  const btnMethodGuide = document.getElementById("btn-open-method-guide");
  if (btnMethodGuide) {
    btnMethodGuide.addEventListener("click", () => {
      document.getElementById("modal-method-guide").classList.remove("hidden");
    });
  }
  const btnCloseMethod = document.getElementById("btn-close-method-modal");
  if (btnCloseMethod) {
    btnCloseMethod.addEventListener("click", () => {
      document.getElementById("modal-method-guide").classList.add("hidden");
    });
  }

  // Balance scale guide modal
  const btnOpenBalanceGuide = document.getElementById("btn-open-balance-guide");
  if (btnOpenBalanceGuide) {
    btnOpenBalanceGuide.addEventListener("click", () => {
      const m = document.getElementById("modal-balance-guide");
      if (m) m.classList.remove("hidden");
    });
  }
  const btnOpenBalanceFromDetails = document.getElementById("btn-open-balance-guide-from-details");
  if (btnOpenBalanceFromDetails) {
    btnOpenBalanceFromDetails.addEventListener("click", () => {
      const m = document.getElementById("modal-balance-guide");
      if (m) m.classList.remove("hidden");
    });
  }
  const btnCloseBalanceModal = document.getElementById("btn-close-balance-modal");
  if (btnCloseBalanceModal) {
    btnCloseBalanceModal.addEventListener("click", () => {
      const m = document.getElementById("modal-balance-guide");
      if (m) m.classList.add("hidden");
    });
  }
  const btnCloseBalanceFooter = document.getElementById("btn-close-balance-footer");
  if (btnCloseBalanceFooter) {
    btnCloseBalanceFooter.addEventListener("click", () => {
      const m = document.getElementById("modal-balance-guide");
      if (m) m.classList.add("hidden");
    });
  }

  // Actor modal close
  const btnCloseActor = document.getElementById("btn-close-actor-modal");
  if (btnCloseActor) {
    btnCloseActor.addEventListener("click", () => {
      document.getElementById("modal-actor-details").classList.add("hidden");
    });
  }

  // Close modals on backdrop click
  window.addEventListener("click", (e) => {
    const mMethod = document.getElementById("modal-method-guide");
    if (e.target === mMethod) mMethod.classList.add("hidden");
    const mActor = document.getElementById("modal-actor-details");
    if (e.target === mActor) mActor.classList.add("hidden");
    const mInterp = document.getElementById("modal-method-interpretation");
    if (e.target === mInterp) mInterp.classList.add("hidden");
    const mBalance = document.getElementById("modal-balance-guide");
    if (e.target === mBalance) mBalance.classList.add("hidden");
  });

  // Run simulation
  document.getElementById("btn-run-sim").addEventListener("click", runScenarioSimulation);
}

// Set Method Variant and update UI
function setMethodVariant(method, shouldRecalculate = true) {
  state.variant = method;
  const selectElem = document.getElementById("variant-select");
  if (selectElem) selectElem.value = method;

  const methodLabels = {
    lipsor_standard: "1. Godet Clásico (LIPSOR Base)",
    softprosp: "2. SoftProsp (Manual Adjunto Ponderado)",
    fuzzy: "3. Variante Difusa (Incertidumbre)",
    game_theory: "4. Teoría de Juegos (Coaliciones)"
  };
  const badge = document.getElementById("badge-active-method-label");
  if (badge) {
    badge.textContent = methodLabels[method] || method;
  }

  // Update card styling
  document.querySelectorAll(".method-card").forEach(card => {
    const cardMethod = card.getAttribute("data-method");
    if (cardMethod === method) {
      card.classList.add("active", "border-blue-500", "bg-blue-50/70", "shadow-xs");
      card.classList.remove("border-slate-200", "bg-slate-50");
    } else {
      card.classList.remove("active", "border-blue-500", "bg-blue-50/70", "shadow-xs");
      card.classList.add("border-slate-200", "bg-slate-50");
    }
  });

  // Synchronize Step 1 radio buttons
  document.querySelectorAll('input[name="method-radio"]').forEach(radio => {
    radio.checked = (radio.value === method);
    const parentLabel = radio.closest("label");
    if (parentLabel) {
      if (radio.value === method) {
        parentLabel.classList.add("border-blue-400", "bg-blue-50/60");
        parentLabel.classList.remove("border-slate-200", "bg-slate-50");
      } else {
        parentLabel.classList.remove("border-blue-400", "bg-blue-50/60");
        parentLabel.classList.add("border-slate-200", "bg-slate-50");
      }
    }
  });

  if (shouldRecalculate) {
    calculateMactor();
  }
}

// Open Interpretation Modal for a specific method
function openInterpretationModal(methodKey = "softprosp") {
  const modal = document.getElementById("modal-method-interpretation");
  if (!modal) return;
  modal.classList.remove("hidden");

  const tabKeyMap = {
    lipsor_standard: "interp-lipsor",
    softprosp: "interp-softprosp",
    fuzzy: "interp-fuzzy",
    game_theory: "interp-game-theory"
  };
  const targetTab = tabKeyMap[methodKey] || "interp-softprosp";
  switchInterpretationTab(targetTab);
}

// Switch tabs inside the interpretation popup
function switchInterpretationTab(targetTabId) {
  // Update button active states
  document.querySelectorAll(".modal-tab-btn").forEach(btn => {
    if (btn.getAttribute("data-interp-tab") === targetTabId) {
      btn.classList.add("active", "text-blue-700", "border-blue-600");
      btn.classList.remove("text-slate-600", "border-transparent");
    } else {
      btn.classList.remove("active", "text-blue-700", "border-blue-600");
      btn.classList.add("text-slate-600", "border-transparent");
    }
  });

  // Switch panes
  document.querySelectorAll(".interp-tab-pane").forEach(pane => {
    if (pane.id === targetTabId) {
      pane.classList.remove("hidden");
    } else {
      pane.classList.add("hidden");
    }
  });
}

// Load preloaded case
async function loadCase(caseId) {
  try {
    const resp = await fetch(`/api/mactor/cases/${caseId}`);
    if (!resp.ok) throw new Error("Error cargando caso");
    const data = await resp.json();
    const c = data.case;

    state.currentCaseId = c.id;
    state.territory = c.territory;
    state.country = c.country || "Colombia";
    state.sector = c.sector || "";
    state.actors = JSON.parse(JSON.stringify(c.actors));
    state.objectives = JSON.parse(JSON.stringify(c.objectives));
    state.mid = JSON.parse(JSON.stringify(c.mid));
    state.mao2 = JSON.parse(JSON.stringify(c.mao2));
    state.variant = c.variant || "softprosp";

    // Synchronize inputs with loaded case - 100% exact match
    if (document.getElementById("input-territory") && c.territory) {
      document.getElementById("input-territory").value = c.territory;
    }
    if (document.getElementById("input-country") && c.country) {
      document.getElementById("input-country").value = c.country;
    }
    if (document.getElementById("input-sector") && c.sector) {
      document.getElementById("input-sector").value = c.sector;
    }
    if (document.getElementById("input-target-actors") && c.actors) {
      const actLen = c.actors.length;
      const targetSel = document.getElementById("input-target-actors");
      if ([5, 8, 10, 12].includes(actLen)) {
        targetSel.value = actLen.toString();
      } else if (actLen <= 5) {
        targetSel.value = "5";
      } else if (actLen <= 8) {
        targetSel.value = "8";
      } else if (actLen <= 10) {
        targetSel.value = "10";
      } else {
        targetSel.value = "12";
      }
    }
    syncTopContextBar();
    setMethodVariant(c.variant || "softprosp", false);

    // Render configuration tables
    renderActorsConfig();
    renderObjectivesConfig();

    // Populate sim dropdowns
    populateSimulationDropdowns();

    // If case has enriched territory intelligence & news sources, render them directly
    if (c.territory_analysis) {
      state.territoryAnalysis = c.territory_analysis;
      renderTerritoryAnalysisResults(c.territory_analysis);

      // Update Search Dock status for preloaded case
      const dock = document.getElementById("live-search-dock");
      const dockTicker = document.getElementById("search-dock-ticker");
      const dockActions = document.getElementById("search-dock-actions");
      const dockProgress = document.getElementById("search-dock-progress-bar");
      const dockPercent = document.getElementById("search-dock-percent");
      const dockStatus = document.getElementById("search-dock-status-text");
      const tickerText = document.getElementById("search-dock-ticker-text");
      const dockBadge = document.getElementById("search-dock-sources-badge");
      
      const allSrcs = c.territory_analysis.news_sources || c.territory_analysis.sources || [];
      if (dock) dock.classList.remove("hidden");
      if (dockProgress) {
        dockProgress.style.width = "100%";
        dockProgress.className = "bg-gradient-to-r from-emerald-500 via-blue-500 to-indigo-500 h-2 rounded-full";
      }
      if (dockPercent) dockPercent.textContent = "100%";
      if (dockStatus) {
        dockStatus.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400"></i><span class="text-emerald-300 font-bold">Fuentes de "${c.territory}" cargadas con éxito (${allSrcs.length} despachos)</span>`;
      }
      if (dockTicker) dockTicker.classList.remove("hidden");
      if (dockActions) dockActions.classList.remove("hidden");
      if (tickerText && allSrcs.length > 0) {
        tickerText.textContent = `📰 Fuente: "${allSrcs[0].title}"`;
      }
      if (dockBadge) {
        dockBadge.textContent = `${allSrcs.length} fuentes`;
      }
    }

    // Calculate MACTOR
    await calculateMactor();

  } catch (err) {
    console.error("Error loading case:", err);
    alert("No se pudo cargar el caso seleccionado: " + err.message);
  }
}

// Calculate MACTOR via Backend
async function calculateMactor() {
  try {
    const payload = {
      actors: state.actors,
      objectives: state.objectives,
      mid: state.mid,
      mao2: state.mao2,
      variant: state.variant
    };

    const resp = await fetch("/api/mactor/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || "Error en el cálculo");
    }

    const data = await resp.json();
    state.results = data.results;

    // Update Banner Winner
    const winner = state.results.dominant_actor;
    document.getElementById("banner-winner").innerHTML = `
      <i class="fa-solid fa-trophy text-amber-400 text-xs mr-1"></i>
      <span>${winner.name} (${winner.convergence_score})</span>
    `;

    // Render Matrices
    renderMidTable();
    renderMaoTables();
    renderAlliancesAndConflictsTables();
    renderQuadrantChart();
    renderAllianceNetwork();
    renderDendrogram(state.treeMode);
    renderMobilizationChart();
    renderObjectivesDiagnostic();
    renderCoalitionsTable();

  } catch (err) {
    console.error("Calculation error:", err);
    alert("Error calculando MACTOR: " + err.message);
  }
}

// Live Territory Analysis with AI Detonator
async function analyzeTerritoryLive() {
  const territoryInput = document.getElementById("input-territory");
  const territory = territoryInput ? territoryInput.value.trim() : "";
  const country = document.getElementById("input-country") ? document.getElementById("input-country").value : "Colombia";
  const sector = document.getElementById("input-sector") ? document.getElementById("input-sector").value.trim() : "";
  const newsapiKey = document.getElementById("input-newsapi-key") ? document.getElementById("input-newsapi-key").value.trim() : "";
  const targetActors = parseInt(document.getElementById("input-target-actors")?.value, 10) || 8;

  if (!territory) {
    alert("Por favor ingrese el nombre de un territorio real (ej. Medellín, Antioquia, La Guajira, Salar de Atacama).");
    if (territoryInput) territoryInput.focus();
    return;
  }

  // Ensure top context bar immediately reflects typed input
  syncTopContextBar();

  const btnStartAi = document.getElementById("btn-start-ai-analysis");
  const origBtnHtml = btnStartAi ? btnStartAi.innerHTML : "";
  if (btnStartAi) {
    btnStartAi.disabled = true;
    btnStartAi.innerHTML = `
      <span class="flex items-center space-x-2">
        <i class="fa-solid fa-spinner fa-spin text-lg text-amber-300"></i>
        <span class="text-base tracking-wide">Rastreando Fuentes en Vivo...</span>
      </span>
    `;
    btnStartAi.classList.add("opacity-80");
  }

  const indicator = document.getElementById("scanning-status");
  if (indicator) indicator.classList.remove("hidden");

  // Activate Bottom Live Search Dock
  const dock = document.getElementById("live-search-dock");
  const dockBody = document.getElementById("search-dock-body");
  const dockLogs = document.getElementById("search-dock-logs");
  const dockProgress = document.getElementById("search-dock-progress-bar");
  const dockPercent = document.getElementById("search-dock-percent");
  const dockStatus = document.getElementById("search-dock-status-text");
  const dockTicker = document.getElementById("search-dock-ticker");
  const dockActions = document.getElementById("search-dock-actions");

  if (dock) dock.classList.remove("hidden");
  if (dockBody) dockBody.classList.remove("hidden");
  if (dockTicker) dockTicker.classList.add("hidden");
  if (dockActions) dockActions.classList.add("hidden");

  if (dockProgress) {
    dockProgress.style.width = "15%";
    dockProgress.className = "bg-gradient-to-r from-emerald-500 via-blue-500 to-indigo-500 h-2 rounded-full transition-all duration-300";
  }
  if (dockPercent) dockPercent.textContent = "15%";
  if (dockStatus) {
    dockStatus.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-blue-400"></i><span>Buscando noticias en NewsData.io, Google News LatAm, BHRRC y Redes...</span>`;
  }

  function addDockLog(msg, colorClass = "text-slate-300") {
    if (!dockLogs) return;
    const time = new Date().toLocaleTimeString();
    const line = document.createElement("div");
    line.className = `${colorClass} text-[11px] leading-relaxed flex items-start space-x-1.5`;
    line.innerHTML = `<span class="text-slate-500 font-mono text-[10px] shrink-0">[${time}]</span><span>${msg}</span>`;
    dockLogs.appendChild(line);
    dockLogs.scrollTop = dockLogs.scrollHeight;
  }

  if (dockLogs) dockLogs.innerHTML = "";
  addDockLog(`🚀 <strong>Iniciando rastreo territorial para:</strong> "${territory}" (${country}) | Sector: "${sector || 'General'}" | Profundidad: ${targetActors} Actores`, "text-cyan-300");

  const stageTimeouts = [
    setTimeout(() => {
      if (dockProgress) dockProgress.style.width = "25%";
      if (dockPercent) dockPercent.textContent = "25%";
      addDockLog(`⚡ <strong>NewsData.io API:</strong> Rastreando despachos de noticias en vivo y reportes sectoriales...`, "text-emerald-300");
    }, 300),
    setTimeout(() => {
      if (dockProgress) dockProgress.style.width = "48%";
      if (dockPercent) dockPercent.textContent = "48%";
      addDockLog(`📰 <strong>Google News LatAm:</strong> Rastreando medios de prensa regional y nacional...`, "text-blue-300");
    }, 900),
    setTimeout(() => {
      if (dockProgress) dockProgress.style.width = "68%";
      if (dockPercent) dockPercent.textContent = "68%";
      addDockLog(`⚖️ <strong>BHRRC:</strong> Consultando base de Empresas & Derechos Humanos...`, "text-amber-300");
    }, 1600),
    setTimeout(() => {
      if (dockProgress) dockProgress.style.width = "84%";
      if (dockPercent) dockPercent.textContent = "84%";
      addDockLog(`📱 <strong>Redes & Gacetas:</strong> Monitoreando X/Twitter, debates comunitarios y documentos oficiales (.gov/.gob)...`, "text-purple-300");
    }, 2400),
    setTimeout(() => {
      if (dockProgress) dockProgress.style.width = "95%";
      if (dockPercent) dockPercent.textContent = "95%";
      addDockLog(`🧠 <strong>Extracción Inteligente MACTOR (${targetActors} Actores):</strong> Deduciendo matrices de influencias y objetivos implícitos...`, "text-sky-200");
    }, 3400)
  ];

try {
  const resp = await fetch("/api/territory/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      territory,
      country,
      sector,
      newsapi_key: newsapiKey,
      target_actors: targetActors,
      max_news: 45
    })
  });

  stageTimeouts.forEach(t => clearTimeout(t));

  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || "Error analizando territorio");
  }

  const json = await resp.json();
  state.territoryAnalysis = json.data;

  // Update Dock to 100% Success
  if (dockProgress) dockProgress.style.width = "100%";
  if (dockPercent) dockPercent.textContent = "100%";
  if (dockStatus) {
    dockStatus.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-400"></i><span class="text-emerald-300 font-bold">¡Rastreo de fuentes completado con éxito!</span>`;
  }

  addDockLog(`✅ <strong>Éxito:</strong> Se indexaron ${json.data.sources ? json.data.sources.length : 0} fuentes y se extrajeron ${json.data.actors ? json.data.actors.length : 0} actores específicos.`, "text-emerald-300 font-bold");

  if (dockTicker) {
    dockTicker.classList.remove("hidden");
    const sampleHeadline = (json.data.sources && json.data.sources.length > 0) ? json.data.sources[0].title : `Noticias recopiladas para ${territory}`;
    const tickerText = document.getElementById("search-dock-ticker-text");
    if (tickerText) tickerText.textContent = `📰 Fuente: "${sampleHeadline}"`;
    const badge = document.getElementById("search-dock-sources-badge");
    if (badge) badge.textContent = `${json.data.sources ? json.data.sources.length : 0} fuentes`;
  }

  if (dockActions) {
    dockActions.classList.remove("hidden");
  }

  renderTerritoryAnalysisResults(json.data);

  // Scroll smoothly to results
  const resultsContainer = document.getElementById("territory-results");
  if (resultsContainer) {
    resultsContainer.scrollIntoView({ behavior: "smooth" });
  }

} catch (err) {
  stageTimeouts.forEach(t => clearTimeout(t));
  console.error("Territory error:", err);

  if (dockProgress) {
    dockProgress.style.width = "100%";
    dockProgress.className = "bg-rose-500 h-2 rounded-full";
  }
  if (dockPercent) dockPercent.textContent = "Error";
  if (dockStatus) {
    dockStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-rose-400"></i><span class="text-rose-300 font-bold">Error durante el rastreo</span>`;
  }
  addDockLog(`❌ <strong>Fallo:</strong> ${err.message}`, "text-rose-400 font-bold");
  alert("Error en el análisis de fuentes del territorio: " + err.message);
} finally {
  if (indicator) indicator.classList.add("hidden");
  if (btnStartAi) {
    btnStartAi.disabled = false;
    btnStartAi.innerHTML = origBtnHtml;
    btnStartAi.classList.remove("opacity-80");
  }
}
}

// Render Territory Extraction Results
function renderTerritoryAnalysisResults(data) {
  // Actors
  const actorsContainer = document.getElementById("actors-list-container");
  document.getElementById("badge-actors-count").textContent = `${data.actors.length} Actores`;
  actorsContainer.innerHTML = data.actors.map((act, idx) => `
    <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-blue-400 hover:shadow-xs transition-all space-y-2">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-md bg-blue-600 text-white font-bold flex items-center justify-center text-xs">${act.id}</span>
          <span class="font-bold text-xs text-slate-900">${act.name}</span>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 font-semibold">${act.category}</span>
      </div>

      <div class="space-y-1 text-[11px] text-slate-600">
        <p><b class="text-emerald-700">Objetivo Explícito:</b> ${act.explicit_objective || act.evidence}</p>
        <p><b class="text-amber-700">Objetivo Implícito:</b> ${act.implicit_objective || 'Mitigación de riesgos y preservación de influencia territorial.'}</p>
      </div>

      <div class="flex items-center justify-between pt-1 border-t border-slate-200/60 text-[10px]">
        <span class="text-slate-400">Poder Godet: <b>Nivel ${act.base_power || 3}/4</b></span>
        <button onclick="openActorDetailsModal(${idx})" class="text-blue-600 hover:text-blue-800 font-bold flex items-center space-x-1 hover:underline">
          <i class="fa-solid fa-address-card"></i>
          <span>Ver Ficha Completa & Posturas</span>
        </button>
      </div>
    </div>
  `).join("");

  // Objectives
  const objContainer = document.getElementById("objectives-list-container");
  document.getElementById("badge-objectives-count").textContent = `${data.objectives.length} Objetivos`;
  objContainer.innerHTML = data.objectives.map(obj => `
    <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 hover:shadow-xs transition-all space-y-1.5">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-md bg-emerald-600 text-white font-bold flex items-center justify-center text-xs">${obj.id}</span>
          <span class="font-bold text-xs text-slate-900">${obj.name}</span>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">Ponderación: ${obj.weight}%</span>
      </div>
      <p class="text-[11px] text-slate-600">${obj.description}</p>
    </div>
  `).join("");

  // Update channel counter badges
  const allNews = data.news_sources || data.sources || [];
  const counts = data.channel_counts || {};
  const countIds = ["all", "newsdata", "bhrrc", "legal", "multilateral", "ngo", "social", "official", "press", "academic"];
  countIds.forEach(ch => {
    const el = document.getElementById(`count-${ch}-sources`);
    if (el) {
      if (ch === "all") {
        el.textContent = counts.all || allNews.length;
      } else {
        el.textContent = counts[ch] !== undefined ? counts[ch] : allNews.filter(n => n.channel === ch).length;
      }
    }
  });

  // Social Pulse Banner
  const pulseBanner = document.getElementById("social-pulse-banner");
  if (data.social_pulse && pulseBanner) {
    pulseBanner.classList.remove("hidden");
    document.getElementById("badge-social-pulse-status").textContent = data.social_pulse.status;
    document.getElementById("social-pulse-summary").textContent = data.social_pulse.summary;
  }

  // Render news cards
  renderNewsCards(allNews);
}

// Render filtered news cards
function renderNewsCards(items) {
  const newsContainer = document.getElementById("news-feed-container");
  if (!newsContainer) return;

  newsContainer.innerHTML = items.map(n => `
    <div class="news-source-card p-3.5 bg-white border border-slate-200 rounded-xl shadow-2xs hover:shadow-sm transition-all flex flex-col justify-between" data-channel="${n.channel || 'press'}">
      <div>
        <div class="flex items-center justify-between text-[10px] mb-2">
          <span class="inline-flex items-center space-x-1 px-2 py-0.5 rounded font-bold border ${n.channel_badge_class || 'bg-slate-100 text-slate-800 border-slate-200'}">
            <i class="${n.channel_icon || 'fa-regular fa-newspaper'} text-[10px] mr-1"></i>
            <span>${n.channel_label || 'Prensa'}</span>
          </span>
          <span class="text-slate-400 font-medium">${n.date ? n.date.slice(0, 16) : ""}</span>
        </div>
        <h5 class="font-bold text-xs text-slate-900 leading-snug line-clamp-2">${n.title}</h5>
        <p class="text-[11px] text-slate-500 mt-1 line-clamp-2">${n.summary || ''}</p>
      </div>
      <div class="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px]">
        <span class="font-bold text-slate-500 truncate max-w-[130px]">${n.source}</span>
        ${n.link ? `<a href="${n.link}" target="_blank" class="font-bold text-blue-600 hover:text-blue-800 flex items-center space-x-1 hover:underline"><span>Ver Publicación</span> <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i></a>` : ''}
      </div>
    </div>
  `).join("");
}

// Filter news cards by channel
function filterNewsCardsByChannel(channel) {
  if (!state.territoryAnalysis) return;
  const allItems = state.territoryAnalysis.news_sources || state.territoryAnalysis.sources || [];
  if (channel === "all") {
    renderNewsCards(allItems);
  } else {
    const filtered = allItems.filter(item => item.channel === channel);
    renderNewsCards(filtered);
  }
}

// Open detailed modal for an actor
function openActorDetailsModal(idx) {
  const actor = state.territoryAnalysis ? state.territoryAnalysis.actors[idx] : state.actors[idx];
  if (!actor) return;

  const objectives = state.territoryAnalysis ? state.territoryAnalysis.objectives : state.objectives;

  document.getElementById("modal-actor-badge").textContent = actor.id || `A${idx + 1}`;
  document.getElementById("modal-actor-name").textContent = actor.name;
  document.getElementById("modal-actor-category").textContent = actor.category || "Actor Territorial";
  document.getElementById("modal-actor-role").textContent = actor.role_description || "Actor con intereses y capacidad de movilización en el territorio analizado.";
  document.getElementById("modal-actor-power-desc").textContent = actor.power_rationale || `Nivel de Poder: ${actor.base_power || 3} de 4 en la escala LIPSOR.`;
  document.getElementById("modal-actor-explicit").textContent = actor.explicit_objective || actor.evidence || "Defensa de intereses institucionales y cumplimiento de normatividad.";
  document.getElementById("modal-actor-implicit").textContent = actor.implicit_objective || "Preservación de gobernabilidad, mitigación de conflictos y optimización de recursos.";
  document.getElementById("modal-actor-evidence").textContent = `"${actor.evidence_headline || actor.evidence || 'Rastreado en la estructura territorial.'}"`;

  // Link
  const linkBox = document.getElementById("modal-actor-link-container");
  if (actor.evidence_link) {
    linkBox.innerHTML = `<a href="${actor.evidence_link}" target="_blank" class="text-blue-600 font-semibold text-xs hover:underline flex items-center space-x-1"><span>Ir a la noticia / documento fuente (${actor.evidence_source || 'Medio'})</span> <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>`;
  } else {
    linkBox.innerHTML = `<span class="text-slate-400 text-[11px]">Fuente: ${actor.evidence_source || 'Análisis Territorial Institucional'}</span>`;
  }

  // Postures table
  const tbody = document.getElementById("modal-actor-postures-tbody");
  tbody.innerHTML = objectives.map(obj => {
    let score = 0;
    let rationale = "Postura inferida en función de sus competencias institucionales y prioridades estratégicas.";
    if (actor.postures && actor.postures[obj.id]) {
      score = actor.postures[obj.id].score;
      rationale = actor.postures[obj.id].rationale;
    } else if (state.mao2 && state.mao2[idx]) {
      const objIdx = objectives.findIndex(o => o.id === obj.id);
      if (objIdx >= 0) score = state.mao2[idx][objIdx];
    }

    const badgeBg = score > 0 ? 'bg-emerald-100 text-emerald-800' : (score < 0 ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700');
    const sign = score > 0 ? `+${score}` : `${score}`;

    return `
      <tr class="border-b border-slate-100 hover:bg-slate-50">
        <td class="p-2.5 font-bold text-slate-800">${obj.id} - ${obj.name}</td>
        <td class="p-2.5 text-center">
          <span class="inline-block px-2 py-0.5 rounded font-bold text-xs ${badgeBg}">${sign}</span>
        </td>
        <td class="p-2.5 text-slate-600 leading-relaxed">${rationale}</td>
      </tr>
    `;
  }).join("");

  document.getElementById("modal-actor-details").classList.remove("hidden");
}

// Transfer territory extraction to current working matrices
function applyTerritoryToWorkspace() {
  if (!state.territoryAnalysis) {
    alert("Primero realice un análisis territorial en vivo.");
    return;
  }

  const d = state.territoryAnalysis;
  state.territory = d.territory;
  state.country = d.country || "Colombia";
  state.sector = d.sector || "";
  state.actors = d.actors;
  state.objectives = d.objectives;
  state.mid = d.mid;
  state.mao2 = d.mao2;

  // Sync inputs with extracted analysis
  if (document.getElementById("input-territory")) {
    document.getElementById("input-territory").value = d.territory;
  }
  if (document.getElementById("input-country") && d.country) {
    document.getElementById("input-country").value = d.country;
  }
  if (document.getElementById("input-sector") && d.sector) {
    document.getElementById("input-sector").value = d.sector;
  }
  syncTopContextBar();

  renderActorsConfig();
  renderObjectivesConfig();
  populateSimulationDropdowns();
  calculateMactor();

  alert(`¡Se han transferido exitosamente ${d.actors.length} actores y ${d.objectives.length} objetivos a las matrices de trabajo!`);

  // Switch to MID tab
  document.querySelector('[data-tab="tab-mid"]').click();
}

// Render Configuration Lists
function renderActorsConfig() {
  const container = document.getElementById("actors-config-table");
  container.innerHTML = state.actors.map((act, idx) => `
    <div class="flex items-center justify-between p-2.5 bg-slate-50 border border-slate-200 rounded-lg gap-2 text-xs">
      <div class="w-8 h-8 rounded bg-blue-600 text-white font-bold flex items-center justify-center shrink-0 cursor-pointer" onclick="openActorDetailsModal(${idx})" title="Ver ficha técnica">
        ${act.id || 'A' + (idx + 1)}
      </div>
      <div class="flex-grow">
        <input type="text" value="${act.name}" onchange="updateActorName(${idx}, this.value)" class="w-full font-bold text-slate-800 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-blue-500 focus:outline-none">
        <div class="flex items-center space-x-2 mt-0.5 text-[10px] text-slate-500">
          <span>Categoría: ${act.category || 'General'}</span>
          <span>&bull;</span>
          <button onclick="openActorDetailsModal(${idx})" class="text-blue-600 hover:underline font-semibold">Ver Ficha & Posturas</button>
        </div>
      </div>
      <button onclick="removeActor(${idx})" class="text-rose-500 hover:text-rose-700 p-1.5 rounded hover:bg-rose-50" title="Eliminar actor">
        <i class="fa-solid fa-trash-can"></i>
      </button>
    </div>
  `).join("");
}

function renderObjectivesConfig() {
  const container = document.getElementById("objectives-config-table");
  container.innerHTML = state.objectives.map((obj, idx) => `
    <div class="flex items-center justify-between p-2.5 bg-slate-50 border border-slate-200 rounded-lg gap-2 text-xs">
      <div class="w-8 h-8 rounded bg-emerald-600 text-white font-bold flex items-center justify-center shrink-0">
        ${obj.id || 'O' + (idx + 1)}
      </div>
      <div class="flex-grow">
        <input type="text" value="${obj.name}" onchange="updateObjectiveName(${idx}, this.value)" class="w-full font-bold text-slate-800 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-emerald-500 focus:outline-none">
        <div class="flex items-center space-x-2 mt-1">
          <label class="text-[10px] text-slate-500 font-medium">Ponderación (%):</label>
          <input type="number" min="1" max="100" value="${obj.weight || 20}" onchange="updateObjectiveWeight(${idx}, this.value)" class="w-16 px-1.5 py-0.5 border border-slate-300 rounded text-center font-bold text-emerald-700 focus:outline-none">
        </div>
      </div>
      <button onclick="removeObjective(${idx})" class="text-rose-500 hover:text-rose-700 p-1.5 rounded hover:bg-rose-50" title="Eliminar objetivo">
        <i class="fa-solid fa-trash-can"></i>
      </button>
    </div>
  `).join("");
}

// Add / Remove Actor / Objective
function addNewActor() {
  const newIdx = state.actors.length + 1;
  const newActor = {
    id: `A${newIdx}`,
    name: `Nuevo Actor Estratégico ${newIdx}`,
    short_name: `Actor ${newIdx}`,
    category: "Sector Emergente",
    base_power: 2
  };
  state.actors.push(newActor);

  // Expand MID with 0s
  state.mid.forEach(row => row.push(0));
  state.mid.push(new Array(state.actors.length).fill(0));

  // Expand 2MAO
  state.mao2.push(new Array(state.objectives.length).fill(0));

  renderActorsConfig();
  populateSimulationDropdowns();
  calculateMactor();
}

function removeActor(idx) {
  if (state.actors.length <= 2) {
    alert("Se requieren al menos 2 actores para el análisis MACTOR.");
    return;
  }
  state.actors.splice(idx, 1);
  state.mid.splice(idx, 1);
  state.mid.forEach(row => row.splice(idx, 1));
  state.mao2.splice(idx, 1);

  renderActorsConfig();
  populateSimulationDropdowns();
  calculateMactor();
}

function addNewObjective() {
  const newIdx = state.objectives.length + 1;
  const newObj = {
    id: `O${newIdx}`,
    name: `Nuevo Objetivo Territorial ${newIdx}`,
    short_name: `Obj ${newIdx}`,
    weight: 20.0
  };
  state.objectives.push(newObj);

  // Expand 2MAO columns
  state.mao2.forEach(row => row.push(0));

  renderObjectivesConfig();
  populateSimulationDropdowns();
  calculateMactor();
}

function removeObjective(idx) {
  if (state.objectives.length <= 1) {
    alert("Se requiere al menos 1 objetivo para el análisis MACTOR.");
    return;
  }
  state.objectives.splice(idx, 1);
  state.mao2.forEach(row => row.splice(idx, 1));

  renderObjectivesConfig();
  populateSimulationDropdowns();
  calculateMactor();
}

function updateActorName(idx, val) {
  state.actors[idx].name = val;
  state.actors[idx].short_name = val.length > 20 ? val.slice(0, 18) + ".." : val;
  calculateMactor();
}

function updateObjectiveName(idx, val) {
  state.objectives[idx].name = val;
  state.objectives[idx].short_name = val.length > 20 ? val.slice(0, 18) + ".." : val;
  calculateMactor();
}

function updateObjectiveWeight(idx, val) {
  state.objectives[idx].weight = parseFloat(val) || 1.0;
  calculateMactor();
}

// Render MID Table (Direct Influences)
function renderMidTable() {
  const container = document.getElementById("mid-table-container");
  const N = state.actors.length;

  let html = `<table class="w-full text-[11px] border border-slate-200 rounded-lg overflow-hidden table-matrix">
    <thead class="bg-slate-800 text-white font-bold">
      <tr>
        <th class="py-1.5 px-2 border border-slate-700 bg-slate-900 text-left whitespace-nowrap">Actores (Inf. \\ Dep.)</th>
        ${state.actors.map((a, idx) => `<th class="py-1.5 px-1.5 border border-slate-700 whitespace-nowrap" title="${a.name}">${a.id || 'A' + (idx + 1)}</th>`).join("")}
        <th class="py-1.5 px-2 border border-slate-700 bg-blue-900 whitespace-nowrap" title="Influencia Directa Total">Inf. (I_i)</th>
      </tr>
    </thead>
    <tbody>`;

  for (let i = 0; i < N; i++) {
    const actRow = state.actors[i];
    const rowSum = state.results ? state.results.mid_metrics.influence[i] : state.mid[i].reduce((a, b) => a + b, 0);
    const shortLbl = actRow.short_name || actRow.name;
    html += `<tr class="hover:bg-slate-50/70 transition-colors">
      <td class="py-1 px-2 font-bold bg-slate-100 border border-slate-200 text-left whitespace-nowrap max-w-[180px] truncate" title="${actRow.name}">
        <span class="text-blue-700 mr-1">${actRow.id || 'A' + (i + 1)}</span>${escapeXml(shortLbl)}
      </td>`;

    for (let j = 0; j < N; j++) {
      if (i === j) {
        html += `<td class="p-1 border border-slate-200 bg-slate-200/80 font-bold text-slate-400 text-[11px]">0</td>`;
      } else {
        const val = state.mid[i][j];
        const bgClass = val === 4 ? "bg-blue-600 text-white border-blue-700" :
                        (val === 3 ? "bg-blue-200 text-blue-900 border-blue-300" :
                        (val === 2 ? "bg-blue-50 text-blue-800 border-blue-200" :
                        (val === 0 ? "bg-slate-50 text-slate-400" : "bg-white text-slate-800")));
        html += `<td class="p-0.5 border border-slate-200">
          <input type="number" min="0" max="4" value="${val}" data-row="${i}" data-col="${j}" class="mid-cell matrix-input ${bgClass}" onchange="onMidCellChange(${i}, ${j}, this.value)">
        </td>`;
      }
    }

    html += `<td class="py-1 px-2 font-bold bg-blue-50 text-blue-900 border border-slate-200 whitespace-nowrap">${rowSum}</td>
    </tr>`;
  }

  // Footer Row: Dependences (D_i)
  html += `<tr class="bg-blue-900 text-white font-bold">
    <td class="py-1.5 px-2 border border-slate-700 text-left whitespace-nowrap">Total Dep. (D_i)</td>
    ${state.actors.map((_, j) => {
    const colSum = state.results ? state.results.mid_metrics.dependence[j] : 0;
    return `<td class="py-1.5 px-1.5 border border-slate-700">${colSum}</td>`;
  }).join("")}
    <td class="py-1.5 px-2 border border-slate-700 bg-blue-950">${state.results ? state.results.mid_metrics.total_influence : 0}</td>
  </tr>
  </tbody></table>`;

  container.innerHTML = html;

  // Render MIDI if results exist
  if (state.results && state.results.midi) {
    renderMidiTable();
  }
}

// Render MIDI Table
function renderMidiTable() {
  const container = document.getElementById("midi-table-container");
  const N = state.actors.length;
  const midi = state.results.midi;
  const force = state.results.force_metrics;

  let html = `<table class="w-full text-[11px] border border-slate-200 rounded-lg overflow-hidden table-matrix">
    <thead class="bg-slate-700 text-white font-bold">
      <tr>
        <th class="py-1.5 px-2 border border-slate-600 text-left whitespace-nowrap">Actores</th>
        ${state.actors.map((a, idx) => `<th class="py-1.5 px-1.5 border border-slate-600 whitespace-nowrap" title="${a.name}">${a.id || 'A' + (idx + 1)}</th>`).join("")}
        <th class="py-1.5 px-2 border border-slate-600 bg-amber-700 whitespace-nowrap">Fuerza (r_i)</th>
      </tr>
    </thead>
    <tbody>`;

  for (let i = 0; i < N; i++) {
    const act = state.actors[i];
    const shortLbl = act.short_name || act.name;
    html += `<tr class="hover:bg-slate-50/70">
      <td class="py-1 px-2 font-bold bg-slate-50 border border-slate-200 text-left whitespace-nowrap max-w-[180px] truncate" title="${act.name}">
        <span class="text-slate-600 mr-1">${act.id || 'A' + (i + 1)}</span>${escapeXml(shortLbl)}
      </td>`;
    for (let j = 0; j < N; j++) {
      html += `<td class="py-1 px-1.5 border border-slate-200 ${i === j ? 'bg-slate-100 text-slate-400' : ''}">${midi[i][j]}</td>`;
    }
    html += `<td class="py-1 px-2 font-bold bg-amber-50 text-amber-900 border border-slate-200 whitespace-nowrap">${force.r_i[i].toFixed(2)}</td>
    </tr>`;
  }
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function onMidCellChange(r, c, val) {
  let num = parseInt(val, 10);
  if (isNaN(num) || num < 0) num = 0;
  if (num > 4) num = 4;
  state.mid[r][c] = num;
  calculateMactor();
}

// Render 2MAO & 3MAO Tables
function renderMaoTables() {
  const container2 = document.getElementById("mao2-table-container");
  const N = state.actors.length;
  const M = state.objectives.length;

  let html2 = `<table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden table-matrix">
    <thead class="bg-indigo-900 text-white font-bold">
      <tr>
        <th class="p-2 border border-indigo-800 bg-indigo-950">Actores \\ Objetivos</th>
        ${state.objectives.map(o => `<th class="p-2 border border-indigo-800" title="${o.name}">${o.id || o.short_name} <br><span class="text-[10px] text-indigo-300 font-normal">(${o.weight || 20}%)</span></th>`).join("")}
      </tr>
    </thead>
    <tbody>`;

  for (let i = 0; i < N; i++) {
    html2 += `<tr>
      <td class="p-2 font-bold bg-slate-100 border border-slate-200 text-left">${state.actors[i].id} - ${state.actors[i].name}</td>`;
    for (let j = 0; j < M; j++) {
      const val = state.mao2[i][j];
      const bg = val > 0 ? "bg-emerald-50 text-emerald-900 font-bold" : (val < 0 ? "bg-rose-50 text-rose-900 font-bold" : "bg-white text-slate-400");
      html2 += `<td class="p-1 border border-slate-200">
        <input type="number" min="-4" max="4" value="${val}" class="matrix-input ${bg}" onchange="onMao2CellChange(${i}, ${j}, this.value)">
      </td>`;
    }
    html2 += `</tr>`;
  }
  html2 += `</tbody></table>`;
  container2.innerHTML = html2;

  // 3MAO
  if (state.results && state.results.mao3) {
    const container3 = document.getElementById("mao3-table-container");
    const mao3 = state.results.mao3;
    let html3 = `<table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden table-matrix">
      <thead class="bg-slate-700 text-white font-bold">
        <tr>
          <th class="p-2 border border-slate-600">Actores \\ Objetivos (3MAO)</th>
          ${state.objectives.map(o => `<th class="p-2 border border-slate-600">${o.id}</th>`).join("")}
        </tr>
      </thead>
      <tbody>`;
    for (let i = 0; i < N; i++) {
      html3 += `<tr>
        <td class="p-2 font-bold bg-slate-50 border border-slate-200 text-left">${state.actors[i].id}</td>`;
      for (let j = 0; j < M; j++) {
        const v = mao3[i][j];
        const clr = v > 0 ? "text-emerald-700 font-bold" : (v < 0 ? "text-rose-700 font-bold" : "text-slate-400");
        html3 += `<td class="p-2 border border-slate-200 ${clr}">${v.toFixed(2)}</td>`;
      }
      html3 += `</tr>`;
    }
    html3 += `</tbody></table>`;
    container3.innerHTML = html3;
  }

  // Update LIPSOR Position Figures (Balanza de Posición)
  populateBalanceDropdowns();
  renderBalanceScaleView();
}

function onMao2CellChange(r, c, val) {
  let num = parseFloat(val);
  if (isNaN(num)) num = 0;
  if (num > 4) num = 4;
  if (num < -4) num = -4;
  state.mao2[r][c] = num;
  calculateMactor();
}

// ========================================================
// FIGURAS DE POSICIÓN LIPSOR MACTOR (Balanza de Posición)
// ========================================================

function escapeXml(unsafe) {
  if (!unsafe) return "";
  return String(unsafe).replace(/[<>&'"]/g, function (c) {
    switch (c) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '&': return '&amp;';
      case '\'': return '&apos;';
      case '"': return '&quot;';
    }
  });
}

function setupBalanceScaleHandlers() {
  const btnSingle = document.getElementById("btn-balance-mode-single");
  const btnGallery = document.getElementById("btn-balance-mode-gallery");
  const btnActor = document.getElementById("btn-balance-mode-actor");

  if (btnSingle) btnSingle.addEventListener("click", () => setBalanceMode("single"));
  if (btnGallery) btnGallery.addEventListener("click", () => setBalanceMode("gallery"));
  if (btnActor) btnActor.addEventListener("click", () => setBalanceMode("actor"));

  const selObj = document.getElementById("select-balance-objective");
  if (selObj) {
    selObj.addEventListener("change", (e) => {
      state.balanceScale.objIndex = parseInt(e.target.value, 10) || 0;
      renderBalanceScaleView();
    });
  }

  const btnPrev = document.getElementById("btn-balance-prev");
  if (btnPrev) {
    btnPrev.addEventListener("click", () => {
      if (!state.objectives || state.objectives.length === 0) return;
      state.balanceScale.objIndex = (state.balanceScale.objIndex - 1 + state.objectives.length) % state.objectives.length;
      if (selObj) selObj.value = state.balanceScale.objIndex;
      renderBalanceScaleView();
    });
  }

  const btnNext = document.getElementById("btn-balance-next");
  if (btnNext) {
    btnNext.addEventListener("click", () => {
      if (!state.objectives || state.objectives.length === 0) return;
      state.balanceScale.objIndex = (state.balanceScale.objIndex + 1) % state.objectives.length;
      if (selObj) selObj.value = state.balanceScale.objIndex;
      renderBalanceScaleView();
    });
  }

  const checkWeighted = document.getElementById("check-balance-weight-3mao");
  if (checkWeighted) {
    checkWeighted.addEventListener("change", (e) => {
      state.balanceScale.weighted = e.target.checked;
      renderBalanceScaleView();
    });
  }

  const selActor = document.getElementById("select-balance-actor");
  if (selActor) {
    selActor.addEventListener("change", (e) => {
      state.balanceScale.actorIndex = parseInt(e.target.value, 10) || 0;
      renderBalanceScaleView();
    });
  }

  const btnExport = document.getElementById("btn-export-balance-svg");
  if (btnExport) {
    btnExport.addEventListener("click", exportBalanceScaleSvg);
  }
}

function setBalanceMode(mode) {
  state.balanceScale.mode = mode;

  const btnSingle = document.getElementById("btn-balance-mode-single");
  const btnGallery = document.getElementById("btn-balance-mode-gallery");
  const btnActor = document.getElementById("btn-balance-mode-actor");

  const singleControls = document.getElementById("balance-single-controls");
  const actorControls = document.getElementById("balance-actor-controls");
  const metricsBar = document.getElementById("balance-metrics-bar");
  const neutralBar = document.getElementById("balance-neutral-bar");

  // Reset classes
  [btnSingle, btnGallery, btnActor].forEach(b => {
    if (b) {
      b.classList.remove("bg-white", "text-indigo-700", "shadow-2xs", "font-bold");
      b.classList.add("text-slate-600");
    }
  });

  if (mode === "single") {
    if (btnSingle) {
      btnSingle.classList.add("bg-white", "text-indigo-700", "shadow-2xs", "font-bold");
      btnSingle.classList.remove("text-slate-600");
    }
    if (singleControls) singleControls.classList.remove("hidden");
    if (actorControls) actorControls.classList.add("hidden");
    if (metricsBar) metricsBar.classList.remove("hidden");
  } else if (mode === "gallery") {
    if (btnGallery) {
      btnGallery.classList.add("bg-white", "text-indigo-700", "shadow-2xs", "font-bold");
      btnGallery.classList.remove("text-slate-600");
    }
    if (singleControls) singleControls.classList.remove("hidden");
    if (actorControls) actorControls.classList.add("hidden");
    if (metricsBar) metricsBar.classList.add("hidden");
    if (neutralBar) neutralBar.classList.add("hidden");
  } else if (mode === "actor") {
    if (btnActor) {
      btnActor.classList.add("bg-white", "text-indigo-700", "shadow-2xs", "font-bold");
      btnActor.classList.remove("text-slate-600");
    }
    if (singleControls) singleControls.classList.add("hidden");
    if (actorControls) actorControls.classList.remove("hidden");
    if (metricsBar) metricsBar.classList.add("hidden");
    if (neutralBar) neutralBar.classList.add("hidden");
  }

  renderBalanceScaleView();
}

function populateBalanceDropdowns() {
  const selObj = document.getElementById("select-balance-objective");
  if (selObj && state.objectives) {
    const curVal = parseInt(selObj.value, 10);
    selObj.innerHTML = state.objectives.map((o, idx) => `
      <option value="${idx}" ${idx === state.balanceScale.objIndex ? "selected" : ""}>
        ${o.id || `O${idx + 1}`}: ${o.name || o.short_name}
      </option>
    `).join("");
    if (!isNaN(curVal) && curVal >= 0 && curVal < state.objectives.length) {
      state.balanceScale.objIndex = curVal;
      selObj.value = curVal;
    }
  }

  const selActor = document.getElementById("select-balance-actor");
  if (selActor && state.actors) {
    const curActor = parseInt(selActor.value, 10);
    selActor.innerHTML = state.actors.map((a, idx) => `
      <option value="${idx}" ${idx === state.balanceScale.actorIndex ? "selected" : ""}>
        ${a.id || `A${idx + 1}`}: ${a.name}
      </option>
    `).join("");
    if (!isNaN(curActor) && curActor >= 0 && curActor < state.actors.length) {
      state.balanceScale.actorIndex = curActor;
      selActor.value = curActor;
    }
  }
}

function renderBalanceScaleView() {
  const container = document.getElementById("balance-svg-container");
  if (!container) return;

  if (!state.objectives || state.objectives.length === 0 || !state.actors || state.actors.length === 0) {
    container.innerHTML = `<div class="p-8 text-center text-slate-400 text-xs">Cargue o configure actores y objetivos para visualizar la balanza LIPSOR.</div>`;
    return;
  }

  const mode = state.balanceScale.mode;

  if (mode === "single") {
    const objIdx = state.balanceScale.objIndex || 0;
    const isWeighted = state.balanceScale.weighted;
    const svg = generateSingleBalanceSvg(objIdx, isWeighted, 820, 520, false);
    container.innerHTML = svg;
    updateBalanceMetrics(objIdx, isWeighted);
  } else if (mode === "gallery") {
    renderBalanceGallery();
  } else if (mode === "actor") {
    const actorIdx = state.balanceScale.actorIndex || 0;
    const svg = renderActorProfileSvg(actorIdx);
    container.innerHTML = svg;
  }
}

function updateBalanceMetrics(objIdx, isWeighted) {
  const obj = state.objectives[objIdx];
  if (!obj) return;

  let fPlus = 0;
  let fMinus = 0;
  const neutralActors = [];

  for (let i = 0; i < state.actors.length; i++) {
    const act = state.actors[i];
    const rawVal = (state.mao2 && state.mao2[i]) ? state.mao2[i][objIdx] : 0;
    let w = Math.abs(rawVal);
    if (isWeighted && state.results && state.results.mao3 && state.results.mao3[i]) {
      w = Math.abs(state.results.mao3[i][objIdx]);
    }

    if (rawVal > 0) {
      fPlus += w;
    } else if (rawVal < 0) {
      fMinus += w;
    } else {
      neutralActors.push(act.short_name || act.name);
    }
  }

  const net = fPlus - fMinus;

  if (document.getElementById("metric-balance-f-plus")) {
    document.getElementById("metric-balance-f-plus").textContent = fPlus.toFixed(2);
  }
  if (document.getElementById("metric-balance-f-minus")) {
    document.getElementById("metric-balance-f-minus").textContent = fMinus.toFixed(2);
  }
  if (document.getElementById("metric-balance-f-net")) {
    const netEl = document.getElementById("metric-balance-f-net");
    netEl.textContent = (net >= 0 ? "+" : "") + net.toFixed(2);
    netEl.className = net > 0 ? "text-lg font-bold text-emerald-800" : (net < 0 ? "text-lg font-bold text-rose-800" : "text-lg font-bold text-slate-700");
  }

  let diagText = "Disputa Abierta";
  let diagIcon = "⚖️";
  const tot = fPlus + fMinus;

  if (tot === 0) {
    diagText = "Indiferencia / Sin posturas";
    diagIcon = "⚪";
  } else if (fMinus === 0 && fPlus > 0) {
    diagText = "Consenso Favorable Absoluto";
    diagIcon = "🟢";
  } else if (fPlus === 0 && fMinus > 0) {
    diagText = "Rechazo Total / Veto Absoluto";
    diagIcon = "🔴";
  } else if (fPlus >= 2 * fMinus) {
    diagText = "Dominio Favorable Mayoritario";
    diagIcon = "✅";
  } else if (fMinus >= 2 * fPlus) {
    diagText = "Oposición Mayoritaria Dominante";
    diagIcon = "⛔";
  } else if (Math.abs(net) <= 0.25 * tot) {
    diagText = "Empate de Fuerzas / Conflicto Agudo";
    diagIcon = "⚠️";
  } else {
    diagText = net > 0 ? "Favorable pero con Conflicto" : "Desfavorable con Oposición Fuerte";
    diagIcon = "⚖️";
  }

  if (document.getElementById("metric-balance-diagnosis")) {
    document.getElementById("metric-balance-diagnosis").textContent = diagText;
  }
  if (document.getElementById("metric-balance-icon")) {
    document.getElementById("metric-balance-icon").textContent = diagIcon;
  }

  const neutralBox = document.getElementById("balance-neutral-bar");
  const neutralList = document.getElementById("balance-neutral-list");
  if (neutralBox && neutralList) {
    if (neutralActors.length > 0) {
      neutralBox.classList.remove("hidden");
      neutralList.textContent = neutralActors.join(" • ");
    } else {
      neutralBox.classList.add("hidden");
    }
  }
}

function generateSingleBalanceSvg(objIdx, isWeighted, width = 820, height = 520, isMini = false) {
  const obj = state.objectives[objIdx];
  if (!obj) return "";

  const favorable = [];
  const opposed = [];
  let fPlus = 0;
  let fMinus = 0;

  for (let i = 0; i < state.actors.length; i++) {
    const act = state.actors[i];
    const rawVal = (state.mao2 && state.mao2[i]) ? state.mao2[i][objIdx] : 0;
    let w = Math.abs(rawVal);
    let weightedVal = rawVal;
    if (isWeighted && state.results && state.results.mao3 && state.results.mao3[i]) {
      w = Math.abs(state.results.mao3[i][objIdx]);
      weightedVal = state.results.mao3[i][objIdx];
    }

    if (rawVal > 0) {
      favorable.push({
        name: act.short_name || act.name,
        rawVal: rawVal,
        valStr: `+${rawVal}`,
        weightedVal: weightedVal.toFixed(1),
        weight: w
      });
      fPlus += w;
    } else if (rawVal < 0) {
      opposed.push({
        name: act.short_name || act.name,
        rawVal: rawVal,
        valStr: `${rawVal}`,
        weightedVal: weightedVal.toFixed(1),
        weight: w
      });
      fMinus += w;
    }
  }

  const tot = fPlus + fMinus;
  let diff = tot > 0 ? (fPlus - fMinus) / tot : 0;
  diff = Math.max(-1, Math.min(1, diff));

  const maxDisp = isMini ? 35 : 75;
  const dY = diff * maxDisp;
  const tiltAngle = -diff * (isMini ? 18 : 22);

  const yLeft = (isMini ? 190 : 330) + dY;
  const yRight = (isMini ? 190 : 330) - dY;

  const xLeft = isMini ? 95 : 180;
  const xRight = isMini ? 295 : 640;
  const cX = isMini ? 195 : 410;
  const pivotY = isMini ? 42 : 74;

  const uid = Math.random().toString(36).substring(2, 7);

  // Stack actors on left pan
  let leftActorsText = "";
  if (isMini) {
    leftActorsText = `<text x="${xLeft}" y="${yLeft - 12}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="10" font-weight="bold" fill="#047857">${favorable.length} a favor (${fPlus.toFixed(1)})</text>`;
  } else {
    const lineH = Math.min(22, Math.max(14, 140 / Math.max(1, favorable.length)));
    const fSize = favorable.length > 6 ? 10 : (favorable.length > 4 ? 11 : 12);
    favorable.forEach((act, idx) => {
      const actY = yLeft - 14 - (idx * lineH);
      const score = isWeighted ? act.weightedVal : act.valStr;
      leftActorsText += `<text x="${xLeft}" y="${actY}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="${fSize}" font-weight="600" fill="#0f172a">
        ${escapeXml(act.name)} <tspan font-weight="bold" fill="#047857">(${score})</tspan>
      </text>`;
    });
  }

  // Stack actors on right pan
  let rightActorsText = "";
  if (isMini) {
    rightActorsText = `<text x="${xRight}" y="${yRight - 12}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="10" font-weight="bold" fill="#b91c1c">${opposed.length} en contra (${fMinus.toFixed(1)})</text>`;
  } else {
    if (opposed.length === 0) {
      rightActorsText = `<text x="${xRight}" y="${yRight - 16}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-style="italic" fill="#94a3b8">Sin oposición</text>`;
    } else {
      const lineH = Math.min(22, Math.max(14, 140 / Math.max(1, opposed.length)));
      const fSize = opposed.length > 6 ? 10 : (opposed.length > 4 ? 11 : 12);
      opposed.forEach((act, idx) => {
        const actY = yRight - 14 - (idx * lineH);
        const score = isWeighted ? act.weightedVal : act.valStr;
        rightActorsText += `<text x="${xRight}" y="${actY}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="${fSize}" font-weight="600" fill="#0f172a">
          ${escapeXml(act.name)} <tspan font-weight="bold" fill="#b91c1c">(${score})</tspan>
        </text>`;
      });
    }
  }

  const panRx = isMini ? 55 : 100;
  const panRy = isMini ? 10 : 17;
  const panDepth = isMini ? 12 : 24;
  const panLip = isMini ? 8 : 18;

  const needleLen = isMini ? 190 : 340;
  const needlePath = isMini
    ? `M ${cX - 2} ${pivotY} L ${cX - 1} ${pivotY + needleLen - 20} L ${cX} ${pivotY + needleLen} L ${cX + 1} ${pivotY + needleLen - 20} L ${cX + 2} ${pivotY} Z`
    : `M ${cX - 3} ${pivotY} L ${cX - 2} ${pivotY + needleLen - 35} L ${cX} ${pivotY + needleLen} L ${cX + 2} ${pivotY + needleLen - 35} L ${cX + 3} ${pivotY} Z`;

  const archSpan = isMini ? 70 : 140;
  const archSag = isMini ? 20 : 42;
  const archThick = isMini ? 10 : 22;

  const cordLeft1X = isMini ? xLeft - 35 : xLeft - 80;
  const cordLeft2X = isMini ? xLeft + 35 : xLeft + 80;
  const cordLeftTop1X = isMini ? cX - 45 : cX - 110;
  const cordLeftTop2X = isMini ? cX - 25 : cX - 80;

  const cordRight1X = isMini ? xRight - 35 : xRight - 80;
  const cordRight2X = isMini ? xRight + 35 : xRight + 80;
  const cordRightTop1X = isMini ? cX + 25 : cX + 80;
  const cordRightTop2X = isMini ? cX + 45 : cX + 110;

  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" class="w-full max-w-4xl select-none" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.03));">
      <defs>
        <linearGradient id="gold-arch-${uid}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fef08a" />
          <stop offset="45%" stop-color="#eab308" />
          <stop offset="100%" stop-color="#854d0e" />
        </linearGradient>
        <linearGradient id="gold-needle-${uid}" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#fef08a" />
          <stop offset="50%" stop-color="#ca8a04" />
          <stop offset="100%" stop-color="#713f12" />
        </linearGradient>
        <linearGradient id="pan-gold-top-${uid}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fef9c3" />
          <stop offset="50%" stop-color="#facc15" />
          <stop offset="100%" stop-color="#ca8a04" />
        </linearGradient>
        <linearGradient id="pan-gold-body-${uid}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#ca8a04" />
          <stop offset="35%" stop-color="#eab308" />
          <stop offset="100%" stop-color="#713f12" />
        </linearGradient>
      </defs>

      <!-- Frame & Background -->
      <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5" />

      <!-- Canonical LIPSOR Title -->
      <text x="${cX}" y="${isMini ? 18 : 32}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="${isMini ? 10 : 15}" font-weight="bold" fill="#1e293b">
        Position scale by valued objectives weighted competitiveness
      </text>

      <!-- Subtitle (Objective Name) -->
      <text x="${cX}" y="${isMini ? 32 : 54}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="${isMini ? 9 : 13}" font-weight="bold" fill="#0f172a" text-decoration="underline">
        Objective : ${escapeXml(obj.name || obj.short_name)}
      </text>

      <!-- Center Dashed Equilibrium Reference Line -->
      <line x1="${cX}" y1="${pivotY}" x2="${cX}" y2="${height - (isMini ? 25 : 55)}" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4" />

      <!-- Suspension Cords -->
      <g opacity="0.45" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3">
        <line x1="${cordLeft1X}" y1="${yLeft}" x2="${cordLeftTop1X}" y2="${pivotY + 8}" />
        <line x1="${cordLeft2X}" y1="${yLeft}" x2="${cordLeftTop2X}" y2="${pivotY + 8}" />
        <line x1="${cordRight1X}" y1="${yRight}" x2="${cordRightTop1X}" y2="${pivotY + 8}" />
        <line x1="${cordRight2X}" y1="${yRight}" x2="${cordRightTop2X}" y2="${pivotY + 8}" />
      </g>

      <!-- Top Golden Arch / Curved Lever -->
      <path d="M ${cX - archSpan} ${pivotY + 10} Q ${cX} ${pivotY - archSag} ${cX + archSpan} ${pivotY + 10} Q ${cX} ${pivotY - archSag + archThick} ${cX - archSpan} ${pivotY + 10} Z" fill="url(#gold-arch-${uid})" stroke="#854d0e" stroke-width="1" />

      <!-- Center Pivot Pin -->
      <circle cx="${cX}" cy="${pivotY}" r="${isMini ? 3.5 : 5.5}" fill="#713f12" />
      <circle cx="${cX}" cy="${pivotY}" r="${isMini ? 1.8 : 2.8}" fill="#fef08a" />

      <!-- Dynamic Central Needle -->
      <g transform="rotate(${tiltAngle}, ${cX}, ${pivotY})">
        <path d="${needlePath}" fill="url(#gold-needle-${uid})" stroke="#713f12" stroke-width="0.8" />
      </g>

      <!-- Stacked Text of Actors (Left Pan) -->
      ${leftActorsText}

      <!-- Left Pan (Golden 3D Oval) -->
      <g>
        <path d="M ${xLeft - panRx} ${yLeft} C ${xLeft - panRx} ${yLeft + panDepth} ${xLeft + panRx} ${yLeft + panDepth} ${xLeft + panRx} ${yLeft} L ${xLeft + panRx} ${yLeft + panLip} C ${xLeft + panRx} ${yLeft + panDepth + panLip} ${xLeft - panRx} ${yLeft + panDepth + panLip} ${xLeft - panRx} ${yLeft + panLip} Z" fill="url(#pan-gold-body-${uid})" stroke="#854d0e" stroke-width="1" />
        <ellipse cx="${xLeft}" cy="${yLeft}" rx="${panRx}" ry="${panRy}" fill="url(#pan-gold-top-${uid})" stroke="#854d0e" stroke-width="1.2" />
      </g>

      <!-- Stacked Text of Actors (Right Pan) -->
      ${rightActorsText}

      <!-- Right Pan (Golden 3D Oval) -->
      <g>
        <path d="M ${xRight - panRx} ${yRight} C ${xRight - panRx} ${yRight + panDepth} ${xRight + panRx} ${yRight + panDepth} ${xRight + panRx} ${yRight} L ${xRight + panRx} ${yRight + panLip} C ${xRight + panRx} ${yRight + panDepth + panLip} ${xRight - panRx} ${yRight + panDepth + panLip} ${xRight - panRx} ${yRight + panLip} Z" fill="url(#pan-gold-body-${uid})" stroke="#854d0e" stroke-width="1" />
        <ellipse cx="${xRight}" cy="${yRight}" rx="${panRx}" ry="${panRy}" fill="url(#pan-gold-top-${uid})" stroke="#854d0e" stroke-width="1.2" />
      </g>

      <!-- Bottom Status Badges (+ and -) -->
      <g>
        <circle cx="${xLeft}" cy="${height - (isMini ? 22 : 42)}" r="${isMini ? 12 : 18}" fill="#10b981" stroke="#059669" stroke-width="2" />
        <text x="${xLeft}" y="${height - (isMini ? 17 : 35)}" text-anchor="middle" fill="#ffffff" font-size="${isMini ? 14 : 20}" font-weight="bold" font-family="'Segoe UI', Arial, sans-serif">+</text>
      </g>
      <g>
        <circle cx="${xRight}" cy="${height - (isMini ? 22 : 42)}" r="${isMini ? 12 : 18}" fill="#ef4444" stroke="#dc2626" stroke-width="2" />
        <text x="${xRight}" y="${height - (isMini ? 17 : 35)}" text-anchor="middle" fill="#ffffff" font-size="${isMini ? 16 : 22}" font-weight="bold" font-family="'Segoe UI', Arial, sans-serif">-</text>
      </g>

      <!-- Watermark -->
      <text x="${width - 15}" y="${height - 12}" text-anchor="end" font-family="monospace" font-size="${isMini ? 7.5 : 9.5}" font-weight="bold" fill="#94a3b8">
        @LIPSOR-EPITA-MACTOR
      </text>
    </svg>
  `;
}

function renderBalanceGallery() {
  const container = document.getElementById("balance-svg-container");
  if (!container || !state.objectives) return;

  const isWeighted = state.balanceScale.weighted;
  let html = `<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 w-full">`;

  state.objectives.forEach((obj, idx) => {
    const miniSvg = generateSingleBalanceSvg(idx, isWeighted, 390, 270, true);
    html += `
      <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl hover:border-indigo-400 hover:shadow-sm transition-all flex flex-col items-center cursor-pointer" onclick="selectObjectiveFromGallery(${idx})">
        <div class="w-full flex justify-between items-center text-xs font-bold text-slate-800 mb-1 px-1">
          <span class="truncate max-w-[280px]" title="${obj.name}">${obj.id || `O${idx + 1}`}: ${obj.name}</span>
          <span class="px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 text-[10px] shrink-0">${obj.weight ? `${obj.weight}%` : ''}</span>
        </div>
        ${miniSvg}
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
}

function selectObjectiveFromGallery(idx) {
  state.balanceScale.objIndex = idx;
  setBalanceMode("single");
  const sel = document.getElementById("select-balance-objective");
  if (sel) sel.value = idx;
}

function renderActorProfileSvg(actorIdx) {
  const actor = state.actors[actorIdx];
  if (!actor || !state.objectives) return "";

  const M = state.objectives.length;
  const width = 820;
  const height = Math.max(480, 120 + (M * 42));
  const cX = 410;
  const startY = 90;
  const barH = 22;
  const rowH = 40;
  const maxBarW = 280;

  let barsSvg = "";

  for (let j = 0; j < M; j++) {
    const obj = state.objectives[j];
    const rawVal = (state.mao2 && state.mao2[actorIdx]) ? state.mao2[actorIdx][j] : 0;
    const y = startY + (j * rowH);

    // Grid row background
    barsSvg += `<line x1="80" y1="${y + rowH / 2}" x2="740" y2="${y + rowH / 2}" stroke="#f1f5f9" stroke-width="1" />`;

    // Objective Label on the left
    const objLabel = `${obj.id || `O${j + 1}`}: ${obj.short_name || obj.name}`;
    barsSvg += `<text x="70" y="${y + 15}" text-anchor="end" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="600" fill="#334155" title="${escapeXml(obj.name)}">${escapeXml(objLabel.substring(0, 32))}</text>`;

    if (rawVal > 0) {
      const w = (rawVal / 4) * maxBarW;
      barsSvg += `
        <rect x="${cX}" y="${y}" width="${w}" height="${barH}" rx="4" fill="#10b981" />
        <text x="${cX + w + 8}" y="${y + 15}" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="bold" fill="#047857">+${rawVal}</text>
      `;
    } else if (rawVal < 0) {
      const w = (Math.abs(rawVal) / 4) * maxBarW;
      barsSvg += `
        <rect x="${cX - w}" y="${y}" width="${w}" height="${barH}" rx="4" fill="#ef4444" />
        <text x="${cX - w - 8}" y="${y + 15}" text-anchor="end" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="bold" fill="#b91c1c">${rawVal}</text>
      `;
    } else {
      barsSvg += `
        <circle cx="${cX}" cy="${y + barH / 2}" r="4" fill="#94a3b8" />
        <text x="${cX + 10}" y="${y + 15}" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#94a3b8">0 (Neutro)</text>
      `;
    }
  }

  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" class="w-full max-w-4xl select-none">
      <rect width="100%" height="100%" fill="#ffffff" rx="12" stroke="#e2e8f0" stroke-width="1.5" />
      
      <text x="${cX}" y="32" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="15" font-weight="bold" fill="#1e293b">
        Perfil de Compromiso Estratégico del Actor (Escala -4 a +4)
      </text>
      <text x="${cX}" y="52" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="13" font-weight="bold" fill="#4338ca" text-decoration="underline">
        Actor : ${escapeXml(actor.name)} (${actor.id})
      </text>

      <!-- Center Zero Axis -->
      <line x1="${cX}" y1="75" x2="${cX}" y2="${height - 35}" stroke="#cbd5e1" stroke-width="2" />
      <text x="${cX}" y="${height - 18}" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" fill="#64748b">0 (Neutro)</text>

      <!-- Opposed Legend -->
      <text x="${cX - maxBarW}" y="75" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" fill="#ef4444">◀ Oposición (-4 a -1)</text>

      <!-- Favorable Legend -->
      <text x="${cX + maxBarW}" y="75" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="11" font-weight="bold" fill="#10b981">Apoyo / Favorable (+1 a +4) ▶</text>

      <!-- Bars -->
      ${barsSvg}

      <!-- Watermark -->
      <text x="${width - 15}" y="${height - 12}" text-anchor="end" font-family="monospace" font-size="9.5" font-weight="bold" fill="#94a3b8">
        @LIPSOR-EPITA-MACTOR
      </text>
    </svg>
  `;
}

function exportBalanceScaleSvg() {
  const container = document.getElementById("balance-svg-container");
  if (!container) return;
  const svg = container.querySelector("svg");
  if (!svg) {
    alert("No hay figura de balanza para exportar en este momento.");
    return;
  }
  const svgData = new XMLSerializer().serializeToString(svg);
  const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const downloadLink = document.createElement("a");
  const objName = (state.objectives && state.objectives[state.balanceScale.objIndex]) ? (state.objectives[state.balanceScale.objIndex].id || "OBJ") : "objetivo";
  downloadLink.href = url;
  downloadLink.download = `MACTOR_Balanza_Posicion_${objName}.svg`;
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
  URL.revokeObjectURL(url);
}

// Render 3CAA (Alliances) and 3DAA (Conflicts) Tables
function renderAlliancesAndConflictsTables() {
  if (!state.results) return;
  const caaContainer = document.getElementById("caa3-table-container");
  const daaContainer = document.getElementById("daa3-table-container");
  const N = state.actors.length;
  const caa3 = state.results.caa3;
  const daa3 = state.results.daa3;
  const convSums = state.results.actor_convergence;

  // 3CAA
  let htmlC = `<table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden table-matrix">
    <thead class="bg-emerald-800 text-white font-bold">
      <tr>
        <th class="p-2 border border-emerald-700">Actores</th>
        ${state.actors.map(a => `<th class="p-2 border border-emerald-700">${a.id}</th>`).join("")}
        <th class="p-2 border border-emerald-700 bg-emerald-950">Convergencia Total</th>
      </tr>
    </thead>
    <tbody>`;
  for (let i = 0; i < N; i++) {
    htmlC += `<tr>
      <td class="p-2 font-bold bg-slate-50 border border-slate-200 text-left">${state.actors[i].id}</td>`;
    for (let j = 0; j < N; j++) {
      const v = caa3[i][j];
      const isWinner = convSums[i] === Math.max(...convSums);
      htmlC += `<td class="p-2 border border-slate-200 ${i === j ? 'bg-slate-100 text-slate-300' : (v > 10 ? 'bg-emerald-100 font-bold text-emerald-900' : '')}">${i === j ? '-' : v.toFixed(1)}</td>`;
    }
    htmlC += `<td class="p-2 font-bold bg-emerald-50 text-emerald-900 border border-slate-200">${convSums[i].toFixed(1)}</td>
    </tr>`;
  }
  htmlC += `</tbody></table>`;
  caaContainer.innerHTML = htmlC;

  // 3DAA
  let htmlD = `<table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden table-matrix">
    <thead class="bg-rose-800 text-white font-bold">
      <tr>
        <th class="p-2 border border-rose-700">Actores</th>
        ${state.actors.map(a => `<th class="p-2 border border-rose-700">${a.id}</th>`).join("")}
      </tr>
    </thead>
    <tbody>`;
  for (let i = 0; i < N; i++) {
    htmlD += `<tr>
      <td class="p-2 font-bold bg-slate-50 border border-slate-200 text-left">${state.actors[i].id}</td>`;
    for (let j = 0; j < N; j++) {
      const v = daa3[i][j];
      htmlD += `<td class="p-2 border border-slate-200 ${i === j ? 'bg-slate-100 text-slate-300' : (v > 5 ? 'bg-rose-100 font-bold text-rose-900' : '')}">${i === j ? '-' : v.toFixed(1)}</td>`;
    }
    htmlD += `</tr>`;
  }
  htmlD += `</tbody></table>`;
  daaContainer.innerHTML = htmlD;
}

// Render Hierarchical Dendrogram (Árboles de Convergencia / Divergencia)
function renderDendrogram(mode = "convergence") {
  if (!state.results) return;
  const container = document.getElementById("dendrogram-svg-container");
  if (!container) return;

  const isConv = mode === "convergence";
  const treeData = isConv ? state.results.convergence_tree : state.results.divergence_tree;
  if (!treeData || !treeData.root) {
    container.innerHTML = `<div class="p-8 text-center text-slate-400 text-xs">No hay datos suficientes para trazar el árbol jerárquico.</div>`;
    return;
  }

  const root = treeData.root;
  const leaves = treeData.leaves;
  const maxDistance = treeData.max_distance > 0 ? treeData.max_distance : 1.0;

  document.getElementById("tree-root-distance-label").textContent = `Distancia Raíz: ${root.height.toFixed(1)} / Máx: ${maxDistance}`;

  // Dimension setup
  const leafCount = leaves.length;
  const rowHeight = 65;
  const width = Math.max(680, container.clientWidth || 700);
  const height = Math.max(380, leafCount * rowHeight + 80);
  const leftMargin = 60;
  const rightMargin = 220; // Room for actor labels
  const treeWidth = width - leftMargin - rightMargin;

  // Map leaf positions (y-axis)
  const leafYMap = {};
  leaves.forEach((leaf, idx) => {
    leafYMap[leaf.id] = 50 + idx * rowHeight;
  });

  // Calculate (x, y) for all tree nodes
  // In dendrograms: leaf height = 0 (rightmost), root height = max (leftmost)
  function computeCoordinates(node) {
    if (!node) return;
    if (node.is_leaf) {
      node.y = leafYMap[node.id];
      node.x = leftMargin + treeWidth; // right boundary of tree
      return;
    }
    computeCoordinates(node.left);
    computeCoordinates(node.right);
    node.y = (node.left.y + node.right.y) / 2;
    // Map height to x coordinate: 0 distance = rightmost, max distance = leftMargin
    const distRatio = Math.min(1.0, Math.max(0.0, node.height / maxDistance));
    node.x = leftMargin + treeWidth * (1.0 - distRatio);
  }
  computeCoordinates(root);

  // SVG Elements Generation
  let pathsHtml = "";
  let nodesHtml = "";
  const lineColor = isConv ? "#059669" : "#e11d48";
  const accentFill = isConv ? "#10b981" : "#f43f5e";

  function drawBranch(parent) {
    if (!parent || parent.is_leaf) return;

    const left = parent.left;
    const right = parent.right;

    // Orthogonal connection:
    // Vertical line between left.y and right.y at parent.x
    // Horizontal lines from parent.x to left.x at left.y, and to right.x at right.y
    pathsHtml += `
      <!-- Vertical backbone -->
      <line x1="${parent.x}" y1="${left.y}" x2="${parent.x}" y2="${right.y}" stroke="${lineColor}" stroke-width="2.5" stroke-linecap="round" />
      <!-- Horizontal to left child -->
      <line x1="${parent.x}" y1="${left.y}" x2="${left.x}" y2="${left.y}" stroke="${lineColor}" stroke-width="2.5" stroke-linecap="round" />
      <!-- Horizontal to right child -->
      <line x1="${parent.x}" y1="${right.y}" x2="${right.x}" y2="${right.y}" stroke="${lineColor}" stroke-width="2.5" stroke-linecap="round" />
      
      <!-- Merge junction point -->
      <circle cx="${parent.x}" cy="${parent.y}" r="4.5" fill="#1e293b" stroke="#ffffff" stroke-width="1.5" />
      <!-- Height distance badge -->
      <rect x="${parent.x - 22}" y="${parent.y - 18}" width="44" height="15" rx="4" fill="#ffffff" stroke="${lineColor}" stroke-width="1" />
      <text x="${parent.x}" y="${parent.y - 7}" font-family="Segoe UI, sans-serif" font-size="9" font-weight="bold" fill="${lineColor}" text-anchor="middle">d=${parent.height.toFixed(1)}</text>
    `;

    drawBranch(left);
    drawBranch(right);
  }
  drawBranch(root);

  // Draw Leaf Nodes & Actor Cards on the right
  leaves.forEach(leaf => {
    const actIdx = state.actors.findIndex(a => a.id === leaf.label || a.short_name === leaf.label || a.name === leaf.full_name);
    const act = actIdx >= 0 ? state.actors[actIdx] : { id: leaf.label, name: leaf.full_name };
    const qColor = (state.results && state.results.quadrants && state.results.quadrants[actIdx]) ? state.results.quadrants[actIdx].color : "#2563eb";
    const yPos = leafYMap[leaf.id];
    const xPos = leftMargin + treeWidth;

    nodesHtml += `
      <!-- Leaf connector dot -->
      <circle cx="${xPos}" cy="${yPos}" r="5" fill="${accentFill}" stroke="#ffffff" stroke-width="2" />
      <!-- Dashed connector to label -->
      <line x1="${xPos}" y1="${yPos}" x2="${xPos + 20}" y2="${yPos}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3" />
      <!-- Actor Box -->
      <g transform="translate(${xPos + 22}, ${yPos - 16})" class="cursor-pointer" onclick="openActorDetailsModal(${actIdx})">
        <rect width="180" height="32" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.2" />
        <rect width="6" height="32" rx="2" fill="${qColor}" />
        <text x="14" y="14" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold" fill="#0f172a">${act.id || 'A'} - ${act.short_name || act.name}</text>
        <text x="14" y="26" font-family="Segoe UI, sans-serif" font-size="9" fill="#64748b">${act.category || 'Actor Estratégico'}</text>
      </g>
    `;
  });

  // Scale axis at bottom
  let axisHtml = `
    <g transform="translate(${leftMargin}, ${height - 25})">
      <line x1="0" y1="0" x2="${treeWidth}" y2="0" stroke="#94a3b8" stroke-width="1.5" />
      <text x="0" y="15" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#475569">Mayor Distancia (d=${maxDistance})</text>
      <text x="${treeWidth}" y="15" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#475569" text-anchor="end">Identidad / Cero Distancia (d=0)</text>
    </g>
  `;

  // Render SVG
  container.innerHTML = `
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" class="w-full h-auto select-none">
      ${pathsHtml}
      ${nodesHtml}
      ${axisHtml}
    </svg>
  `;

  // Populate Coalitional Blocs Breakdown
  renderCoalitionsList(root, isConv);
}

// Render Coalitions list from tree clusters
function renderCoalitionsList(root, isConv) {
  const container = document.getElementById("tree-coalitions-container");
  if (!container || !root) return;

  const clusters = [];
  function collectInternalNodes(n) {
    if (!n || n.is_leaf) return;
    clusters.push(n);
    collectInternalNodes(n.left);
    collectInternalNodes(n.right);
  }
  collectInternalNodes(root);

  // Sort by merge distance ascending (earliest alliances first)
  clusters.sort((a, b) => a.height - b.height);

  container.innerHTML = clusters.map((c, i) => {
    const names = c.elements.map(e => state.actors[e] ? (state.actors[e].id || state.actors[e].name) : `A${e + 1}`).join(" + ");
    return `
      <div class="p-2.5 bg-white border border-slate-200 rounded-lg shadow-2xs hover:border-emerald-300 transition-all">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-slate-800">Bloque ${i + 1}: <span class="${isConv ? 'text-emerald-700' : 'text-rose-700'}">${names}</span></span>
          <span class="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">d = ${c.height.toFixed(1)}</span>
        </div>
        <p class="text-[10px] text-slate-500 mt-1">
          ${isConv ? 'Agrupación por convergencia positiva en objetivos clave.' : 'Agrupación por conflicto u oposición a objetivos comunes.'}
        </p>
      </div>
    `;
  }).join("");
}
function renderQuadrantChart() {
  if (!state.results) return;
  const ctx = document.getElementById("quadrant-chart");
  if (!ctx) return;

  const quads = state.results.quadrants;
  const infValues = quads.map(q => q.influence);
  const depValues = quads.map(q => q.dependence);

  const meanInf = infValues.reduce((a, b) => a + b, 0) / (infValues.length || 1);
  const meanDep = depValues.reduce((a, b) => a + b, 0) / (depValues.length || 1);

  const dataPoints = quads.map(q => ({
    x: q.dependence,
    y: q.influence,
    label: `${q.id}: ${q.name}`,
    quadrant: q.quadrant
  }));

  if (state.quadrantChart) {
    state.quadrantChart.destroy();
  }

  state.quadrantChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Actores',
        data: dataPoints,
        backgroundColor: '#2563eb',
        borderColor: '#1d4ed8',
        pointRadius: 8,
        pointHoverRadius: 11
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1,
      layout: {
        padding: 10
      },
      scales: {
        x: {
          title: { display: true, text: 'Dependencia Directa (D_i)', font: { weight: 'bold', size: 11 } },
          grid: { color: '#e2e8f0' }
        },
        y: {
          title: { display: true, text: 'Influencia Directa (I_i)', font: { weight: 'bold', size: 11 } },
          grid: { color: '#e2e8f0' }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              const p = context.raw;
              return [`${p.label}`, `Influencia: ${p.y}, Dependencia: ${p.x}`, `Cuadrante: ${p.quadrant}`];
            }
          }
        },
        legend: { display: false }
      }
    }
  });

  // Renderizar también las métricas de red y centralización
  renderNetworkCentralityMetrics();
}

// Renderizar Métricas de Centralidad de Red (SNA sobre MID)
function renderNetworkCentralityMetrics() {
  if (!state.results || !state.results.network_metrics) return;
  const net = state.results.network_metrics;
  const actors = state.actors || [];

  // Tarjetas Macro
  const elOut = document.getElementById("net-centralization-out");
  const elIn = document.getElementById("net-centralization-in");
  const elDensity = document.getElementById("net-density");
  const elMean = document.getElementById("net-mean-intensity");

  if (elOut) elOut.textContent = `${(net.centralization_out * 100).toFixed(1)}%`;
  if (elIn) elIn.textContent = `${(net.centralization_in * 100).toFixed(1)}%`;
  if (elDensity) elDensity.textContent = `${(net.density * 100).toFixed(1)}%`;
  if (elMean) elMean.textContent = `${net.mean_intensity.toFixed(2)}`;

  // Tabla por Actor
  const tbody = document.getElementById("network-centrality-tbody");
  if (!tbody) return;

  const rowsHtml = actors.map((act, i) => {
    const cOut = net.out_centrality[i] || 0;
    const cIn = net.in_centrality[i] || 0;

    let role = "Intermediario";
    let roleBadge = "bg-slate-100 text-slate-700";
    if (cOut >= 0.35 && cIn <= 0.2) {
      role = "Emisor Dominante (Líder)";
      roleBadge = "bg-indigo-100 text-indigo-800 font-bold";
    } else if (cOut >= 0.3 && cIn >= 0.25) {
      role = "Nodo de Alta Tensión / Puente";
      roleBadge = "bg-amber-100 text-amber-800 font-bold";
    } else if (cOut < 0.2 && cIn >= 0.25) {
      role = "Receptor Dependiente";
      roleBadge = "bg-rose-100 text-rose-800 font-bold";
    } else if (cOut < 0.15 && cIn < 0.15) {
      role = "Actor Periférico";
      roleBadge = "bg-slate-100 text-slate-500";
    }

    return `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="p-2.5 font-semibold text-slate-800">
          <span class="font-mono text-indigo-600 mr-1">${act.id || 'A' + (i + 1)}</span>
          ${act.short_name || act.name}
        </td>
        <td class="p-2.5 text-center font-mono font-bold text-indigo-700">
          ${(cOut * 100).toFixed(1)}%
        </td>
        <td class="p-2.5 text-center">
          <div class="w-24 bg-slate-200 h-2 rounded-full mx-auto overflow-hidden">
            <div class="bg-indigo-600 h-2 rounded-full" style="width: ${Math.min(100, cOut * 100 * 2)}%"></div>
          </div>
        </td>
        <td class="p-2.5 text-center font-mono font-bold text-blue-700">
          ${(cIn * 100).toFixed(1)}%
        </td>
        <td class="p-2.5 text-center">
          <div class="w-24 bg-slate-200 h-2 rounded-full mx-auto overflow-hidden">
            <div class="bg-blue-600 h-2 rounded-full" style="width: ${Math.min(100, cIn * 100 * 2)}%"></div>
          </div>
        </td>
        <td class="p-2.5 text-center">
          <span class="px-2 py-0.5 rounded-full text-[10px] ${roleBadge}">${role}</span>
        </td>
      </tr>
    `;
  }).join("");

  tbody.innerHTML = rowsHtml;
}

// Vis.js: Interactive Network Graph
function renderAllianceNetwork() {
  if (!state.results) return;
  const container = document.getElementById("network-graph-container");
  if (!container) return;

  const threshold = parseFloat(document.getElementById("network-filter-threshold").value) || 0;
  const N = state.actors.length;
  const caa3 = state.results.caa3;
  const daa3 = state.results.daa3;
  const r_i = state.results.force_metrics.r_i;
  const quads = state.results.quadrants;

  const nodes = [];
  const edges = [];

  for (let i = 0; i < N; i++) {
    const act = state.actors[i];
    const q = quads[i];
    nodes.push({
      id: i,
      label: act.short_name || act.name,
      title: `${act.name}<br>Fuerza r_i: ${r_i[i].toFixed(2)}<br>Cuadrante: ${q.quadrant}`,
      value: Math.max(10, r_i[i] * 12),
      color: {
        background: q.color || '#3b82f6',
        border: '#1e293b',
        highlight: { background: '#f59e0b', border: '#b45309' }
      },
      font: { color: '#1e293b', size: 12, face: 'Segoe UI', bold: true }
    });
  }

  // Edges
  for (let i = 0; i < N; i++) {
    for (let j = i + 1; j < N; j++) {
      const conv = caa3[i][j];
      const div = daa3[i][j];

      if (conv >= threshold && conv > 0) {
        edges.push({
          from: i,
          to: j,
          value: Math.max(1, conv * 0.35),
          color: { color: '#10b981', highlight: '#059669' },
          title: `Alianza (3CAA): ${conv.toFixed(1)}`,
          smooth: { type: 'continuous' }
        });
      }

      if (div >= threshold && div > 0) {
        edges.push({
          from: i,
          to: j,
          value: Math.max(1, div * 0.4),
          color: { color: '#ef4444', highlight: '#dc2626' },
          dashes: true,
          title: `Conflicto (3DAA): ${div.toFixed(1)}`,
          smooth: { type: 'continuous' }
        });
      }
    }
  }

  const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
  const options = {
    nodes: { shape: 'dot', scaling: { min: 14, max: 32 } },
    edges: { scaling: { min: 1, max: 7 }, smooth: true },
    physics: {
      solver: 'forceAtlas2Based',
      forceAtlas2Based: { gravitationalConstant: -50, centralGravity: 0.01, springLength: 100 }
    },
    interaction: { hover: true, tooltipDelay: 100 }
  };

  if (state.networkInstance) {
    state.networkInstance.destroy();
  }
  state.networkInstance = new vis.Network(container, data, options);
}

// Chart.js: Objectives Mobilization & Consensus Chart
function renderMobilizationChart() {
  if (!state.results || !state.results.objective_metrics) return;
  const ctx = document.getElementById("mobilization-chart");
  if (!ctx) return;

  const metrics = state.results.objective_metrics;
  const labels = metrics.map(m => m.id);
  const mobData = metrics.map(m => m.mobilization);
  const balData = metrics.map(m => m.net_balance);

  if (state.mobilizationChart) {
    state.mobilizationChart.destroy();
  }

  state.mobilizationChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Movilización Total (|3MAO|)',
          data: mobData,
          backgroundColor: '#0284c7',
          borderRadius: 4
        },
        {
          label: 'Balance Neto de Postura',
          data: balData,
          backgroundColor: balData.map(v => v >= 0 ? '#10b981' : '#f43f5e'),
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { grid: { color: '#e2e8f0' } }
      },
      plugins: {
        legend: { position: 'top', labels: { font: { size: 11 } } },
        tooltip: {
          callbacks: {
            afterLabel: function (ctx) {
              const m = metrics[ctx.dataIndex];
              return `Diagnóstico: ${m.status}\nA Favor: ${m.favorable_actors} | En Contra: ${m.opposed_actors}`;
            }
          }
        }
      }
    }
  });
}

// Render Diagnostic Cards for Objectives
function renderObjectivesDiagnostic() {
  const container = document.getElementById("objectives-diagnostic-container");
  if (!state.results || !state.results.objective_metrics) return;

  const metrics = state.results.objective_metrics;
  container.innerHTML = metrics.map(m => {
    const isConflict = m.conflict_index > 0.5;
    const badgeBg = isConflict ? "bg-rose-100 text-rose-800" : "bg-emerald-100 text-emerald-800";
    return `
      <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5 hover:border-blue-300 transition-all">
        <div class="flex items-center justify-between">
          <span class="font-bold text-xs text-slate-800">${m.id} - ${m.name}</span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded ${badgeBg}">${m.status}</span>
        </div>
        <div class="flex items-center space-x-4 text-[11px] text-slate-500">
          <span>Ponderación: <b class="text-slate-700">${(m.weight * 100).toFixed(0)}%</b></span>
          <span>Movilización: <b class="text-slate-700">${m.mobilization}</b></span>
          <span>Balance: <b class="${m.net_balance >= 0 ? 'text-emerald-600' : 'text-rose-600'}">${m.net_balance > 0 ? '+' + m.net_balance : m.net_balance}</b></span>
          <span>Índice Conflicto: <b class="text-slate-700">${m.conflict_index}</b></span>
        </div>
      </div>
    `;
  }).join("");
}

// Coalitions table
function renderCoalitionsTable() {
  const container = document.getElementById("coalitions-table-container");
  if (!state.results || !state.results.coalitions) return;

  const coalitions = state.results.coalitions;
  let html = `<table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden">
    <thead class="bg-slate-800 text-white font-bold">
      <tr>
        <th class="p-2 text-left">Pares de Actores</th>
        <th class="p-2 text-center">Convergencia (3CAA)</th>
        <th class="p-2 text-center">Divergencia (3DAA)</th>
        <th class="p-2 text-center">Afinidad Neta</th>
        <th class="p-2 text-center">Estabilidad de Coalición</th>
      </tr>
    </thead>
    <tbody>`;

  coalitions.slice(0, 8).forEach(c => {
    const isStable = c.stability === "Muy Estable" || c.stability === "Alianza Táctica";
    html += `<tr class="border-b border-slate-200 hover:bg-slate-50">
      <td class="p-2 font-medium text-slate-800">${c.actor1} <i class="fa-solid fa-arrows-left-right text-[10px] text-slate-400 mx-1"></i> ${c.actor2}</td>
      <td class="p-2 text-center text-emerald-700 font-bold">${c.convergence}</td>
      <td class="p-2 text-center text-rose-700 font-bold">${c.divergence}</td>
      <td class="p-2 text-center font-bold ${c.net_affinity >= 0 ? 'text-blue-700' : 'text-rose-700'}">${c.net_affinity > 0 ? '+' + c.net_affinity : c.net_affinity}</td>
      <td class="p-2 text-center">
        <span class="text-[10px] font-bold px-2 py-0.5 rounded ${isStable ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">${c.stability}</span>
      </td>
    </tr>`;
  });

  html += `</tbody></table>`;
  container.innerHTML = html;
}

// Populate simulation dropdowns
function populateSimulationDropdowns() {
  const actorSel = document.getElementById("sim-actor-select");
  const objSel = document.getElementById("sim-objective-select");

  if (actorSel) {
    actorSel.innerHTML = state.actors.map((a, i) => `<option value="${i}">${a.id || 'A' + (i + 1)} - ${a.name}</option>`).join("");
  }
  if (objSel) {
    objSel.innerHTML = state.objectives.map((o, j) => `<option value="${j}">${o.id || 'O' + (j + 1)} - ${o.name}</option>`).join("");
  }
}

// Run Scenario Simulation
async function runScenarioSimulation() {
  readMatricesFromDOM();
  const actorIdx = parseInt(document.getElementById("sim-actor-select").value, 10);
  const objIdx = parseInt(document.getElementById("sim-objective-select").value, 10);
  const newPosture = parseFloat(document.getElementById("sim-new-posture").value);

  // Clone 2MAO
  const simMao2 = JSON.parse(JSON.stringify(state.mao2));
  simMao2[actorIdx][objIdx] = newPosture;

  const payload = {
    base_data: {
      actors: state.actors,
      objectives: state.objectives,
      mid: state.mid,
      mao2: state.mao2,
      variant: state.variant
    },
    modifications: {
      mao2: simMao2
    }
  };

  try {
    const resp = await fetch("/api/mactor/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) throw new Error("Error en la simulación");
    const data = await resp.json();

    renderSimulationResults(data, actorIdx, objIdx, newPosture);

  } catch (err) {
    console.error("Simulation error:", err);
    alert("Error ejecutando la simulación: " + err.message);
  }
}

// Render Simulation Delta Results
function renderSimulationResults(data, actorIdx, objIdx, newPosture) {
  const container = document.getElementById("sim-delta-results");
  const baseWinner = data.base_dominant;
  const simWinner = data.sim_dominant;
  const deltas = data.convergence_delta;
  const targetActor = state.actors[actorIdx];
  const targetObj = state.objectives[objIdx];

  const winnerChanged = baseWinner.name !== simWinner.name;

  container.innerHTML = `
    <div class="p-4 ${winnerChanged ? 'bg-amber-50 border-amber-300' : 'bg-blue-50 border-blue-200'} border rounded-xl space-y-3">
      <div class="flex items-center justify-between">
        <span class="font-bold text-xs uppercase tracking-wider text-slate-700">Resultado del Escenario Proyectado</span>
        <span class="text-[10px] font-bold px-2 py-0.5 rounded ${winnerChanged ? 'bg-amber-200 text-amber-900' : 'bg-blue-200 text-blue-900'}">
          ${winnerChanged ? '⚠️ Cambio en Actor Ganador' : 'Consistencia Estratégica'}
        </span>
      </div>

      <p class="text-xs text-slate-600">
        Se modificó la postura de <b>${targetActor.name}</b> ante el objetivo <b>${targetObj.name}</b> a una intensidad de <b>${newPosture > 0 ? '+' + newPosture : newPosture}</b>.
      </p>

      <div class="grid grid-cols-2 gap-3 text-xs pt-2 border-t border-slate-200">
        <div>
          <span class="text-[10px] text-slate-400 block font-semibold uppercase">Escenario Base</span>
          <span class="font-bold text-slate-800">${baseWinner.name} (${baseWinner.convergence_score})</span>
        </div>
        <div>
          <span class="text-[10px] text-slate-400 block font-semibold uppercase">Escenario Simulado</span>
          <span class="font-bold ${winnerChanged ? 'text-amber-700' : 'text-blue-700'}">${simWinner.name} (${simWinner.convergence_score})</span>
        </div>
      </div>

      <div class="pt-2">
        <span class="text-[10px] text-slate-500 font-bold block mb-1">Deltas de Convergencia por Actor:</span>
        <div class="flex flex-wrap gap-2 text-[11px]">
          ${state.actors.map((a, i) => {
    const d = deltas[i];
    const bg = d > 0 ? 'bg-emerald-100 text-emerald-800' : (d < 0 ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-600');
    return `<span class="px-2 py-0.5 rounded font-semibold ${bg}">${a.id}: ${d > 0 ? '+' + d : d}</span>`;
  }).join("")}
        </div>
      </div>
    </div>
  `;
}

// Render Executive Report View
function renderExecutiveReport() {
  const container = document.getElementById("executive-report-content");
  if (!state.results) return;

  const res = state.results;
  const dom = res.dominant_actor;

  container.innerHTML = `
    <!-- Summary Section -->
    <div class="space-y-4">
      <div class="p-4 bg-blue-50 border-l-4 border-blue-600 rounded-r-lg">
        <h4 class="font-bold text-sm text-blue-900">Conclusión Prospectiva Clave</h4>
        <p class="text-xs text-blue-800 mt-1 leading-relaxed">
          De acuerdo con el modelo MACTOR (LIPSOR / Godet) aplicado sobre el territorio <b>"${state.territory}"</b> bajo la variante <b>"${res.variant.toUpperCase()}"</b>, el actor con mayor capacidad de convocatoria y alineación estratégica es:
        </p>
        <div class="mt-3 flex items-center space-x-3">
          <div class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-lg">
            ${res.actors[dom.index].id || '👑'}
          </div>
          <div>
            <h5 class="font-bold text-sm text-slate-900">${dom.name}</h5>
            <span class="text-xs text-emerald-700 font-semibold">Puntaje de Convergencia Ponderada: ${dom.convergence_score} | Relación de Fuerza r_i: ${dom.r_i}</span>
          </div>
        </div>
      </div>

      <!-- Quadrants Breakdown Table -->
      <div>
        <h4 class="font-bold text-sm text-slate-900 mb-2">1. Diagnóstico de Posicionamiento de Actores (Godet)</h4>
        <table class="w-full text-xs border border-slate-200 rounded-lg overflow-hidden">
          <thead class="bg-slate-800 text-white">
            <tr>
              <th class="p-2 text-left">Actor</th>
              <th class="p-2 text-center">Influencia (I_i)</th>
              <th class="p-2 text-center">Dependencia (D_i)</th>
              <th class="p-2 text-center">Relación Fuerza (r_i)</th>
              <th class="p-2 text-left">Cuadrante Estratégico</th>
            </tr>
          </thead>
          <tbody>
            ${res.quadrants.map(q => `
              <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-2 font-bold text-slate-800">${q.id} - ${q.name}</td>
                <td class="p-2 text-center">${q.influence}</td>
                <td class="p-2 text-center">${q.dependence}</td>
                <td class="p-2 text-center font-bold text-blue-700">${res.force_metrics.r_i[q.index].toFixed(2)}</td>
                <td class="p-2 font-semibold" style="color: ${q.color}">${q.quadrant}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>

      <!-- Objectives Viability -->
      <div>
        <h4 class="font-bold text-sm text-slate-900 mb-2">2. Priorización y Focos de Conflicto en Objetivos Territoriales</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          ${res.objective_metrics.map(om => `
            <div class="p-3 border border-slate-200 rounded-lg bg-slate-50">
              <div class="flex items-center justify-between font-bold">
                <span class="text-slate-800">${om.id} - ${om.name}</span>
                <span class="text-[10px] px-2 py-0.5 rounded ${om.conflict_index > 0.5 ? 'bg-rose-100 text-rose-800' : 'bg-emerald-100 text-emerald-800'}">${om.status}</span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1">Movilización: <b>${om.mobilization}</b> | Balance: <b>${om.net_balance}</b> | Índice Disputa: <b>${om.conflict_index}</b></p>
            </div>
          `).join("")}
        </div>
      </div>

      <!-- 3. Canonical Position Scale (Balanza de Posición) -->
      <div>
        <h4 class="font-bold text-sm text-slate-900 mb-2">3. Balanza Canónica LIPSOR MACTOR del Objetivo Prioritario</h4>
        <p class="text-xs text-slate-500 mb-2">Inclinación de la balanza de actores a favor (+) vs oposición (-) ponderada por la relación de fuerza r_i y competitividad valorada.</p>
        <div class="border border-slate-200 rounded-xl p-3 bg-white flex justify-center overflow-x-auto shadow-2xs">
          ${generateSingleBalanceSvg(state.balanceScale.objIndex || 0, true, 800, 500, false)}
        </div>
        
        <!-- Quick Guidance Card under Report Balance -->
        <div class="mt-3 p-3.5 bg-indigo-50/70 border border-indigo-200 rounded-xl space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-indigo-950 flex items-center space-x-1.5">
              <i class="fa-solid fa-graduation-cap text-indigo-600"></i>
              <span>¿Cómo interpretar este pulso de fuerzas?</span>
            </span>
            <button onclick="document.getElementById('modal-balance-guide').classList.remove('hidden')" class="text-[11px] text-indigo-700 hover:text-indigo-900 font-semibold underline cursor-pointer">
              Ver Guía Metodológica Completa
            </button>
          </div>
          <p class="text-[11px] text-slate-700 leading-relaxed">
            Cada actor pesa en su respectivo platillo según su postura nominal ponderada por su fuerza relativa (<b>r_i × 2MAO</b>). 
            La inclinación visual no es una votación de mayoría simple, sino el resultado del equilibrio físico de poder.
            El platillo <b>verde</b> agrupa el respaldo favorable (viabilidad política), el <b>rojo</b> agrupa el rechazo y veto, y los actores fuera de la balanza son <b>neutros disputables</b>.
          </p>
        </div>
      </div>

      <!-- Methodological Reference -->
      <div class="p-4 bg-slate-100 rounded-lg text-xs text-slate-600 space-y-1">
        <span class="font-bold text-slate-800">Referencia Metodológica:</span>
        <p>Villabona, N., Oyola, P. S., & Franco, D. A. (2018). Aplicación de la técnica MACTOR para la selección del caballo ganador en una competencia de paso. <i>AGLALA</i>, 9(1), 309-318. DOI: 10.22519/22157360.1206.</p>
        <p>Godet, M., & Durance, P. (2007/2009). Prospectiva estratégica: problemas y métodos. Cuadernos de LIPSOR / Dunod.</p>
      </div>
    </div>
  `;
}

// Read matrices back from input elements in DOM
function readMatricesFromDOM() {
  const midInputs = document.querySelectorAll(".mid-cell");
  midInputs.forEach(input => {
    const r = parseInt(input.getAttribute("data-row"), 10);
    const c = parseInt(input.getAttribute("data-col"), 10);
    let val = parseInt(input.value, 10);
    if (!isNaN(r) && !isNaN(c) && !isNaN(val)) {
      state.mid[r][c] = val;
    }
  });
}

// Export to Microsoft Word (.docx)
async function exportWordDocx() {
  readMatricesFromDOM();
  const btn1 = document.getElementById("btn-export-docx");
  const btn2 = document.getElementById("btn-export-docx-2");
  const oldText1 = btn1 ? btn1.innerHTML : "";
  const oldText2 = btn2 ? btn2.innerHTML : "";

  if (btn1) {
    btn1.disabled = true;
    btn1.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span class="hidden md:inline">Generando Word...</span>`;
  }
  if (btn2) {
    btn2.disabled = true;
    btn2.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span>Generando Informe Word...</span>`;
  }

  try {
    const payload = {
      actors: state.actors,
      objectives: state.objectives,
      mid: state.mid,
      mao2: state.mao2,
      variant: state.variant || "softprosp",
      options: {
        territory: state.territory || "Territorio",
        country: state.country || "Colombia",
        sector: state.sector || "",
        case_id: state.activeCaseId || "",
        news_items: state.newsItems || []
      }
    };

    const resp = await fetch("/api/mactor/export/word", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      throw new Error(errData.detail || "Error al procesar la solicitud en el servidor");
    }

    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const terrClean = (state.territory || "Territorio").replace(/[^a-zA-Z0-9]/g, "_");
    a.download = `Informe_Prospectivo_MACTOR_${terrClean}.docx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

  } catch (err) {
    console.error("Export Word error:", err);
    alert("Error exportando a Word: " + err.message);
  } finally {
    if (btn1) {
      btn1.disabled = false;
      btn1.innerHTML = oldText1;
    }
    if (btn2) {
      btn2.disabled = false;
      btn2.innerHTML = oldText2;
    }
  }
}

// Export to Excel
async function exportExcel() {
  readMatricesFromDOM();
  try {
    const payload = {
      actors: state.actors,
      objectives: state.objectives,
      mid: state.mid,
      mao2: state.mao2,
      variant: state.variant,
      options: {
        territory: state.territory || "Territorio",
        country: state.country || "Colombia",
        sector: state.sector || "",
        case_id: state.activeCaseId || ""
      }
    };

    const resp = await fetch("/api/mactor/export/excel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) throw new Error("Error generando archivo Excel");

    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Estudio_Prospectivo_MACTOR_${(state.territory || 'Territorio').replace(/[^a-zA-Z0-9]/g, '_')}.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

  } catch (err) {
    console.error("Export error:", err);
    alert("Error exportando a Excel: " + err.message);
  }
}
