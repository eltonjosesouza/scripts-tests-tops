import torch
import time
import platform

# Detecta os dispositivos disponíveis
has_cuda = torch.cuda.is_available()
has_mps = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()

# Tamanho da matriz
N = 4096  # ajuste conforme desejado

# Lista de devices para testar
all_devices = []
if has_cuda:
    all_devices.append('cuda')
if has_mps:
    all_devices.append('mps')
all_devices.append('cpu')  # CPU sempre disponível

print(f"Dispositivos detectados: {all_devices}")

# Função de benchmark

def int8_matmul(a, b):
    # PyTorch não suporta matmul direto em int8, converte para float32
    return torch.matmul(a.float(), b.float())

for device in all_devices:
    print(f"\nRodando benchmark em: {device.upper()}")
    a = torch.randint(-128, 127, (N, N), dtype=torch.int8, device=device)
    b = torch.randint(-128, 127, (N, N), dtype=torch.int8, device=device)

    # Warmup
    for _ in range(3 if device == 'cpu' else 10):
        c = int8_matmul(a, b)
    if device == 'cuda':
        torch.cuda.synchronize()
    if device == 'mps':
        torch.mps.synchronize()

    # Benchmark
    reps = 10 if device == 'cpu' else 100
    start = time.time()
    for _ in range(reps):
        c = int8_matmul(a, b)
    if device == 'cuda':
        torch.cuda.synchronize()
    if device == 'mps':
        torch.mps.synchronize()
    end = time.time()

    tempo_medio = (end - start) / reps
    print(f"Tempo médio por matmul INT8 ({device.upper()}): {tempo_medio:.6f} segundos")

    # Calcula OPS (operações inteiras por segundo)
    ops = 2 * (N ** 3) / tempo_medio
    tops = ops / 1e12
    print(f"Desempenho estimado: {tops:.2f} TOPS (INT8 simulado, {device.upper()})")
