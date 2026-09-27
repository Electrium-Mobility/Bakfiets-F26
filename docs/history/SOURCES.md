# Where these files came from

Copied on 2026-09-26 from [Electrium-Mobility/bakfiets](https://github.com/Electrium-Mobility/bakfiets), which stays unchanged as the archive. Its full commit history is there.

| Folder here | Source | Commit |
| --- | --- | --- |
| `mechanical/cad-2024/` | `mechanical/` on `main` | 4b86a22 (2024-07-04) |
| `mechanical/cad-2025-coop/` | `mechanical/bakfiets_coop_version/` on `summer2025coop` | 6fc9958 (2025-05-28) |
| `mechanical/cad-2025-coop/edited-2024-parts/` | five top-level `mechanical/` files as edited on `summer2025coop` | 6fc9958 |
| `firmware/display-2024/` | `firmware/main.cpp`, `firmware/display-prototype.jpeg` on `main` | 4b86a22 |
| `firmware/desk-demo/` | copy of `firmware/main.cpp` with `LED_PIN` changed from 9 to 5 | new |
| `firmware/simulator-2024/` | `firmware/simulator/` on `main`, without the 314 MB `target/` build folder | 4b86a22 |
| `firmware/can-twai-2024/` | `twai_can_sender/`, `twai_can_receiver/` on `twai_can` (open pull request #2 there) | 34b9d66 (2024-11-11) |
| `electrical/diagrams/high-level-circuit-diagram-2024.png` | `firmware/high-level-circuit-diagram.png` on `main` | 4b86a22 |
| `electrical/diagrams/*.png` (other), `firmware/diagrams/`, `docs/diagrams/` | drawn this term by the `.py` script next to each image | new |
| `docs/images/doc_hw_*.png` | composited from `docs/images/cad-previews/` | new |
| `docs/history/website-*.md`, `docs/images/render-2024.png`, `team-w2024.png` | [electrium-w24website](https://github.com/Electrium-Mobility/electrium-w24website) bakfiets pages | |
| `docs/images/cad-previews/` | preview images extracted from inside the SolidWorks files | new |
| `docs/images/doc_elec_examples.png`, `doc_hw_longtail.png` | F25 Skateboard and W2025 longtail pages on the website, and esc-w26 | |

Left out on purpose: `Frame 2.0-Static 2.CWR` (95 MB FEA results; rerun the study), SolidWorks lock files (`~$*`), `.DS_Store`, `sdkconfig.old`, and the simulator's build folder.

## 2024 team (from the club website)

| Role | People |
| --- | --- |
| Team lead and mechanical lead | Jerry Chen |
| Firmware lead | Patrick He |
| Electrical lead | Samuel Ke |
| Mechanical | Kevin Ng, Aidan Thompson, Aiyesha Shibly, Samual Wong, Allen Lu |
| Firmware | Kimberley Hoang, Alisa Wu, Aman Zaveri |
| Electrical | Jacob Wielowieyski, Alex Liu, Suhyma Rahman |

Other contributors on GitHub: etanguan (steering, jig, Frame 2.0 FEA, 2024), Simra Khan (CAN code, Nov 2024), Anthony3141 (co-op CAD, May 2025).
