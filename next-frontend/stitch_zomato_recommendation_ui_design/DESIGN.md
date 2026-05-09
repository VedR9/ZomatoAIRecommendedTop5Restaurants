---
name: Vibrant Cravings
colors:
  surface: '#fbf9f8'
  surface-dim: '#dbdad9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#efeded'
  surface-container-high: '#e9e8e7'
  surface-container-highest: '#e4e2e2'
  on-surface: '#1b1c1c'
  on-surface-variant: '#5b403f'
  inverse-surface: '#303031'
  inverse-on-surface: '#f2f0f0'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#5b5c5c'
  on-tertiary: '#ffffff'
  tertiary-container: '#737575'
  on-tertiary-container: '#fcfcfc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e2'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The brand personality of the design system is energetic, appetizing, and hyper-reliable. It is designed to evoke the immediate sensory delight of food through high-velocity interactions and bold visual cues. The target audience is the urban explorer—users who value speed, visual clarity, and trustworthy recommendations.

The design style follows a **Modern / Minimalist** approach with a heavy emphasis on **High-Contrast** elements. It utilizes significant whitespace to let high-quality food photography act as the primary texture, while using vibrant red accents to drive action and urgency. Elements are treated with soft, tactile edges to remain approachable, but the information density is optimized for quick scanning and decision-making.

## Colors

The palette is anchored by the signature primary red, which serves as the "appetite trigger" and the primary color for calls to action. White (#FFFFFF) is the structural foundation, providing a clean canvas that ensures food photography pops without distraction.

- **Primary (#E23744):** Used for buttons, price points, and critical brand moments.
- **Deep Grey (#2D2D2D):** The primary color for headlines and heavy body text to ensure maximum legibility and a premium feel.
- **Medium Grey (#696969):** Utilized for secondary information, metadata, and iconography.
- **Soft Light Grey (#F4F4F4):** Used for background containers and subtle dividers to create depth without using heavy lines.

## Typography

This design system utilizes **Plus Jakarta Sans** for its structural and headline elements due to its modern, geometric, and friendly character. It strikes the perfect balance between professional utility and an inviting, optimistic aesthetic.

For labels and metadata, **Be Vietnam Pro** is used to provide a slightly more contemporary and warm feel in dense information areas. Typography should always favor high contrast against the background. Headlines use a tight letter-spacing to appear bold and editorial, while body text maintains generous line height for effortless readability during a hungry search.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a standard 12-column structure for desktop and a single or double-column structure for mobile. A strict 8px-based spacing system (with 4px increments for micro-adjustments) ensures a rhythmic and predictable flow.

- **Content Width:** Mobile uses 16px side margins; Desktop scales with a maximum container width of 1200px.
- **Gutters:** Standard 16px gutters are used between cards to maintain a dense but breathable catalog feel.
- **Vertical Rhythm:** Generous padding (32px to 48px) is applied between major sections to prevent visual fatigue.

## Elevation & Depth

Depth in this design system is created through **Tonal Layers** and **Ambient Shadows**. Instead of harsh borders, surfaces are differentiated by subtle shifts in background color (e.g., placing a white card on a #F4F4F4 background).

Where shadows are necessary for interaction, they should be "delicious"—extra-diffused, low-opacity, and slightly tinted with the primary red or a warm grey. 
- **Resting state:** No shadow or a very soft 4px blur.
- **Hover/Active state:** A medium-diffused shadow (12px blur, 8% opacity) to make cards feel like they are lifting off the page.

## Shapes

The shape language is consistently **Rounded**. Soft edges are used to mirror the organic nature of food and to make the interface feel safe and welcoming. 

- **Standard Elements:** Buttons and input fields use a 0.5rem (8px) radius.
- **Container Elements:** Food cards and restaurant banners use a 1rem (16px) radius to create a soft, framed look for photography.
- **Badges/Chips:** Use a fully rounded pill shape to differentiate them from functional buttons.

## Components

- **Buttons:** Primary buttons are solid #E23744 with white text, utilizing the `rounded-lg` (16px) or `rounded` (8px) corners. Secondary buttons use a transparent background with a 1px #E23744 border.
- **Cards:** The "Restaurant Card" is the hero component. It features a top-aligned image with a 1:1 or 4:3 aspect ratio, followed by a headline and a secondary row for ratings and delivery time.
- **Chips:** Used for cuisine filters (e.g., "Italian", "Fast Food"). These are pill-shaped with light grey backgrounds that turn primary red when selected.
- **Inputs:** Search bars should be prominent, featuring a soft shadow and a 16px border radius to encourage user interaction.
- **Ratings Badge:** Always displayed in a high-contrast green box or with a gold star icon, positioned in the top right of food cards for instant recognition.
- **Food Photography:** Images should be high-saturation, close-up, and utilize natural lighting to look appetizing. Avoid flat, clinical studio shots.