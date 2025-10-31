import React, { useEffect, useState } from "react";
import { DndContext } from "@dnd-kit/core";
import { getTasks, updateTask } from "../api/tasks";
import KanbanColumn from "../components/KanbanColumn";
import TaskForm from "../components/TaskForm";

function getWeekRange(weekNumber) {
  const now = new Date();
  const year = now.getFullYear();
  const firstDay = new Date(year, 0, 1);
  const start = new Date(firstDay.getTime() + (weekNumber - 1) * 7 * 86400000);
  start.setDate(start.getDate() - (start.getDay() + 6) % 7);
  const end = new Date(start.getTime() + 6 * 86400000);

  return {
    start: start.toLocaleDateString("hr-HR"),
    end: end.toLocaleDateString("hr-HR"),
  };
}

function getCurrentWeekNumber() {
  const now = new Date();
  const oneJan = new Date(now.getFullYear(), 0, 1);
  const numberOfDays = Math.floor((now - oneJan) / (24 * 60 * 60 * 1000));
  return Math.ceil((now.getDay() + 1 + numberOfDays) / 7);
}

function KanbanBoard({ category }) {
  const [tasks, setTasks] = useState([]);
  const [week, setWeek] = useState(getCurrentWeekNumber());

  const fetchTasks = async () => {
    try {
      const data = await getTasks(week, category);
      setTasks(data || []);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [week, category]);

  const { start, end } = getWeekRange(week);

  const handleDragEnd = async ({ active, over }) => {
    if (!over) return;
    const parts = active.id.split("-");
    const taskId = Number(parts.pop());
    const newStatus = over.id.split("-")[1];

    await updateTask(taskId, { status: newStatus, category });
    fetchTasks();
  };

  const handleMoveWeek = async (task) => {
    await updateTask(task.id, { week: week + 1, category });
    fetchTasks();
  };

  const handleTaskDeleted = () => fetchTasks();

  const statuses = ["new", "active", "testing", "done"];

  return (
    <div style={{ marginBottom: "50px", maxWidth: "1350px", margin: "0 auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "15px" }}>
        {category === "business" ? "Business Tasks" : "Personal Tasks"}
      </h2>

      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <button onClick={() => setWeek((w) => Math.max(1, w - 1))}>⬅ Prev</button>
        <span style={{ margin: "0 20px", fontWeight: "bold" }}>
          Week {week} ({start} – {end})
        </span>
        <button onClick={() => setWeek((w) => w + 1)}>Next ➡</button>
      </div>

      <TaskForm onTaskAdded={fetchTasks} defaultWeek={week} category={category} />

      <DndContext onDragEnd={handleDragEnd}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "18px",
            minHeight: "65vh",
          }}
        >
          {statuses.map((status) => (
            <KanbanColumn
              key={status}
              id={`${category}-${status}`}
              title={status}
              tasks={tasks.filter((t) => t.status === status)}
              onTaskDeleted={handleTaskDeleted}
              onMoveWeek={handleMoveWeek}
            />
          ))}
        </div>
      </DndContext>
    </div>
  );
}

export default KanbanBoard;
