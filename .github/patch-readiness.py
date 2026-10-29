from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = """let atlasActivationTimer = 0;
let blackReturnOverlayProgress = 0;"""
new = """let atlasActivationTimer = 0;
let atlasBootPromise = null;
let blackReturnOverlayProgress = 0;"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

old = """const ensurePortalPreview = () => {
  if (portalPreviewMode || portalPreviewFrame) return portalPreviewFrame;
  const frame = document.createElement('iframe');
  frame.id = 'portal-preview';
  frame.title = \"The Philosopher's Stone Atlas\";
  frame.tabIndex = -1;
  frame.setAttribute('aria-hidden', 'true');
  frame.src = ATLAS_URL + '?embedded=1';
  document.body.appendChild(frame);
  portalPreviewFrame = frame;
  return frame;
};"""
new = """const waitForAtlasWorkerActivation = worker => {
  if (!worker || worker.state === 'activated' || worker.state === 'redundant') {
    return Promise.resolve();
  }
  return new Promise(resolve => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      worker.removeEventListener('statechange', onStateChange);
      resolve();
    };
    const onStateChange = () => {
      if (worker.state === 'activated' || worker.state === 'redundant') finish();
    };
    worker.addEventListener('statechange', onStateChange);
    setTimeout(finish, 3500);
  });
};
const refreshAtlasOfflineWorker = async () => {
  if (!('serviceWorker' in navigator) || ATLAS_ORIGIN !== location.origin) return;
  try {
    const registrations = await navigator.serviceWorker.getRegistrations();
    const registration = registrations.find(item => ATLAS_URL.startsWith(item.scope));
    if (!registration) return;
    await registration.update();
    await waitForAtlasWorkerActivation(registration.installing || registration.waiting);
  } catch {
    // The embedded online Atlas must remain usable even if an optional offline worker cannot update.
  }
};
const startAtlasFrameLoad = frame => {
  if (atlasBootPromise) return atlasBootPromise;
  atlasBootPromise = (async () => {
    await refreshAtlasOfflineWorker();
    if (
      frame === portalPreviewFrame && frame.isConnected &&
      !frame.hasAttribute('src')
    ) {
      frame.src = ATLAS_URL + '?embedded=1';
    }
  })();
  return atlasBootPromise;
};
const ensurePortalPreview = () => {
  if (portalPreviewMode || portalPreviewFrame) return portalPreviewFrame;
  const frame = document.createElement('iframe');
  frame.id = 'portal-preview';
  frame.title = \"The Philosopher's Stone Atlas\";
  frame.tabIndex = -1;
  frame.setAttribute('aria-hidden', 'true');
  document.body.appendChild(frame);
  portalPreviewFrame = frame;
  startAtlasFrameLoad(frame);
  return frame;
};"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

old = """const activateAtlasComposition = () => {
  const frame = ensurePortalPreview();
  if (!frame) return;
  clearTimeout(atlasActivationTimer);
  frame.classList.add('is-committing');
  frame.style.opacity = '1';
  frame.setAttribute('aria-hidden', 'false');
  if (atlasReady) {
    syncAtlasFromBlack();
    postAtlasMessage({ type: 'stone-composition-activate-atlas' });
  }
  atlasActivationTimer = setTimeout(() => {
    if (compositionMode !== 'atlas') return;
    frame.classList.add('is-active');
    frame.classList.remove('is-committing');
  }, 300);
};"""
new = """const activateAtlasComposition = () => {
  const frame = ensurePortalPreview();
  if (!frame) return;
  clearTimeout(atlasActivationTimer);
  if (!atlasReady) {
    frame.classList.remove('is-active', 'is-committing');
    frame.style.opacity = '0';
    frame.setAttribute('aria-hidden', 'true');
    return;
  }
  frame.classList.add('is-committing');
  frame.style.opacity = '1';
  frame.setAttribute('aria-hidden', 'false');
  syncAtlasFromBlack();
  postAtlasMessage({ type: 'stone-composition-activate-atlas' });
  atlasActivationTimer = setTimeout(() => {
    if (compositionMode !== 'atlas') return;
    frame.classList.add('is-active');
    frame.classList.remove('is-committing');
  }, 300);
};"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

old = """  if (!portalPreviewFrame) return;
  const state = atlasPortalState;"""
new = """  if (!portalPreviewFrame) return;
  if (!atlasReady) {
    blackReturnOverlayProgress = 0;
    portalPreviewFrame.style.opacity = '0';
    return;
  }
  const state = atlasPortalState;"""
assert s.count(old) == 1
s = s.replace(old, new, 1)

checks = [
    'let atlasBootPromise = null;',
    'const refreshAtlasOfflineWorker = async () => {',
    'await registration.update();',
    'await waitForAtlasWorkerActivation(registration.installing || registration.waiting);',
    "!frame.hasAttribute('src')",
    "if (!atlasReady) {\n    frame.classList.remove('is-active', 'is-committing');",
    "if (!atlasReady) {\n    blackReturnOverlayProgress = 0;\n    portalPreviewFrame.style.opacity = '0';",
]
for marker in checks:
    assert marker in s, marker

p.write_text(s)
