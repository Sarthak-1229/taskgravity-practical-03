import React, { useState, useEffect, useMemo } from 'react';
import StatsBar from './components/StatsBar';
import FilterBar from './components/FilterBar';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';

const SEED_TASKS = [
  {
    id: 'tg-r101',
    title: 'Migrate Task State to React Hooks',
    category: 'Frontend',
    priority: 'High',
    dueDate: '2026-11-21',
    estimatedHours: 4,
    description: 'Decompose monolithic vanilla JS UI into modular, reactive functional components.',
    status: 'in-progress',
    createdAt: '2026-11-15T08:00:00Z'
  },
  {
    id: 'tg-r102',
    title: 'Form Validation with Controlled Components',
    category: 'Frontend',
    priority: 'Urgent',
    dueDate: '2026-11-22',
    estimatedHours: 3,
    description: 'Implement real-time error clearance and accessible validation badges.',
    status: 'completed',
    createdAt: '2026-11-15T10:00:00Z'
  },
  {
    id: 'tg-r103',
    title: 'PostgreSQL & MongoDB Comparison Matrix',
    category: 'Database',
    priority: 'Medium',
    dueDate: '2026-11-25',
    estimatedHours: 5,
    description: 'Document schema tradeoffs for TaskGravity scaling benchmarks.',
    status: 'pending',
    createdAt: '2026-11-16T12:00:00Z'
  }
];

export default function App() {
  const [tasks, setTasks] = useState(() => {
    try {
      const saved = localStorage.getItem('TaskGravity_React_v3');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn('Error reading from localStorage:', e);
    }
    return SEED_TASKS;
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [sortBy, setSortBy] = useState('dueDate');

  // Persist to localStorage on change
  useEffect(() => {
    try {
      localStorage.setItem('TaskGravity_React_v3', JSON.stringify(tasks));
    } catch (e) {
      console.error('Failed to sync tasks:', e);
    }
  }, [tasks]);

  const handleAddTask = (newTask) => {
    setTasks(prev => [newTask, ...prev]);
  };

  const handleToggleStatus = (id) => {
    setTasks(prev => prev.map(t => {
      if (t.id === id) {
        const nextStatus = t.status === 'pending'
          ? 'in-progress'
          : t.status === 'in-progress'
            ? 'completed'
            : 'pending';
        return { ...t, status: nextStatus };
      }
      return t;
    }));
  };

  const handleDeleteTask = (id) => {
    const target = tasks.find(t => t.id === id);
    if (!target) return;
    if (window.confirm(`Delete task "${target.title}"?`)) {
      setTasks(prev => prev.filter(t => t.id !== id));
    }
  };

  // Filtered & Sorted Tasks using useMemo for performance
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      if (statusFilter !== 'all' && task.status !== statusFilter) return false;
      if (categoryFilter !== 'all' && task.category !== categoryFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const matchesTitle = task.title.toLowerCase().includes(q);
        const matchesDesc = (task.description || '').toLowerCase().includes(q);
        if (!matchesTitle && !matchesDesc) return false;
      }
      return true;
    }).sort((a, b) => {
      if (sortBy === 'dueDate') return new Date(a.dueDate) - new Date(b.dueDate);
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'hours') return b.estimatedHours - a.estimatedHours;
      if (sortBy === 'priority') {
        const weights = { Urgent: 4, High: 3, Medium: 2, Low: 1 };
        return (weights[b.priority] || 0) - (weights[a.priority] || 0);
      }
      return new Date(b.createdAt) - new Date(a.createdAt);
    });
  }, [tasks, searchQuery, statusFilter, categoryFilter, sortBy]);

  return (
    <div>
      {/* Header */}
      <header className="app-header">
        <div className="container header-inner">
          <a href="#" className="brand">
            <span className="brand-badge">TG</span>
            <span>TaskGravity</span>
          </a>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <span className="badge badge-category">Practical 03 &bull; ReactJS</span>
            <span className="badge badge-status-completed">Hooks &amp; Controlled Forms</span>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="container">
        {/* Stats */}
        <StatsBar tasks={tasks} />

        {/* Layout */}
        <div className="main-grid">
          <TaskForm onAddTask={handleAddTask} />

          <section>
            <FilterBar
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              statusFilter={statusFilter}
              setStatusFilter={setStatusFilter}
              categoryFilter={categoryFilter}
              setCategoryFilter={setCategoryFilter}
              sortBy={sortBy}
              setSortBy={setSortBy}
            />

            <TaskList
              tasks={filteredTasks}
              onToggleStatus={handleToggleStatus}
              onDelete={handleDeleteTask}
            />
          </section>
        </div>
      </div>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--tg-border)', background: '#fff', padding: '1.5rem 0', fontSize: '0.8rem', color: '#64748b' }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <strong>TaskGravity</strong> &bull; Practical 03 React Application | Student: <strong>Sarthak Bhosale</strong> (PRN: 202401100051)
          </div>
          <div>Department of Computer Engineering (Software Engineering)</div>
        </div>
      </footer>
    </div>
  );
}
