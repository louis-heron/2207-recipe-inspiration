function r(l) {
  return l.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const n = ({
  data: l,
  parentElement: a
}) => {
  const { copyright: t, links: p } = l;
  let e = a.querySelector("#app-footer");
  e || (e = document.createElement("footer"), e.id = "app-footer", a.appendChild(e)), e.innerHTML = `
    <p>${r(t)}</p>
    <ul role="list">
      ${p.map(
    (o) => `
        <li>
          <a href="${r(o.url)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="${r(o.label)} — opens in a new tab">
            ${r(o.label)}
          </a>
        </li>`
  ).join("")}
    </ul>
  `;
};
export {
  n as default
};
