# Snapshot RUP

Datapoints de Ramp-Up Time (`RUP`) nos primeiros 10 minutos de 1º de setembro de 2026 (UTC).

- Projeto CDF: `bdx-dev`
- Space da timeseries: `sp_otm_san_dat`
- External ID: `{assetExternalId}-parameter-RUP`
- Janela: `2026-09-01T00:00:00Z` inclusive até `2026-09-01T00:10:00Z` exclusive
- Unidade: não definida na série
- Releitura: a ZN02 permaneceu idêntica à leitura anterior, ponto a ponto

Cada série tem 10 pontos, um por minuto.

| Timestamp (UTC) | ZN02 | CL52 | CL53 | CL43 |
|---|---:|---:|---:|---:|
| 2026-09-01T00:00:00Z | 0.8261666666666667 | 0.12408333333333334 | 0.0 | 0.0 |
| 2026-09-01T00:01:00Z | 1.0 | 1.0 | 0.7614 | 0.0 |
| 2026-09-01T00:02:00Z | 0.9832166666666667 | 1.0 | 1.0 | 0.0 |
| 2026-09-01T00:03:00Z | 1.0 | 1.0 | 1.0 | 0.29375 |
| 2026-09-01T00:04:00Z | 1.0 | 1.0 | 1.0 | 1.0 |
| 2026-09-01T00:05:00Z | 0.3070333333333333 | 1.0 | 0.21641666666666665 | 1.0 |
| 2026-09-01T00:06:00Z | 0.0 | 1.0 | 0.0 | 0.9104166666666667 |
| 2026-09-01T00:07:00Z | 0.0 | 0.6219333333333333 | 0.0 | 0.0 |
| 2026-09-01T00:08:00Z | 0.0 | 0.0 | 0.0 | 0.0 |
| 2026-09-01T00:09:00Z | 0.0 | 0.0 | 0.0 | 0.0 |

| Asset | Nome | Descrição | Timeseries |
|---|---|---|---|
| `ZNE-c3f8c22976e17c1844da1e971d06b704` | ZN02 | L10 Z2 Catheter Tipping | `ZNE-c3f8c22976e17c1844da1e971d06b704-parameter-RUP` |
| `MCH-16b9877c5d5f8f08ff36e32fbcdffe6e` | CL52 | L10 Z5 C52 Catheter Orientation and Inspection | `MCH-16b9877c5d5f8f08ff36e32fbcdffe6e-parameter-RUP` |
| `MCH-333370cac9c4b486133369bac11151c7` | CL53 | L10 Z5 C53 Flow Test and Barrel Load | `MCH-333370cac9c4b486133369bac11151c7-parameter-RUP` |
| `MCH-acea58aa17f237391294124100c22a28` | CL43 | L10 Z4 C43 Cannula Bonding and Lubrication | `MCH-acea58aa17f237391294124100c22a28-parameter-RUP` |
