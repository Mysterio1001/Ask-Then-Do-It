import "./style.css";
import {
  createIcons,
  ArrowUpRight,
  ArrowRight,
  ArrowDown,
  ChevronDown,
  Check,
  Copy,
  Pause,
  Play,
  Github,
  Terminal,
  Plus,
} from "lucide";
import { createI18n } from "./lib/i18n.js";
import { product, journeyStops } from "./data/product.js";
import { scrollProgress, stageForProgress } from "./lib/journey.js";

const iconSet = {
  ArrowUpRight,
  ArrowRight,
  ArrowDown,
  ChevronDown,
  Check,
  Copy,
  Pause,
  Play,
  Github,
  Terminal,
  Plus,
};
const icon = (name, className = "") =>
  `<i data-lucide="${name}" class="${className}" aria-hidden="true"></i>`;
const text = (key, tag = "span", className = "") =>
  `<${tag} class="${className}" data-i18n="${key}"></${tag}>`;
const external = 'target="_blank" rel="noopener noreferrer"';

document.querySelector("#app").innerHTML = `
  <a class="skip-link" href="#aegis" data-i18n="common.skip"></a>
  <div class="universe" aria-hidden="true">
    <div class="space-fallback"></div>
    <canvas id="universe-canvas"></canvas>
    <div class="scene-shade"></div>
    <div class="scene-grain"></div>
  </div>
  <header class="site-header">
    <div class="brand" aria-label="Ask-Then-Do-It"><img class="brand-mark" src="/logo.png" alt="" width="34" height="34"><span>ASK THEN DO IT<span class="brand-period">.</span></span></div>
    <div class="header-actions">
      <div class="language-switcher">
        <button id="language-toggle" class="language-toggle" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="language-menu" data-i18n-aria="nav.language"><span id="current-language">繁中</span>${icon("chevron-down")}</button>
        <div id="language-menu" class="language-menu" hidden>
          <button type="button" data-locale="zh-TW" lang="zh-TW">繁體中文<span>ZH</span></button>
          <button type="button" data-locale="en" lang="en">English<span>EN</span></button>
          <button type="button" data-locale="ja" lang="ja">日本語<span>JA</span></button>
        </div>
      </div>
      <span class="header-divider"></span>
      <a class="github-link" href="${product.repository}" ${external} aria-label="GitHub">${icon("github")}<span>GitHub</span>${icon("arrow-up-right", "github-arrow")}</a>
    </div>
  </header>

  <main class="mission-viewport" id="mission-content">
    <div class="mission-id mono"><span class="status-dot"></span><span>ATDI / EXPLORATION PROGRAM</span><span class="mission-id-separator">/</span><span class="muted">MISSION 001</span></div>
    <div class="top-coordinates mono"><span>SYS. ONLINE</span><span id="coordinates">X 000.00 &nbsp; Y 000.00</span></div>

    <section class="story-panel hero-panel is-active" data-stage="0" aria-labelledby="hero-title">
      <div class="eyebrow mono"><span class="orbit-number">00</span><span data-i18n="hero.eyebrow"></span><span class="eyebrow-line"></span></div>
      <h1 id="hero-title"><span data-i18n="hero.line1"></span><span class="accent-text" data-i18n="hero.line2"></span></h1>
      ${text("stages.0.title", "p", "hero-statement")}
      ${text("hero.description", "p", "story-description")}
      <div class="hero-actions"><a class="button button-primary" href="#aeris">${text("hero.begin")}${icon("arrow-right")}</a><a class="button button-text" href="#aegis">${icon("terminal")}${text("hero.install")}${icon("arrow-up-right")}</a></div>
    </section>

    ${journeyStops
      .slice(1, 4)
      .map(
        (stop, index) => `
      <section class="story-panel orbit-panel" data-stage="${index + 1}" aria-labelledby="title-${stop.id}" hidden>
        <div class="eyebrow mono"><span class="orbit-number">${stop.number}</span>${text(`stages.${index + 1}.tag`)}<span class="eyebrow-line"></span></div>
        <p class="planet-name mono">${stop.name}<span>/</span>ORBIT ${stop.number}</p>
        <h2 id="title-${stop.id}" data-i18n="stages.${index + 1}.title"></h2>
        ${text(`stages.${index + 1}.desc`, "p", "story-description")}
        <ul class="principles">${[1, 2, 3].map((n) => `<li>${icon("check")}${text(`stages.${index + 1}.feature${n}`)}</li>`).join("")}</ul>
        <a class="button button-text stage-next" href="#${journeyStops[index + 2].id}">${text("common.next")}${icon("arrow-right")}</a>
      </section>`,
      )
      .join("")}

    <section class="story-panel terminal-panel" data-stage="4" aria-labelledby="terminal-title" hidden>
      <div class="eyebrow mono"><span class="orbit-number">04</span>${text("terminal.eyebrow")}<span class="eyebrow-line"></span></div>
      <p class="planet-name mono">AEGIS STATION<span>/</span>TERMINAL</p>
      <h2 id="terminal-title" data-i18n="terminal.title"></h2>
      ${text("terminal.desc", "p", "story-description")}
      <div class="install-terminal">
        <div class="terminal-heading"><span class="terminal-lights"><i></i><i></i><i></i></span>${text("terminal.terminalTitle", "span", "mono")}<span class="terminal-shell mono">zsh</span></div>
        <div class="install-tabs" role="tablist" aria-label="Installation platform">
          ${["codex", "claude", "clone"].map((mode, i) => `<button type="button" id="tab-${mode}" role="tab" aria-controls="command-panel" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}" data-install-mode="${mode}" data-i18n="terminal.${mode}"></button>`).join("")}
        </div>
        <div id="command-panel" class="command-panel" role="tabpanel" aria-labelledby="tab-codex"><span class="command-prompt mono">$</span><pre><code id="install-command"></code></pre><button type="button" id="copy-command" class="icon-button" data-i18n-aria="terminal.copy">${icon("copy")}<span class="tooltip" data-i18n="terminal.copy"></span></button></div>
        <div id="copy-status" class="copy-status mono" role="status" aria-live="polite"></div>
      </div>
      <div class="terminal-actions"><a class="button button-primary" href="${product.repository}" ${external}>${icon("github")}${text("terminal.repository")}${icon("arrow-up-right")}</a><a id="docs-link" class="button button-text" href="${product.docs["zh-TW"]}" ${external}>${text("terminal.viewDocs")}${icon("arrow-up-right")}</a></div>
      ${text("terminal.footer", "p", "terminal-footnote mono")}
    </section>

    <aside class="planet-annotation" aria-hidden="true"><span class="annotation-cross">+</span><span class="annotation-line"></span><div><span id="planet-label" class="mono"></span><span id="planet-type"></span></div></aside>
    <div class="planet-telemetry mono" aria-hidden="true"><div><span class="telemetry-label">SECTOR</span><span id="sector-number">00 / 04</span></div><div><span class="telemetry-label">SIGNAL</span><span id="signal-value"></span><span class="signal-bars"><i></i><i></i><i></i><i></i><i></i></span></div></div>
    <div class="scene-status" id="scene-status" role="status" data-i18n="common.loading"></div>
  </main>

  <div class="flight-deck">
    <div class="flight-deck-heading mono"><span class="flight-label"><span class="status-dot"></span>${text("journey.label")}</span><span class="scroll-cue">${icon("arrow-down")}${text("journey.scroll")}</span><div class="flight-controls"><span id="progress-value">00%</span><button id="pause-motion" class="icon-button" type="button" aria-pressed="false" data-i18n-aria="common.pause">${icon("pause")}<span class="tooltip" data-i18n="common.pause"></span></button></div></div>
    <nav class="journey-nav" aria-label="Orbits"><div class="route-line"><div id="route-progress"></div></div>${journeyStops.map((stop, i) => `<a href="#${stop.id}" class="journey-stop ${i === 0 ? "is-current" : ""}" data-stop="${i}" ${i === 0 ? 'aria-current="step"' : ""}><span class="route-dot"></span><span class="stop-heading mono"><span class="stop-number">${stop.number}</span><span>${stop.name}</span>${icon("arrow-up-right")}</span>${text(`stages.${i}.tag`, "span", "stop-subtitle")}</a>`).join("")}</nav>
    <footer class="site-footer mono">
      <span class="footer-developer">${text("footer.developer")}<strong>交給我科技工作室</strong><span>Handle by me Tech Studio 2026</span></span>
      <a class="footer-contact" href="mailto:contact@handlebyme.com">${text("footer.contact")}<span>contact@handlebyme.com</span></a>
    </footer>
  </div>
  <div class="scroll-track" aria-hidden="true">${journeyStops.map((stop) => `<div id="${stop.id}" class="scroll-stop"></div>`).join("")}</div>
