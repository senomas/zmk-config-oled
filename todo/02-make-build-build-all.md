<!-- auto-generated from 2-make-build-build-all.json — do not edit manually -->

# Add BUILD variable to control which firmware `make build` builds (default: nice_corne_left/right_oled), and add `make build_all` to build everything

- [ ] Add BUILD variable with default firmware selection
      Insert the following block right before the `ZMK_WORKSPACE :=` line (before the 'CI-aligned codebase target' comment block):
      
      ```makefile
      # Default firmware to build (space-separated artifact names from build.yaml).
      # Set to empty to build all, or list specific artifacts (e.g. nice_corne_left_oled).
      BUILD ?= nice_corne_left_oled nice_corne_right_oled
      ```
      
      This uses `?=` so it can be overridden by env or command line (e.g. `make build BUILD="nice_settings_reset"`).
  - ⚙️ [x] Inserted `BUILD ?= nice_corne_left_oled nice_corne_right_oled` before the ZMK_WORKSPACE line. Uses `?=` for env/CLI override support.
- [ ] Add filter logic in build target to skip non-BUILD artifacts
      In the `build:` target, two changes:
      
      1. Change the first shell line from:
         `@python3 scripts/parse-build-yaml.py | jq -c '.[]' | while IFS= read -r entry; do \`
         to:
         `@build_filter="$(BUILD)"; \`
         `python3 scripts/parse-build-yaml.py | jq -c '.[]' | while IFS= read -r entry; do \`
      
      2. After the line `artifact=$$(echo "$$artifact" | tr " " "_"); \` and before `snippet_flag=""; \`, insert:
      
      ```makefile
      		if [ -n "$$build_filter" ]; then \
      			case " $$build_filter " in \
      				*" $$artifact "*) ;; \
      				*) echo "Skipping $$artifact (not in BUILD)"; continue ;; \
      			esac; \
      		fi; \
      ```
      
      The double-escaping (`$$build_filter`, `$$artifact`) is required because these are shell variables inside a make recipe. The `case` pattern uses spaces around both the filter list and the artifact name to ensure exact word matching (e.g. `nice_corne_left` won't accidentally match `nice_corne_left_oled`).
  - ⚙️ [x] Changed build target: prepended `build_filter="$(BUILD)"` variable, added case-match filter block after artifact name normalization. Uses `" $$build_filter "` / `" $$artifact "` space-padded pattern for exact word matching.
- [ ] Add build_all target
      Insert the following block right before `### CODEBASE_UROB START`:
      
      ```makefile
      # Build all firmware defined in build.yaml (no filter)
      build_all:
      	$(MAKE) build BUILD=""
      ```
      
      When BUILD is empty, `[ -n "$$build_filter" ]` is false, so the filter block is skipped entirely and everything in build.yaml gets built.
  - ⚙️ [x] Added `build_all:` target before `### CODEBASE_UROB START` that invokes `$(MAKE) build BUILD=""` to build everything with no filter.
- [ ] Update help text descriptions for build and build_all
      In the `help:` target, update the 'Primary targets (CI-aligned):' section:
      
      1. Change the `build` description from:
         `@echo "  build          Build all firmware defined in build.yaml (what CI builds)"`
         to:
         `@echo "  build          Build selected firmware (BUILD var, default: nice_corne_left/right_oled)"`
      
      2. Add a new line after the `build` description:
         `@echo "  build_all      Build all firmware defined in build.yaml"`
  - ⚙️ [x] Updated build help line to mention BUILD variable and default. Added build_all help line.
