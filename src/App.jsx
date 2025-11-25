import { Routes, Route, Navigate } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import ResultPage from "./pages/ResultPage";

export default function App() {
  return (
    <Routes>
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/results" element={<ResultPage />} />

      { /* Default: go to Upload Page */ }
      <Route path="/" element={<Navigate to="/upload" replace />} />
    </Routes>
  );
}
