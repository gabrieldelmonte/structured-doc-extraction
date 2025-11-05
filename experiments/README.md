# Experimentos

Este diretório contém notebooks experimentais para testar diferentes modelos de OCR e extração de informações de documentos

## Notebooks Disponíveis

### 1. `deepseek_ocr.ipynb` - DeepSeek OCR (4-bit Quantizado)

Experimento com o modelo **DeepSeek-OCR** quantizado em 4-bit para extração de texto de imagens

**Características:**
- Modelo quantizado (4-bit) para uso eficiente de memória
- Otimizado para Google Colab com GPU T4
- Suporta OCR em múltiplos tipos de documentos
- Configurações ajustáveis de qualidade vs velocidade

**Requisitos recomendados:**
- Python 3.11+
- GPU NVIDIA com CUDA
- ~8-12GB de VRAM (com quantização 4-bit)

**Como usar:**
1. Abra o notebook no Google Colab ou Jupyter
2. Execute as células sequencialmente
3. Ajuste os parâmetros conforme necessário
4. Coloque suas imagens no diretório `data_experiments/`
5. Execute o processamento de OCR

### 2. `florence_2_large.ipynb` - Florence-2 Large

Experimento com o modelo **Florence-2 Large** da Microsoft para extração de texto e análise de documentos

**Características:**
- Modelo de visão e linguagem multimodal da Microsoft
- Suporta múltiplas tarefas de visão computacional
- OCR de alta qualidade sem quantização
- Beam search para melhor precisão

**Requisitos recomendados:**
- Python 3.11+
- GPU NVIDIA com CUDA
- ~6-8GB de VRAM

**Como usar:**
1. Abra o notebook no Google Colab ou Jupyter
2. Execute as células sequencialmente
3. O modelo usa o prompt `<OCR>` para extração de texto
4. Coloque suas imagens no diretório `data_experiments/`
5. Execute o processamento de OCR

**Observação:** foi possível executar este experimento em CPU, mas é altamente recomendado o uso de GPU para melhor desempenho! 

### 3. `paddleocr_vl.ipynb` - PaddleOCR VL

Experimento com o modelo **PaddleOCR-VL** da PaddlePaddle para OCR multilíngue e reconhecimento de documentos

**Características:**
- Modelo de visão e linguagem multilíngue
- Suporta múltiplas tarefas: OCR, tabelas, fórmulas, gráficos
- Reconhecimento de texto em diversos idiomas
- Arquitetura moderna Vision-Language

**Requisitos recomendados:**
- Python 3.11+
- GPU NVIDIA com CUDA
- ~8-10GB de VRAM

**Como usar:**
1. Abra o notebook no Google Colab ou Jupyter
2. Execute as células sequencialmente
3. Escolha a tarefa desejada (OCR, Table, Chart, Formula)
4. Coloque suas imagens no diretório `data_experiments/`
5. Execute o processamento

## Estrutura de Diretórios

```
experiments/
├── data_experiments/       # Diretório para armazenar imagens de teste
│   └── ...
├── deepseek_ocr.ipynb      # Experimento DeepSeek-OCR
├── florence_2_large.ipynb  # Experimento Florence-2
├── paddleocr_vl.ipynb      # Experimento PaddleOCR
└── README.md               # Este arquivo
```

## Notas adicionais

- Todos os notebooks foram testados no Google Colab com GPU T4
- Por conta da limitação de memória do ambiente gratuito e da limitação de meu hardware local, alguns modelos foram descartados mesmo tendo apresentado bons resultados em benchmarks públicos. Recomendo testar esses modelos em ambientes com mais recursos computacionais, se possível, sendo eles:
  - **deepseek-ai/DeepSeek-OCR**: modelo base não quantizado (maior qualidade, maior uso de memória)
  - **allenai/olmOCR-2-7B-1025-FP8**: modelo OCR da AllenAI com desempenho excelente em sua demonstração pública porém não foi possível testá-lo devido ao seu grande tamanho e falta de recursos computacionais disponíveis
  - **lightonai/LightOnOCR-1B-1025**: modelo OCR da LightOnAI que não foi possível testá-lo e descartado por não possuir total suporte à biblioteca Transformers, dificultando sua integração e uso com o restante do código desenvolvido
