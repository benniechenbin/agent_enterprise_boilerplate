from enum import Enum

class AppEnv(str, Enum):
    DEV = "development"
    TEST = "testing"
    PROD = "production"

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    DEEPSEEK = "deepseek"
