from importlib.resources import files


def load_prompt(name: str) -> str:
    """Load a packaged prompt by its short name."""
    return files("app.resources").joinpath(f"{name}_prompt.md").read_text(encoding="utf-8")
