# P01 GPT Human Review Order v1

Open canonical `REF01`–`REF03` side-by-side for every review. The Identity Master may be viewed for human benchmark context only; it was not used as a production generation input.

1. **BUS_01**
   - C01 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_01_v1\P01_BUS_01_GPT_C01.png` — machine mean `0.885309`
   - C02 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_01_v1\P01_BUS_01_GPT_C02.png` — machine mean `0.867965`
   - C03 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_01_v1\P01_BUS_01_GPT_C03.png` — machine mean `0.872464`
2. **BUS_03**
   - C01 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_03_v1\P01_BUS_03_GPT_C01.png` — machine mean `0.880694`
   - C02 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_03_v1\P01_BUS_03_GPT_C02.png` — machine mean `0.853416`
   - C03 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_03_v1\P01_BUS_03_GPT_C03.png` — machine mean `0.843049`
3. **BUS_05**
   - C01 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_05_v1\P01_BUS_05_GPT_C01.png` — machine mean `0.839156`
   - C02 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_05_v1\P01_BUS_05_GPT_C02.png` — machine mean `0.800374`
   - C03 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_05_v1\P01_BUS_05_GPT_C03.png` — machine mean `0.797974`
4. **BUS_09**
   - C01 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_09_v1\P01_BUS_09_GPT_C01.png` — machine mean `0.760114` — incomplete run (`1/3`), non-equivalent.
5. **BUS_10**
   - C01 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_10_v1\P01_BUS_10_GPT_C01.png` — machine mean `0.502434`
   - C02 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_10_v1\P01_BUS_10_GPT_C02.png` — machine mean `0.515471`
   - C03 — `D:\AI\ONYX\09 Experiments\identity_benchmark_v1\P01_M30_Corporate\03_benchmark_runs\gpt_BUS_10_v1\P01_BUS_10_GPT_C03.png` — machine mean `0.542918`

BUS_10 is a high-priority calibration case: machine similarity is approximately `0.50–0.54` while face area remains materially larger than BUS_09. Review it to distinguish genuine identity drift from low similarity caused mainly by small face scale; do not conclude the cause automatically.
