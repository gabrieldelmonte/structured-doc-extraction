from typing import List
import io
from PIL import Image
from pdf2image import convert_from_bytes
from app.models.enums import DocumentType
from app.services.ocr_service import ocr_service

class ImageProcessor:
	"""Handles image processing workflows"""

	@staticmethod
	def _convert_pdf_to_images(pdf_content: bytes, max_size: int = 1000) -> List[bytes]:
		"""
		Convert PDF to list of image bytes.
		Each page becomes one image, resized to max_size x max_size.
		
		Args:
			pdf_content: PDF file bytes
			max_size: Maximum width or height for images
			
		Returns:
			List of image bytes
		"""
		# Convert PDF to images (one per page)
		images = convert_from_bytes(pdf_content, dpi=200)
		
		image_bytes_list = []
		for img in images:
			# Resize maintaining aspect ratio
			width, height = img.size
			if width > max_size or height > max_size:
				scale = min(max_size / width, max_size / height)
				new_width = int(width * scale)
				new_height = int(height * scale)
				img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
			
			# Convert to bytes
			img_byte_arr = io.BytesIO()
			img.save(img_byte_arr, format='PNG')
			image_bytes_list.append(img_byte_arr.getvalue())
		
		return image_bytes_list

	@staticmethod
	def _is_pdf(file_content: bytes) -> bool:
		"""Check if file is a PDF"""
		return file_content.startswith(b'%PDF')

	@staticmethod
	async def process_single_document(
		file_content: bytes,
		document_type: DocumentType
	) -> dict:
		"""Process a single document image or PDF"""
		# Check if it's a PDF
		if ImageProcessor._is_pdf(file_content):
			# Convert PDF pages to images
			image_list = ImageProcessor._convert_pdf_to_images(file_content)
			
			# If single page, process as single image
			if len(image_list) == 1:
				result = await ocr_service.process_image(image_list[0], document_type)
				return result
			else:
				# Multiple pages - process as multi-page document
				return await ImageProcessor.process_multiple_pages(image_list, document_type)
		else:
			# Regular image
			result = await ocr_service.process_image(file_content, document_type)
			return result

	@staticmethod
	async def process_multiple_pages(
		files_content: List[bytes],
		document_type: DocumentType
	) -> dict:
		"""Process multiple pages of a document"""
		results = []

		for idx, content in enumerate(files_content, start=1):
			page_result = await ocr_service.process_image(
				content,
				document_type,
				page_number=idx
			)
			results.append(page_result)

		return {
			'total_pages': len(files_content),
			'content': results,
			'summary': 'Document processed successfully'
		}

# Global instance
image_processor = ImageProcessor()
