// JS ports, our own minimal versions. Reads JSON list of strings on stdin, prints {port: [accepted strings]}.
const C = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const split2 = (s, t) => { if (s.split('.').length !== 2) return false; const [a, b] = s.split('.'); return t(a) && t(b); };
const P = {
  'js Number()': s => s.trim() !== '' && Number.isFinite(Number(s)),
  'js parseFloat': s => Number.isFinite(parseFloat(s)),
  'js round-trip toFixed(2)': s => Number(s).toFixed(2) === s,
  'js split+!isNaN': s => split2(s, p => p !== '' && !isNaN(p)),
  'js split+Number.isInteger': s => split2(s, p => p !== '' && Number.isInteger(Number(p))),
  'js split+parseInt': s => split2(s, p => !isNaN(parseInt(p, 10))),
  'js /^\\d+\\.\\d+$/m': s => /^\d+\.\d+$/m.test(s),
  'js /^[0-9]+\\.[0-9]+$/': s => /^[0-9]+\.[0-9]+$/.test(s),
};
const out = {}; for (const [k, f] of Object.entries(P)) out[k] = C.filter(s => { try { return f(s); } catch (e) { return false; } });
console.log(JSON.stringify(out));
