<!-- auto-generated from 5-disable-oled-animation.json — do not edit manually -->

# Disable all animated widgets (Bongo Cat, peripheral cat) on OLED displays across all shields (corne, sofle, lily58, splitkb_aurora_sofle)

- [x] Disable Bongo Cat and peripheral animation in corne.conf `(8f95ef9b)`
      In config/corne.conf, in the ### OLED DISPLAY section (around line 102), add three lines right after the existing CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      Explanations:
      - WPM_BONGO_CAT=n: disables the animated bongo cat on the central (left) side
      - WPM_NUMBER=y: replaces the now-empty WPM area with a plain number readout showing current WPM. Without this, the WPM area is completely blank because speedometer and graph are both off by default and the graph is also blocked by MODIFIERS_INDICATORS_FIXED=y (layout constraint).
      - ANIMATION_PERIPHERAL=n: disables the looping cat animation on the peripheral (right) side
  - ⚙️ [x] Added three lines after CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n: `(a2dc355c)`
    - CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n (disables animated bongo cat on central side)
    - CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y (replaces empty WPM area with plain number)
    - CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n (disables looping cat animation on peripheral side)
    - 📋 Verified: config/corne.conf lines 107-109 contain all three required configs after CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n in the OLED DISPLAY section. WPM_BONGO_CAT=n, WPM_NUMBER=y, ANIMATION_PERIPHERAL=n — all present and correct. `(819412da)`
- [x] Disable Bongo Cat and peripheral animation in sofle.conf `(ea7d1c8d)`
      In config/sofle.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      Note: sofle.conf does not have a pre-existing CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n line, so these will be the first nice_oled widget animation overrides. WPM_NUMBER=y is needed to avoid empty space where bongo cat was (see corne task for full explanation).
  - ⚙️ [x] Added three lines after CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y in the ### OLED DISPLAY section: `(e98d8dd7)`
    - CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
    - CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
    - CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
    - 📋 Verified: config/sofle.conf lines 108-110 contain all three required configs in the OLED DISPLAY section. WPM_BONGO_CAT=n, WPM_NUMBER=y, ANIMATION_PERIPHERAL=n — all present and correct. `(0ef5861a)`
- [x] Disable Bongo Cat and peripheral animation in lily58.conf `(a4f150ba)`
      In config/lily58.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      WPM_NUMBER=y is needed to avoid empty space where bongo cat was.
  - ⚙️ [x] Added three lines after CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y in the ### OLED DISPLAY section: `(c252f5ae)`
    - CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
    - CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
    - CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
    - 📋 Verified: config/lily58.conf lines 114-116 contain all three required configs in the OLED DISPLAY section. WPM_BONGO_CAT=n, WPM_NUMBER=y, ANIMATION_PERIPHERAL=n — all present and correct. `(c5e295c3)`
- [x] Disable Bongo Cat and peripheral animation in splitkb_aurora_sofle.conf `(b4d3b931)`
      In config/splitkb_aurora_sofle.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      WPM_NUMBER=y is needed to avoid empty space where bongo cat was.
  - ⚙️ [x] Added three lines after CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y in the ### OLED DISPLAY section: `(fb9aaceb)`
    - CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
    - CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
    - CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
    - 📋 Verified: config/splitkb_aurora_sofle.conf lines 108-110 contain all three required configs in the OLED DISPLAY section. WPM_BONGO_CAT=n, WPM_NUMBER=y, ANIMATION_PERIPHERAL=n — all present and correct. `(10e43723)`
