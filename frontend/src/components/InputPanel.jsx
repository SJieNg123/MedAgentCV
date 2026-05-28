import { useState } from "react";

const MIN = 3;
const MAX = 500;

export default function InputPanel({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [description, setDescription] = useState("");
  const [touched, setTouched] = useState(false);

  const descLen = description.trim().length;
  const descOk = descLen >= MIN && descLen <= MAX;
  const canSubmit = file && descOk && !loading;

  function handleFile(e) {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setFileName(f ? f.name : "");
  }

  function submit(e) {
    e.preventDefault();
    setTouched(true);
    if (!canSubmit) return;
    onAnalyze({ file, description: description.trim() });
  }

  return (
    <form className="input-form" onSubmit={submit}>
      <h2 className="col-title">Input</h2>

      <label className="field-label">Chest X-ray image</label>
      <label className={`dropzone ${file ? "has-file" : ""}`}>
        <input type="file" accept="image/*" onChange={handleFile} hidden />
        <span className="dropzone-icon">⌖</span>
        <span className="dropzone-text">
          {fileName || "Click to select a PNG / JPG"}
        </span>
      </label>
      {touched && !file && <p className="field-error">Please select an image.</p>}

      <label className="field-label" htmlFor="desc">
        Disease / symptom description
      </label>
      <textarea
        id="desc"
        className="textarea"
        rows={4}
        placeholder="e.g. 60yo patient, shortness of breath, suspected cardiomegaly…"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <div className="char-row">
        <span className={descOk ? "muted" : "field-error"}>
          {descLen}/{MAX} (min {MIN})
        </span>
      </div>

      <button className="primary-btn" type="submit" disabled={!canSubmit}>
        {loading ? "Analyzing…" : "Run Analysis ▶"}
      </button>
    </form>
  );
}
