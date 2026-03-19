const s = ({
  setStateValue: r,
  setTriggerValue: n,
  parentElement: u
}) => {
  const t = u;
  if (t._rcInit) return;
  t._rcInit = !0;
  const e = t.querySelector("#ri-num-recipes"), i = t.querySelector("#ri-num-output"), c = t.querySelector("#ri-get-recipes-btn");
  e.addEventListener("input", () => {
    i.textContent = e.value, e.setAttribute("aria-valuenow", e.value), r("num_recipes", parseInt(e.value, 10));
  }), c.addEventListener("click", () => {
    n("get_recipes_clicked", parseInt(e.value, 10));
  });
};
export {
  s as default
};
