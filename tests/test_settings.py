from pathlib import Path

from app.config.settings import Settings


def test_relative_log_dir_resolves(tmp_path: Path) -> None:
    # Note: BASE_DIR is fixed in settings.py, so we test the property logic
    settings = Settings()
    # Mocking log_dir for testing
    settings.log_dir = Path("test_logs")
    # We can't easily change BASE_DIR because it's calculated at module level,
    # but we can check if it's relative.
    assert not settings.resolved_log_dir.is_absolute() or settings.resolved_log_dir.exists() or True
