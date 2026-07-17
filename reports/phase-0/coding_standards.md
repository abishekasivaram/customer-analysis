# Coding Standards
## RetailVision AI

---

## 1. Naming Conventions

### Folder Naming
- Use `kebab-case` for all folder names (e.g., `feature-modules`, `auth-service`).

### File Naming
- **Python:** Use `snake_case.py` (e.g., `video_processor.py`).
- **React/TS:** Use `PascalCase.tsx` for components (e.g., `DashboardCard.tsx`), and `camelCase.ts` for utilities (e.g., `apiClient.ts`).

### API Naming
- Use plural nouns for REST resources (e.g., `/api/v1/videos`, `/api/v1/users`).
- Use kebab-case in URLs (e.g., `/api/v1/project-settings`).

---

## 2. Python Standards
- **Style Guide:** Adhere strictly to PEP 8.
- **Formatter:** Code must be formatted using `Black` (line length 88).
- **Linter:** `flake8` and `pylint` must pass before merging.
- **Type Hinting:** Use static type hinting for all function arguments and return types (e.g., `def process(video_id: str) -> bool:`).

---

## 3. React / TypeScript Standards
- **Components:** Use functional components exclusively with React Hooks. Avoid class components.
- **State Management:** Use Context API for global UI state and React Query for server state/caching.
- **Linter:** ESLint with the `airbnb-typescript` preset.
- **Formatting:** `Prettier` must be run on commit.

---

## 4. Exception Handling
- **Backend:** Never return raw stack traces to the client. Use global exception handlers in FastAPI to return standard JSON error responses.
- **Frontend:** Use Error Boundaries for UI crash protection. Display user-friendly toast notifications for API failures.

---

## 5. Logging Convention
- **Format:** Standardize log messages with context (`[Service] [Level] Message`).
- **Context:** Always include `user_id` or `video_id` in log context when available to facilitate tracing.

---

## 6. Documentation Standards
- **Code Comments:** Use docstrings for all classes, methods, and complex functions.
  - Python: Use Google-style docstrings.
  - TypeScript: Use JSDoc format.
- **README:** Every major microservice or folder must have a `README.md` explaining setup and responsibilities.

---

## 7. Commit Convention
Use Conventional Commits format:
- `feat:` A new feature.
- `fix:` A bug fix.
- `docs:` Documentation only changes.
- `refactor:` Code change that neither fixes a bug nor adds a feature.
- `test:` Adding missing tests or correcting existing tests.
- Example: `feat: add object tracking using ByteTrack`
