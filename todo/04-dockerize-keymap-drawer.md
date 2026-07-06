<!-- auto-generated from 4-dockerize-keymap-drawer.json — do not edit manually -->

# Make keymap-drawer target run inside Docker instead of requiring host pipx

- [ ] Rewrite keymap-drawer target to use docker run with pip install keymap-drawer
      Replace the host pipx check with a docker run that installs keymap-drawer via pip inside the zmk-build-arm container, mounts config/ and keymap-drawer/ dirs, and processes all *.keymap files in a single run.
  - ⚙️ [x] Done. Changes:
    - Added `.keymap-drawer-venv/` to `.gitignore`
    - Rewrote `keymap-drawer` target to use `python:3-slim` Docker image
    - Uses `PYTHONUSERBASE=/venv pip install --user` to install keymap-drawer into a host-cached directory (`.keymap-drawer-venv/`)
    - Sets `PYTHONPATH` so the `keymap` CLI can find its modules
    - Fixed `-c` flag placement: `-c config` goes before subcommand (`parse`/`draw`), `-c 12` (columns) goes after `parse`
    - Generates SVGs for all 4 keymaps (corne, lily58, sofle, splitkb_aurora_sofle)
- [ ] Verify keymap-drawer target works end-to-end
      Run make keymap-drawer and confirm SVGs are generated without host pipx dependency.
  - ⚙️ [x] `make build` ran successfully: codebase (west update), keymap-drawer (generated 4 SVGs from cached venv, no pip install needed), and both firmware targets (nice_corne_left_oled, nice_corne_right_oled) built to completion. No pipx dependency on host.
