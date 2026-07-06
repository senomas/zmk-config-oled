<!-- auto-generated from 4-dockerize-keymap-drawer.json — do not edit manually -->

# Make keymap-drawer target run inside Docker instead of requiring host pipx

- [x] Rewrite keymap-drawer target to use docker run with pip install keymap-drawer
      Replace the host pipx check with a docker run that installs keymap-drawer via pip inside the zmk-build-arm container, mounts config/ and keymap-drawer/ dirs, and processes all *.keymap files in a single run.
  - ⚙️ [x] Done. Changes:
    - Added `.keymap-drawer-venv/` to `.gitignore`
    - Rewrote `keymap-drawer` target to use `python:3-slim` Docker image
    - Uses `PYTHONUSERBASE=/venv pip install --user` to install keymap-drawer into a host-cached directory (`.keymap-drawer-venv/`)
    - Sets `PYTHONPATH` so the `keymap` CLI can find its modules
    - Fixed `-c` flag placement: `-c config` goes before subcommand (`parse`/`draw`), `-c 12` (columns) goes after `parse`
    - Generates SVGs for all 4 keymaps (corne, lily58, sofle, splitkb_aurora_sofle)
    - 📋 All implementation claims verified:
      - `.keymap-drawer-venv/` in `.gitignore` ✓
      - Uses python:3-slim Docker image (lighter than zmk-build-arm — sensible deviation from the "zmk-build-arm container" mentioned in the task, since keymap-drawer is a pure Python tool) ✓
      - Host-cached venv via PYTHONUSERBASE=/venv pip install --user ✓
      - PYTHONPATH set for module resolution ✓
      - Correct -c flag placement (config before subcommand, columns after parse) ✓
      - Processes all 4 keymaps: corne, lily58, sofle, splitkb_aurora_sofle ✓
      - No host pipx dependency ✓
- [x] Verify keymap-drawer target works end-to-end
      Run make keymap-drawer and confirm SVGs are generated without host pipx dependency.
  - ⚙️ [x] `make build` ran successfully: codebase (west update), keymap-drawer (generated 4 SVGs from cached venv, no pip install needed), and both firmware targets (nice_corne_left_oled, nice_corne_right_oled) built to completion. No pipx dependency on host.
    - 📋 End-to-end verification confirmed:
      - All 4 SVGs present in keymap-drawer/: corne.svg (42K), lily58.svg (40K), sofle.svg (42K), splitkb_aurora_sofle.svg (41K)
      - Intermediate YAML files also generated correctly
      - config_keymap-drawer.yaml exists (12K config)
      - .keymap-drawer-venv/ cached on host with bin/ and lib/
      - No host pipx required — everything runs inside python:3-slim container
