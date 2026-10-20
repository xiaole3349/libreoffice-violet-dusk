# Violet Dusk — LibreOffice dark chrome + light violet canvas

[简体中文](README.md) · **English**

An appearance theme for **LibreOffice 25.2+**: deep violet chrome (`#343061`) with pure white text, a light violet document canvas (`#F4F1FD`) with dark ink text, and a `#8B79E8` cell locator — all taken from the same violet family.

It ships as a standard `.oxt` extension (double-click to install) plus a matching `.soc` palette for use inside documents.

```
Chrome      AppBackground / WindowColor / FaceColor   #343061
Menu bar    MenuBarColor                              #343061
Nav text    MenuBarTextColor / WindowTextColor        #FFFFFF
Cells       DocColor                                  #F4F1FD
Grid        CalcGrid                                  #D9D1F2
Body text   CalcText / FontColor                      #241F3D
Locator     CalcCellFocus                             #8B79E8
```

## Installation

**Option 1 — double-click (recommended)**

1. Quit LibreOffice completely (including the quickstarter in the system tray; no `soffice.bin` should remain in Task Manager).
2. Double-click `dist/Violet-Dusk-1.1.0.oxt` and confirm the installation.
3. Restart LibreOffice.
4. Go to `Tools → Options → LibreOffice → Appearance`, pick **Violet Dusk** from the theme dropdown and enable **Use application theme**.

**Option 2 — command line**

```bash
# Windows
"C:\Program Files\LibreOffice\program\unopkg.exe" add "Violet-Dusk-1.1.0.oxt"

# Linux / macOS
unopkg add Violet-Dusk-1.1.0.oxt
```

The extension contains no absolute paths, so it can be deployed across machines. On a fresh profile the theme is selected automatically.

**Palette (optional)**

`Tools → Options → LibreOffice → Colors → Open`, then choose `dist/Violet-Dusk-palette.soc`. All 23 colors — including the `#F4F1FD` canvas and `#8B79E8` locator — become available in every color picker (cell background, font color, chart colors, …).

## Configuration reference

Every color lives under the same configuration path; values are decimal RRGGBB integers:

```
org.openoffice.Office.UI / ColorScheme / ColorSchemes / Violet Dusk / <entry> / Color
```

### Chrome

| Entry | Applies to | Value |
|---|---|---|
| `AppBackground` | Application background around documents | `#343061` |
| `WindowColor` | Windows and toolbar background | `#343061` |
| `FaceColor` | Toolbar and dialog faces | `#343061` |
| `BaseColor` | Base widget color | `#343061` |
| `MenuBarColor` | Menu bar background | `#343061` |
| `MenuColor` | Dropdown menu background | `#2C2953` |
| `MenuBarTextColor` | Menu bar text | `#FFFFFF` |
| `MenuTextColor` | Dropdown menu text | `#FFFFFF` |
| `WindowTextColor` | Toolbar / window text | `#FFFFFF` |
| `MenuBarHighlightColor` / `MenuHighlightColor` | Hover and selection blocks | `#4A4494` |
| `ActiveColor` | Button hover | `#423D7A` |
| `SeparatorColor` | Separators and borders | `#4A4685` |
| `DisabledTextColor` | Disabled text | `#8B87B8` |
| `AccentColor` | Accent color | `#9B8CFF` |

### Document and cells

| Entry | Applies to | Value |
|---|---|---|
| `DocColor` | Cell / page background | `#F4F1FD` |
| `DocBoundaries` / `TableBoundaries` | Object and table boundaries | `#D9D1F2` |
| `CalcGrid` / `DrawGrid` | Grid lines | `#D9D1F2` |
| `CalcText` / `FontColor` | Cell text / body text | `#241F3D` |
| `CalcValue` | Numeric values | `#1F5AA8` |
| `CalcFormula` | Formulas | `#1F7A4C` |
| `CalcReference` | Reference highlights | `#A8387F` |
| `CalcCellFocus` / `CalcDBFocus` | Cell locator | `#8B79E8` |
| `CalcNotesBackground` / `CalcProtectedBackground` | Notes and protected areas | `#E9E3FA` |
| `Links` / `LinksVisited` | Links / visited links | `#1F5AA8` / `#6C4FC9` |
| `Author1`–`Author9` | Comment author colors | Dark variants of the same family |

All 93 entries are generated into `Theme.xcu` and match the `UI/ColorScheme` schema of LibreOffice 26.8 one-to-one.

## Contrast (WCAG 2.1)

| Foreground / background | Used for | Ratio |
|---|---|---|
| `#241F3D` / `#F4F1FD` | Cell and body text | **14.08:1** |
| `#FFFFFF` / `#343061` | Menu bar and toolbar | **12.06:1** |
| `#1F5AA8` / `#F4F1FD` | Values and links | 6.11:1 |
| `#6B5A00` / `#F4F1FD` | Strings | 6.10:1 |
| `#B3362F` / `#F4F1FD` | Spelling / errors | 5.41:1 |
| `#A8387F` / `#F4F1FD` | References | 5.33:1 |
| `#1F7A4C` / `#F4F1FD` | Formulas | 4.78:1 |
| `#8B79E8` / `#F4F1FD` | Locator (graphical, 3:1 threshold) | 3.14:1 |

## Building from source

Python 3 only — no third-party dependencies:

```bash
python build-violet-dusk-theme.py
```

Outputs `dist/Violet-Dusk-<version>.oxt`, `dist/Violet-Dusk-palette.soc` and `docs/导入说明.txt`.

To recolor, edit the three dictionaries at the top of the script — `UI` (chrome), `DOC` (document canvas) and `IDE` (Basic IDE) — and bump `THEME_VERSION` accordingly.

## Known limitations

- **`DocColor` is the global document background.** Changing it affects Calc cells, Writer pages and Draw pages alike; the theme framework has no separate "Calc cell background" entry.
- Do **not** enable **Use white document background** in the Appearance page — it forces a pure white canvas and cancels the light violet.
- An OS-level **high contrast mode** overrides every custom color.
- Requires **LibreOffice 25.2+**. Older versions lack the Appearance theme framework, so the theme will not appear in the dropdown.
- The Basic IDE stays dark (`#2B2852`); code editors do not suit a light canvas.

## Releasing

Pushing a tag triggers GitHub Actions, which builds the package and attaches the `.oxt` / `.soc` to a release:

```bash
git tag v1.1.0 && git push origin v1.1.0
```

If a release for that tag already exists, the workflow skips automatically to avoid duplicate artifacts.

## License

MIT — see `LICENSE`. Palette and implementation are original to this project.

---

[← 简体中文版](README.md)
