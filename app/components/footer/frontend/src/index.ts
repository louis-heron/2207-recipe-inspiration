import { escapeHtml } from "@recipe/shared"
import type { FrontendRenderer } from "@streamlit/component-v2-lib"

interface FooterLink {
  label: string
  url: string
}

interface FooterData {
  copyright: string
  links: FooterLink[]
}

const Footer: FrontendRenderer<Record<string, never>, FooterData> = ({
  data,
  parentElement,
}) => {
  const { copyright, links } = data

  // Find or create the footer element — no dependency on a pre-existing skeleton
  let footerEl = parentElement.querySelector<HTMLElement>("#app-footer")
  if (!footerEl) {
    footerEl = document.createElement("footer")
    footerEl.id = "app-footer"
    parentElement.appendChild(footerEl)
  }

  footerEl.innerHTML = `
    <p>${escapeHtml(copyright)}</p>
    <ul role="list">
      ${links
        .map(
          (link) => `
        <li>
          <a href="${escapeHtml(link.url)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="${escapeHtml(link.label)} — opens in a new tab">
            ${escapeHtml(link.label)}
          </a>
        </li>`
        )
        .join("")}
    </ul>
  `
}

export default Footer
