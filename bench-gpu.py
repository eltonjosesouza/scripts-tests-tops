import torch
import time

# Tamanho da matriz (quanto maior, mais pesado o teste)
N = 8*1024

# Cria duas matrizes aleatórias INT8 na GPU
# PyTorch não suporta matmul direto de int8 na GPU, então convertemos para float32 na multiplicação
# Isso simula a carga de trabalho INT8, mas o resultado real de TOPS depende do suporte do hardware/framework

a = (torch.randint(-128, 127, (N, N), dtype=torch.int8, device='cuda'))
b = (torch.randint(-128, 127, (N, N), dtype=torch.int8, device='cuda'))

# Função para multiplicação INT8, convertendo para float32 para matmul
# (PyTorch atualmente não suporta torch.matmul direto em int8 na GPU)
def int8_matmul(a, b):
    return torch.matmul(a.float(), b.float())

# Aquece a GPU (warmup)
for _ in range(10):
    c = int8_matmul(a, b)

torch.cuda.synchronize()

# Mede o tempo de 100 multiplicações de matriz
start = time.time()
for _ in range(100):
    c = int8_matmul(a, b)
torch.cuda.synchronize()
end = time.time()

tempo_medio = (end - start) / 100
print(f"Tempo médio por matmul INT8: {tempo_medio:.6f} segundos")

# Calcula OPS (operações inteiras por segundo)
# Para multiplicação de matriz: 2*N^3 operações
ops = 2 * (N ** 3) / tempo_medio
tops = ops / 1e12
print(f"Desempenho estimado: {tops:.2f} TOPS (INT8 simulado)")