"""
GPIWD-Dragon: Configuration Management
Loads all settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class GPIWDSettings(BaseSettings):
    """
    GPIWD Core Configuration.
    All values can be overridden via environment variables or .env file.
    """

    # --- App ---
    APP_NAME: str = "GPIWD-Dragon"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"  # development | staging | production
    DEBUG: bool = False

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 7777
    WORKERS: int = 4

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None

    # --- PostgreSQL ---
    DATABASE_URL: str = "postgresql://gpiwd:gpiwd_pass@localhost:5432/gpiwd"

    # --- Security ---
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    API_KEY_HEADER: str = "X-GPIWD-Key"

    # --- Rate Limiting ---
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    RATE_LIMIT_BURST: int = 20

    # --- WAF ---
    WAF_ENABLED: bool = True
    WAF_BLOCK_SQLI: bool = True
    WAF_BLOCK_XSS: bool = True
    WAF_BLOCK_SSRF: bool = True
    WAF_BLOCK_RCE: bool = True
    WAF_THREAT_SCORE_THRESHOLD: float = 0.6

    # --- IP Intelligence ---
    ABUSEIPDB_API_KEY: Optional[str] = None
    ABUSEIPDB_CONFIDENCE_THRESHOLD: int = 75
    GEO_BLOCK_COUNTRIES: str = ""  # Comma separated ISO codes

    # --- AI Security (V4) ---
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    AI_SECURITY_ENABLED: bool = False  # Enable in V4

    # --- Telegram Alerts ---
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_ALERT_CHAT_ID: Optional[str] = None
    TELEGRAM_ALERTS_ENABLED: bool = False

    # --- Dashboard ---
    DASHBOARD_ENABLED: bool = True
    SOC_POLL_INTERVAL_SECONDS: int = 30

    # --- Targets (upstream services to protect) ---
    TARGET_GAS_BACKEND: str = "http://localhost:8085"
    TARGET_AI_AGENT: str = "http://localhost:9499"
    TARGET_AI_STUDIO: str = "http://localhost:9500"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = GPIWDSettings()
