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

def int8_simulated_benchmark(N, device):
    '''
    Benchmark rodando em float32, mas calculando TOPS como se fosse INT8.
    '''
    import torch.nn as nn
    # Cria camada Linear em float32
    linear = nn.Linear(N, N, bias=False).to(device)
    linear.eval()

    # Dados de entrada (float32)
    a = torch.randn(N, N).to(device)

    # Warmup
    for _ in range(3):
        out = linear(a)
    # Benchmark
    reps = 10
    import time
    start = time.time()
    for _ in range(reps):
        out = linear(a)
    # Sincroniza para garantir medição correta em dispositivos acelerados
    if device == 'cuda':
        torch.cuda.synchronize()
    elif device == 'mps' and hasattr(torch, 'mps') and hasattr(torch.mps, 'synchronize'):
        torch.mps.synchronize()
    end = time.time()
    tempo_medio = (end - start) / reps
    print(f"Tempo médio por Linear (float32, simulando INT8): {tempo_medio:.6f} segundos")
    # Calcula OPS (operações inteiras por segundo) como se fosse INT8
    ops = 2 * (N ** 3) / tempo_medio
    tops = ops / 1e12
    print(f"Desempenho estimado: {tops:.2f} TOPS (simulação INT8, cálculo em float32, CPU)")
    return tops


for device in all_devices:
    print(f"\nRodando benchmark simulando INT8 (cálculo em float32, device={device})")
    int8_simulated_benchmark(N, device)
# Observação: Este benchmark roda em float32, mas calcula o desempenho como se fosse INT8, para comparação com números de fabricantes.
