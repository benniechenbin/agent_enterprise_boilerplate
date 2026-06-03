import pytest

from app.config.enums import ModelProvider
from app.config.settings import Settings
from app.core.container import Container


def test_container_validate_rejects_missing_openai_key() -> None:
    app_settings = Settings(
        _env_file=None,
        default_model_provider=ModelProvider.OPENAI,
        openai_api_key=None,
    )
    container = Container(app_settings=app_settings)

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        container.validate()


def test_container_validate_accepts_openai_key() -> None:
    app_settings = Settings(
        _env_file=None,
        default_model_provider=ModelProvider.OPENAI,
        openai_api_key="sk-test",
    )
    container = Container(app_settings=app_settings)

    container.validate()
