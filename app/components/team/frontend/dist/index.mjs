function n(r) {
  return r.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
const p = ["-9s", "-1s", "-5s"], u = ({ data: r, parentElement: o }) => {
  const l = r.members ?? [], c = o.querySelector(".hex-list");
  c && l.forEach((e, a) => {
    const s = p[a] ?? `${-(a * 12 / l.length) % 12}s`, t = document.createElement("li");
    if (t.className = "hex-wrapper", t.setAttribute("tabindex", "0"), t.style.setProperty("--delay", s), e.photo_url) {
      const i = document.createElement("style");
      i.textContent = `#team-orbit li.hex-wrapper:nth-child(${a + 1}) figure::before { background-image: url('${e.photo_url}'); }`, o.appendChild(i);
    }
    t.innerHTML = `
      <figure>
        <p class="member-name">${n(e.name)}</p>
        <figcaption>
          <blockquote class="member-quote">
            ${n(e.quote)}
            <footer><cite>${n(e.cite)}</cite></footer>
          </blockquote>
          <a class="member-linkedin"
            href="${n(e.linkedin)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn — opens in a new tab">
            LinkedIn
          </a>
        </figcaption>
      </figure>
    `, c.appendChild(t);
  });
};
export {
  u as default
};
