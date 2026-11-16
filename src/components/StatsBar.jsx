import React from 'react';

export default function StatsBar({ tasks }) {
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'completed').length;
  const inProgress = tasks.filter(t => t.status === 'in-progress').length;
  const pending = tasks.filter(t => t.status === 'pending').length;
  const velocity = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <section className="stats-grid">
      <div className="stat-card">
        <div className="stat-title">Total Tasks</div>
        <div className="stat-number">{total}</div>
        <div className="stat-sub">Across all streams</div>
      </div>
      <div className="stat-card">
        <div className="stat-title">In Progress</div>
        <div className="stat-number" style={{ color: '#1d4ed8' }}>{inProgress}</div>
        <div className="stat-sub">Active engineering</div>
      </div>
      <div className="stat-card">
        <div className="stat-title">Pending Review</div>
        <div className="stat-number" style={{ color: '#92400e' }}>{pending}</div>
        <div className="stat-sub">Awaiting verification</div>
      </div>
      <div className="stat-card">
        <div className="stat-title">Completion Velocity</div>
        <div className="stat-number" style={{ color: '#047857' }}>{velocity}%</div>
        <div className="stat-sub">{completed} completed units</div>
      </div>
    </section>
  );
}
