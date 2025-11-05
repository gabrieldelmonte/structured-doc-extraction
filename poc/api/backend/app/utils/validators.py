from fastapi import UploadFile, HTTPException
from app.config import settings

class FileValidator:
	"""Validates uploaded files"""

	ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
	ALLOWED_BILL_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']

	@staticmethod
	def validate_image(file: UploadFile):
		"""Validate that file is an image"""
		if file.content_type not in FileValidator.ALLOWED_IMAGE_TYPES:
			raise HTTPException(
				status_code = 400,
				detail = f'File must be an image (JPG, PNG). Received: {file.content_type}'
			)

	@staticmethod
	def validate_bill_file(file: UploadFile):
		"""Validate energy bill file (image or PDF)"""
		if file.content_type not in FileValidator.ALLOWED_BILL_TYPES:
			raise HTTPException(
				status_code = 400,
				detail = f'File must be an image or PDF. Received: {file.content_type}'
			)

	@staticmethod
	def validate_file_size(file_content: bytes):
		"""Validate file size"""
		if len(file_content) > settings.MAX_FILE_SIZE:
			raise HTTPException(
				status_code = 400,
				detail = f'File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB'
			)
