import type { FrontendRenderer, FrontendState } from "@streamlit/component-v2-lib"

type RecipeControlsState = FrontendState & {
  num_recipes: number | null
  get_recipes_clicked: number | null
}

interface RecipeControlsElement extends HTMLElement {
  _rcInit?: boolean
}

const RecipeControls: FrontendRenderer<RecipeControlsState, Record<string, never>> = ({
  setStateValue,
  setTriggerValue,
  parentElement,
}) => {
  const pe = parentElement as RecipeControlsElement
  if (pe._rcInit) return
  pe._rcInit = true

  const slider    = pe.querySelector<HTMLInputElement>("#ri-num-recipes")!
  const output    = pe.querySelector<HTMLOutputElement>("#ri-num-output")!
  const submitBtn = pe.querySelector<HTMLButtonElement>("#ri-get-recipes-btn")!

  slider.addEventListener("input", () => {
    output.textContent = slider.value
    slider.setAttribute("aria-valuenow", slider.value)
    setStateValue("num_recipes", parseInt(slider.value, 10))
  })

  submitBtn.addEventListener("click", () => {
    setTriggerValue("get_recipes_clicked", parseInt(slider.value, 10))
  })
}

export default RecipeControls
