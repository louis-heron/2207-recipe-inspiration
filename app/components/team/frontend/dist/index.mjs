function r(n) {
  return n.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const p = ["-9s", "-1s", "-5s"], u = ({ data: n, parentElement: s }) => {
  const o = n.members ?? [], a = s.querySelector(".hex-list");
  a && o.forEach((e, l) => {
    const c = p[l] ?? `${-(l * 12 / o.length) % 12}s`, t = document.createElement("li");
    if (t.className = "hex-wrapper", t.setAttribute("tabindex", "0"), t.style.setProperty("--delay", c), e.photo_url) {
      const i = e.photo_url.replace(/\.[^.]+$/, "");
      t.style.setProperty("--photo", `url('${i}.webp')`);
    }
    t.innerHTML = `
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
  u as default
};
