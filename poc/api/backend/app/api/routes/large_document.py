from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from app.models.schemas import LargeDocumentResponse
from app.models.enums import DocumentType
from app.services.image_processor import image_processor
from app.utils.validators import FileValidator
from app.config import settings

router = APIRouter()

@router.post('/ocr/large-document', response_model = LargeDocumentResponse)
async def process_large_document(files: List[UploadFile] = File(...)):
	"""Process a large multi-page document"""
	if len(files) == 0:
		raise HTTPException(status_code = 400, detail = 'At least one file must be provided')

	if len(files) > settings.MAX_PAGES_LARGE_DOC:
		raise HTTPException(
			status_code = 400,
			detail = f'Too many pages. Maximum: {settings.MAX_PAGES_LARGE_DOC} pages'
		)

	# Validate all files
	for file in files:
		FileValidator.validate_image(file)

	try:
		# Read all files
		files_content = []
		for file in files:
			content = await file.read()
			FileValidator.validate_file_size(content)
			files_content.append(content)

		result = await image_processor.process_multiple_pages(
			files_content,
			DocumentType.LARGE_DOCUMENT
		)
		return LargeDocumentResponse(**result)
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code = 500, detail = f'Error processing document: {str(e)}')
