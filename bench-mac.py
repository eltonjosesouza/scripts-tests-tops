import torch
import time
import platform

# Detecta se está em Mac com Apple Silicon (M1/M2/M3)
is_apple_silicon = platform.system() == "Darwin" and torch.backends.mps.is_available()

# Tamanho da matriz
N = 4096  # ajuste conforme desejado

device = 'mps' if is_apple_silicon else 'cpu'
print(f"Rodando benchmark em: {device.upper()}")

# Cria duas matrizes aleatórias INT8 no device adequado
a = torch.randint(-128, 127, (N, N), dtype=torch.int8, device=device)
b = torch.randint(-128, 127, (N, N), dtype=torch.int8, device=device)

def int8_simulated_matmul_mac(a, b):
    # Matmul em float32, mas calcula desempenho como se fosse INT8
    return torch.matmul(a.float(), b.float())

# Aquece o device (warmup)
for _ in range(3):
    c = int8_simulated_matmul_mac(a, b)

if device == 'mps':
    torch.mps.synchronize()

# Mede o tempo de 10 multiplicações de matriz
start = time.time()
for _ in range(10):
    c = int8_simulated_matmul_mac(a, b)
if device == 'mps':
    torch.mps.synchronize()
end = time.time()

tempo_medio = (end - start) / 10
print(f"Tempo médio por matmul (float32, simulando INT8, {device.upper()}): {tempo_medio:.6f} segundos")

# Calcula OPS (operações inteiras por segundo)
ops = 2 * (N ** 3) / tempo_medio
tops = ops / 1e12
print(f"Desempenho estimado: {tops:.2f} TOPS (simulação INT8, cálculo em float32, {device.upper()})")
