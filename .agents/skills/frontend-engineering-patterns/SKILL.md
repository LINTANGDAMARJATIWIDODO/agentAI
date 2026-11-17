---
name: frontend-engineering-patterns
description: Engineer accessible, responsive, high-performance web frontends and enterprise dashboards using React, Next.js, and TypeScript. Implement state management, optimistic UI, and Web Vitals optimization. Use when building client interfaces.
---

# SKILL: Enterprise Frontend Engineering & Component Patterns

> **Origin Repository:** https://github.com/j4flmao/agent-skills  
> **Source License:** MIT License  
> **Attribution:** Adapted from `agent-skills` (j4flmao) Frontend Foundations category.  
> **Target Owner:** RAKA (Director of Technology & Engineering)

---

## 1. PURPOSE & OBJECTIVE
To construct accessible, modular, type-safe, and highly performant enterprise web applications, data dashboards, and real-time control canvases using modern frontend paradigms.

## 2. SCOPE
- React 19 / Next.js App Router, TypeScript strict mode, responsive Tailwind CSS layouts, state machines, real-time WebSockets, Core Web Vitals (LCP, FID/INP, CLS), and accessibility (WCAG 2.1 AA).

## 3. CORE ARCHITECTURAL PATTERNS
1. **Separation of Presentation & Business Logic:** Dumb UI presentational components decoupled from custom data-fetching hooks.
2. **Server-Driven Data & Optimistic Updates:** Render initial states server-side; apply immediate optimistic UI feedback for user mutations.
3. **Resilient Error Boundaries:** Wrap component sub-trees in granular error boundaries to prevent a single widget failure from crashing the entire application.

## 4. STEP-BY-STEP PROCEDURE
1. **Component Hierarchy Design:** Break UI mockups into atomic components (Atoms, Molecules, Organisms).
2. **Strict TypeScript Typing:** Define interface contracts for all component props and API responses.
3. **Responsive & Accessible Layout:** Use CSS Grid and Flexbox with mobile-first breakpoints and semantic HTML elements.
4. **Performance Tuning:** Code-split route bundles, lazy-load heavy visualization libraries, and memoize expensive calculations.
5. **State Management:** Keep state local whenever possible; use lightweight stores (Zustand) or server-cache managers (TanStack Query) for global state.

## 5. QUALITY METRICS
- Lighthouse Performance score >= 90; Accessibility score >= 95.
- Zero TypeScript `any` types in production application code.

## 6. CONSTRAINTS
- Never store sensitive auth tokens (e.g. refresh tokens) in insecure `localStorage` (use `httpOnly` secure cookies).
- Avoid unnecessary re-renders through proper dependency array management and key usage.
