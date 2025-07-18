import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    url: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        url = os.getenv("DATABASE_URL")

        if not url:
            raise ValueError("DATABASE_URL environment variable not set")
        return cls(url=url)

@dataclass
class ProcessingConfig:
    version: float = 28.0
    language: str = "en"
    batch_size: int = 5000
    encoding: str = "UTF-8"
    separator: str = "$"
    
    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.version <= 0:
            raise ValueError("version must be positive")

@dataclass
class AppConfig:
    database: DatabaseConfig
    processing: ProcessingConfig
    
    @classmethod
    def from_env(cls, **overrides) -> 'AppConfig':
        processing_config = ProcessingConfig(**overrides)
        database_config = DatabaseConfig.from_env()

        return cls(
            database=database_config,
            processing=processing_config
        )