from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import EnergyBillResponse
from app.models.enums import DocumentType
from app.services.image_processor import image_processor
from app.utils.validators import FileValidator

router = APIRouter()

@router.post('/ocr/energy-bill', response_model = EnergyBillResponse)
async def process_energy_bill(file: UploadFile = File(...)):
	"""Process a Brazilian energy bill"""
	FileValidator.validate_bill_file(file)

	try:
		content = await file.read()
		FileValidator.validate_file_size(content)

		result = await image_processor.process_single_document(
			content,
			DocumentType.ENERGY_BILL
		)
		return EnergyBillResponse(**result)
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code = 500, detail = f'Error processing document: {str(e)}')