`;

const renderIcons = () =>
  createIcons({ icons: iconSet, attrs: { "stroke-width": 1.6 } });
let stage = 0;
let installMode = "codex";
let universe;
let paused = false;
let copyTimer;
let copyOperation = 0;
let copyResult = "";
let pendingFocus = null;
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const panels = [...document.querySelectorAll("[data-stage]")];
const stops = [...document.querySelectorAll("[data-stop]")];

const i18n = createI18n({ onChange: updateLanguage });

function updateLanguage() {
  if (!document.querySelector("#current-language")) return;
  document.querySelector("#current-language").textContent = {
    "zh-TW": "繁中",
    en: "EN",
    ja: "日本語",
  }[i18n.locale];
  document
    .querySelectorAll("[data-locale]")
    .forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.locale === i18n.locale),
      ),
    );
  document.querySelector("#docs-link").href = product.docs[i18n.locale];
  updateAnnotations();
  updateMotionButton();
  if (copyResult)
    document.querySelector("#copy-status").textContent = i18n.t(
      `terminal.${copyResult}`,
    );
}

function updateAnnotations() {
  document.querySelector("#planet-label").textContent = i18n.t(
    `stages.${stage}.planetLabel`,
  );
  document.querySelector("#planet-type").textContent = i18n.t(
    `stages.${stage}.planetType`,
  );
  document.querySelector("#signal-value").textContent = i18n.t(
    `stages.${stage}.signal`,
  );
  document.querySelector("#sector-number").textContent =
    `${String(stage).padStart(2, "0")} / 04`;
}

function updateMotionButton() {
  const button = document.querySelector("#pause-motion");
  const key = paused ? "common.resume" : "common.pause";
  button.setAttribute("aria-pressed", String(paused));
  button.setAttribute("aria-label", i18n.t(key));
  button.innerHTML = `${icon(paused ? "play" : "pause")}<span class="tooltip">${i18n.t(key)}</span>`;
  renderIcons();
}

function updateStage(nextStage) {
  if (stage === nextStage) return;
  stage = nextStage;
  panels.forEach((panel, index) => {
    panel.hidden = index !== stage;
    panel.classList.toggle("is-active", index === stage);
  });
  stops.forEach((stop, index) => {
    stop.classList.toggle("is-current", index === stage);
    stop.classList.toggle("is-past", index < stage);
    if (index === stage) stop.setAttribute("aria-current", "step");
    else stop.removeAttribute("aria-current");
  });
  document.body.dataset.stage = String(stage);
  updateAnnotations();
  if (pendingFocus === stage) {
    const heading = panels[stage].querySelector("h1, h2");
    heading.tabIndex = -1;
    heading.focus({ preventScroll: true });
    pendingFocus = null;
  }
}

let scrollScheduled = false;
function syncScroll() {
  const progress = scrollProgress(
    window.scrollY,
    document.documentElement.scrollHeight,
    window.innerHeight,
  );
  universe?.setProgress(progress);
  updateStage(stageForProgress(progress));
  document.querySelector("#progress-value").textContent = `${Math.round(
    progress * 100,
  )
    .toString()
    .padStart(2, "0")}%`;
  document.querySelector("#route-progress").style.transform =
    `scaleX(${progress})`;
  document.querySelector("#coordinates").textContent =
    `X ${(progress * 184).toFixed(2).padStart(6, "0")}   Y -${(progress * 62).toFixed(2).padStart(5, "0")}`;
  scrollScheduled = false;
}

window.addEventListener(
  "scroll",
  () => {
    if (!scrollScheduled) requestAnimationFrame(syncScroll);
    scrollScheduled = true;
  },
  { passive: true },
);
window.addEventListener(
  "resize",
  () => {
    universe?.resize();
    syncScroll();
  },
  { passive: true },
);
window.addEventListener(
  "pointermove",
  (event) => {
    if (event.pointerType === "mouse")
      universe?.setPointer(
        (event.clientX / innerWidth) * 2 - 1,
        (event.clientY / innerHeight) * 2 - 1,
      );
  },
  { passive: true },
);
document.documentElement.addEventListener("pointerleave", () =>
  universe?.setPointer(0, 0),
);

// Anchor destinations use the same normalized stops as the camera and HUD.
document.querySelectorAll('a[href^="#"]').forEach((link) =>
  link.addEventListener("click", (event) => {
    const stop = journeyStops.find(
      (item) => `#${item.id}` === link.getAttribute("href"),
    );
    if (!stop) return;
    event.preventDefault();
    if (link.closest(".story-panel")) pendingFocus = journeyStops.indexOf(stop);
    history.replaceState(null, "", `#${stop.id}`);
    window.scrollTo({
      top:
        stop.progress * (document.documentElement.scrollHeight - innerHeight),
      behavior: reduceMotion.matches || paused ? "instant" : "smooth",
    });
    if (link.classList.contains("skip-link")) {
      window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: "instant",
      });
      syncScroll();
      document.querySelector("#tab-codex").focus({ preventScroll: true });
    }
  }),
);

