from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
	# API Settings
	API_V1_PREFIX: str = '/api/v1'
	PROJECT_NAME: str = 'OCR API'

	# CORS Settings
	ALLOWED_ORIGINS: List[str] = [
		'http://localhost:3000',
		'http://localhost:5173',
		'http://localhost:8080'  # Frontend HTTP server
	]

	# Model Settings
	MODEL_API_URL: str = ''
	MODEL_API_KEY: str = ''
	FLORENCE2_MODEL_NAME: str = 'microsoft/Florence-2-large'
	MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB

	# Processing Settings
	MAX_PAGES_LARGE_DOC: int = 100

	class Config:
		env_file = ".env"
		case_sensitive = True

settings = Settings()
