# Testing Implementation

- Unit: `pytest` in `tests/unit` with coverage on `controller`, `nodes`, `utils`.
- Integration: `make test-integration` brings up compose, runs end-to-end.
- Load: `tests/load/upload_test.py` with configurable users and ramp.
- Security: `make test-security` runs Bandit/Safety and `npm audit` in web-ui.
- CI (future): Github Actions for PR checks and nightly load tests.
