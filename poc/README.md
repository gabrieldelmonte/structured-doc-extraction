# POC - Prova de conceito para extração de informações estruturadas

Este diretório contém duas implementações de Prova de Conceito (POC) para extração de informações estruturadas de documentos utilizando o modelo de OCR Florence-2 Large e olmOCR-2-7B, este quantizado para 4 bits.

## Índice

- [Visão geral](#visão-geral)
- [Estrutura do projeto](#estrutura-do-projeto)
- [POC 1: API com FastAPI](#poc-1-api-com-fastapi)
- [POC 2: Jupyter Notebook](#poc-2-jupyter-notebook)
- [Requisitos](#requisitos)
- [Casos de uso](#casos-de-uso)
- [Comparação entre POCs](#comparação-entre-pocs)

## Visão geral

Este projeto demonstra duas abordagens diferentes para processar documentos e extrair informações estruturadas em formato JSON:

1. **API RESTful** - Solução completa de produção com backend FastAPI e frontend web
2. **Jupyter Notebook** - Ambiente interativo para experimentação e prototipagem rápida

Ambas as implementações processam três tipos de documentos:
- Carteira Nacional de Habilitação (CNH)
- Conta de Energia
- Documentos de múltiplas páginas (PDF)

## Estrutura do projeto

```
poc/
├── api/                # POC 1: aplicação web completa
│   ├── backend/        # Backend baseado em FastAPI
│   │   └── ...
│   ├── frontend/       # Frontend em JavaScript
│   │   └── ...
│   ├── logs/           # Logs da aplicação
│   │   └── ...
│   ├── start.sh        # Script de inicialização
│   └── stop.sh         # Script de parada
│
├── jupyter_notebook/   # POC 2: Notebook interativo
│   ├── poc_jn.ipynb    # POC completa
│   └── data_poc/       # Dados de teste
│       ├── case_01_drivers_license.jpeg
│       ├── case_02_bill.jpg
│       └── case_03_large_document.pdf
│
└── README.md           # Este arquivo
```

## POC 1: API com FastAPI

### Descrição

Solução completa de produção com arquitetura cliente-servidor, containerizada com Docker. Ideal para implantação em ambientes de produção e integração com outros sistemas.

### Características

**Backend:**
- API RESTful com FastAPI
- Documentação automática com OpenAPI/Swagger
- Validação de arquivos e tratamento de erros
- Suporte a CORS para requisições cross-origin
- Processamento de imagens e PDFs
- Integração com modelo Florence-2 Large
- Endpoints específicos para cada tipo de documento

**Frontend:**
- Interface web moderna e responsiva
- Upload de arquivos via drag & drop
- Preview de imagens em tempo real
- Exibição estruturada de resultados
- Design mobile-friendly
- JavaScript vanilla (sem dependências)

**DevOps:**
- Servidor web Nginx para frontend
- Scripts de inicialização automatizada
- Health checks para monitoramento

### Como Usar

#### Manual:
**Backend:**
```bash
cd api/backend
python -m venv env_api
source env_api/bin/activate  # Windows: env_api\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd api/frontend
python -m http.server 8080
```

#### Utilizando os scripts:
```bash
cd api
./start.sh  # Iniciar a aplicação
./stop.sh   # Parar a aplicação
```

### Endpoints da API

```
POST /api/v1/ocr/drivers-license    # Processar CNH
POST /api/v1/ocr/energy-bill         # Processar conta de energia
POST /api/v1/ocr/large-document      # Processar documento grande
GET  /health                         # Verificar saude da API
```

### Documentação completa

Para informações detalhadas sobre a API, consulte: [api/README.md](api/README.md)

## POC 2: Jupyter Notebook

### Descrição

Ambiente interativo para experimentação rápida com modelos de OCR. Ideal para prototipagem, testes e análise de resultados.

### Características

- Processamento de imagens e PDFs
- Redimensionamento automático de imagens (máx. 1200px)
- Conversão de PDFs em imagens individuais por página
- Extração de informações estruturadas em JSON
- Integração com modelo olmOCR-2-7B-1025-INT4
- Correção automática de JSON malformado
- Salvamento de resultados em arquivos JSON
- Código documentado em inglês
- Markdown em português

### Notebook disponível

**poc_jn.ipynb**
    - POC completa e estruturada
    - Funções de pré-processamento
    - Processamento em lote de documentos
    - Suporte a múltiplas páginas em PDF
    - Salvamento automático de resultados

### Como Usar

Este notebook foi totalmente projetado para ser executado no ambiente Google Colab! Basta abrir o arquivo `poc_jn.ipynb` no Colab e seguir as instruções nas células.

### Funções principais

- `resize_image()` - Redimensiona imagem mantendo proporção
- `convert_pdf_to_images()` - Converte PDF em lista de imagens
- `image_to_base64()` - Converte imagem para base64
- `extract_structured_info()` - Extrai informações com modelo OCR
- `parse_json_output()` - Corrige e valida JSON
- `process_document()` - Processa qualquer tipo de documento

### Dados de teste

Os documentos de testes estão localizados em `jupyter_notebook/data_challenge/`:
- `case_01_drivers_license.jpeg` - Carteira de habilitação
- `case_02_bill.jpg` - Fatura de energia
- `case_03_large_document.pdf` - Documento com múltiplas páginas

## Requisitos

### POC 1 (API)

- Python 3.11+
- pip

### POC 2 (Jupyter Notebook)

- Python 3.11+
- CUDA (recomendado para GPU)
- 8GB+ RAM
- Jupyter Notebook ou Google Colab

### Dependências Python comuns entre os projetos

```
torch
transformers
pillow
pdf2image
json-repair
```

## Casos de uso

### 1. Carteira Nacional de Habilitação (CNH)

### 2. Conta de Energia

### 3. Documentos Grandes

## Comparação entre POCs

| Aspecto               | POC 1 (API)       | POC 2 (Notebook)          |
|-----------------------|-------------------|---------------------------|
| **Ambiente**          | Produção          | Experimentação            |
| **Interface**         | Web UI            | Jupyter/VS Code           |
| **Modelo**            | Florence-2 Large  | olmOCR-2-7B quantizado    |
| **Escalabilidade**    | Alta              | Baixa                     |
| **Facilidade de Uso** | Alta              | Média                     |
| **Flexibilidade**     | Média             | Alta                      |
| **Documentação**      | API Docs          | Código comentado          |
