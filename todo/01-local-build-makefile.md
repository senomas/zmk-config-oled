<!-- auto-generated from 1-local-build-makefile.json — do not edit manually -->

# Make the project build locally via Makefile + host docker/podman, producing firmware identical to CI (build.yaml-driven)

- [ ] Add container runtime auto-detection
      Add CONTAINER_RUNTIME variable at top of Makefile that auto-detects docker vs podman (prefer docker). Error out if neither found. Replace all hardcoded 'docker' commands (docker_opts, docker run, docker cp, docker ps, docker volume) with $(CONTAINER_RUNTIME).
      
      Insert at line ~62 (after the header comment block, before the first config vars).
      
      Code pattern:
        CONTAINER_RUNTIME := $(shell which docker 2>/dev/null || which podman 2>/dev/null)
        ifeq ($(CONTAINER_RUNTIME),)
          $(error Neither docker nor podman found. Install Docker Desktop or Podman.)
        endif
      
      Then replace 'docker' in:
      - docker_opts (line ~54): change 'docker run' references to '$(CONTAINER_RUNTIME) run'
      - All target recipes using 'docker run', 'docker cp', 'docker ps', 'docker volume'
      - clean target (line ~405-406): docker container rm, docker volume rm
  - ⚙️ [x] Inserted CONTAINER_RUNTIME auto-detection (docker preferred, podman fallback, error if neither) after the header comment block. Replaced all hardcoded 'docker' commands (docker run, docker cp, docker ps, docker volume, docker container) with $(CONTAINER_RUNTIME) throughout the Makefile. Fixed self-referential sed issue in the definition itself.
- [ ] Add CI-aligned codebase target
      Add a new 'codebase' target that mirrors the CI approach: uses config/west.yml to fetch ZMK at the pinned version (v0.3.0) instead of cloning zmk separately.
      
      Insert after the existing codebase_urob target (around line 118).
      
      Behavior:
      - Runs a temporary container with zmkfirmware/zmk-build-arm:stable
      - Mounts ./config as /zmk-config
      - Runs: west init -l /zmk-config && west update
      - The west workspace (modules, zephyr, zmk, etc.) stays in a named volume 'zmk-workspace' that is reused across builds
      
      Docker run pattern:
        $(CONTAINER_RUNTIME) run --rm \
          -v zmk-workspace:/workspace \
          -v $(PWD)/config:/zmk-config:Z \
          -v $(PWD)/boards:/boards:Z \
          -w /workspace \
          zmkfirmware/zmk-build-arm:stable \
          sh -c 'west init -l /zmk-config && west update'
      
      This is separate from the existing codebase_default/codebase_urob targets which clone zmk directly — those remain unchanged for backward compat.
  - ⚙️ [x] Added 'codebase' target after codebase_urob. Uses zmkfirmware/zmk-build-arm:stable container with a named volume 'zmk-workspace' for the west workspace. Mounts ./config as /zmk-config, runs 'west init -l /zmk-config && west update'. Existing clone-based codebase_default/codebase_urob targets remain unchanged.
- [ ] Add build.yaml-driven build target
      Add a 'build' target that parses build.yaml and builds firmware for every entry in 'include[]', matching what CI produces.
      
      Depends on the 'codebase' target.
      
      Insert after the new 'codebase' target.
      
      Parsing strategy:
      - Use 'yq' to extract each entry's fields (board, shield, cmake-args, artifact-name, snippet)
      - If yq is not installed, print a clear error: 'yq is required. Install it: brew install yq  or  apt install yq'
      - Iterate over entries and run west build for each inside a container
      
      For each entry, construct and run:
        $(CONTAINER_RUNTIME) run --rm \
          -v zmk-workspace:/workspace \
          -v $(PWD)/config:/zmk-config:Z \
          -v $(PWD)/boards:/boards:Z \
          -v $(PWD)/firmware:/firmware:Z \
          -w /workspace \
          zmkfirmware/zmk-build-arm:stable \
          sh -c 'west build -s zmk/app -d build/$(artifact) -b $(board) \
            $(snippet_flag) -- -DSHIELD="$(shield)" \
            -DZMK_CONFIG=/zmk-config \
            -DZMK_EXTRA_MODULES=/boards \
            $(cmake_args) && \
            cp build/$(artifact)/zephyr/zmk.uf2 /firmware/$(artifact).uf2'
      
      Output: firmware files in ./firmware/ matching artifact-name from build.yaml.
      
      Edge cases:
      - Handle entries without 'shield' (board only builds like settings_reset)
      - Handle entries without 'cmake-args'
      - Handle entries without 'snippet'
      - Handle entries without 'artifact-name' (fall back to board-shield naming)
  - ⚙️ [x] Added 'build' target that depends on 'codebase'. Uses yq to parse build.yaml include[] entries. For each entry: extracts board, shield, cmake-args, artifact-name, snippet; constructs west build command in the zmk-build-arm container; copies zmk.uf2 to firmware/<artifact>.uf2. Handles entries without shield (board-only builds like settings_reset), without cmake-args, without snippet, and without artifact-name (falls back to board-shield naming). Errors out with clear message if yq is not installed.
