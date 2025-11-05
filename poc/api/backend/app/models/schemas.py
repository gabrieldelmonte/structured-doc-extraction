from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DriverLicenseResponse(BaseModel):
	# Structured fields (optional until LLM structuring is implemented)
	name: Optional[str] = None
	cpf: Optional[str] = None
	birth_date: Optional[str] = None
	emission_date: Optional[str] = None
	father_name: Optional[str] = None
	mother_name: Optional[str] = None
	
	# Raw OCR output (always present)
	raw_ocr: Optional[Dict[str, Any]] = None
	
	# Additional metadata
	structured: bool = Field(default=False, description='Whether the data has been structured by LLM')

class EnergyBillResponse(BaseModel):
	# Structured fields (optional until LLM structuring is implemented)
	customer_name: Optional[str] = None
	customer_id: Optional[str] = None
	address: Optional[str] = None
	reference_month: Optional[str] = None
	due_date: Optional[str] = None
	total_amount: Optional[float] = None
	consumption_kwh: Optional[float] = None
	installation_number: Optional[str] = None
	
	# Raw OCR output (always present)
	raw_ocr: Optional[Dict[str, Any]] = None
	
	# Additional metadata
	structured: bool = Field(default=False, description='Whether the data has been structured by LLM')

class LargeDocumentResponse(BaseModel):
	total_pages: int
	content: List[Dict[str, Any]]
	summary: Optional[str] = None
	
	# Raw OCR output for each page
	raw_ocr: Optional[List[Dict[str, Any]]] = None
	
	# Additional metadata
	structured: bool = Field(default=False, description='Whether the data has been structured by LLM')

class ErrorResponse(BaseModel):
	error: str
	detail: Optional[str] = None
