function a(o) {
  return o.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const u = ["-9s", "-1s", "-5s"], f = ({ data: o, parentElement: p }) => {
  const s = o.members ?? [], l = p.querySelector(".hex-list");
  l && s.forEach((e, n) => {
    const i = u[n] ?? `${-(n * 12 / s.length) % 12}s`, t = document.createElement("li");
    if (t.className = "hex-wrapper", t.setAttribute("tabindex", "0"), t.style.setProperty("--delay", i), e.photo_url) {
      const r = e.photo_url.replace(/\.[^.]+$/, ""), c = CSS.supports("background-image", "image-set(url('x') type('image/avif'))") ? `image-set(url('${r}.avif') type('image/avif'), url('${r}.webp') type('image/webp'), url('${e.photo_url}') type('image/png'))` : `url('${r}.webp')`;
      t.style.setProperty("--photo", c);
    }
    t.innerHTML = `
      <figure>
        <p class="member-name">${a(e.name)}</p>
        <figcaption>
          <blockquote class="member-quote">
            ${a(e.quote)}
            <footer><cite>${a(e.cite)}</cite></footer>
          </blockquote>
          <a class="member-linkedin"
            href="${a(e.linkedin)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn — opens in a new tab">
            LinkedIn
          </a>
        </figcaption>
      </figure>
    `, l.appendChild(t);
  });
};
export {
  f as default
};
