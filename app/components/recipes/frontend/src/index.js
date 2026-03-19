import { escapeHtml } from "@recipe/shared";
function parseScore(matchScore) {
    if (!matchScore.includes("/"))
        return { pct: 0, label: "", mod: "" };
    const parts = matchScore.split("/");
    const pct = parseInt(parts[0]) / parseInt(parts[1]);
    if (Number.isNaN(pct))
        return { pct: 0, label: "", mod: "" };
    if (pct === 1.0)
        return { pct, label: "Perfect match", mod: "perfect" };
    if (pct >= 0.8)
        return { pct, label: "Great match", mod: "great" };
    if (pct >= 0.5)
        return { pct, label: "Good match", mod: "good" };
    return { pct, label: "Partial match", mod: "partial" };
}
function getMatchPct(recipe) {
    if (!recipe.match_score?.includes("/"))
        return 0;
    const parts = recipe.match_score.split("/");
    return parseInt(parts[0]) / parseInt(parts[1]);
}
function renderCard(recipe) {
    const title = escapeHtml(recipe.title ?? "Untitled");
    const matchScore = escapeHtml(recipe.match_score ?? "");
    const { pct, label, mod } = parseScore(recipe.match_score ?? "");
    const matched = recipe.matched_ingredients ?? [];
    let ingredients = [];
    let directions = [];
    try {
        ingredients = JSON.parse(recipe.ingredients ?? "[]");
    }
    catch { /* noop */ }
    try {
        const dirs = JSON.parse(recipe.directions ?? "[]");
        directions = dirs.filter(d => typeof d === "string" && d.trim());
    }
    catch { /* noop */ }
    const barHtml = pct > 0
        ? `<meter class="rc-progress" value="${pct}" min="0" max="1" aria-label="Match score ${Math.round(pct * 100)}%"></meter>`
        : "";
    const scoreHtml = label
        ? `<p class="rc-score rc-score--${mod}">${matchScore} ${label}</p>`
        : matchScore
            ? `<p class="rc-score">${matchScore}</p>`
            : "";
    const matchedHtml = matched.length > 0
        ? `<p class="rc-matched"><strong>Matched:</strong> ${matched.map(m => `<code class="rc-chip">${escapeHtml(m)}</code>`).join("")}</p>`
        : "";
    const ingItems = ingredients
        .map(item => `<li>${escapeHtml(String(item))}</li>`)
        .join("");
    const dirItems = directions
        .map((step, i) => `<li><span class="rc-step-num">${i + 1}.</span> ${escapeHtml(step)}</li>`)
        .join("");
    return `
    <li>
      <article class="rc-card">
        <h3 class="rc-title">${title}</h3>
        ${scoreHtml}
        ${barHtml}
        ${matchedHtml}
        <details class="rc-details rc-details--ing">
          <summary>Ingredients</summary>
          <ul class="rc-list">${ingItems}</ul>
        </details>
        <details class="rc-details rc-details--dir">
          <summary>Directions</summary>
          <ol class="rc-list">${dirItems}</ol>
        </details>
      </article>
    </li>`;
}
const Recipes = ({ data, parentElement }) => {
    const { recipes = [], ingredients_used = [] } = data;
    let container = parentElement.querySelector(".rc-wrapper");
    if (!container) {
        container = document.createElement("section");
        container.className = "rc-wrapper";
        container.setAttribute("aria-labelledby", "rc-page-title");
        parentElement.appendChild(container);
    }
    const sorted = [...recipes].sort((a, b) => getMatchPct(b) - getMatchPct(a));
    const count = recipes.length;
    const basedOn = ingredients_used.length > 0
        ? `<p class="rc-based-on">Based on: ${ingredients_used.map(i => escapeHtml(i)).join(", ")}</p>`
        : "";
    container.innerHTML = `
    <header class="rc-header">
      <h1 class="rc-page-title" id="rc-page-title">Recipes</h1>
      <p class="rc-count">${count} recipe${count !== 1 ? "s" : ""} found</p>
      ${basedOn}
    </header>
    <hr class="rc-divider" />
    <ul class="rc-grid">
      ${sorted.map(renderCard).join("")}
    </ul>
  `;
};
export default Recipes;
