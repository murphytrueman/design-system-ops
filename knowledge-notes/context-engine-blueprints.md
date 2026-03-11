---
name: context-engine-blueprints
type: knowledge
---

# Context engine blueprint templates

**Knowledge note for Design System Ops**
**Auto-loaded by:** context-engine-builder

---

## Purpose

This reference contains the YAML output templates for each of the seven context engine blueprints plus the engine manifest and usage guide. The context-engine-builder skill references these templates when generating output — they define the structure, field names, and example values that each blueprint file must follow.

Each template shows the minimum viable structure. Real output will contain more entries per section, populated from the target design system's actual components, tokens, patterns, and rules.

---

## UX blueprint template

```yaml
ux_blueprint:
  version: "1.0"
  patterns:
    modal_dialog:
      trigger: "User action requiring confirmation or focused input"
      states: [closed, opening, open, closing]
      transitions:
        - from: closed
          to: opening
          trigger: "User clicks trigger element"
        - from: open
          to: closing
          trigger: "User clicks close, presses Escape, or clicks backdrop"
      completion: "User completes or dismisses the dialog"
      errors:
        - condition: "Form validation fails inside modal"
          behaviour: "Keep modal open, show inline errors"
      edge_cases:
        - "Nested modals: prohibited. Use drill-down pattern instead."
        - "Long content: modal body scrolls, header and footer remain fixed."

    selection_rules:
      - intent: "Confirm a destructive action"
        use: "confirmation_dialog"
        not: "toast_notification"
        reason: "Destructive actions require explicit user confirmation"
      - intent: "Show non-blocking feedback"
        use: "toast_notification"
        not: "modal_dialog"
        reason: "Feedback should not interrupt the user's workflow"
```

---

## UI blueprint template

```yaml
ui_blueprint:
  version: "1.0"
  tokens:
    color:
      action:
        primary: { value: "{color.blue.600}", usage: "Primary interactive elements" }
        primary_hover: { value: "{color.blue.700}", usage: "Hover state for primary actions" }
      surface:
        default: { value: "{color.neutral.0}", usage: "Default page background" }
        elevated: { value: "{color.neutral.0}", usage: "Cards and elevated containers" }

  layout:
    grid:
      columns: { mobile: 4, tablet: 8, desktop: 12 }
      gutter: { mobile: "16px", tablet: "24px", desktop: "24px" }
    breakpoints:
      mobile: { max: "599px" }
      tablet: { min: "600px", max: "1023px" }
      desktop: { min: "1024px" }

  visual_rules:
    elevation:
      - level: 0
        shadow: "none"
        usage: "Flat elements on default surface"
      - level: 1
        shadow: "0 1px 3px rgba(0,0,0,0.12)"
        usage: "Cards, dropdowns, subtle lift"
```

---

## Content blueprint template

```yaml
content_blueprint:
  version: "1.0"
  voice:
    attributes: ["clear", "helpful", "respectful", "concise"]
    vocabulary:
      preferred:
        - { term: "sign in", not: "log in" }
        - { term: "select", not: "choose" }
      prohibited:
        - { term: "please", reason: "Implies the system is asking a favour" }

  tone:
    contexts:
      success: { tone: "warm, brief", example: "Changes saved." }
      error: { tone: "clear, actionable", example: "Card declined. Try a different payment method." }
      empty_state: { tone: "encouraging, guiding", example: "No projects yet. Create your first project to get started." }

  patterns:
    button_labels:
      format: "Verb + noun (when noun adds clarity)"
      max_length: 25
      examples: ["Save changes", "Create project", "Delete", "Cancel"]
    error_messages:
      format: "What happened + what to do"
      examples:
        - { bad: "Error 403", good: "You don't have access to this page. Ask your admin for permission." }
```

---

## Accessibility blueprint template

```yaml
accessibility_blueprint:
  version: "1.0"
  component_contracts:
    modal_dialog:
      role: "dialog"
      aria_required: ["aria-labelledby", "aria-modal"]
      keyboard:
        - { key: "Escape", action: "Close dialog, return focus to trigger" }
        - { key: "Tab", action: "Cycle focus within dialog (trap)" }
      focus:
        on_open: "First focusable element or close button"
        on_close: "Element that triggered the dialog"
      announcements:
        on_open: "Dialog title announced via aria-labelledby"

  system_rules:
    focus_visible:
      style: "2px solid {color.focus.ring}, 2px offset"
      applies_to: "All interactive elements"
    colour_contrast:
      text_on_surface: "4.5:1 minimum (AA)"
      large_text: "3:1 minimum"
      interactive_elements: "3:1 minimum against adjacent colours"
    motion:
      max_duration: "300ms for UI transitions"
      reduced_motion: "Respect prefers-reduced-motion: honour the media query for all animations"
```

---

## Ethical blueprint template

