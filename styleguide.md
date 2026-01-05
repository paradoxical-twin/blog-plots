# Plot Style Guide

Based on the visual language of entropicthoughts.com. Designed for clean, academic-quality data visualization that prioritizes readability and minimalism.

---

## Core Philosophy

- **Minimal decoration**: Remove anything that doesn't convey information
- **Let data breathe**: Generous whitespace, no visual clutter
- **Muted palette**: Earth tones that don't compete with the data
- **Readable at small sizes**: Works well in blog column width (~600-700px)

---

## Color Palette

### Primary Fill Color
```
fill: #D4C4B0  (warm beige/tan)
```
Alternative formulations:
- RGB: `212, 196, 176`
- HSL: `33°, 30%, 76%`

This is the signature fill color for areas, distributions, bars, etc.

### Lines and Text
```
stroke: #000000  (black)
text: #000000    (black)
axis: #000000    (black)
```

### Transparency
- Use `opacity: 0.85-0.95` for fills where overlap might occur
- For ridge plots: higher opacity is fine since they're stacked vertically

### Secondary/Accent Colors (if needed for multiple series)
Avoid unless necessary. If multiple series are required:
- Keep them in the same warm/muted family
- Consider using line styles (dashed, dotted) instead of colors
- Grey (`#666666`) for secondary reference lines

---

## Typography

### Font Family
```
font-family: "Charter", Georgia, "Times New Roman", serif
```
Charter is the site's body font. Use this exact stack for consistency with surrounding text.

**Note on SVG font rendering**: If Charter isn't installed on the viewer's system, it falls back through the stack. For critical plots, consider converting text to paths on export (loses editability but guarantees appearance).

### Font Sizes (for ~600px wide plots)
- **Title**: 14-16px, regular weight
- **Axis labels**: 11-12px, regular weight
- **Tick labels**: 10-11px, regular weight
- **Annotations**: 10-11px

### Text Positioning
- Titles: Top-left aligned, above the plot area
- Y-axis labels: Right-aligned, adjacent to axis (or as row labels for ridge plots)
- X-axis labels: Centered below ticks

---

## Axes and Grid

### Axes
- **Stroke width**: 0.5-1px
- **Color**: Black
- **Style**: Simple lines, no arrow heads
- **Spines**: Only show bottom (x) and left (y) spines. Remove top and right.

### Ticks
- **Length**: 4-5px
- **Direction**: Outward from plot area
- **Stroke width**: 0.5-1px

