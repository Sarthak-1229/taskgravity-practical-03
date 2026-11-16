import React from 'react';

export default function FilterBar({
  searchQuery,
  setSearchQuery,
  statusFilter,
  setStatusFilter,
  categoryFilter,
  setCategoryFilter,
  sortBy,
  setSortBy
}) {
  return (
    <div className="filter-row">
      <div className="filter-controls">
        <input
          type="search"
          className="form-control"
          placeholder="Search tasks..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ width: '220px' }}
        />
        <select
          className="form-control"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          style={{ width: 'auto' }}
        >
          <option value="all">Status: All</option>
          <option value="pending">Pending</option>
          <option value="in-progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <select
          className="form-control"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          style={{ width: 'auto' }}
        >
          <option value="all">Category: All</option>
          <option value="Frontend">Frontend</option>
          <option value="Backend">Backend</option>
          <option value="Database">Database</option>
          <option value="DevOps">DevOps</option>
          <option value="Testing">Testing</option>
          <option value="UI/UX">UI/UX</option>
        </select>
      </div>

      <div className="filter-controls">
        <label style={{ fontSize: '0.8rem', fontWeight: 600 }}>Sort:</label>
        <select
          className="form-control"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{ width: 'auto' }}
        >
          <option value="dueDate">Deadline (Earliest)</option>
          <option value="priority">Priority (Highest)</option>
          <option value="hours">Effort (Largest)</option>
          <option value="title">Title (A-Z)</option>
        </select>
      </div>
    </div>
  );
}
