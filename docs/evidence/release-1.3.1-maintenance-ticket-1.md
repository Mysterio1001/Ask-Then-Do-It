# Ask Then Do It 1.3.1 Maintenance Ticket 1 Implementation Evidence

Artifact type: TDD Implementation Evidence

Artifact ID: `release-1-3-1-maintenance-ticket-1-implementation`

Workflow ID: `release-1-3-1-maintenance`

Core version: `1.3.0`

Target release version: `1.3.1`

Ticket: `1 - 讓 development dependency manifest 可獨立支撐完整測試`

Execution mode: `tdd` (`Add tests`, explicitly selected by the user)

Status: Completed

Inputs: Approved [Specification](../specs/release-1.3.1-maintenance.md)、Approved [Ticket Plan](../plans/release-1.3.1-maintenance.md)、目前 `requirements-dev.txt` 與 release dependency/package contracts。

Assumptions: 本 Ticket 只更正 development/test dependency manifest，不改 consumer runtime inventory。驗證環境是一次性 Windows CPython 3.12.13 venv，不代表其他 Python/Pillow major versions。

Deferred: Windows replacement/recovery reliability（Ticket 2）、lockstep `1.3.1` identity/packages（Ticket 3）、final release validation/evidence（Ticket 4），以及全部 external publication actions。

Handoff: 交給獨立 `$review-code` 對照 Approved Specification、Ticket 1 scope、Red/Green evidence 與 final diff；Review 不授權自行修正 finding。

Approval: Implementation authority comes from the Approved Ticket Plan and its approved `tdd` mode.

## Outcome

- `requirements-dev.txt` 現在明確宣告既有 `PyYAML>=6.0,<7` 與核准的 `Pillow>=12.3,<13`。
- 新 release contract test 會拒絕 Pillow declaration 缺漏或 range 漂移。
- 一次性 CPython 3.12.13 venv 在 `include-system-site-packages=false`、`PYTHONPATH=None` 下，安裝前無法 import `PIL`；只執行 `pip install -r requirements-dev.txt` 後取得 Pillow 12.3.0 與 PyYAML 6.0.3。
- Pillow 與 PyYAML 都從該 venv 的 `Lib/site-packages` 載入；focused tests 與完整 195-test discovery 最終通過。

## Files changed

- `requirements-dev.txt`: 新增 `Pillow>=12.3,<13` development/test dependency。
- `tests/release/test_release_contract.py`: 新增 exact development-dependency manifest contract。
- 本 evidence 與 Approved Plan 的 Ticket 1 status；沒有修改 runtime source、consumer package inventory、README 或 lockfile。

## Red

Command:

`<bundled-cpython-3.12> -m unittest tests.release.test_release_contract.ReleaseContractTests.test_development_dependencies_cover_release_validation`

Observed result: exit `1`; one test failed only because the expected set contained `Pillow>=12.3,<13` while `requirements-dev.txt` did not。這證明 test 命中核准的 missing behavior，而非 setup failure。

## Focused Green

After adding only `Pillow>=12.3,<13`:

- Same dependency contract command: exit `0`; `Ran 1 test`; `OK`。
- Isolated-venv focused command running the dependency contract plus `tests.release.test_plugin_assets`: exit `0`; `Ran 4 tests in 0.964s`; `OK`。
- `python -m pip check`: exit `0`; `No broken requirements found.`

## Isolated environment evidence

- Base interpreter: `CPython 3.12.13`。
- Venv config: `include-system-site-packages = false`。
- Runtime state before installation: `sys.prefix != sys.base_prefix`、`PYTHONPATH=None`、`import PIL` failed with `ModuleNotFoundError`。
- Install command: `<isolated-venv>\Scripts\python.exe -m pip install -r requirements-dev.txt`。
- Install result: exit `0`; `Successfully installed Pillow-12.3.0 PyYAML-6.0.3`。
- Loaded Pillow path: the disposable venv's `Lib\site-packages\PIL\__init__.py`。
- Loaded PyYAML path: the disposable venv's `Lib\site-packages\yaml\__init__.py`。
- No repository or bundled dependency path was added through `PYTHONPATH`。

## Broader verification

First full command:

`<isolated-venv>\Scripts\python.exe -m unittest discover -s tests -p test_*.py`

Observed result: 195 tests ran; one failure occurred in `ReleaseSafetyTests.test_repeated_build_replaces_only_a_complete_valid_output_set` because the existing builder encountered transient Windows `WinError 5` during managed-output replacement。這是 Approved Ticket 2 的已知問題，不是 dependency/import failure。

Follow-up observations:

- Targeted repeated-build test rerun: exit `0`; `Ran 1 test`; `OK`。
- Full isolated discovery rerun: exit `0`; `Ran 195 tests in 14.988s`; `OK`。
- `git diff --check`: exit `0`; only Git's existing LF-to-CRLF warnings were emitted。
- Repository-root scan found no leftover test staging or temporary directories。

## Refactor and scope inspection

No refactor was needed. The production change is one dependency declaration and the test is limited to the stable root manifest boundary. Final diff inspection found no consumer runtime dependency, documentation expansion, version bump, package rebuild, Token proxy change, CI, lockfile, or unrelated cleanup。

## Residual risk

The observed `WinError 5` remains a known builder reliability defect until Approved Ticket 2 is implemented and reviewed. Ticket 1 itself has complete Red/Green and isolated dependency evidence; external package availability remains an operational dependency of online installation rather than an offline-install guarantee。
