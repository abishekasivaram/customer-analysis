# Product Design System Blueprint
## RetailVision AI

---

## 1. Brand Identity
The UI must evoke the feel of a premium, enterprise SaaS product (similar to Stripe, Vercel, or Datadog). It should feel analytical, precise, trustworthy, and fast. Avoid generic "admin template" aesthetics.

---

## 2. Typography
- **Primary Font:** `Inter` or `Roboto` (Clean, highly legible for data-dense dashboards).
- **Monospace Font:** `JetBrains Mono` or `Fira Code` (For displaying IDs, code snippets, or raw data).
- **Hierarchy:** Strict typographic hierarchy using modular scale (Base size: 16px).

---

## 3. Color Tokens
The color palette should rely heavily on neutrals to let the data (charts, video highlights) stand out.

**Dark Theme (Default):**
- **Background:** Slate 900 (`#0f172a`)
- **Surface/Card:** Slate 800 (`#1e293b`)
- **Primary Accent:** Indigo 500 (`#6366f1`)
- **Success:** Emerald 500 (`#10b981`) - Used for completed processing, high KPIs.
- **Warning:** Amber 500 (`#f59e0b`) - Used for processing warnings, low battery on edge devices.
- **Danger:** Rose 500 (`#f43f5e`) - Used for system errors.

**Light Theme:**
- **Background:** Gray 50 (`#f9fafb`)
- **Surface/Card:** White (`#ffffff`)
- **Primary Accent:** Indigo 600 (`#4f46e5`)

---

## 4. Spacing Scale & Grid System
- **Scale:** 4pt grid system (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px).
- **Grid:** 12-column responsive grid layout for the dashboard.

---

## 5. Card Design
- **Style:** Subtle borders (1px solid slate-700 in dark mode) instead of heavy drop shadows.
- **Padding:** Generous internal padding (24px standard) to let data breathe.
- **Border Radius:** `8px` (md) for a sharp, professional look.

---

## 6. Chart Guidelines
- **Library:** Recharts or Chart.js (React wrapper).
- **Style:** Minimalist axes. Remove heavy grid lines (use faint, dashed lines if necessary).
- **Interactivity:** All charts must have custom tooltips that match the UI theme and provide exact numbers on hover.

---

## 7. Animation Guidelines
- **Micro-interactions:** Fast, subtle transitions (150ms-200ms ease-in-out) on hover states for buttons and table rows.
- **Data Loading:** Use skeleton loaders instead of full-page spinners for a smoother perceived performance.

---

## 8. Icons
- **Library:** `Lucide React` or `Heroicons`.
- **Style:** Outline style, 2px stroke, strictly standardized size (usually 20x20px for inline, 24x24px for sidebar).

---

## 9. Dashboard Principles
1. **Data over Decoration:** Visual elements exist only to clarify data, not to distract.
2. **Progressive Disclosure:** Show high-level KPIs first; allow drilling down into specific video frames or raw data tables.
3. **Actionable State:** Empty states must explain *why* they are empty and provide a clear Call to Action (e.g., "Upload your first video to generate analytics").
