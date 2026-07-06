<!-- auto-generated from 5-disable-oled-animation.json — do not edit manually -->

# Disable all animated widgets (Bongo Cat, peripheral cat) on OLED displays across all shields (corne, sofle, lily58, splitkb_aurora_sofle)

- [ ] Disable Bongo Cat and peripheral animation in corne.conf
      In config/corne.conf, in the ### OLED DISPLAY section (around line 102), add three lines right after the existing CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      Explanations:
      - WPM_BONGO_CAT=n: disables the animated bongo cat on the central (left) side
      - WPM_NUMBER=y: replaces the now-empty WPM area with a plain number readout showing current WPM. Without this, the WPM area is completely blank because speedometer and graph are both off by default and the graph is also blocked by MODIFIERS_INDICATORS_FIXED=y (layout constraint).
      - ANIMATION_PERIPHERAL=n: disables the looping cat animation on the peripheral (right) side
- [ ] Disable Bongo Cat and peripheral animation in sofle.conf
      In config/sofle.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      Note: sofle.conf does not have a pre-existing CONFIG_NICE_OLED_WIDGET_WPM_LUNA=n line, so these will be the first nice_oled widget animation overrides. WPM_NUMBER=y is needed to avoid empty space where bongo cat was (see corne task for full explanation).
- [ ] Disable Bongo Cat and peripheral animation in lily58.conf
      In config/lily58.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      WPM_NUMBER=y is needed to avoid empty space where bongo cat was.
- [ ] Disable Bongo Cat and peripheral animation in splitkb_aurora_sofle.conf
      In config/splitkb_aurora_sofle.conf, in the ### OLED DISPLAY section, add:
      
      CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT=n
      CONFIG_NICE_OLED_WIDGET_WPM_NUMBER=y
      CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL=n
      
      WPM_NUMBER=y is needed to avoid empty space where bongo cat was.
