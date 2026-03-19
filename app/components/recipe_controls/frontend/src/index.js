const RecipeControls = ({ setStateValue, setTriggerValue, parentElement, }) => {
    const pe = parentElement;
    if (pe._rcInit)
        return;
    pe._rcInit = true;
    const slider = pe.querySelector("#ri-num-recipes");
    const output = pe.querySelector("#ri-num-output");
    const submitBtn = pe.querySelector("#ri-get-recipes-btn");
    slider.addEventListener("input", () => {
        output.textContent = slider.value;
        slider.setAttribute("aria-valuenow", slider.value);
        setStateValue("num_recipes", parseInt(slider.value, 10));
    });
    submitBtn.addEventListener("click", () => {
        setTriggerValue("get_recipes_clicked", parseInt(slider.value, 10));
    });
};
export default RecipeControls;
