import "./App.css";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Insights from "./pages/Insights";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route index element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/insights" element={<Insights />} />
      </Routes>
    </Router>
  );
}

export default App;
