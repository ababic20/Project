import React from "react";
import { useDroppable } from "@dnd-kit/core";
import TaskCard from "./TaskCard";

const statusColors = {
  new: "var(--color-new)",
  active: "var(--color-active)",
  testing: "var(--color-testing)",
  done: "var(--color-done)",
};

function KanbanColumn({ id, title, tasks, onTaskDeleted, onMoveWeek }) {
  const { isOver, setNodeRef } = useDroppable({ id });

  return (
    <div
      ref={setNodeRef}
      className={isOver ? "column-hover" : ""}
      style={{
        background: "var(--bg-column)",
        padding: "15px",
        borderRadius: "12px",
        border: `2px solid ${statusColors[title]}`,
        minHeight: "65vh",
        transition: "0.2s",
      }}
    >
      <h3
        style={{
          textAlign: "center",
          marginBottom: "12px",
          fontSize: "18px",
          fontWeight: "700",
          color: statusColors[title],
        }}
      >
        {title.toUpperCase()}
      </h3>

      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onTaskDeleted={onTaskDeleted}
          onMoveWeek={() => onMoveWeek(task)}
        />
      ))}
    </div>
  );
}

export default KanbanColumn;
