function l(t) {
  return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const s = ({
  data: t,
  setTriggerValue: c,
  parentElement: r
}) => {
  const { logo_svg: g, logo_alt: o, logo_page: i, nav_links: n, active_page: p } = t;
  let e = r.querySelector("#app-header");
  e || (e = document.createElement("header"), e.id = "app-header", r.appendChild(e)), e.innerHTML = `
    <a class="logo-link" data-page="${l(i)}" href="#" aria-label="${l(o)}">
      ${g}
    </a>
    <nav aria-label="Main navigation">
      <ul role="list">
        ${n.map(
    (a) => `
          <li>
            <a
              class="nav-link${a.label === p ? " active" : ""}"
              data-page="${l(a.page)}"
              href="#"
              ${a.label === p ? 'aria-current="page"' : ""}
            >${l(a.label)}</a>
          </li>`
  ).join("")}
      </ul>
    </nav>
  `, e.querySelectorAll("[data-page]").forEach((a) => {
    a.onclick = (d) => {
      d.preventDefault(), a.dataset.page && c("page_clicked", a.dataset.page);
    };
  });
};
export {
  s as default
};
