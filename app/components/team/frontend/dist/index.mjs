function a(r) {
  return r.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const c = ["-9s", "-1s", "-5s"], u = ({ data: r, parentElement: s }) => {
  const o = r.members ?? [], l = s.querySelector(".hex-list");
  l && o.forEach((e, n) => {
    const p = c[n] ?? `${-(n * 12 / o.length) % 12}s`, t = document.createElement("li");
    if (t.className = "hex-wrapper", t.setAttribute("tabindex", "0"), t.style.setProperty("--delay", p), e.photo_url) {
      const i = e.photo_url.replace(/\.[^.]+$/, "");
      t.style.setProperty(
        "--photo",
        `image-set(url('${i}.avif') type('image/avif'), url('${i}.webp') type('image/webp'), url('${e.photo_url}') type('image/png'))`
      );
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
  u as default
};
