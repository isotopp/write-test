# Runtime Results

## M1 Mac

Local 1 TB NVME, apfs

| Op                     | Runtime (ns)   | Runtime (ms) |
|------------------------|----------------|--------------|
| Create table           | 36998000 ns    | 36.998 ms    |
| Write data             | 11005393000 ns | 11005.393 ms |
| Recreate table         | 22558000 ns    | 22.558 ms    |
| Write data slowly      | 30811135000 ns | 30811.135 ms |
| Recreate table again   | 18370000 ns    | 18.37 ms     |
| Write data very slowly | 41130705000 ns | 41130.705 ms |

## Ubuntu 22.04 on i7-3770

Local 512 GB Crucial SSD

| Op      | Runtime (ns)   | Runtime (ms)    |
|---------|----------------|-----------------|
| Create: | 47036782 ns    | 47.036782 ms    |
| Write:  | 37819320227 ns | 37819.320227 ms |
