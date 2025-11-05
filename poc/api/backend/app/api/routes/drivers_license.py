from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import DriverLicenseResponse
from app.models.enums import DocumentType
from app.services.image_processor import image_processor
from app.utils.validators import FileValidator

router = APIRouter()

@router.post('/ocr/drivers-license', response_model = DriverLicenseResponse)
async def process_drivers_license(file: UploadFile = File(...)):
	"""Process a Brazilian driver's license (CNH)"""
	FileValidator.validate_image(file)

	try:
		content = await file.read()
		FileValidator.validate_file_size(content)

		result = await image_processor.process_single_document(
			content,
			DocumentType.DRIVERS_LICENSE
		)
		return DriverLicenseResponse(**result)
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code = 500, detail = f'Error processing document: {str(e)}')
