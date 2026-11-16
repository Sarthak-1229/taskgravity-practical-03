import React, { useState } from 'react';

const INITIAL_FORM_STATE = {
  title: '',
  category: 'Frontend',
  priority: 'Medium',
  dueDate: '',
  estimatedHours: '',
  description: ''
};

export default function TaskForm({ onAddTask }) {
  const [formData, setFormData] = useState(INITIAL_FORM_STATE);
  const [errors, setErrors] = useState({});
  const [successMsg, setSuccessMsg] = useState('');
  const [errorBanner, setErrorBanner] = useState('');

  const validate = () => {
    const errs = {};
    if (!formData.title.trim()) {
      errs.title = 'Task title is required.';
    } else if (formData.title.trim().length < 3) {
      errs.title = 'Title must be at least 3 characters.';
    } else if (formData.title.trim().length > 80) {
      errs.title = 'Title cannot exceed 80 characters.';
    }

    if (!formData.dueDate) {
      errs.dueDate = 'Target deadline date is required.';
    } else {
      const selected = new Date(formData.dueDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (selected < today) {
        errs.dueDate = 'Deadline cannot be in the past.';
      }
    }

    const hours = parseFloat(formData.estimatedHours);
    if (!formData.estimatedHours || isNaN(hours) || hours <= 0) {
      errs.estimatedHours = 'Estimated effort must be greater than 0.';
    } else if (hours > 100) {
      errs.estimatedHours = 'Effort cannot exceed 100 hours.';
    }

    if (formData.description && formData.description.length > 300) {
      errs.description = 'Description cannot exceed 300 characters.';
    }

    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear field-specific error as user types
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    setErrorBanner('');
    setSuccessMsg('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setErrorBanner('Please resolve form validation errors below.');
      return;
    }

    const newTask = {
      id: 'tg-r' + Date.now().toString().slice(-4),
      title: formData.title.trim(),
      category: formData.category,
      priority: formData.priority,
      dueDate: formData.dueDate,
      estimatedHours: parseFloat(formData.estimatedHours),
      description: formData.description.trim(),
      status: 'pending',
      createdAt: new Date().toISOString()
    };

    onAddTask(newTask);
    setSuccessMsg(`Task "${newTask.title}" successfully added!`);
    setFormData(INITIAL_FORM_STATE);
    setErrors({});
    setErrorBanner('');

    setTimeout(() => setSuccessMsg(''), 3500);
  };

  return (
    <aside className="panel">
      <div className="panel-header">
        <h2 className="panel-title">Add Work Item</h2>
        <p className="panel-desc">Client-side React state validation with instantaneous feedback.</p>
      </div>

      {successMsg && <div className="alert alert-success">{successMsg}</div>}
      {errorBanner && <div className="alert alert-danger">{errorBanner}</div>}

      <form onSubmit={handleSubmit} noValidate>
        {/* Title */}
        <div className="form-group">
          <label className="form-label" htmlFor="title">Task Title *</label>
          <input
            id="title"
            name="title"
            type="text"
            className={`form-control ${errors.title ? 'error' : ''}`}
            placeholder="e.g. Implement React State Hooks"
            value={formData.title}
            onChange={handleChange}
          />
          {errors.title && <div className="error-text">{errors.title}</div>}
        </div>

        {/* Category & Priority */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="category">Category *</label>
            <select
              id="category"
              name="category"
              className="form-control"
              value={formData.category}
              onChange={handleChange}
            >
              <option value="Frontend">Frontend</option>
              <option value="Backend">Backend</option>
              <option value="Database">Database</option>
              <option value="DevOps">DevOps</option>
              <option value="Testing">Testing</option>
              <option value="UI/UX">UI/UX</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="priority">Priority *</label>
            <select
              id="priority"
              name="priority"
              className="form-control"
              value={formData.priority}
              onChange={handleChange}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Urgent">Urgent</option>
            </select>
          </div>
        </div>

        {/* Deadline & Estimated Hours */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
          <div className="form-group">
            <label className="form-label" htmlFor="dueDate">Deadline *</label>
            <input
              id="dueDate"
              name="dueDate"
              type="date"
              className={`form-control ${errors.dueDate ? 'error' : ''}`}
              value={formData.dueDate}
              onChange={handleChange}
            />
            {errors.dueDate && <div className="error-text">{errors.dueDate}</div>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="estimatedHours">Hours *</label>
            <input
              id="estimatedHours"
              name="estimatedHours"
              type="number"
              min="1"
              max="100"
              className={`form-control ${errors.estimatedHours ? 'error' : ''}`}
              placeholder="e.g. 5"
              value={formData.estimatedHours}
              onChange={handleChange}
            />
            {errors.estimatedHours && <div className="error-text">{errors.estimatedHours}</div>}
          </div>
        </div>

        {/* Scope Description */}
        <div className="form-group">
          <label className="form-label" htmlFor="description">Scope Description</label>
          <textarea
            id="description"
            name="description"
            rows="3"
            className={`form-control ${errors.description ? 'error' : ''}`}
            placeholder="Context, dependencies, criteria..."
            value={formData.description}
            onChange={handleChange}
          />
          {errors.description && <div className="error-text">{errors.description}</div>}
        </div>

        <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '0.5rem' }}>
          Add Task to Board
        </button>
      </form>
    </aside>
  );
}
