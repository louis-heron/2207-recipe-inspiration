function n(e) {
  return e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function b(e) {
  if (!e.includes("/")) return { pct: 0, label: "", mod: "" };
  const r = e.split("/"), t = parseInt(r[0]) / parseInt(r[1]);
  return Number.isNaN(t) ? { pct: 0, label: "", mod: "" } : t === 1 ? { pct: t, label: "Perfect match", mod: "perfect" } : t >= 0.8 ? { pct: t, label: "Great match", mod: "great" } : t >= 0.5 ? { pct: t, label: "Good match", mod: "good" } : { pct: t, label: "Partial match", mod: "partial" };
}
function u(e) {
  var t;
  if (!((t = e.match_score) != null && t.includes("/"))) return 0;
  const r = e.match_score.split("/");
  return parseInt(r[0]) / parseInt(r[1]);
}
function y(e) {
  const r = n(e.title ?? "Untitled"), t = n(e.match_score ?? ""), { pct: c, label: s, mod: p } = b(e.match_score ?? ""), i = e.matched_ingredients ?? [];
  let o = [], a = [];
  try {
    o = JSON.parse(e.ingredients ?? "[]");
  } catch {
  }
  try {
    a = JSON.parse(e.directions ?? "[]").filter((d) => typeof d == "string" && d.trim());
  } catch {
  }
  const m = c > 0 ? `<meter class="rc-progress" value="${c}" min="0" max="1" aria-label="Match score ${Math.round(c * 100)}%"></meter>` : "", h = s ? `<p class="rc-score rc-score--${p}">${t} ${s}</p>` : t ? `<p class="rc-score">${t}</p>` : "", g = i.length > 0 ? `<p class="rc-matched"><strong>Matched:</strong> ${i.map((l) => `<code class="rc-chip">${n(l)}</code>`).join("")}</p>` : "", $ = o.map((l) => `<li>${n(String(l))}</li>`).join(""), f = a.map((l, d) => `<li><span class="rc-step-num">${d + 1}.</span> ${n(l)}</li>`).join("");
  return `
    <li>
      <article class="rc-card">
        <h3 class="rc-title">${r}</h3>
        ${h}
        ${m}
        ${g}
        <details class="rc-details rc-details--ing">
          <summary>Ingredients</summary>
          <ul class="rc-list">${$}</ul>
        </details>
        <details class="rc-details rc-details--dir">
          <summary>Directions</summary>
          <ol class="rc-list">${f}</ol>
        </details>
      </article>
    </li>`;
}
const I = ({ data: e, parentElement: r }) => {
  const { recipes: t = [], ingredients_used: c = [] } = e;
  let s = r.querySelector(".rc-wrapper");
  s || (s = document.createElement("section"), s.className = "rc-wrapper", s.setAttribute("aria-labelledby", "rc-page-title"), r.appendChild(s));
  const p = [...t].sort((a, m) => u(m) - u(a)), i = t.length, o = c.length > 0 ? `<p class="rc-based-on">Based on: ${c.map((a) => n(a)).join(", ")}</p>` : "";
  s.innerHTML = `
    <header class="rc-header">
      <h1 class="rc-page-title" id="rc-page-title">Recipes</h1>
      <p class="rc-count">${i} recipe${i !== 1 ? "s" : ""} found</p>
      ${o}
    </header>
    <hr class="rc-divider" />
    <ul class="rc-grid">
      ${p.map(y).join("")}
    </ul>
  `;
};
export {
  I as default
};
