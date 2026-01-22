# Snapshot Configuration

- Metadata backups: Periodic snapshots of `controller/metadata.json`.
- Storage volumes: Docker named volumes per node for persistence.
- Backup cadence: Daily by default; configurable via Makefile task.
- Restore: Validate integrity before applying snapshots.
- Offsite storage: Optional push to cloud bucket (future).
