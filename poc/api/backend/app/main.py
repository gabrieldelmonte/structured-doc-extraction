from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import drivers_license, energy_bill, large_document
from app.config import settings

app = FastAPI(
	title = 'OCR Document Processing API',
	description = 'API for processing documents',
	version = '1.0.0'
)

# CORS middleware for frontend integration
app.add_middleware(
	CORSMiddleware,
	allow_origins = settings.ALLOWED_ORIGINS,
	allow_credentials = True,
	allow_methods = ['*'],
	allow_headers = ['*'],
)

# Include routers
app.include_router(drivers_license.router, prefix = '/api/v1', tags = ['Driver\'s License'])
app.include_router(energy_bill.router, prefix = '/api/v1', tags = ['Energy Bill'])
app.include_router(large_document.router, prefix = '/api/v1', tags = ['Large Document'])

@app.get('/')
async def root():
	return {
		'message': 'OCR Document Processing API',
		'version': '1.0.0',
		'docs': '/docs'
	}

@app.get('/health')
async def health_check():
	return {'status': 'healthy'}

if __name__ == '__main__':
	import uvicorn
	uvicorn.run(app, host = '0.0.0.0', port = 8000)
