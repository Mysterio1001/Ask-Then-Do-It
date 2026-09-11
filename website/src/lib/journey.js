export function clampProgress(value) {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
}

export function stageForProgress(progress, count = 5) {
  return Math.round(clampProgress(progress) * (count - 1));
}

export function scrollProgress(scrollY, scrollHeight, viewportHeight) {
  const distance = scrollHeight - viewportHeight;
  return distance > 0 ? clampProgress(scrollY / distance) : 0;
}
