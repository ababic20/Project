import KanbanBoard from "./pages/KanbanBoard";

export default function App() {
  return (
    <div>
      <KanbanBoard category="business" />
      <KanbanBoard category="personal" />
    </div>
  );
}