### Grid Lines
- **Default**: No grid lines
- **If absolutely necessary**: Very light grey (#CCCCCC), 0.5px, dashed

### Axis Limits
- Extend slightly beyond data range for breathing room
- Use "nice" round numbers for tick positions (0, 0.25, 0.5, 0.75, 1.0)

---

## Plot-Specific Guidelines

### Ridge Plots / Joy Plots
```
- Vertical stacking with consistent spacing
- Labels on right side of each ridge
- Fill color: #D4C4B0
- Stroke: Black, 1px
- Baseline: Thin black line at y=0 for each ridge
- Overlap: Slight overlap between adjacent ridges acceptable
- Reference line: Vertical black line at key value (e.g., x=1.0) if needed
```

### Line Charts / Time Series
```
- Line stroke: Black, 1-1.5px
- Area fill (if used): #D4C4B0 with slight transparency
- Points: Generally omit unless highlighting specific values
- If points needed: Small circles, 3-4px diameter, filled black
```

### Control Charts (XmR / Process Behavior Charts)
```
- Data line: Black, connected points
- Points: Small black circles (3px)
- Center line (mean): Black, solid, 1px
- Control limits: Black, 1px
- Optional: Light fill between control limits
- No grid lines
```

### Bar Charts
```
- Fill: #D4C4B0
- Border: Black, 0.5-1px
- Spacing: Gap between bars ~20-30% of bar width
- Horizontal orientation often preferred for categorical data with labels
```

### Histograms
```
- Fill: #D4C4B0
- Border: Black, 0.5px
- No gaps between bins
- Overlay: If showing theoretical distribution, use black line (no fill)
```

### Scatter Plots
```
- Points: Black circles, 3-5px diameter
- Fill: Black or #D4C4B0 with black stroke
- For many points: Consider reducing opacity
- Trend/fit lines: Solid black, 1px
```

---

## Layout and Dimensions

### Aspect Ratio
- Default: ~3:2 (width:height) for most plots
- Tall plots (ridge plots): Determined by number of series
- Time series: Can go wider (~2:1)

### Margins
- **Top**: 30-40px (space for title)
- **Right**: 80-120px (space for right-aligned labels)
- **Bottom**: 40-50px (space for x-axis label and ticks)
- **Left**: 50-60px (space for y-axis ticks)

Adjust based on label length.

### Plot Width
- Target: 600-700px for blog display
- SVG output preferred for crisp scaling

---

## Reference Lines and Annotations

### Vertical/Horizontal Reference Lines
```
- Color: Black
- Stroke width: 1px
- Style: Solid (not dashed, unless for different meaning)
```

### Direct Labeling
- Prefer labeling data directly over using legends
- Place labels close to the data they describe
- Use consistent positioning (e.g., all labels right-aligned)

### Legends
- Avoid if possible through direct labeling
- If necessary: Minimal, positioned inside plot area or below
- No border/box around legend

---

## Output Format

### SVG (Default)
- **Use for**: Most plots—line charts, bar charts, ridge plots, control charts, anything with <1000 elements
- **Advantages**: Crisp at any scale, small file size, editable
- **Font handling options**:
  1. Accept fallback (usually fine—Charter fallback stack is decent)
  2. Convert text to paths on export (guarantees appearance, loses editability)
  3. Embed font subset (bloats file, use sparingly)

### PNG (When Needed)
- **Use for**: Scatter plots with many points, heatmaps, anything with >1000 elements
- **Export at 2x resolution** for retina displays (e.g., 1200px wide for 600px display width)
- Guarantees pixel-perfect font rendering without embedding

### Filename Convention
```
descriptive-name-NN.svg  (or .png)
```

### GitHub Pages Notes
- SVG serves fine, no special configuration needed
- Consider adding `width` attribute to `<img>` tags to prevent layout shift

---

## Implementation Notes

### Python (Matplotlib)

```python
import matplotlib.pyplot as plt

# Style setup
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Charter', 'Georgia', 'Times New Roman'],
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.edgecolor': 'black',
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': False,
})

FILL_COLOR = '#D4C4B0'
LINE_COLOR = 'black'
```

**Note**: Matplotlib needs Charter installed on your system. On Linux: `apt install fonts-charter` or grab from Font Squirrel.

### R (ggplot2)

```r
library(ggplot2)

theme_entropic <- theme_minimal() +
  theme(
    text = element_text(family = "Charter", size = 11),
    panel.grid = element_blank(),
    panel.border = element_blank(),
    axis.line = element_line(color = "black", linewidth = 0.5),
    axis.ticks = element_line(color = "black", linewidth = 0.5),
    axis.ticks.length = unit(4, "pt"),
    plot.title = element_text(size = 14, hjust = 0),
    legend.position = "none"
  )

fill_color <- "#D4C4B0"
```

**Note**: May need `extrafont` or `showtext` package to use Charter in R. `showtext` is easier: `font_add_google()` won't work for Charter, but `font_add("Charter", "/path/to/Charter.ttf")` will.

### Observable / D3.js

```javascript
const FILL_COLOR = "#D4C4B0";
const LINE_COLOR = "#000000";
const FONT_FAMILY = '"Charter", Georgia, "Times New Roman", serif';

// Remove default axis domain styling, add custom
```

---

## Quick Reference Checklist

Before finalizing any plot:

- [ ] Top and right spines removed
- [ ] No grid lines (unless specifically needed)
- [ ] Fill color is #D4C4B0
- [ ] All lines/strokes are black
- [ ] Font is Charter (with proper fallback stack)
- [ ] Title is left-aligned above plot
- [ ] Data is directly labeled where possible (no legend)
- [ ] Axis ticks point outward
- [ ] Tick values are "nice" round numbers
- [ ] Sufficient whitespace/margins
- [ ] Output is SVG (or PNG at 2x if >1000 elements)

---

## Examples Reference

Common plot types seen on entropicthoughts.com:

1. **Ridge plots**: LLM benchmark comparisons
2. **XmR control charts**: Process behavior analysis  
3. **Line charts with shaded area**: Theoretical vs. empirical distributions
4. **Scatter with trend**: Performance vs. cost analyses
5. **Simple bar charts**: Coefficient comparisons
6. **Histograms with overlay**: CLT convergence demonstrations

---

*Last updated: January 2026*
*Source aesthetic: entropicthoughts.com*
