from enum import Enum

class DocumentType(str, Enum):
	DRIVERS_LICENSE = 'drivers_license'
	ENERGY_BILL = 'energy_bill'
	LARGE_DOCUMENT = 'large_document'