```yaml
ethical_blueprint:
  version: "1.0"
  prohibitions:
    - pattern: "Confirmshaming"
      rule: "Decline options must use neutral language"
      bad_example: "No thanks, I don't want to save money"
      good_example: "No thanks"
    - pattern: "Forced continuity"
      rule: "Cancellation flow must require equal or fewer steps than sign-up"

  inclusive_design:
    name_inputs:
      min_length: 1
      max_length: 256
      character_support: "Full Unicode"
      required_fields: ["display name"]
      optional_fields: ["first name", "last name"]
      notes: "Do not require first/last name split. Single name field with optional components."
    gender:
      rule: "Never require binary gender selection"
      pattern: "Open text field with optional common selections"

  data_privacy:
    consent:
      marketing_email: "Explicit opt-in required"
      analytics: "Informed opt-out permitted"
      third_party_sharing: "Explicit opt-in required per third party"
```

---

## Technical blueprint template

```yaml
technical_blueprint:
  version: "1.0"
  component_contracts:
    Button:
      props:
        - { name: "variant", type: "'primary' | 'secondary' | 'ghost'", default: "'primary'", required: false }
        - { name: "size", type: "'sm' | 'md' | 'lg'", default: "'md'", required: false }
        - { name: "disabled", type: "boolean", default: "false", required: false }
        - { name: "onClick", type: "(event: MouseEvent) => void", required: false }
        - { name: "children", type: "ReactNode", required: true }
      ref_forwarding: true
      polymorphic: { as_prop: true, default_element: "button" }

  composition:
    rules:
      - parent: "Form"
        valid_children: ["FormField", "FormSection", "Button"]
        invalid_children: ["Modal", "Toast"]
      - parent: "Card"
        valid_children: ["CardHeader", "CardBody", "CardFooter"]
        notes: "Direct children must be Card sub-components"

  performance:
    bundle_budget:
      per_component: "10KB gzipped maximum"
      total_library: "100KB gzipped maximum"
    ssr: "All components must render without window/document access"
```

---

## Business intelligence blueprint template

```yaml
business_intelligence_blueprint:
  version: "1.0"
  component_outcomes:
    primary_cta:
      business_function: "conversion"
      primary_metric: "click-through rate"
      secondary_metrics: ["form completion rate", "session conversion rate"]
      anti_metrics: ["Do not optimise click-through at the expense of user trust"]
    onboarding_flow:
      business_function: "activation"
      primary_metric: "onboarding completion rate"
      secondary_metrics: ["time to first value", "7-day retention"]

  experimentation:
    safe_to_test: ["button copy", "CTA colour within brand palette", "illustration choice"]
    never_test: ["removing accessibility features", "hiding cancellation options", "dark patterns"]
    requires_review: ["layout changes", "navigation restructuring", "form flow changes"]

  analytics:
    required_events:
      - { event: "component_render", data: ["component_name", "variant", "page"] }
      - { event: "component_interaction", data: ["component_name", "interaction_type", "outcome"] }
      - { event: "component_error", data: ["component_name", "error_type", "user_action"] }
```

---

## Engine manifest template

```yaml
context_engine:
  version: "1.0"
  generated: "[date]"
  system_name: "[design system name]"
  blueprints:
    - id: ux
      file: ux-blueprint.yml
      coverage: "[percentage of patterns documented]"
    - id: ui
      file: ui-blueprint.yml
      coverage: "[percentage of tokens and rules documented]"
    - id: content
      file: content-blueprint.yml
      coverage: "[percentage of content patterns documented]"
    - id: accessibility
      file: accessibility-blueprint.yml
      coverage: "[percentage of components with a11y contracts]"
    - id: ethical
      file: ethical-blueprint.yml
      coverage: "[percentage of ethical rules documented]"
    - id: technical
      file: technical-blueprint.yml
      coverage: "[percentage of component APIs documented]"
    - id: business_intelligence
      file: business-intelligence-blueprint.yml
      coverage: "[percentage of components with outcome mapping]"
  total_coverage: "[weighted average across blueprints]"
```

---

## Usage guide template

The context engine includes a `usage-guide.md` that teaches AI agents how to consume the engine:

### Loading the engine

Load `engine-manifest.yml` first. It provides the list of blueprints, their coverage levels, and their file locations.

### Blueprint selection by task

Not every task requires every blueprint. Load blueprints based on the task:

| Task type | Required blueprints |
|---|---|
| Generate a component | technical, ui, accessibility |
| Write UI copy | content, ethical |
| Build a page layout | ux, ui, technical |
| Create a form | ux, accessibility, content, technical |
| Review for compliance | ethical, accessibility |
| Assess business impact | business_intelligence |
| Full design review | all blueprints |

### Query patterns

- **"How should [component] behave?"** → Load ux-blueprint.yml → patterns → [component]
- **"What tokens apply to [element]?"** → Load ui-blueprint.yml → tokens → [category]
- **"What copy should [element] use?"** → Load content-blueprint.yml → patterns → [element type]
- **"Is [pattern] accessible?"** → Load accessibility-blueprint.yml → component_contracts → [pattern]
- **"Is [pattern] ethical?"** → Load ethical-blueprint.yml → prohibitions and inclusive_design
