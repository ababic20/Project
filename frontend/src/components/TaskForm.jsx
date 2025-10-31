import React, { useState } from "react";
import { createTask } from "../api/tasks";

function TaskForm({ onTaskAdded, defaultWeek, category }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    await createTask({
      title,
      description,
      status: "new",
      week: defaultWeek,
      category
    });

    setTitle("");
    setDescription("");
    onTaskAdded();
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px", textAlign: "center" }}>
      <input
        type="text"
        placeholder="Task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{
          padding: "10px",
          width: "220px",
          marginRight: "10px",
          borderRadius: "6px",
          border: "1px solid #333",
          background: "#111",
          color: "#fff"
        }}
        required
      />
      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        style={{
          padding: "10px",
          width: "300px",
          marginRight: "10px",
          borderRadius: "6px",
          border: "1px solid #333",
          background: "#111",
          color: "#fff"
        }}
      />
      <button
        type="submit"
        style={{
          padding: "10px 20px",
          borderRadius: "6px",
          cursor: "pointer",
          backgroundColor: "#4caf50",
          border: "none",
          color: "#fff",
          fontWeight: "bold"
        }}
      >
        Add
      </button>
    </form>
  );
}

export default TaskForm;
