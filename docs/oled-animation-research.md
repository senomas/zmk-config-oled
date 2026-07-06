# OLED Animation Research — zmk-nice-oled

## Overview

The project uses the `zmk-nice-oled` module (from `mctechnology17/zmk-nice-oled`, revision `main`)
as a Zephyr module, defined in `config/west.yml`. This module provides a custom status screen with
widgets including animated characters.

The shield `nice_oled` is applied on top of `corne_left`/`corne_right` in `build.yaml`:
```yaml
- board: nice_nano_v2
  shield: corne_left nice_oled
```

## Animation Widgets Inventory

All Kconfig options are defined in:
`.zmk-workspace/zmk-nice-oled/boards/shields/nice_oled/Kconfig.defconfig`

### 1. Bongo Cat (WPM-triggered) — central side

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT` | `y` | Animated bongo cat that taps with WPM |
| `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT_ANIMATION_MS` | `300` | Frame interval in ms |

Bongo Cat is mutually exclusive with Luna in the WPM widget — only one can be active at a time
(see `screen.c` init: Luna checked first via `#elif`).

### 2. Luna (WPM-triggered) — central side

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_WPM_LUNA` | `n` | Animated Luna pet (dog) |
| `CONFIG_NICE_OLED_WIDGET_WPM_LUNA_ANIMATION_MS` | `300` | Frame interval |

**Already set to `n`** in all `.conf` files.

### 3. Peripheral Animation — right/slave side

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL` | `y` | Enable animation on peripheral half |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT` | `y` | Cat animation (default choice) |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_GEM` | `n` | Gem animation |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_HEAD` | `n` | Head animation |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_POKEMON` | `n` | Pokemon animation |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_SPACEMAN` | `n` | Spaceman animation |
| `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_MS` | varies | Frame interval |

Implemented in `widgets/screen_peripheral.c` / `widgets/animation.c`.

### 4. HID Indicators Luna/Bongo Cat — central side

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_LUNA` | `n` | Luna reacts to CapsLock/NumLock |
| `CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT` | `n` | Bongo cat reacts to CapsLock/NumLock |

Both default to `n` — **not active**.

### 5. Modifiers Indicators Luna/Bongo Cat — central side

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_LUNA` | `n` | Luna reacts to modifiers |
| `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_BONGO_CAT` | `n` | Bongo cat reacts to modifiers |

Both default to `n` — **not active**.

### 6. Responsive Bongo Cat

| Kconfig | Default | Description |
|---------|---------|-------------|
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE` | `n` | Responsive mode (needs more resources) |
| `CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT` | `n` | Responsive bongo cat |

Both default to `n` — **not active**.

## Current Effective State

From what is configured in `config/corne.conf` (and the three other shield `.conf` files):

| Animation | Status | Why |
|-----------|--------|-----|
| **Bongo Cat (WPM)** | **ACTIVE** | `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT` defaults to `y`, not overridden |
| Luna (WPM) | Disabled | `CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n` in corne.conf |
| **Peripheral Cat** | **ACTIVE** | `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL` defaults to `y` |
| HID Indicators | Disabled | Both default to `n` |
| Modifiers Indicators | Disabled | Both default to `n` |
| Responsive Bongo Cat | Disabled | Both default to `n` |

## How to Disable Animations

### Option A: Disable all animations, keep static widgets (RECOMMENDED)

In each `.conf` file (`config/corne.conf`, `config/sofle.conf`, `config/lily58.conf`,
`config/splitkb_aurora_sofle.conf`):

```ini
# Disable animated characters
CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n            # already set in corne.conf
CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
# Show WPM as plain number (replaces empty space left by bongo cat)
CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
```

**Why `WPM_NUMBER=y` is needed**: With the current defaults, the WPM area is rendered
entirely by Bongo Cat. Speedometer (`WPM_SPEEDOMETER`) defaults to `n` on OLED, and the
WPM graph (`WPM_GRAPH`) is blocked by a preprocessor condition in `wpm.c` that skips it
when `MODIFIERS_INDICATORS_FIXED=y` (no room on the 128px canvas). Without Bongo Cat and
without `WPM_NUMBER`, the WPM area is completely blank.

### Option B: Disable WPM widget entirely (removes both animation and gauge)

```ini
CONFIG_NICE_OLED_WIDGET_WPM=n
CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
```

### Option C: Replace Bongo Cat with static Luna (if Luna is less "animated")

Luna is not purely static — it's still frame-based animation. For truly no animation, use Option A.

## Performance Impact

- `CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT` → enables `LV_USE_ANIMIMG` and `LV_USE_ANIMATION` via the
  `NICE_OLED_WIDGET_STATUS` select chain. Disabling Bongo Cat alone may NOT remove the LVGL
  animation dependency if the peripheral animation is still active.
- `CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n` → if set alongside Bongo Cat disabled, this
  removes the last consumer of `LV_USE_ANIMIMG`. The Kconfig might still select it transitively
  through `NICE_OLED_WIDGET_STATUS`, but this is harmless.

## Can the right side show modifiers and layer?

**No — not with config changes alone.** The peripheral (right) half runs completely different
code (`screen_peripheral.c`, compiled via CMakeLists.txt `else` branch for non-central).
The peripheral firmware does NOT have access to:

- **Layer state**: only `zmk_keymap_highest_layer_active()` is available on the central
- **HID modifier state**: only `zmk_hid_get_explicit_mods()` is available on the central

These aren't synced across the BLE split connection. The peripheral only knows:
battery level, USB presence, and split connection status.

Adding mods/layer to the right side would require:
1. Forking ZMK to add custom split transport messages for layer + HID modifier state
2. Modifying `screen_peripheral.c` to include and render those widgets
3. Modifying `CMakeLists.txt` to compile layer/modifier sources for peripheral

This is firmware-level work, not a zmk-config change.

## Files to Modify

- `config/corne.conf`
- `config/sofle.conf`
- `config/lily58.conf`
- `config/splitkb_aurora_sofle.conf`

Each needs the same 3 lines added in the `### OLED DISPLAY` section.
