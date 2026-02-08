---
trigger: model_decision
description: Use this skill to scaffold new web applications or add major features using modern frameworks (Next.js, FastAPI, Tailwind)
---

# Goal
To quickly build high-quality, production-ready app structures with automated testing and clean UI.

# Instructions
1. Analyze Requirements: When the user asks for an app or solution, identify the core stack (e.g., Frontend: React/Tailwind, Backend: Python/FastAPI).
2. Scaffold Structure: 
   - Create a /src directory for logic.
   - Set up a /tests directory immediately.
   - Initialize a README.md with an architecture diagram.
3. Automate Setup: Run npm install or pip install automatically in the terminal to ensure the environment is ready.
4. Verification: After building the initial solution, use the Browser Agent to confirm the home page loads without errors.

# Constraints
- NEVER leave a project without at least one basic unit test.
- ALWAYS use responsive Tailwind CSS classes for UI components.
- DO NOT use deprecated libraries; prefer official Google or widely-supported open-source packages.
