# Practical 03: Modern Frontend Application using ReactJS

## TaskGravity — Functional Components, React Hooks, Form Validation & Responsive Design

### 1. Overview
Practical 03 rebuilds the TaskGravity client-side frontend using modern ReactJS. It enforces reactive state management, functional components, controlled form input validation, and interactive event handling.

### 2. Architecture & Components
- `src/App.jsx`: Main container component managing persistent task state via `useState`, `useEffect`, and `useMemo`.
- `src/components/TaskForm.jsx`: Controlled form component implementing real-time client-side validation rules (min/max length, future date checks, effort bounds) with clear field-level and banner feedback.
- `src/components/StatsBar.jsx`: Calculates and displays high-velocity metrics (Total, In Progress, Pending Review, Velocity %).
- `src/components/FilterBar.jsx`: Interactive live-search query, category filter, status filter, and multiple sort parameters.
- `src/components/TaskList.jsx` & `TaskCard.jsx`: Modular list and item presentation with status toggling and removal controls.
- `src/index.css`: Flat, minimalist TaskGravity design system adhering to strict non-AI gradient rules.

### 3. Execution Options

#### Option A: Run via Vite Dev Server
```bash
cd Practical3
npm install
npm run dev
```

#### Option B: Zero-Dependency Standalone Browser Preview
Simply double-click `standalone.html` in any browser to execute the complete React 18 application directly!
