const pw = document.getElementById("password");
const form = document.getElementById("pwForm");
const btn = document.getElementById("checkBtn");
const result = document.getElementById("result");
const err = document.getElementById("error");

// 2) Extract features in the browser (shown live)
function features(p) {
  return {
    length: p.length,
    uppercase: [...p].filter(c => /[A-Z]/.test(c)).length,
    lowercase: [...p].filter(c => /[a-z]/.test(c)).length,
    numeric: [...p].filter(c => /[0-9]/.test(c)).length,
    special: [...p].filter(c => !/[A-Za-z0-9]/.test(c)).length,
  };
}
function showFeatures(f) {
  for (const k in f) document.getElementById("f-" + k).textContent = f[k];
}
pw.addEventListener("input", () => { showFeatures(features(pw.value)); result.classList.add("hidden"); });

document.getElementById("toggle").addEventListener("click", e => {
  const show = pw.type === "password";
  pw.type = show ? "text" : "password";
  e.target.textContent = show ? "Hide" : "Show";
});

// 3) Send to Python backend, 4) model predicts, 5) display result
form.addEventListener("submit", async e => {
  e.preventDefault();
  err.textContent = "";
  btn.disabled = true; btn.textContent = "Checking…";
  try {
    const r = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: pw.value }),
      cache: "no-store",
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error || "Request failed");
    showFeatures(d.features);
    result.className = "result " + d.strength.toLowerCase();
    document.getElementById("label").textContent = d.strength;
    document.getElementById("conf").textContent = d.confidence != null ? `Model confidence: ${d.confidence}%` : "";
  } catch (ex) {
    err.textContent = ex.message;
  } finally {
    btn.disabled = false; btn.textContent = "Check Strength";
  }
});
