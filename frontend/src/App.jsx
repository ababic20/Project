import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import KanbanBoard from "./pages/KanbanBoard";
import Login from "./pages/LoginPage";

function ProtectedKanban() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div>
      <div style={{ textAlign: "right", margin: "10px 20px" }}>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <KanbanBoard category="business" />
      <KanbanBoard category="personal" />
    </div>
  );
}

export default function App() {
  const token = localStorage.getItem("token");

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/kanban"
          element={token ? <ProtectedKanban /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}
