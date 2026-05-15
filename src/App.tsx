import { Routes, Route } from "react-router-dom";
import { HomePage } from "./pages/HomePage";
import { InstallPage } from "./pages/InstallPage";
import { PreviewPage } from "./pages/PreviewPage";
import { useVisitTracker } from "./hooks/useVisitTracker";

export default function App() {
  useVisitTracker();

  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/install" element={<InstallPage />} />
      <Route path="/preview" element={<PreviewPage />} />
    </Routes>
  );
}
