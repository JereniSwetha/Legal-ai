import { useLocation, useNavigate } from "react-router-dom";
import "./result.css";

export default function ResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const fileName = location.state?.fileName;

  return (
  <div className="results-container">
    <h1>Results</h1>

    {fileName ? (
      <>
        <p className="results-info">File analyzed: {fileName}</p>
        <p>AI analysis will be shown here.</p>
      </>
    ) : (
      <p>No file was uploaded.</p>
    )}

    <button className="results-btn" onClick={() => navigate("/upload")}>
      Upload Another
    </button>
  </div>
);
}