import torch
import time

# Tamanho da matriz
N = 4096  # ajuste para testar diferentes cargas

# Cria duas matrizes aleatórias INT8 na CPU
a = torch.randint(-128, 127, (N, N), dtype=torch.int8, device='cpu')
b = torch.randint(-128, 127, (N, N), dtype=torch.int8, device='cpu')

def int8_matmul_cpu(a, b):
    # PyTorch não suporta matmul direto em int8, converte para float32
    return torch.matmul(a.float(), b.float())

# Aquece a CPU (warmup)
for _ in range(3):
    c = int8_matmul_cpu(a, b)

# Mede o tempo de 10 multiplicações de matriz
start = time.time()
for _ in range(10):
    c = int8_matmul_cpu(a, b)
end = time.time()

tempo_medio = (end - start) / 10
print(f"Tempo médio por matmul INT8 (CPU): {tempo_medio:.6f} segundos")

# Calcula OPS (operações inteiras por segundo)
ops = 2 * (N ** 3) / tempo_medio
tops = ops / 1e12
print(f"Desempenho estimado: {tops:.2f} TOPS (INT8 simulado, CPU)")
