import secrets
from typing import Any, Dict, List, Optional
from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, RedisDsn, AmqpDsn, validator, BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    INIT_PASSWORD: str = "admin"
    # 60 seconds * 60 minutes * 24 hours * 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24 * 7

    PROJECT_NAME: str = "Security DataCenter"

    MYSQL_DATABASE_URI: Optional[PostgresDsn] = "mysql://root:admin@localhost/db_name?charset=utf8"
    
    MONGO_DATABASE = "datacenter"
    MONGO_DATABASE_URI: Optional[str] = "mongodb://root:admin@localhost:27017/datacenter?retryWrites=true&w=majority"
    
    REDIS_DATABASE_URI: Optional[RedisDsn] = "redis://:admin@localhost:6379/0"
    
    AMQP_DATABASE_URI: Optional[AmqpDsn] = "amqp://root:admin@localhost:5672//"

    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = "smtp.qq.com"
    SMTP_USER: Optional[str] = "619511821@qq.com"
    SMTP_PASSWORD: Optional[str] = "admin"
    EMAILS_FROM_EMAIL: Optional[EmailStr] = "619511821@qq.com"
    EMAILS_FROM_NAME: Optional[str] = "Mr.Wang"
    EMAILS_ENABLED: bool = True
    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("SMTP_HOST") and values.get("SMTP_PORT") and values.get("EMAILS_FROM_EMAIL"))

    FIRST_SUPERUSER: str = "secpf"
    FIRST_SUPERUSER_EMAIL: str = "app.secpf@h3c.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"    

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
