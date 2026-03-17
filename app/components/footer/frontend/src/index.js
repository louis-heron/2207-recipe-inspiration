import { escapeHtml } from "@recipe/shared";
const Footer = ({ data, parentElement, }) => {
    const { copyright, links } = data;
    // Find or create the footer element — no dependency on a pre-existing skeleton
    let footerEl = parentElement.querySelector("#app-footer");
    if (!footerEl) {
        footerEl = document.createElement("footer");
        footerEl.id = "app-footer";
        parentElement.appendChild(footerEl);
    }
    footerEl.innerHTML = `
    <p>${escapeHtml(copyright)}</p>
    <ul role="list">
      ${links
        .map((link) => `
        <li>
          <a href="${escapeHtml(link.url)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="${escapeHtml(link.label)} — opens in a new tab">
            ${escapeHtml(link.label)}
          </a>
        </li>`)
        .join("")}
    </ul>
  `;
};
export default Footer;
