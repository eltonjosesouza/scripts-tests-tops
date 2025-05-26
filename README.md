# Benchmarks de Matriz INT8 com PyTorch

Este projeto contém scripts para benchmark de multiplicação de matrizes INT8 utilizando PyTorch em diferentes dispositivos (CPU, GPU CUDA, Apple Silicon/MPS).

## Scripts Disponíveis
- `bench-auto.py`: Detecta automaticamente os dispositivos disponíveis e executa o benchmark em cada um.
- `bench-cpu.py`: Executa o benchmark apenas na CPU.
- `bench-gpu.py`: Executa o benchmark apenas na GPU CUDA (NVIDIA).
- `bench-mac.py`: Executa o benchmark em Macs com Apple Silicon (M1/M2/M3) usando MPS, ou na CPU caso não disponível.

## Como usar

### 1. Crie e ative um ambiente virtual (venv)

**macOS/Linux:**
```sh
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instale as dependências

```sh
pip install -r requirements.txt
```

> **Nota:**
> Recomenda-se instalar o PyTorch conforme seu hardware e sistema operacional. Consulte: https://pytorch.org/get-started/locally/

### 3. Execute o script desejado

```sh
python bench-auto.py
python bench-cpu.py
python bench-gpu.py
python bench-mac.py
```

## Observações
- Para benchmarks em GPU CUDA, é necessário ter uma placa NVIDIA compatível e PyTorch instalado com suporte CUDA.
- Para benchmarks em Apple Silicon, é necessário PyTorch >= 1.12 com suporte MPS.
- Ajuste o tamanho das matrizes (variável `N` nos scripts) conforme sua memória disponível.

---

Se tiver dúvidas ou quiser expandir os benchmarks, contribuições são bem-vindas!
