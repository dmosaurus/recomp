// ── UI Helpers ────────────────────────────────────────────────────────────────

function toastMsg(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 3000);
}

function toggleDay(el) {
  const body = el.nextElementSibling;
  body.classList.toggle("open");
}

function showPhase(n, btn) {
  [1, 2, 3].forEach(i => {
    const el = document.getElementById("phase" + i);
    if (el) el.style.display = i === n ? "block" : "none";
  });
  document.querySelectorAll("#phase-tabs .btn").forEach(b => b.className = "btn btn-ghost btn-sm");
  btn.className = "btn btn-o btn-sm";
}

// ── Log Workout Form ──────────────────────────────────────────────────────────

function setType(type, btn) {
  document.querySelectorAll("#type-btns .btn").forEach(b => b.className = "btn btn-ghost btn-sm");
  btn.className = "btn btn-o btn-sm";
  document.getElementById("type-hidden").value = type;
  const isStrength = type === "Upper Strength" || type === "Lower Strength";
  document.getElementById("log-cardio").style.display  = isStrength ? "none" : "block";
  document.getElementById("log-strength").style.display = isStrength ? "block" : "none";
  if (isStrength && !document.querySelector(".ex-row")) addExercise();
}

let exCount = 0;
function addExercise() {
  exCount++;
  const div = document.createElement("div");
  div.className = "ex-row";
  div.style.cssText = "display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:8px;margin-bottom:8px;align-items:end";
  div.innerHTML = `
    <div class="lf-field"><label>Exercise</label><input type="text" name="exercise_name[]" placeholder="Trap Bar Deadlift"></div>
    <div class="lf-field"><label>Sets</label><input type="number" name="exercise_sets[]" placeholder="4"></div>
    <div class="lf-field"><label>Reps</label><input type="number" name="exercise_reps[]" placeholder="5"></div>
    <div class="lf-field"><label>Weight (lbs)</label><input type="number" name="exercise_weight[]" placeholder="185"></div>
  `;
  document.getElementById("ex-list").appendChild(div);
}

// ── Nutrition Form ────────────────────────────────────────────────────────────

function setMealType(type, btn) {
  document.querySelectorAll("#meal-type-btns .btn").forEach(b => b.className = "btn btn-ghost btn-sm");
  btn.className = "btn btn-o btn-sm";
  document.getElementById("meal-type-hidden").value = type;
}

function quickAdd(key) {
  const f = window.QUICK_FOODS[key];
  if (!f) return;
  document.getElementById("n-food").value         = f.food;
  document.getElementById("n-serving-size").value = f.servingSize;
  document.getElementById("n-serving-unit").value = f.servingUnit;
  document.getElementById("n-cal").value          = f.cal;
  document.getElementById("n-pro").value          = f.pro;
  document.getElementById("n-carb").value         = f.carb;
  document.getElementById("n-fat").value          = f.fat;
  document.getElementById("n-sugar").value        = f.sugar;
  document.getElementById("n-fiber").value        = f.fiber;
}

// ── Charts ────────────────────────────────────────────────────────────────────

function drawLine(id, labels, data, color, ymin, ymax) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const W = canvas.parentElement.offsetWidth || 400, H = 160;
  canvas.width = W; canvas.height = H;
  ctx.clearRect(0, 0, W, H);
  const pad = { t: 10, r: 10, b: 30, l: 44 };
  const cW = W - pad.l - pad.r, cH = H - pad.t - pad.b;
  ctx.strokeStyle = "#1e1e1e"; ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + (cH / 4) * i;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(pad.l + cW, y); ctx.stroke();
    ctx.fillStyle = "#444"; ctx.font = "9px JetBrains Mono"; ctx.textAlign = "right";
    ctx.fillText(Math.round(ymax - ((ymax - ymin) / 4) * i), pad.l - 4, y + 3);
  }
  if (!data.length) {
    ctx.fillStyle = "#333"; ctx.font = "11px Syne"; ctx.textAlign = "center";
    ctx.fillText("Log workouts to see data", W / 2, H / 2); return;
  }
  const xOf = i => pad.l + (i / Math.max(data.length - 1, 1)) * cW;
  const yOf = v => pad.t + cH - ((v - ymin) / (ymax - ymin)) * cH;
  ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.lineJoin = "round";
  ctx.beginPath();
  data.forEach((v, i) => i === 0 ? ctx.moveTo(xOf(i), yOf(v)) : ctx.lineTo(xOf(i), yOf(v)));
  ctx.stroke();
  ctx.beginPath();
  data.forEach((v, i) => i === 0 ? ctx.moveTo(xOf(i), yOf(v)) : ctx.lineTo(xOf(i), yOf(v)));
  ctx.lineTo(xOf(data.length - 1), pad.t + cH); ctx.lineTo(pad.l, pad.t + cH); ctx.closePath();
  const grad = ctx.createLinearGradient(0, pad.t, 0, pad.t + cH);
  grad.addColorStop(0, color + "44"); grad.addColorStop(1, color + "00");
  ctx.fillStyle = grad; ctx.fill();
  data.forEach((v, i) => {
    ctx.beginPath(); ctx.arc(xOf(i), yOf(v), 3, 0, Math.PI * 2);
    ctx.fillStyle = color; ctx.fill();
    if (labels[i]) {
      ctx.fillStyle = "#555"; ctx.font = "8px JetBrains Mono"; ctx.textAlign = "center";
      ctx.fillText(labels[i], xOf(i), H - 8);
    }
  });
}

function drawCharts() {
  fetch("/api/chart-data").then(r => r.json()).then(d => {
    drawLine("hrChart",   d.labels,    d.hr,       "#00e5a0", 100, 200);
    drawLine("distChart", d.labels,    d.dist,     "#3d9eff", 0,   8);
    drawLine("dlChart",   d.dl_labels, d.dl_vals,  "#ff5500", 100, 350);
    drawLine("calChart",  d.labels,    d.cal,      "#ffd93d", 0,   800);
  });
}
