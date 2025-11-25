import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";
import "./upload.css";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload a file.");

    // Simulate processing
    navigate("/results", { state: { fileName: file.name } });
  };

  return (
  <div className="upload-container">
    <h1>Upload Document</h1>

    <form onSubmit={handleSubmit} className="upload-card">
      <FileUpload onFileSelect={setFile} />

      {file && <p className="file-preview">Selected: {file.name}</p>}

      <button className="upload-btn">Upload & Analyze</button>
    </form>
  </div>
);

}
