function w(d) {
  return d.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const q = ({
  data: d,
  setStateValue: f,
  parentElement: C
}) => {
  const e = C, k = e.querySelector("#ri-cb-label"), A = e.querySelector("#ri-cb-field"), m = e.querySelector("#ri-cb-chips"), n = e.querySelector("#ri-cb-input"), s = e.querySelector("#ri-cb-listbox");
  e._riData = d;
  const S = d.selected ?? [], h = d.version ?? 0;
  if (e._riInit ? h !== e._riVersion && (e._riSelected = [...S], e._riVersion = h, f("selected", [...e._riSelected])) : (e._riSelected = [...S], e._riVersion = h), k.textContent = d.label ?? "", n.placeholder = d.placeholder ?? "", b(), e._riInit) return;
  e._riInit = !0;
  let r = -1;
  A.addEventListener("click", () => n.focus()), n.addEventListener("input", () => {
    r = -1, x(n.value), y();
  }), n.addEventListener("keydown", (t) => {
    const i = Array.from(s.querySelectorAll('[role="option"]'));
    if (t.key === "ArrowDown")
      t.preventDefault(), E() || (x(n.value), y()), r = Math.min(r + 1, i.length - 1), L(i);
    else if (t.key === "ArrowUp")
      t.preventDefault(), r = Math.max(r - 1, -1), L(i), r === -1 && n.setAttribute("aria-activedescendant", "");
    else if (t.key === "Enter" || t.key === " " && r >= 0) {
      if (E() && r >= 0) {
        t.preventDefault();
        const l = i[r].dataset.value;
        l && g(l);
      }
    } else t.key === "Escape" ? (t.preventDefault(), u(), n.value = "") : t.key === "Backspace" && n.value === "" ? e._riSelected.length > 0 && (e._riSelected.pop(), b(), f("selected", [...e._riSelected])) : t.key === "Tab" && u();
  }), document.addEventListener("click", (t) => {
    e.contains(t.target) || u();
  });
  function E() {
    return !s.hidden;
  }
  function y() {
    s.children.length !== 0 && (s.hidden = !1, n.setAttribute("aria-expanded", "true"));
  }
  function u() {
    s.hidden = !0, n.setAttribute("aria-expanded", "false"), n.setAttribute("aria-activedescendant", ""), r = -1;
  }
  function L(t) {
    if (t.forEach((i, l) => {
      i.classList.toggle("ri-cb__option--active", l === r);
    }), r >= 0) {
      const i = t[r];
      n.setAttribute("aria-activedescendant", i.id), i.scrollIntoView({ block: "nearest" });
    }
  }
  function g(t) {
    e._riSelected.includes(t) || (e._riSelected.push(t), f("selected", [...e._riSelected])), n.value = "", u(), b(), n.focus();
  }
  function x(t) {
    const i = t.trim().toLowerCase(), l = e._riSelected, o = e._riData.options ?? [], _ = i.length > 0 ? o.filter((a) => !l.includes(a) && a.toLowerCase().includes(i)).sort((a, v) => {
      const c = a.toLowerCase(), p = v.toLowerCase();
      return c.startsWith(i) && !p.startsWith(i) ? -1 : p.startsWith(i) && !c.startsWith(i) ? 1 : c.localeCompare(p);
    }).slice(0, 50) : [];
    s.innerHTML = "", _.forEach((a, v) => {
      const c = document.createElement("li");
      c.setAttribute("role", "option"), c.setAttribute("aria-selected", "false"), c.id = `ri-cb-opt-${v}`, c.dataset.value = a, c.className = "ri-cb__option", c.textContent = a, c.addEventListener("mousedown", (p) => {
        p.preventDefault(), g(a);
      }), s.appendChild(c);
    }), s.children.length === 0 && u();
  }
  function b() {
    m.innerHTML = "", e._riSelected.forEach((t) => {
      const i = document.createElement("li");
      i.className = "ri-cb__chip";
      const l = document.createElement("span");
      l.textContent = t;
      const o = document.createElement("button");
      o.type = "button", o.className = "ri-cb__chip-remove", o.setAttribute("aria-label", `Remove ${w(t)}`), o.textContent = "×", o.addEventListener("click", () => {
        e._riSelected = e._riSelected.filter((_) => _ !== t), b(), f("selected", [...e._riSelected]), n.focus();
      }), i.appendChild(l), i.appendChild(o), m.appendChild(i);
    });
  }
};
export {
  q as default
};
