import { Routes, Route } from "react-router-dom";
import { HomePage } from "./pages/HomePage";
import { InstallPage } from "./pages/InstallPage";
import { PreviewPage } from "./pages/PreviewPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/install" element={<InstallPage />} />
      <Route path="/preview" element={<PreviewPage />} />
    </Routes>
  );
}
