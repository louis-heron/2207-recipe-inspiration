import { escapeHtml } from "@recipe/shared"
import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

interface NavLink {
  label: string
  page: string
}

interface HeaderData {
  logo_svg: string
  logo_alt: string
  logo_page: string
  nav_links: NavLink[]
  active_page: string
}

type HeaderState = FrontendState & { page_clicked?: string | null }

const Header: FrontendRenderer<HeaderState, HeaderData> = ({
  data,
  setTriggerValue,
  parentElement,
}) => {
  const { logo_svg, logo_alt, logo_page, nav_links, active_page } = data

  let headerEl = parentElement.querySelector<HTMLElement>("#app-header")
  if (!headerEl) {
    headerEl = document.createElement("header")
    headerEl.id = "app-header"
    parentElement.appendChild(headerEl)
  }

  headerEl.innerHTML = `
    <a class="logo-link" data-page="${escapeHtml(logo_page)}" href="#" aria-label="${escapeHtml(logo_alt)}">
      ${logo_svg}
      Recipe Inspiration
    </a>
    <nav aria-label="Main navigation">
      <ul role="list">
        ${nav_links
          .map(
            (link) => `
          <li>
            <a
              class="nav-link${link.label === active_page ? " active" : ""}"
              data-page="${escapeHtml(link.page)}"
              href="#"
              ${link.label === active_page ? 'aria-current="page"' : ""}
            >${escapeHtml(link.label)}</a>
          </li>`
          )
          .join("")}
      </ul>
    </nav>
  `

  headerEl.querySelectorAll<HTMLAnchorElement>("[data-page]").forEach((a) => {
    a.onclick = (e) => {
      e.preventDefault()
      if (a.dataset.page) setTriggerValue("page_clicked", a.dataset.page)
    }
  })
}

export default Header
