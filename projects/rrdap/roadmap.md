# RRDAP milestones and scope

High-level planning only. Do not expose future detailed tasks, expected pain points or intended solutions in ordinary sessions. Adjust sequence from current requirements and verified implementation. No phase forces a technology.

| Phase | Area | Status |
| --- | --- | --- |
| 1 | Initial retail business operations | Active: RDS-001 Product Catalogue, awaiting learner approach |
| 2 | Continuous synthetic business activity | Planned |
| 3 | Additional business systems and data sources | Planned |
| 4 | Cross-system data integration | Planned |
| 5 | Analytical storage and transformations | Planned |
| 6 | Batch and real-time processing | Planned |
| 7 | Business reporting | Planned |
| 8 | Performance and scaling | Planned |
| 9 | Reliability and recovery | Planned |
| 10 | Final integration and demonstration | Planned |

## Delivery target

30 November 2026 is a stretch target for a first demonstrable end-to-end flow across operational data, ingestion, processing and reporting. Zero phases complete. Do not claim feasibility from the date alone; evaluate scope and throughput from actual early implementation. Remaining effort is not yet estimated from evidence. The superseded RetailFlow 200-250-hour estimate is not a validated estimate for this larger project. Retain existing sustainable weekly study targets and reviews; protect correctness and learning quality.

Long-term scope: simulated retail operations, continuous generation, genuinely independent sources representing one business, real-time/near-real-time and batch/incremental movement, transactional/analytical storage, transformations, orchestration, distributed experiments, marts/reporting, monitoring/recovery, archives and tested database restoration. Introduce entities and tables only when current business requirements need them.

The eventual generator uses Python Faker plus business rules; do not introduce it into RDS-001 as a compulsory solution. Long-term objectives are 20 million records per day and up to 300 GB of actual stored analytical data, conditional on measured hardware/storage capacity. Generated counts and successfully stored counts must be reported separately. Begin with representative bounded workloads; no volume generated during setup. Master data growth must stay realistic.

Future capacity experiments may use 1/5/10/30/100 million-row checkpoints and larger partitions when justified. Record actual bytes/rows, runtime, CPU, peak memory, disk I/O, throughput, latency, pressure, correctness and recovery; for distributed tests also shuffle/spill/network. Establish resource limits and stop conditions before scaling. Never deliberately exhaust memory or fill disks.

Continuous generation eventually needs adjustable rates, bounded batches/memory/disk use, consistent IDs and transaction rules, pause/resume, graceful shutdown and safe restart. Independent sources can include databases, business files, APIs and events where justified; do not feed the whole final platform from one CSV/database or use disconnected random datasets to tick connector boxes.

Archive/backup work requires verification and isolated restoration; table exports alone are not a complete recoverable database backup. Preserve the original working data. Adopt/reject/postpone tool decisions only after fair same-workload comparison and recorded evidence; do not build the whole inventory upfront.
