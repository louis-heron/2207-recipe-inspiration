function r(n) {
  return n.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const i = ["-9s", "-1s", "-5s"], p = ({ data: n, parentElement: s }) => {
  const o = n.members ?? [], a = s.querySelector(".hex-list");
  a && o.forEach((e, l) => {
    const c = i[l] ?? `${-(l * 12 / o.length) % 12}s`, t = document.createElement("li");
    t.className = "hex-wrapper", t.setAttribute("tabindex", "0"), t.style.setProperty("--delay", c), e.photo_url && t.style.setProperty("--photo", `url('${e.photo_url}')`), t.innerHTML = `
      <figure>
        <p class="member-name">${r(e.name)}</p>
        <figcaption>
          <blockquote class="member-quote">
            ${r(e.quote)}
            <footer><cite>${r(e.cite)}</cite></footer>
          </blockquote>
          <a class="member-linkedin"
            href="${r(e.linkedin)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn — opens in a new tab">
            LinkedIn
          </a>
        </figcaption>
      </figure>
    `, a.appendChild(t);
  });
};
export {
  p as default
};
