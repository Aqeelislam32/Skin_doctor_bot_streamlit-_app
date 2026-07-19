---
name: Clinical Intelligence
colors:
  surface: '#f9f9ff'
  surface-dim: '#cadaff'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e8edff'
  surface-container-high: '#e0e8ff'
  surface-container-highest: '#d7e2ff'
  on-surface: '#041b3c'
  on-surface-variant: '#434654'
  inverse-surface: '#1d3052'
  inverse-on-surface: '#edf0ff'
  outline: '#737685'
  outline-variant: '#c3c6d6'
  surface-tint: '#0c56d0'
  primary: '#003d9b'
  on-primary: '#ffffff'
  primary-container: '#0052cc'
  on-primary-container: '#c4d2ff'
  inverse-primary: '#b2c5ff'
  secondary: '#5b5f62'
  on-secondary: '#ffffff'
  secondary-container: '#dde0e3'
  on-secondary-container: '#5f6366'
  tertiary: '#004b58'
  on-tertiary: '#ffffff'
  tertiary-container: '#006476'
  on-tertiary-container: '#70e2ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001848'
  on-primary-fixed-variant: '#0040a2'
  secondary-fixed: '#e0e3e6'
  secondary-fixed-dim: '#c3c7ca'
  on-secondary-fixed: '#181c1e'
  on-secondary-fixed-variant: '#43474a'
  tertiary-fixed: '#adecff'
  tertiary-fixed-dim: '#5dd6f3'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5d'
  background: '#f9f9ff'
  on-background: '#041b3c'
  surface-variant: '#d7e2ff'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-display:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  margin-page: 2rem
  gutter-grid: 1.5rem
  control-panel-width: 320px
  stack-gap: 1rem
  section-padding: 1.5rem
---

## Brand & Style

The design system is engineered for high-stakes medical environments, prioritizing clarity, trust, and rapid information synthesis. The visual narrative combines **Corporate Modern** efficiency with **Minimalist** restraint to reduce cognitive load for healthcare professionals.

The style leverages a systematic approach to density—using ample white space to separate critical data points while maintaining a professional, "clinical" atmosphere. It avoids unnecessary decoration, focusing instead on structural integrity and functional aesthetics that evoke the precision of modern diagnostic equipment.

## Colors

The palette is anchored by **Medical Blue**, a color associated with stability and surgical precision. This is used for primary actions and brand presence. The **Secondary Light Slate** serves as the primary canvas color, providing a soft, non-reflective background that reduces eye strain during long shifts.

- **Primary:** High-visibility blue for CTAs, active states, and focus indicators.
- **Secondary:** Neutral slate for background surfaces and subtle container differentiation.
- **Tertiary:** A calming teal for secondary data visualizations or "success" statuses.
- **Neutral:** A deep navy for high-contrast typography and iconography.
- **System States:** Standardized red (#DE350B) for alerts and green (#36B37E) for normal readings.

## Typography

The design system utilizes **Inter** for its exceptional legibility and systematic weight distribution. The typography is scaled to ensure that critical patient metrics and AI insights are immediately scannable.

- **Headlines:** Use Semi-Bold (600) for clear section identification.
- **Body:** Regular (400) weight for descriptions and patient notes to ensure a high-quality reading experience.
- **Data Display:** Bold (700) weight for numerical values and diagnostic results to create immediate visual hierarchy.
- **Labels:** Medium (500) with slight letter spacing for meta-data and form headers.

## Layout & Spacing

The dashboard employs a **Two-Column Fixed-Fluid Split**. 

1.  **Left Column (Input Control):** A fixed 320px sidebar containing patient parameters, filters, and AI toggle controls. This ensures tools are always accessible.
2.  **Right Column (Results Canvas):** A fluid workspace that expands to fill the remaining area, utilizing a 12-column internal grid for organizing results, charts, and diagnostic cards.

**Breakpoints:**
- **Desktop (1280px+):** Full two-column view with 24px gutters.
- **Tablet (768px - 1279px):** The Control Panel collapses into a drawer or shifts to a full-width top section.
- **Mobile (<767px):** Single column stack; inputs move to the top or a dedicated configuration tab.

## Elevation & Depth

To maintain a "clinical" look, depth is communicated through **Soft Ambient Shadows** rather than heavy borders.

- **Base Layer:** The Secondary Color (#F4F7FA) acts as the foundation.
- **Card Layer:** White (#FFFFFF) surfaces with a subtle 1px border (#E1E4E8) and a soft shadow (0px 4px 12px rgba(0, 0, 0, 0.05)).
- **Active Overlay:** Modal dialogs and active dropdowns use an increased shadow spread (0px 12px 24px rgba(0, 0, 0, 0.1)) to signify temporal priority.
- **Depth Hierarchy:** Higher elevation indicates "actionable" results or "critical" AI alerts that require immediate clinician attention.

## Shapes

The design system uses a **Rounded (8px-16px)** shape language. This softens the technical nature of the AI, making the interface feel more approachable and modern without appearing toy-like.

- **Primary Cards:** 16px (rounded-xl) for main containers to define distinct data clusters.
- **Buttons & Inputs:** 8px (rounded-md) for interactive elements to maintain a professional, organized structure.
- **Tags/Chips:** Fully pill-shaped for status indicators and categorizations.

## Components

### Buttons & Controls
- **Primary Button:** Solid Medical Blue with white text, 8px corner radius.
- **Secondary Button:** Ghost style with Medical Blue border and text.
- **Input Fields:** White background with a subtle slate border. Focus state uses a 2px Medical Blue outline.

### Cards & Results
- **Diagnostic Card:** 16px rounded corners, white background, soft shadow. Features a 4px left-accent bar in Primary Blue (or status color).
- **Large Icons:** Use 32px or 48px stroke-based icons (2px weight) for high-level category navigation within the Control Panel.

### Lists & Data
- **Metric List:** Clean rows with 1px dividers, using `data-display` typography for the primary value and `label-sm` for the unit (e.g., "98 bpm").

### Medical Specifics
- **AI Confidence Gauge:** A semi-circular progress bar or a simple pill-shaped percentage indicator used within Result Cards.
- **Status Chips:** High-contrast background with white text for critical alerts; light-tinted background with dark text for stable statuses.