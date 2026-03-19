const FileUploader = ({ setStateValue, setTriggerValue, parentElement, }) => {
    const pe = parentElement;
    if (pe._ruInit)
        return;
    pe._ruInit = true;
    const label = pe.querySelector(".ri-upload__label");
    const input = pe.querySelector("#ri-file-input");
    const status = pe.querySelector("#ri-upload-status");
    const preview = pe.querySelector(".ri-upload__preview");
    const img = pe.querySelector("#ri-preview-img");
    const caption = pe.querySelector("#ri-preview-caption");
    const detectBtn = pe.querySelector("#ri-detect-btn");
    label.addEventListener("dragover", (e) => {
        e.preventDefault();
        label.classList.add("ri-upload__label--dragover");
    });
    label.addEventListener("dragleave", () => {
        label.classList.remove("ri-upload__label--dragover");
    });
    label.addEventListener("drop", (e) => {
        e.preventDefault();
        label.classList.remove("ri-upload__label--dragover");
        const file = e.dataTransfer?.files[0];
        if (file)
            processFile(file);
    });
    input.addEventListener("change", () => {
        const file = input.files?.[0];
        if (file)
            processFile(file);
    });
    detectBtn.addEventListener("click", () => {
        setTriggerValue("detect_clicked", true);
    });
    function processFile(file) {
        if (!["image/jpeg", "image/png"].includes(file.type)) {
            status.textContent = "Please select a JPG or PNG file.";
            return;
        }
        status.textContent = "Loading...";
        const reader = new FileReader();
        reader.onload = (event) => {
            const result = event.target?.result;
            const base64 = result.split(",")[1];
            img.src = result;
            img.alt = file.name;
            caption.textContent = `${file.name} — ${(file.size / 1024).toFixed(0)} KB`;
            preview.hidden = false;
            detectBtn.hidden = false;
            status.textContent = "File ready.";
            setStateValue("file", {
                name: file.name,
                type: file.type,
                data: base64,
                size: file.size,
            });
        };
        reader.readAsDataURL(file);
    }
};
export default FileUploader;
