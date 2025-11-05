from app.models.enums import DocumentType

class PromptManager:
	"""Manages prompts for different document types"""

	PROMPTS = {
		DocumentType.DRIVERS_LICENSE: """
		Extract the following information from this Brazilian driver's license (CNH):
		- Full name
		- CPF
		- RG
		- Birth date
		- License number
		- Category
		- Expiration date
		- First license date
		Return the information as a JSON object.
		""",
		DocumentType.ENERGY_BILL: """
		Extract the following information from this Brazilian energy bill:
		- Customer name
		- Customer ID
		- Address
		- Reference month
		- Due date
		- Total amount
		- Consumption in kWh
		- Installation number
		Return the information as a JSON object.
		""",
		DocumentType.LARGE_DOCUMENT: """
		Extract all text content from this document page.
		Identify main sections and organize the content logically.
		Return the information as a JSON object with text and sections.
		"""
	}

	@classmethod
	def get_prompt(cls, document_type: DocumentType) -> str:
		return cls.PROMPTS.get(document_type, '')
