# Desafio técnico - Tech for Humans

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Funcionalidades](#funcionalidades)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Experimentos](#experimentos)

## Sobre o projeto

Este projeto foi desenvolvido como parte do programa de estágio da empresa Tech for Humans e tem como objetivo criar uma solução completa para extração automatizada de informações estruturadas de documentos brasileiros. O sistema utiliza modelos de OCR de última geração para processar diferentes tipos de documentos e extrair dados relevantes em formato JSON estruturado.

### Objetivos

- Automatizar a extração de informações de documentos brasileiros
- Experimentar e comparar diferentes modelos de OCR
- Disponibilizar ambiente interativo para prototipagem rápida


## Estrutura do repositório

```
structured-doc-extraction/
├── data/                               # Dados de teste e exemplos
│   ├── Challenge.pdf                   # Descrição do desafio
│   ├── case_01_drivers_license.jpeg    # Exemplo de CNH
│   ├── case_02_bill.jpg                # Exemplo de fatura de energia
│   └── case_03_large_document.pdf      # Exemplo de documento
│
├── experiments/                        # Experimentos com diferentes modelos
│   ├── deepseek_ocr.ipynb              # Experimento: DeepSeek-OCR
│   ├── florence_2_large.ipynb          # Experimento: Florence-2 Large
│   ├── paddleocr_vl.ipynb              # Experimento: PaddleOCR-VL
│   ├── data_experiments/               # Dados para experimentos
│   └── README.md                       # Documentação dos experimentos
│
├── poc/                                # Provas de conceito
│   ├── api/                            # POC 1: API RESTful
│   │   ├── backend/                    # Backend: FastAPI
│   │   ├── frontend/                   # Frontend: JavaScript
│   │   ├── logs/                       # Logs da aplicação
│   │   ├── start.sh                    # Script de inicialização
│   │   └── stop.sh                     # Script de parada
│   │
│   ├── jupyter_notebook/               # POC 2: Jupyter Notebook
│   │   ├── poc_jn.ipynb                # Notebook completo
│   │   └── data_challenge/             # Dados de teste
│   │
│   └── README.md                       # Documentação das POCs
│
├── LICENSE                             # Licença MIT
└── README.md                           # Este arquivo
```

## Funcionalidades

### Processamento de documentos

- **Carteira Nacional de Habilitação (CNH)**

- **Fatura de energia**

- **Documentos de múltiplas páginas**

### Pré-processamento

- Redimensionamento automático de imagens (máx. 1200px)
- Conversão de PDF para imagens
- Manutenção de proporções originais
- Otimização para inferência

### Pós-processamento

- Correção automática de JSON malformado
- Validação de estrutura de dados
- Formatação padronizada de saída
- Tratamento de erros robusto

## Tecnologias utilizadas

### Modelos de IA

- **Florence-2 Large** (Microsoft) - OCR de alta qualidade para produção
- **olmOCR-2-7B-1025-INT4** (AllenAI) - OCR quantizado para experimentação
- **DeepSeek-OCR** - Modelo experimental (4-bit quantizado)
- **PaddleOCR-VL** - OCR multilíngue experimental

### Backend

- **FastAPI** - Framework web moderno e performático
- **Pydantic** - Validação de dados e schemas
- **Uvicorn** - Servidor ASGI de alta performance
- **Python 3.11+** - Linguagem base

### Frontend

- **JavaScript Vanilla** - Sem dependências, leve e rápido
- **HTML5/CSS3** - Interface moderna e responsiva
- **Nginx** - Servidor web para produção

### Processamento

- **PyTorch** - Framework de deep learning
- **Transformers** (HuggingFace) - Modelos pré-treinados
- **Pillow (PIL)** - Processamento de imagens
- **pdf2image** - Conversão de PDF para imagem
- **json-repair** - Correção de JSON

### Infraestrutura

- **Docker** - Containerização (opcional para API)
- **Jupyter Notebook** - Ambiente interativo
- **Google Colab** - Execução em nuvem


## Implementações

### POC 1: API RESTful

Solução completa de produção com arquitetura cliente-servidor.

**Características:**
- Backend FastAPI com documentação automática
- Frontend web moderno e responsivo
- Upload via drag & drop
- Processamento em tempo real
- Scripts de inicialização automática

### POC 2: Jupyter Notebook

Ambiente interativo para experimentação e prototipagem.

**Características:**
- Processamento em lote
- Funcoes reutilizaveis
- Visualização de resultados
- Suporte a GPU
- Executável no Google Colab

## Experimentos

O diretório `experiments/` contém notebooks experimentais testando diferentes modelos de OCR:

### Modelos Testados

1. **Florence-2 Large** (Microsoft)
   - Modelo multimodal visão-linguagem
   - Alta qualidade de OCR
   - Executável em CPU (lento) ou GPU

2. **DeepSeek-OCR** (4-bit Quantizado)
   - Modelo quantizado para economia de memória
   - Requer GPU
   - Boa precisão com menor uso de recursos

3. **PaddleOCR-VL** (PaddlePaddle)
   - OCR multilíngue
   - Suporte a tabelas, fórmulas e gráficos
   - Versão Vision-Language moderna

**Documentação:** [experiments/README.md](experiments/README.md)

## Requisitos

### Requisitos mínimos

- **Python**: 3.11 ou superior
- **RAM**: 16GB
- **Espaço em disco**: 20GB

### Requisitos opcionais

- **GPU**: NVIDIA com CUDA (para melhor performance)
- **VRAM**: 10-16GB (para modelos completos)

### Dependências Python

```
torch>=2.0.0
transformers>=4.30.0
fastapi>=0.100.0
uvicorn>=0.23.0
pillow>=10.0.0
pdf2image>=1.16.0
json-repair>=0.7.0
pydantic>=2.0.0
python-multipart>=0.0.6
```
