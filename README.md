# London Sport × OpenActive
### Exploring innovative use of OpenActive data to increase physical activity in London

![Status](https://img.shields.io/badge/status-in%20development-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Unit](https://img.shields.io/badge/Bristol-SEMTM0044-red)
![Access](https://img.shields.io/badge/access-private%20%26%20confidential-lightgrey)

MSc Data Science group project (capstone) at the **University of Bristol**, delivered in partnership with **London Sport**. The project investigates how OpenActive open data can help more Londoners — especially the least active — find and take part in local physical activity.

> **Status — direction being finalised.** The precise research direction is being agreed with our academic supervisor and the project partner. This repository's structure and scope may evolve until the project plan is signed off. Current planning lives in `docs/`.

---

## Contents
- [About the project](#about-the-project)
- [Repository structure](#repository-structure)
- [Getting started](#getting-started)
- [Data](#data)
- [Ways of working](#ways-of-working)
- [Project milestones](#project-milestones)
- [Tech stack](#tech-stack)
- [Team](#team)
- [Acknowledgements](#acknowledgements)
- [Confidentiality](#confidentiality)

---

## About the project

| | |
|---|---|
| **Institution** | University of Bristol — MSc Data Science |
| **Unit** | Data Science Group Project (`SEMTM0044`, 60 credits, capstone) |
| **Partner** | London Sport |
| **Brief** | Exploring innovative use of OpenActive data to increase physical activity in London |
| **Cohort** | 2025/26 |
| **Final hand-in** | 4 September 2026 |

**Background.** OpenActive is the national open-data standard for the sport and physical-activity sector, publishing structured data on activity sessions, locations, schedules, prices and availability. The dataset has grown from roughly 76,000 opportunities in 2017 to more than two million in 2024. Despite this scale, finding and booking activities remains fragmented, and provision is uneven across London's diverse communities. This project reviews and analyses OpenActive data and develops new models, prototypes or recommendations to improve how Londoners discover and engage with local activity.

---

## Repository structure

```text
ls-openactive/
├── data/            # Raw and processed data — git-ignored, never committed
│   ├── raw/         # Original, untouched source data
│   └── processed/   # Cleaned, analysis-ready data
├── notebooks/       # Exploratory analysis and prototyping
├── src/             # Reusable, tested code and pipeline modules
├── tests/           # Automated tests
├── docs/            # Planning, methodology, data dictionary, team notes
├── reports/         # Figures, outputs and report assets
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md
```

---

## Getting started

**Prerequisites:** Python 3.10+ and Git.

```bash
# 1. Clone the repository
git clone https://github.com/michaelsamuel2005/ls-openactive.git
cd ls-openactive

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

Datasets are **not** included (see [Data](#data)) — you fetch them locally.

---

## Data

This project uses open data, and **no datasets are committed to the repository**. The `data/` folder is git-ignored by design.

- Place original source data in `data/raw/` and cleaned outputs in `data/processed/`.
- Record every data source — its URL, licence, and the date retrieved — in `docs/`.
- Any data shared privately by London Sport stays in `data/` (git-ignored) and must never be pushed.

Primary source: OpenActive feeds for London. Complementary open datasets (for example deprivation, demographic, and activity-participation data) may be added once the direction is confirmed.

---

## Ways of working

We use a branch-based pull-request workflow — no direct commits to `main`.

```bash
git checkout main && git pull          # start from the latest main
git checkout -b feature/short-name     # one branch per task
# ...do the work, then:
git add .
git commit -m "Clear, present-tense message"
git push -u origin feature/short-name
gh pr create --fill                    # open a pull request
```

A teammate reviews the pull request; it is then squash-merged into `main` and the branch deleted. Pull `main` again before starting new work.

**Branch naming:** `feature/…` (new work), `fix/…` (bug fixes), `docs/…` (documentation), `chore/…` (housekeeping).
**Commits:** small, frequent, and clearly described.

---

## Project milestones

| Milestone | Target |
|---|---|
| Project direction agreed and signed off | Late June 2026 |
| Formative review-panel presentation | ~4 weeks into the project |
| Data-quality assessment complete | July 2026 |
| Mid-project progress review | Mid-project |
| Full draft report | Mid-August 2026 |
| **Final submission (report, code, presentation)** | **4 September 2026** |
| Optional presentation to London Sport | October 2026 |

*Indicative and subject to confirmation with our supervisor.*

---

## Tech stack

Python · pandas · NumPy · scikit-learn · Jupyter · Matplotlib, with further libraries (for example geospatial tooling) added as the work develops. Version control with Git and GitHub.

---

## Team

See [`docs/team.md`](docs/team.md). The project is delivered by a team of four MSc Data Science students, supervised by Dalila O'Grady with teaching-assistant support from Alex, in partnership with London Sport (problem owners: Josef Baines, Insight Manager; Muhammad Bilal Alam, Data & Analytics Lead).

---

## Acknowledgements

Undertaken with **London Sport** as project partner and supported by the **School of Engineering Mathematics and Technology, University of Bristol**. Built on the **OpenActive** community standard and open data published across the sector.

---

## Confidentiality

This is a private academic project repository and is **not** licensed for public reuse. Any data or materials provided by London Sport are confidential and must not be redistributed. Please do not share repository contents outside the project team, supervisors, and partner without permission.
