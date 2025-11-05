from typing import Optional
import asyncio
from PIL import Image
import io
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from app.models.enums import DocumentType
from app.services.prompt_manager import PromptManager
from app.config import settings

class OCRService:
	"""Service for OCR model operations"""

	def __init__(self):
		self.prompt_manager = PromptManager()
		self.model = None
		self.model_name = settings.FLORENCE2_MODEL_NAME
		self.processor = None
		self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
		self._initialize_model()

	def _initialize_model(self):
		"""Initialize Florence-2 model on startup."""
		try:
			# Detect device
			self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
			print(f'Loading Florence-2 model on {self.device}...')
			
			# Load model and processor
			# Use float32 on CPU to avoid dtype issues
			if self.device == 'cpu':
				self.model = AutoModelForCausalLM.from_pretrained(
					self.model_name,
					trust_remote_code=True
				).to(self.device)
			else:
				# On CUDA, we can use float16
				self.model = AutoModelForCausalLM.from_pretrained(
					self.model_name,
					trust_remote_code=True,
					torch_dtype=torch.float16
				).to(self.device)
			
			self.processor = AutoProcessor.from_pretrained(
				self.model_name,
				trust_remote_code=True
			)
			
			print('Florence-2 model loaded successfully!')
			
		except Exception as e:
			print(f'Error loading Florence-2 model: {str(e)}')
			raise

	def _resize_image(self, image: Image.Image, max_size: int = 1000) -> Image.Image:
		"""
		Resize image maintaining aspect ratio to fit within max_size x max_size.
		
		Args:
			image: PIL Image object
			max_size: Maximum width or height
			
		Returns:
			Resized PIL Image
		"""
		width, height = image.size
		
		if width <= max_size and height <= max_size:
			return image
		
		# Calculate scaling factor
		scale = min(max_size / width, max_size / height)
		new_width = int(width * scale)
		new_height = int(height * scale)
		
		return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

	def _run_florence_ocr(self, image: Image.Image) -> dict:
		"""
		Run Florence-2 OCR on image.
		
		Args:
			image: PIL Image object
			
		Returns:
			OCR result dictionary
		"""
		if self.model is None or self.processor is None:
			raise RuntimeError('Model not initialized')
		
		task_prompt = '<OCR>'
		
		# Prepare inputs - don't convert to float16 on CPU
		inputs = self.processor(
			text=task_prompt,
			images=image,
			return_tensors='pt'
		).to(self.device)
		
		# Generate with appropriate dtype
		with torch.no_grad():
			generated_ids = self.model.generate(
				input_ids=inputs['input_ids'],
				pixel_values=inputs['pixel_values'],
				max_new_tokens=1024,
				early_stopping=False,
				do_sample=False,
				num_beams=3,
			)
		
		generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
		
		parsed_answer = self.processor.post_process_generation(
			generated_text,
			task=task_prompt,
			image_size=(image.width, image.height)
		)
		
		return parsed_answer

	async def process_image(
		self,
		image_data: bytes,
		document_type: DocumentType,
		page_number: Optional[int] = None
	) -> dict:
		"""
		Process a single image with the OCR model.

		Args:
			image_data: The image bytes to process
			document_type: Type of document being processed
			page_number: Optional page number for multi-page documents

		Returns:
			dict: Parsed OCR results
		"""
		# Load and resize image
		image = Image.open(io.BytesIO(image_data)).convert('RGB')
		image = self._resize_image(image)
		
		# Run OCR
		ocr_result = await asyncio.to_thread(self._run_florence_ocr, image)
		
		# TODO: Process OCR result with LLM to convert to structured JSON
		# For now, return raw OCR result with mock structure
		structured_result = await self._structure_result(ocr_result, document_type, page_number)
		
		return structured_result

	async def _structure_result(
		self,
		ocr_result: dict,
		document_type: DocumentType,
		page_number: Optional[int] = None
	) -> dict:
		"""
		Structure OCR result into JSON format.
		TODO: Use small LLM to convert OCR text to structured JSON
		
		For now, returns raw OCR + mock structured fields
		"""
		# Base result with raw OCR data
		result = {
			'raw_ocr': ocr_result,
			'structured': False  # Will be True once LLM structuring is implemented
		}
		
		# TODO: Replace mock data with actual LLM structuring
		# For now, adding mock structured fields for testing
		if document_type == DocumentType.DRIVERS_LICENSE:
			result.update({
				'name': 'João da Silva',
				'cpf': '123.456.789-00',
				'birth_date': '01/01/1990',
				'emission_date': '15/05/2020',
				'father_name': 'Carlos da Silva',
				'mother_name': 'Ana da Silva'
			})
		elif document_type == DocumentType.ENERGY_BILL:
			result.update({
				'customer_name': 'Maria Santos',
				'customer_id': '123456789',
				'address': 'Rua das Flores, 123, São Paulo - SP',
				'reference_month': '10/2024',
				'due_date': '15/11/2024',
				'total_amount': 250.50,
				'consumption_kwh': 350.0,
				'installation_number': '987654321'
			})
		# For large documents, handle in the route handler
		
		return result

	async def _call_model_api(
		self,
		image_data: bytes,
		prompt: str,
		document_type: DocumentType,
		page_number: Optional[int] = None
	) -> dict:
		"""
		DEPRECATED - Mock function kept for reference.
		Use process_image instead.
		"""
		# Simulate API delay
		await asyncio.sleep(0.5)

		# Mock responses (kept for testing without model)
		"""
		if document_type == DocumentType.DRIVERS_LICENSE:
			return {
				'name': 'João da Silva',
				'cpf': '123.456.789-00',
				'birth_date': '01/01/1990',
				'emission_date': '15/05/2020',
				'father_name': 'Carlos da Silva',
				'mother_name': 'Ana da Silva'
			}
		elif document_type == DocumentType.ENERGY_BILL:
			return {
				'customer_name': 'Maria Santos',
				'customer_id': '123456789',
				'address': 'Rua das Flores, 123, São Paulo - SP',
				'reference_month': '10/2024',
				'due_date': '15/11/2024',
				'total_amount': 250.50,
				'consumption_kwh': 350.0,
				'installation_number': '987654321'
			}
		else:
			return {
				'page': page_number or 1,
				'text': f'Content from page {page_number or 1}...',
				'sections': ['Introduction', 'Main Content', 'Conclusion']
			}
		"""
		pass

# Global instance
ocr_service = OCRService()
