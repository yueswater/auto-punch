from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # URLs
    login_url: str
    dashboard_url: str
    clockin_url: str
    clockout_url: str
    
    # Credentials
    username: str
    password: str
    
    # Company location
    company_lat: float
    company_lng: float

    # Timezone
    timezone: str

    # Working schedule
    work_start_earliest: str
    work_start_latest: str

    # Working time
    first_shift: float
    second_shift: float
    breaktime: float

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()