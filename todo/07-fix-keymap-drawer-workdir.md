<!-- auto-generated from 7-fix-keymap-drawer-workdir.json — do not edit manually -->

# Fix broken keymap-drawer Makefile target (workdir /work does not exist in python:3-slim container)

- [ ] Fix -w /work in keymap-drawer target `(2818e9fd)`
      The keymap-drawer target in the Makefile passes `-w /work` to the python:3-slim container, but /work does not exist in that image and is not a mount point — podman fails with 'workdir "/work" does not exist on container' (Error 126). Regression introduced in commit cfca3c5d. Fix: change `-w /work` to `-w /` (root always exists; the script inside only uses absolute paths /config, /venv, /keymap-drawer, so the workdir is irrelevant to its logic). Verify by running `make keymap-drawer` and confirming SVGs are regenerated.
