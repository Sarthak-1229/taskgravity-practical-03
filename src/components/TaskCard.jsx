import React from 'react';

export default function TaskCard({ task, onToggleStatus, onDelete }) {
  const isCompleted = task.status === 'completed';
  const priorityClass = `badge-${task.priority.toLowerCase()}`;
  const statusClass = `badge-status-${task.status}`;
  const statusLabel = task.status === 'in-progress' ? 'In Progress' : (task.status === 'completed' ? 'Completed' : 'Pending');

  return (
    <article className={`task-item ${isCompleted ? 'completed' : ''}`}>
      <div className="task-item-top">
        <label className="task-check-wrap" title="Toggle status">
          <input
            type="checkbox"
            checked={isCompleted}
            onChange={() => onToggleStatus(task.id)}
          />
          <span className="task-title">{task.title}</span>
        </label>
        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span className={`badge ${priorityClass}`}>{task.priority}</span>
          <span className={`badge ${statusClass}`}>{statusLabel}</span>
        </div>
      </div>

      {task.description && <p className="task-desc">{task.description}</p>}

      <div className="task-footer">
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <span className="badge badge-category">{task.category}</span>
          <span>Due: <strong>{task.dueDate}</strong></span>
          <span>Est: <strong>{task.estimatedHours}h</strong></span>
        </div>
        <div style={{ display: 'flex', gap: '0.4rem' }}>
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => onToggleStatus(task.id)}
          >
            Cycle Status
          </button>
          <button
            className="btn btn-danger-text btn-sm"
            onClick={() => onDelete(task.id)}
          >
            Delete
          </button>
        </div>
      </div>
    </article>
  );
}
