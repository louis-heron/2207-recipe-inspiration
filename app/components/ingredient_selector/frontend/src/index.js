import { escapeHtml } from "@recipe/shared";
const IngredientSelector = ({ data, setStateValue, parentElement, }) => {
    const pe = parentElement;
    const labelEl = pe.querySelector("#ri-cb-label");
    const field = pe.querySelector("#ri-cb-field");
    const chipsEl = pe.querySelector("#ri-cb-chips");
    const input = pe.querySelector("#ri-cb-input");
    const listbox = pe.querySelector("#ri-cb-listbox");
    // Always update data reference so event listeners use latest options
    pe._riData = data;
    // Sync selected on external version bump (e.g. detection result)
    const incoming = data.selected ?? [];
    const version = data.version ?? 0;
    if (!pe._riInit) {
        pe._riSelected = [...incoming];
        pe._riVersion = version;
    }
    else if (version !== pe._riVersion) {
        pe._riSelected = [...incoming];
        pe._riVersion = version;
        setStateValue("selected", [...pe._riSelected]);
    }
    labelEl.textContent = data.label ?? "";
    input.placeholder = data.placeholder ?? "";
    renderChips();
    if (pe._riInit)
        return;
    pe._riInit = true;
    let activeIndex = -1;
    field.addEventListener("click", () => input.focus());
    input.addEventListener("input", () => {
        activeIndex = -1;
        renderListbox(input.value);
        openListbox();
    });
    input.addEventListener("keydown", (e) => {
        const opts = Array.from(listbox.querySelectorAll('[role="option"]'));
        if (e.key === "ArrowDown") {
            e.preventDefault();
            if (!isOpen()) {
                renderListbox(input.value);
                openListbox();
            }
            activeIndex = Math.min(activeIndex + 1, opts.length - 1);
            updateActive(opts);
        }
        else if (e.key === "ArrowUp") {
            e.preventDefault();
            activeIndex = Math.max(activeIndex - 1, -1);
            updateActive(opts);
            if (activeIndex === -1)
                input.setAttribute("aria-activedescendant", "");
        }
        else if (e.key === "Enter" || (e.key === " " && activeIndex >= 0)) {
            if (isOpen() && activeIndex >= 0) {
                e.preventDefault();
                const val = opts[activeIndex].dataset["value"];
                if (val)
                    selectOption(val);
            }
        }
        else if (e.key === "Escape") {
            e.preventDefault();
            closeListbox();
            input.value = "";
        }
        else if (e.key === "Backspace" && input.value === "") {
            if (pe._riSelected.length > 0) {
                pe._riSelected.pop();
                renderChips();
                setStateValue("selected", [...pe._riSelected]);
            }
        }
        else if (e.key === "Tab") {
            closeListbox();
        }
    });
    document.addEventListener("click", (e) => {
        if (!pe.contains(e.target))
            closeListbox();
    });
    // ── Helpers ───────────────────────────────────────────
    function isOpen() {
        return !listbox.hidden;
    }
    function openListbox() {
        if (listbox.children.length === 0)
            return;
        listbox.hidden = false;
        input.setAttribute("aria-expanded", "true");
    }
    function closeListbox() {
        listbox.hidden = true;
        input.setAttribute("aria-expanded", "false");
        input.setAttribute("aria-activedescendant", "");
        activeIndex = -1;
    }
    function updateActive(opts) {
        opts.forEach((o, i) => {
            o.classList.toggle("ri-cb__option--active", i === activeIndex);
        });
        if (activeIndex >= 0) {
            const active = opts[activeIndex];
            input.setAttribute("aria-activedescendant", active.id);
            active.scrollIntoView({ block: "nearest" });
        }
    }
    function selectOption(value) {
        if (!pe._riSelected.includes(value)) {
            pe._riSelected.push(value);
            setStateValue("selected", [...pe._riSelected]);
        }
        input.value = "";
        closeListbox();
        renderChips();
        input.focus();
    }
    function renderListbox(query) {
        const q = query.trim().toLowerCase();
        const sel = pe._riSelected;
        const all = pe._riData.options ?? [];
        const candidates = q.length > 0
            ? all
                .filter(o => !sel.includes(o) && o.toLowerCase().includes(q))
                .sort((a, b) => {
                const al = a.toLowerCase(), bl = b.toLowerCase();
                if (al.startsWith(q) && !bl.startsWith(q))
                    return -1;
                if (bl.startsWith(q) && !al.startsWith(q))
                    return 1;
                return al.localeCompare(bl);
            })
                .slice(0, 50)
            : [];
        listbox.innerHTML = "";
        candidates.forEach((item, i) => {
            const li = document.createElement("li");
            li.setAttribute("role", "option");
            li.setAttribute("aria-selected", "false");
            li.id = `ri-cb-opt-${i}`;
            li.dataset["value"] = item;
            li.className = "ri-cb__option";
            li.textContent = item;
            li.addEventListener("mousedown", (e) => {
                e.preventDefault();
                selectOption(item);
            });
            listbox.appendChild(li);
        });
        if (listbox.children.length === 0)
            closeListbox();
    }
    function renderChips() {
        chipsEl.innerHTML = "";
        pe._riSelected.forEach(item => {
            const li = document.createElement("li");
            li.className = "ri-cb__chip";
            const txt = document.createElement("span");
            txt.textContent = item;
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "ri-cb__chip-remove";
            btn.setAttribute("aria-label", `Remove ${escapeHtml(item)}`);
            btn.textContent = "×";
            btn.addEventListener("click", () => {
                pe._riSelected = pe._riSelected.filter(s => s !== item);
                renderChips();
                setStateValue("selected", [...pe._riSelected]);
                input.focus();
            });
            li.appendChild(txt);
            li.appendChild(btn);
            chipsEl.appendChild(li);
        });
    }
};
export default IngredientSelector;
