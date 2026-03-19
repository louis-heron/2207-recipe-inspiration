const m = ({
  setStateValue: p,
  setTriggerValue: v,
  parentElement: g
}) => {
  const t = g;
  if (t._ruInit) return;
  t._ruInit = !0;
  const a = t.querySelector(".ri-upload__label"), s = t.querySelector("#ri-file-input"), i = t.querySelector("#ri-upload-status"), _ = t.querySelector(".ri-upload__preview"), o = t.querySelector("#ri-preview-img"), f = t.querySelector("#ri-preview-caption"), l = t.querySelector("#ri-detect-btn");
  a.addEventListener("dragover", (e) => {
    e.preventDefault(), a.classList.add("ri-upload__label--dragover");
  }), a.addEventListener("dragleave", () => {
    a.classList.remove("ri-upload__label--dragover");
  }), a.addEventListener("drop", (e) => {
    var n;
    e.preventDefault(), a.classList.remove("ri-upload__label--dragover");
    const r = (n = e.dataTransfer) == null ? void 0 : n.files[0];
    r && d(r);
  }), s.addEventListener("change", () => {
    var r;
    const e = (r = s.files) == null ? void 0 : r[0];
    e && d(e);
  }), l.addEventListener("click", () => {
    v("detect_clicked", !0);
  });
  function d(e) {
    if (!["image/jpeg", "image/png"].includes(e.type)) {
      i.textContent = "Please select a JPG or PNG file.";
      return;
    }
    i.textContent = "Loading...";
    const r = new FileReader();
    r.onload = (n) => {
      var u;
      const c = (u = n.target) == null ? void 0 : u.result, y = c.split(",")[1];
      o.src = c, o.alt = e.name, f.textContent = `${e.name} — ${(e.size / 1024).toFixed(0)} KB`, _.hidden = !1, l.hidden = !1, i.textContent = "File ready.", p("file", {
        name: e.name,
        type: e.type,
        data: y,
        size: e.size
      });
    }, r.readAsDataURL(e);
  }
};
export {
  m as default
};
