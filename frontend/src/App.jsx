import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
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
  const [token, setToken] = useState(localStorage.getItem("token"));

  // osvježi stanje ako se token promijeni (npr. login/logout)
  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem("token"));
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login onLogin={() => setToken(localStorage.getItem("token"))} />} />
        <Route
          path="/kanban"
          element={token ? <ProtectedKanban /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}
