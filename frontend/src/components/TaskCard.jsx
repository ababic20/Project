import React, { useState } from "react";
import { useDraggable } from "@dnd-kit/core";
import { deleteTask } from "../api/tasks";
import EditTaskModal from "./EditTaskModal";

function TaskCard({ task, onTaskDeleted, onMoveWeek }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: `${task.category}-${task.status}-${task.id}`,
  });

  const [editing, setEditing] = useState(false);

  const style = {
    transform: transform ? `translate(${transform.x}px, ${transform.y}px)` : undefined,
    background: "var(--bg-card)",
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "14px",
    border: "1px solid #555",
    cursor: "grab",
    transition: "0.2s",
    position: "relative",
  };

  return (
    <>
      <div ref={setNodeRef} style={style}>
        <div
          {...listeners}
          {...attributes}
          style={{
            cursor: "grab",
            opacity: 0.6,
            fontSize: "12px",
            marginBottom: "6px",
            userSelect: "none",
          }}
        >
          ☰ Drag
        </div>

        <button
          onClick={async (e) => {
            e.stopPropagation();
            await deleteTask(task.id);
            onTaskDeleted();
          }}
          style={{
            position: "absolute",
            top: "6px",
            right: "6px",
            background: "#ff4444",
            border: "none",
            borderRadius: "3px",
            fontSize: "10px",
            cursor: "pointer",
            color: "#fff",
          }}
        >
          X
        </button>

        <div onClick={() => setEditing(true)} style={{ cursor: "pointer" }}>
          <strong>{task.title}</strong>
          <p style={{ opacity: 0.85 }}>{task.description}</p>
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            onMoveWeek(task);
          }}
          style={{
            position: "absolute",
            bottom: "6px",
            right: "6px",
            background: "#0a84ff",
            border: "none",
            padding: "4px 7px",
            borderRadius: "3px",
            fontSize: "10px",
            cursor: "pointer",
            color: "#fff",
          }}
        >
          ➜ Next Week
        </button>
      </div>

      {editing && (
        <EditTaskModal
          task={task}
          onClose={() => setEditing(false)}
          onUpdated={() => onTaskDeleted()}
        />
      )}
    </>
  );
}

export default TaskCard;
