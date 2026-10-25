// Shared easing + palette for the animated overlays (loaded by each <name>.html).
const INK = '#16131f', WHITE = '#ffffff', YELLOW = '#ffd23f', MINT = '#6fe3b9', SKY = '#7cc8ff', AMBER = '#ffb340', GREY = '#bcc3cf';
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const local = (t, t0, len) => clamp((t - t0) / len);
const easeOutCubic = (x) => 1 - Math.pow(1 - x, 3);
const easeInOutCubic = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const easeInBack = (x, s = 1.7) => x * x * ((s + 1) * x - s);
const easeOutBack = (x, s = 1.9) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);
// Pop from 0 to 1 with a springy overshoot; u = seconds since the pop started.
const springPop = (u) => (u <= 0 ? 0 : 1 - Math.exp(-7 * u) * Math.cos(15 * u));
// Squash-and-stretch pair [sx, sy] that decays after a pop; u = seconds since the pop started.
const squash = (u, amp = 0.28) => {
  if (u <= 0) return [1, 1];
  const k = amp * Math.exp(-6 * u) * Math.sin(17 * u);
  return [1 - k, 1 + k];
};
// Damped wiggle in [-1, 1]; u = seconds since the wiggle started.
const wiggle = (u, freq = 22, decay = 4) => (u <= 0 ? 0 : Math.exp(-decay * u) * Math.sin(freq * u));
const $ = (id) => document.getElementById(id);
