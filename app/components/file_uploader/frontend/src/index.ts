import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

interface FileInfo {
  name: string
  type: string
  data: string
  size: number
}

type FileUploaderState = FrontendState & {
  file: FileInfo | null
  detect_clicked: boolean | null
}

interface FileUploaderElement extends HTMLElement {
  _ruInit?: boolean
}

const FileUploader: FrontendRenderer<FileUploaderState, Record<string, never>> = ({
  setStateValue,
  setTriggerValue,
  parentElement,
}) => {
  const pe = parentElement as FileUploaderElement
  if (pe._ruInit) return
  pe._ruInit = true

  const label     = pe.querySelector<HTMLElement>(".ri-upload__label")!
  const input     = pe.querySelector<HTMLInputElement>("#ri-file-input")!
  const status    = pe.querySelector<HTMLElement>("#ri-upload-status")!
  const preview   = pe.querySelector<HTMLElement>(".ri-upload__preview")!
  const img       = pe.querySelector<HTMLImageElement>("#ri-preview-img")!
  const caption   = pe.querySelector<HTMLElement>("#ri-preview-caption")!
  const detectBtn = pe.querySelector<HTMLButtonElement>("#ri-detect-btn")!

  label.addEventListener("dragover", (e) => {
    e.preventDefault()
    label.classList.add("ri-upload__label--dragover")
  })

  label.addEventListener("dragleave", () => {
    label.classList.remove("ri-upload__label--dragover")
  })

  label.addEventListener("drop", (e) => {
    e.preventDefault()
    label.classList.remove("ri-upload__label--dragover")
    const file = e.dataTransfer?.files[0]
    if (file) processFile(file)
  })

  input.addEventListener("change", () => {
    const file = input.files?.[0]
    if (file) processFile(file)
  })

  detectBtn.addEventListener("click", () => {
    setTriggerValue("detect_clicked", true)
  })

  function processFile(file: File): void {
    if (!["image/jpeg", "image/png"].includes(file.type)) {
      status.textContent = "Please select a JPG or PNG file."
      return
    }
    status.textContent = "Loading..."
    const reader = new FileReader()
    reader.onload = (event) => {
      const result = event.target?.result as string
      const base64 = result.split(",")[1]

      img.src = result
      img.alt = file.name
      caption.textContent = `${file.name} — ${(file.size / 1024).toFixed(0)} KB`
      preview.hidden = false
      detectBtn.hidden = false
      status.textContent = "File ready."

      setStateValue("file", {
        name: file.name,
        type: file.type,
        data: base64,
        size: file.size,
      })
    }
    reader.readAsDataURL(file)
  }
}

export default FileUploader