const languageToggle = document.querySelector("#language-toggle");
const languageMenu = document.querySelector("#language-menu");
function closeLanguages() {
  languageMenu.hidden = true;
  languageToggle.setAttribute("aria-expanded", "false");
}
languageToggle.addEventListener("click", () => {
  languageMenu.hidden = !languageMenu.hidden;
  languageToggle.setAttribute("aria-expanded", String(!languageMenu.hidden));
  if (!languageMenu.hidden)
    languageMenu.querySelector(`[data-locale="${i18n.locale}"]`).focus();
});
document.querySelectorAll("[data-locale]").forEach((button) =>
  button.addEventListener("click", () => {
    i18n.setLocale(button.dataset.locale);
    closeLanguages();
    languageToggle.focus();
  }),
);
document.addEventListener("click", (event) => {
  if (!event.target.closest(".language-switcher")) closeLanguages();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !languageMenu.hidden) {
    closeLanguages();
    languageToggle.focus();
  }
});

function setInstallMode(mode) {
  installMode = mode;
  copyOperation += 1;
  copyResult = "";
  clearTimeout(copyTimer);
  document.querySelector("#copy-status").textContent = "";
  document.querySelector("#install-command").textContent =
    product.commands[mode];
  document
    .querySelector("#command-panel")
    .setAttribute("aria-labelledby", `tab-${mode}`);
  document.querySelectorAll("[data-install-mode]").forEach((button) => {
    const selected = button.dataset.installMode === mode;
    button.setAttribute("aria-selected", String(selected));
    button.tabIndex = selected ? 0 : -1;
  });
}
const installTabs = [...document.querySelectorAll("[data-install-mode]")];
installTabs.forEach((button, index) => {
  button.addEventListener("click", () =>
    setInstallMode(button.dataset.installMode),
  );
  button.addEventListener("keydown", (event) => {
    const delta = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
    if (delta === undefined && event.key !== "Home" && event.key !== "End")
      return;
    event.preventDefault();
    const nextIndex =
      event.key === "Home"
        ? 0
        : event.key === "End"
          ? installTabs.length - 1
          : (index + delta + installTabs.length) % installTabs.length;
    setInstallMode(installTabs[nextIndex].dataset.installMode);
    installTabs[nextIndex].focus();
  });
});
document.querySelector("#copy-command").addEventListener("click", async () => {
  const operation = ++copyOperation;
  clearTimeout(copyTimer);
  try {
    await navigator.clipboard.writeText(product.commands[installMode]);
    if (operation !== copyOperation) return;
    copyResult = "copied";
  } catch {
    if (operation !== copyOperation) return;
    copyResult = "copyFailed";
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.querySelector("#install-command"));
    selection.removeAllRanges();
    selection.addRange(range);
  }
  document.querySelector("#copy-status").textContent = i18n.t(
    `terminal.${copyResult}`,
  );
  copyTimer = setTimeout(() => {
    copyResult = "";
    document.querySelector("#copy-status").textContent = "";
  }, 5000);
});

