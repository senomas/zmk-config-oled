<!-- auto-generated from 6-set-sleep-timeout-1hour.json — do not edit manually -->

# Set CONFIG_ZMK_IDLE_SLEEP_TIMEOUT to 1 hour (3600000ms) across all board configs

- [ ] Update IDLE_SLEEP_TIMEOUT in all board .conf files
      In each of these files:
      - config/corne.conf
      - config/lily58.conf
      - config/sofle.conf
      - config/splitkb_aurora_sofle.conf
      
      Replace the commented-out CONFIG_ZMK_IDLE_SLEEP_TIMEOUT lines (both the 900000 and 1800000 variants) with a single active line:
      
          CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=3600000
      
      Also consider whether CONFIG_ZMK_IDLE_TIMEOUT should be set explicitly (currently commented out). If IDLE_TIMEOUT remains unset, ZMK defaults to 30 minutes — meaning the keyboard would go idle at 30 min and deep sleep 30 min later (1 hour total). If the intent is deep sleep after 1 hour of total inactivity regardless of idle, no IDLE_TIMEOUT change is needed. If the intent is idle earlier (e.g. 1-2 min), uncomment and set it too.
      
      Remove the alternate 30-minute variant line entirely rather than leaving commented-out cruft.
