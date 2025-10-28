import React, { useState } from "react";
import { updateTask } from "../api/tasks";

function EditTaskModal({ task, onClose, onUpdated }) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");

  const handleSubmit = async (e) => {
    e.preventDefault();

    await updateTask(task.id, { title, description });
    onUpdated();
    onClose();
  };

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      background: "rgba(0,0,0,0.6)",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 999
    }}>
      <div style={{
        background: "#2c2c2c",
        padding: "20px",
        borderRadius: "10px",
        width: "350px",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.4)"
      }}>
        <h3 style={{ marginBottom: "15px", textAlign: "center" }}>Edit Task</h3>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px",
              background: "#3d3d3d",
              border: "1px solid #555",
              borderRadius: "6px",
              color: "#fff"
            }}
          />

          <textarea
            value={description}
            rows={3}
            onChange={e => setDescription(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              background: "#3d3d3d",
              border: "1px solid #555",
              borderRadius: "6px",
              color: "#fff"
            }}
          />

          <div style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "15px"
          }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: "8px 14px",
                background: "#777",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer"
              }}>
              Cancel
            </button>

            <button
              type="submit"
              style={{
                padding: "8px 14px",
                background: "#4caf50",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
                color: "#fff"
              }}>
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditTaskModal;
