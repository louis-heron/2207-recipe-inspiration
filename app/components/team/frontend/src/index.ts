import { escapeHtml } from "@recipe/shared"
import type { FrontendRenderer } from "@streamlit/component-v2-lib"

// DOM order = keyboard focus order:
// index 0 → delay -9s (top)
// index 1 → delay -1s (bottom-right)
// index 2 → delay -5s (bottom-left)
const DELAYS = ["-9s", "-1s", "-5s"]

interface TeamMember {
  name: string
  photo_url: string
  quote: string
  cite: string
  linkedin: string
}

interface TeamData {
  members: TeamMember[]
}

const Team: FrontendRenderer<Record<string, never>, TeamData> = ({ data, parentElement }) => {
  const members = data.members ?? []
  const list = parentElement.querySelector<HTMLUListElement>(".hex-list")

  if (!list) return

  members.forEach((member, i) => {
    const delay = DELAYS[i] ?? `${-((i * 12) / members.length) % 12}s`

    const li = document.createElement("li")
    li.className = "hex-wrapper"
    li.setAttribute("tabindex", "0")

    li.style.setProperty("--delay", delay)

    if (member.photo_url) {
      const base = member.photo_url.replace(/\.[^.]+$/, "")
      li.style.setProperty("--photo", `url('${base}.webp')`)
    }

    li.innerHTML = `
      <figure>
        <p class="member-name">${escapeHtml(member.name)}</p>
        <figcaption>
          <blockquote class="member-quote">
            ${escapeHtml(member.quote)}
            <footer><cite>${escapeHtml(member.cite)}</cite></footer>
          </blockquote>
          <a class="member-linkedin"
            href="${escapeHtml(member.linkedin)}"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn — opens in a new tab">
            LinkedIn
          </a>
        </figcaption>
      </figure>
    `

    list.appendChild(li)
  })
}

export default Team