document.querySelector("#pause-motion").addEventListener("click", () => {
  paused = !paused;
  universe?.setPaused(paused);
  document.body.classList.toggle("motion-paused", paused);
  updateMotionButton();
});
reduceMotion.addEventListener("change", () => {
  paused = reduceMotion.matches;
  universe?.setReducedMotion?.(reduceMotion.matches);
  universe?.setPaused(paused);
  document.body.classList.toggle("motion-paused", paused);
  updateMotionButton();
});

i18n.apply();
paused = reduceMotion.matches;
document.body.classList.toggle("motion-paused", paused);
updateLanguage();
setInstallMode("codex");
renderIcons();
syncScroll();

function restoreAnchor() {
  const stop = journeyStops.find(
    (item) => `#${item.id}` === window.location.hash,
  );
  if (stop) {
    window.scrollTo({
      top:
        stop.progress * (document.documentElement.scrollHeight - innerHeight),
      behavior: "instant",
    });
    syncScroll();
  }
}
requestAnimationFrame(restoreAnchor);
window.addEventListener("hashchange", restoreAnchor);

function sceneError(error) {
  console.warn("3D scene unavailable:", error);
  document.body.classList.add("webgl-unavailable");
  document.body.classList.remove("scene-ready");
  const status = document.querySelector("#scene-status");
  status.hidden = false;
  status.dataset.i18n = "common.webglFallback";
  status.textContent = i18n.t("common.webglFallback");
}

import("./scene/universe.js")
  .then(({ createUniverse }) => {
    universe = createUniverse({
      canvas: document.querySelector("#universe-canvas"),
      reducedMotion: reduceMotion.matches,
      onReady() {
        document.body.classList.add("scene-ready");
        document.body.classList.remove("webgl-unavailable");
        document.querySelector("#scene-status").hidden = true;
      },
      onError: sceneError,
    });
    universe.setPaused(paused);
    syncScroll();
  })
  .catch(sceneError);

if (import.meta.hot) import.meta.hot.dispose(() => universe?.dispose());
