import React from 'react';
import TaskCard from './TaskCard';

export default function TaskList({ tasks, onToggleStatus, onDelete }) {
  if (tasks.length === 0) {
    return (
      <div className="empty-box">
        <div style={{ fontWeight: 600, color: '#0f172a', marginBottom: '0.25rem' }}>
          No work items found
        </div>
        <p style={{ fontSize: '0.85rem' }}>Try clearing your filters or create a new task using the form.</p>
      </div>
    );
  }

  return (
    <div>
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleStatus={onToggleStatus}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
