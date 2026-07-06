# Local Build Design

## Architecture

```
Host machine (docker/podman)
  └─ Makefile
       ├─ Auto-detects docker vs podman (CONTAINER_RUNTIME)
       ├─ Pulls zmkfirmware/zmk-build-arm:stable (same image as CI)
       ├─ Mounts ./config → /zmk-config (ZMK_CONFIG)
       ├─ Mounts ./boards → /boards (ZMK_EXTRA_MODULES)
       ├─ West workspace inside container
       │    ├─ west init -l /zmk-config   (respects config/west.yml v0.3.0 pin)
       │    ├─ west update
       │    └─ west build -s zmk/app -b $board -- -DSHIELD=...
       └─ docker cp firmware/*.uf2 out → ./firmware/
```

The Makefile runs on the **host** (invoked via `hat_make` or directly). The dev
container never runs docker — it only edits files and invokes `make` on the host.

## CI Path (reference — what we want to match)
```
.github/workflows/build.yml
  → zmkfirmware/zmk/.github/workflows/build-user-config.yml@v0.3.0
    → reads build.yaml (yq) → builds matrix
    → container: zmkfirmware/zmk-build-arm:stable
    → west init -l config/      (uses config/west.yml, ZMK pinned at v0.3.0)
    → west update
    → west zephyr-export
    → west build -s zmk/app -b $board -- -DSHIELD="$shield" -DZMK_CONFIG=... $cmake_args
```

## Current Makefile Problems

1. **Container runtime hardcoded**: `docker` used throughout — breaks on podman-only hosts
2. **Version mismatch**: Clones `zmkfirmware/zmk` (main) or `urob/zmk` (main) independently — ignores `config/west.yml` v0.3.0 pin. CI uses v0.3.0.
3. **Container image mismatch**: Uses `zmkfirmware/zmk-dev-arm:3.5` — CI uses `zmk-build-arm:stable`
4. **No build.yaml-driven target**: `build.yaml` defines what CI builds (3 entries). The Makefile has ~30 hardcoded targets — no way to say "build exactly what CI builds"
5. **Divergent targets**: Many hardcoded targets for board/shield combos not in build.yaml (puchi_ble, seeeduino_xiao_ble, urob branch). These are useful but should be secondary to the CI-aligned path.

## Design Decisions

### 1. Container runtime: auto-detect docker vs podman
- Detect via `which docker` / `which podman`
- Use `CONTAINER_RUNTIME` variable throughout (replaces hardcoded `docker`)
- Prefer docker if both present

### 2. Match CI: use `config/west.yml` for ZMK version
- Instead of `git clone zmk` separately, use `west init -l config/` inside container
- This makes `config/west.yml` the single source of truth for ZMK version
- Both CI and local builds use the same ZMK revision (v0.3.0)

### 3. Match CI: use same container image
- `zmkfirmware/zmk-build-arm:stable` — same image CI uses
- (Currently `zmk-dev-arm:3.5` — different image, different toolchain)

### 4. Add `build.yaml`-driven `build` target
- Parses `build.yaml` `include[]` entries
- Iterates and runs west build for each entry
- Output firmware to `firmware/` directory
- This is the **primary** local build target

### 5. Keep existing targets as "advanced"
- `codebase_urob`, `only_*_urob`, flash targets all remain
- Flash targets (`nice_corne_flash_left`, etc.) are still essential
- Document that `make build` is the CI-aligned path; `make corne_urob` is for custom urob builds

## build.yaml Parsing Strategy

Each `include[]` entry has these fields:
- `board` (required) — e.g. `nice_nano_v2`
- `shield` (optional) — e.g. `corne_left nice_oled`
- `cmake-args` (optional) — extra cmake defines
- `artifact-name` (optional) — output filename
- `snippet` (optional) — west build `-S` snippet

Per-entry west build invocation:
```
west build -s zmk/app -d build/<artifact-name> -b <board> \
  [-S <snippet>] \
  -- -DSHIELD="<shield>" -DZMK_CONFIG=/zmk-config <cmake-args>
```

Parsing will use a small shell loop with `yq`. If `yq` is unavailable, provide a
friendly error. We do NOT add a Python dependency just for YAML parsing.

## ZMK Source Management

**Before**: Clone `zmkfirmware/zmk` or `urob/zmk` to `./zmk`, mount as `/zmk`.

**After**: Use `west init -l config/` which reads `config/west.yml`.
West workspace lives in a volume or a host directory.

This change only affects the new `build` target. Existing urob targets keep
their current clone-based approach for backward compatibility.

## Makefile Structure (targeted changes)

```makefile
# --- New: container runtime detection ---
CONTAINER_RUNTIME := $(shell which docker 2>/dev/null || which podman 2>/dev/null)
ifeq ($(CONTAINER_RUNTIME),)
  $(error Neither docker nor podman found. Install one to build locally.)
endif

# --- New: CI-aligned image ---
ZMK_CI_IMAGE := zmkfirmware/zmk-build-arm:stable

# Keep existing vars for backward compat
zmk_image=zmkfirmware/zmk-dev-arm:3.5   # used by urob targets

# --- New: build.yaml-driven build ---
build: codebase
	@# Parse build.yaml and build each entry
	...

# --- New: codebase (west-based, CI-aligned) ---
codebase:
	docker run --rm -v ... ${ZMK_CI_IMAGE} sh -c 'west init -l /zmk-config && west update'

# --- Existing targets preserved ---
codebase_default: ...  # unchanged
codebase_urob: ...      # unchanged
corne_urob: ...         # unchanged
nice_corne_flash_left: ...  # unchanged
shell: ...              # unchanged
clean: ...              # unchanged (but use CONTAINER_RUNTIME)
```

## Risks / Trade-offs

- **yq dependency**: Users need `yq` for the `build` target. It's the same tool CI uses, and is available via `brew install yq`, `apt install yq`, etc. Error message will be clear.
- **Dual ZMK sources**: The new `codebase` + `build` path uses west. Old urob targets still clone zmk directly. Two separate ZMK downloads if you use both paths. Acceptable for backward compat.
- **West workspace size**: ~2GB initial download. Same as CI. Acceptable.