- [ ] Add help target
      Add a 'help' target at the very top of the Makefile (so it's the default when running 'make' with no target).
      
      Insert after the header comment block, before any variable definitions.
      
      It should print:
        Usage: make [target]
      
        Primary targets (CI-aligned):
          build          Build all firmware defined in build.yaml (what CI builds)
          codebase       Initialize west workspace from config/west.yml
      
        Flash targets:
          nice_corne_flash_left     Flash left corne firmware to nice_nano_v2
          nice_corne_flash_right    Flash right corne firmware to nice_nano_v2
          puchi_corne_flash_left    Flash left corne firmware to puchi_ble
          puchi_corne_flash_right   Flash right corne firmware to puchi_ble
      
        Advanced (urob branch):
          codebase_urob  Clone urob/zmk and init
          corne_urob     Build all corne firmware with urob branch
      
        Utility:
          shell          Open a shell in the ZMK build container
          clean          Remove ZMK source and docker containers/volumes
          clean_firmware Remove all built .uf2 files
          clean_all      Remove everything (source + firmware + containers)
      
      Use @echo for each line so make doesn't print the commands.
  - ⚙️ [x] Added 'help' target at the very top of the Makefile with .DEFAULT_GOAL := help so it's the default when running 'make' with no target. Displays all targets organized into: Primary (CI-aligned), Flash, Advanced (urob branch), and Utility sections. Uses @echo for clean output.
- [ ] Update clean targets to use CONTAINER_RUNTIME
      Update the 'clean' target (line ~405) to use $(CONTAINER_RUNTIME) instead of hardcoded 'docker'.
      
      Current code:
        clean: clean_zmk
          docker ps -aq --filter name='^zmk' | xargs -r docker container rm
          docker volume list -q --filter name='zmk' | xargs -r docker volume rm
      
      New code:
        clean: clean_zmk
          $(CONTAINER_RUNTIME) ps -aq --filter name='^zmk' | xargs -r $(CONTAINER_RUNTIME) container rm
          $(CONTAINER_RUNTIME) volume list -q --filter name='zmk' | xargs -r $(CONTAINER_RUNTIME) volume rm
      
      Also add the zmk-workspace volume to the cleanup if the new codebase target uses a named volume.
  - ⚙️ [x] The global sed replacement already updated the clean target to use $(CONTAINER_RUNTIME) for ps, container rm, volume list, and volume rm. The existing name='zmk' filter already matches the new zmk-workspace volume (substring match in docker/podman volume list), so no additional filter change was needed.
- [ ] Update .gitignore for west workspace
      Add entries to .gitignore for the west workspace files that may appear in the project directory:
      
      Add after the existing 'zmk/' line:
        # west workspace
        .west/
        modules/
        bootloader/
        tools/
        zephyr/
      
      These directories may be created if west workspace is stored in the project root rather than a docker volume.
      
      The existing 'zmk/' entry is already there for the clone-based approach.
  - ⚙️ [x] Added west workspace entries to .gitignore after the existing 'zmk/' line: .west/, modules/, bootloader/, tools/, zephyr/. These directories may be created if west workspace is stored in the project root.
- [ ] Update README local installation section
      Update the LOCAL INSTALLATION section of README.md (around line 180) to document the new workflow.
      
      The current section says:
        make codebase_urob
        make corne_urob
      
      Update to:
        1. Install Docker Desktop or Podman
        2. Install yq (brew install yq or apt install yq)
        3. make build    (builds everything in build.yaml — same as CI)
      
      Keep the urob instructions as an 'Advanced / Custom ZMK branch' subsection.
  - ⚙️ [x] Updated the LOCAL INSTALLATION section in README.md. Changed prerequisites to mention Docker Desktop or Podman + yq. Primary command is now 'make build' (CI-aligned). The urob instructions are preserved under a new 'Advanced / Custom ZMK branch' subsection.
