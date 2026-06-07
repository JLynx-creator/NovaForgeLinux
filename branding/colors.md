# NovaForge Linux — Color Palette & Brand Guide

## Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Cyan Neon** | `#00E5FF` | `0, 229, 255` | Primary accent, links, active states, selection highlights |
| **Electric Purple** | `#7C3AED` | `124, 58, 237` | Secondary accent, gradients, hover states |
| **Amber Glow** | `#F59E0B` | `245, 158, 11` | Warnings, notifications, tertiary accent |

## Background Scale (Dark → Light)

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Void** | `#0A0A1A` | `10, 10, 26` | Deepest background, GRUB, boot |
| **Midnight** | `#11111B` | `17, 17, 27` | Primary background, window bg |
| **Obsidian** | `#1E1E2E` | `30, 30, 46` | Secondary background, panels |
| **Slate** | `#313244` | `49, 50, 68` | Elevated surfaces, cards |
| **Storm** | `#45475A` | `69, 71, 90` | Borders, dividers |

## Text Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Snow** | `#CDD6F4` | `205, 214, 244` | Primary text |
| **Mist** | `#7F849C` | `127, 132, 156` | Secondary text, labels |
| **Ghost** | `#585B70` | `88, 91, 112` | Disabled text, placeholders |

## Semantic Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Success** | `#A6E3A1` | `166, 227, 161` | Success states, confirmations |
| **Warning** | `#F9E2AF` | `249, 226, 175` | Warning states |
| **Error** | `#F38BA8` | `243, 139, 168` | Error states, destructive actions |
| **Info** | `#89B4FA` | `137, 180, 250` | Informational states |

## Terminal Colors (ANSI)

| Index | Normal | Bright | Name |
|-------|--------|--------|------|
| 0 | `#45475A` | `#585B70` | Black |
| 1 | `#F38BA8` | `#F38BA8` | Red |
| 2 | `#A6E3A1` | `#A6E3A1` | Green |
| 3 | `#F9E2AF` | `#F9E2AF` | Yellow |
| 4 | `#00E5FF` | `#89B4FA` | Blue |
| 5 | `#CBA6F7` | `#CBA6F7` | Magenta |
| 6 | `#94E2D5` | `#94E2D5` | Cyan |
| 7 | `#BAC2DE` | `#A6ADC8` | White |

## Typography

| Usage | Font | Weight | Size |
|-------|------|--------|------|
| UI Text | Inter | Regular (400) | 10pt |
| UI Bold | Inter | Semi-Bold (600) | 10pt |
| Menu | Inter | Regular (400) | 10pt |
| Small | Inter | Regular (400) | 8pt |
| Toolbar | Inter | Regular (400) | 9pt |
| Monospace | JetBrains Mono | Regular (400) | 11pt |
| Terminal | JetBrains Mono | Regular (400) | 11pt |

## Gradient Recipes

### Hero Gradient
```css
background: linear-gradient(135deg, #0A0A1A 0%, #1E1E2E 50%, #11111B 100%);
```

### Accent Gradient
```css
background: linear-gradient(135deg, #00E5FF 0%, #7C3AED 100%);
```

### Subtle Glow
```css
box-shadow: 0 0 20px rgba(0, 229, 255, 0.15);
```
