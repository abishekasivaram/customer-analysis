# Runtime Readiness Analysis & Issues

This report identifies all issues preventing the repository from executing successfully on a freshly cloned machine without manual intervention.

## 1. Missing Directories (Blocking)
- The pipeline heavily depends on the existence of the `outputs/` directory structure (`outputs/detection/json`, `outputs/behavior/timeline`, `outputs/business/graphs`, etc.). 
- While `backend/core/config.py` attempts to create some Phase 1 output directories, Phase 2, Phase 3, and Phase 4 scripts do not create their required output subdirectories before writing files. This will result in `FileNotFoundError` during `run_phase2.py` and downstream processes.

## 2. Hardcoded Paths (Blocking)
- Over 50 instances across the codebase (specifically in `run_phase*.py` scripts and `backend/services/business/*.py`) use hardcoded string literals like `"outputs/behavior/timeline/*_timeline.json"`.
- This causes the scripts to fail if executed from any directory other than the project root. It breaks Python's standard `pathlib` cross-platform conventions.

## 3. Missing Generated Artifacts (Pipeline Chain Blocker)
- **Phase 1 Missing JSON/CSV:** Phase 2 (`run_phase2.py`) relies entirely on the output of Phase 1 (`outputs/detection/json/*.json`).
- **Phase 2 Missing Timeline:** Phase 3 relies entirely on Phase 2 outputs (`outputs/behavior/timeline/*.json`).
- **Phase 3 Missing Business Logic:** Phase 4 relies on Phase 3 outputs.
- *Issue:* The pipeline cannot be skipped or executed out of order on a fresh clone because the inputs for downstream phases do not exist.

## 4. Execution Orchestration (Missing)
- There is no single entrypoint to run the entire project. A developer would have to manually run `run_pipeline.py`, wait for it to finish, run `run_phase2.py`, etc., in the exact correct order.

## 5. Dependency Problems (Resolved)
- The `backend/requirements.txt` previously contained UTF-16LE encoding errors (`s\x00e\x00a...`) which broke standard `pip install`. This has been resolved, but must be accounted for in environment automation.

## Summary of Fixes Required
1. Dynamically generate all required `outputs/` subdirectories at runtime.
2. Refactor all hardcoded relative string paths to use `pathlib.Path` resolved relative to `BASE_DIR`.
3. Create a master orchestrator (`run_all.py`) that executes the phases in strict sequential order.
