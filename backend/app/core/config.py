from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_time: int
    paypal_mode: str
    paypal_client_id: str
    paypal_client_secret: str
    paypal_api_base: str
    redis_host: str
    redis_port: int
    otp_exp: int
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    from_email: str
    paypal_webhook_id: str
    frontend_url: str

    class Config:
        env_file = ".env"

settings = Settings()
