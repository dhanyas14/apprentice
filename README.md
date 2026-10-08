# ⚡ Apprentice

> **Tagline:** *Show it once. It writes the skill.*  
> **Challenge:** [MLH Open Source AI](https://www.mlh.com/opensource-ai) • **Standard:** [Agent Skills Open Standard](https://agentskills.io/specification) • **License:** [Apache-2.0](LICENSE)

[![Agent Skills Standard](https://img.shields.io/badge/standard-agentskills.io-emerald.svg)](https://agentskills.io/specification)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Model](https://img.shields.io/badge/model-Gemma--2--9B%20%7C%202B-indigo.svg)](https://ai.google.dev/gemma)
[![Python](https://img.shields.io/badge/python-3.10%2B-slate.svg)](https://www.python.org/)

---

## 🎯 The Problem

Nearly all AI Agent skills today are hand-written in code by software developers. Meanwhile, the people who actually possess deep, life-or-death tacit knowledge—electricians, machine operators, solar technicians, agricultural specialists, surgical nurses—**do not write code**.

When non-programmers explain things aloud, current AI systems either build unstructured chat summaries or hallucinate dangerous shortcuts. 

Furthermore, **how do you know the AI didn't invent a dummy or lethal instruction?** In physical trades, trusting an unverified AI skill can fry a \$4,000 optical sensor or trigger an 800V arc-flash explosion.

---

## 💡 The Solution: Apprentice

**Apprentice** turns spoken or filmed human know-how into a valid, standard-compliant Agent Skill (`SKILL.md`), verified through an **AI Teach-Back Oral Exam** and cryptographically certified by **Licensed Company Authorities**.

```
[Person 1: The Practitioner]
       │ (Explains/demonstrates a task over voice or video)
       ▼
[Open-Weight AI (Gemma 2 / Ollama)]
       │ 1. Extracts triggers, prerequisites, sequential steps, safety gotchas
       │ 2. Compiles standard-compliant SKILL.md (agentskills.io)
       │ 3. Generates 5 adversarial challenge scenarios
       ▼
[The AI Teaches Back] ──► Offline student model answers scenarios using ONLY the skill
       │                  Yields a quantitative Skill Fidelity Score (e.g. 95/100)
       ▼
[Person 2: The Licensed Auditor]
       │ 1. Verified against Official Company Licensing Registry (e.g. LIC-88219)
       │ 2. Inspects side-by-side truth vs. generated skill
       │ 3. Interrogates the AI with live corner cases
       ▼
[Verified Skill Commons] ──► Sealed with SHA-256 HMAC signature and published
```

---

## 👥 The Two-Person "Trust Loop"

| Role | Who They Are | What They Do |
| :--- | :--- | :--- |
| **Person 1: The Contributor** | Any frontline technician, farmer, or worker. | Speaks naturally in their own language. No programming knowledge required. |
| **The AI (Apprentice)** | Open-weight model (Gemma 2 2B/9B). | Structures the demonstration into `SKILL.md` and sits for an oral exam. |
| **Person 2: The Licensed Auditor** | Certified safety engineer or company inspector. | Validates license credentials, stresses the AI with oral questions, and stamps it as verified. |

---

## 🔬 Scientific Hook: The Teach-Back Exam & Fidelity Score

Apprentice doesn't just hope the skill works. Before any human signs off, an isolated "student" model is loaded with **only the generated `SKILL.md`** and subjected to 5 adversarial field situations:

1. **Happy Path Sequence Fidelity**: Tests whether the agent correctly initializes prerequisites and step 1.
2. **Safety Hazard Containment**: Simulates a technician in a rush attempting to skip safety gear (e.g. ESD grounding, 5-minute capacitor bleed). The agent must halt and enforce the rule.
3. **Hardware / Tool Substitution**: Evaluates whether the agent detects uncalibrated or out-of-spec equipment.
4. **Diagnostic Gotcha Detection**: Tests if the agent catches subtle anomalies (e.g. 3 blinks vs 4 blinks).
5. **Boundary & Scope Refusal**: Tests if the agent refuses to execute when asked to operate beyond designated equipment ratings.

The results yield an objective **Skill Fidelity Score (0-100)**. Skills scoring below 80% are rejected back to the contributor for re-demonstration.

---

## 📦 Verified Skill Commons

Once approved by Person 2 so that other can belive, skills are saved to `skills_commons/<skill-name>/SKILL.md` with full cryptographic frontmatter:

```yaml
---
name: industrial-rotary-sensor-calibration
description: Standard operating procedure for industrial rotary sensor calibration derived from field expert demonstration.
version: 1.0.0
license: Apache-2.0
author: Ramesh Patel
domain: industrial
tags:
- industrial
- rotary
- sensor
- calibration
fidelity_score: 95
status: certified
verified_by: Sarah Jenkins, PE (LIC-88219)
certifying_authority: National Electrical Contractors & Safety Board
audit_timestamp: '2026-10-04T07:24:50Z'
signature_seal: a82db5017d59c1a9e20f216f1571ed13181a19f4d5d4b9409debf0f8f92999b1
---
```

Any open-source agent runtime (Ollama, OpenCode, Hugging Face, llama.cpp) can mount this folder and execute offline.

---

## 🚀 Quickstart & How to Run

### 1. Installation
Clone the repository and install the lightweight dependencies:

```bash
git clone https://github.com/your-username/apprentice.git
cd apprentice
pip install -r requirements.txt
```

### 2. Launch the Web Application
Start the interactive UI:

```bash
python run.py --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

### 3. Run the CLI Test Demonstration
To run a fast terminal-based verification:

```bash
python run.py --cli
```

### 4. Running with Local Open-Weight Models (Ollama / Gemma)
Apprentice natively interfaces with local open-weight models via Ollama:

```bash
# Pull the open-weight Gemma-2 model (<=10B parameters)
ollama pull gemma2:9b

# Apprentice will automatically detect Ollama at http://localhost:11434
python run.py
```

---

## 🏛️ Open Source & Open Weights Compliance

- **Model Used:** [Google Gemma 2](https://ai.google.dev/gemma) (2B and 9B parameter open-weight models).
- **Model Terms & License:** Open weights under [Gemma Terms of Use](https://ai.google.dev/gemma/terms).
- **Agent Skill Standard:** Fully conforms to [agentskills.io/specification](https://agentskills.io/specification).
- **Repository License:** Licensed under the permissive [Apache License 2.0](LICENSE).

---

## 📂 Project Architecture

```
apprentice/
├── apprentice/
│   ├── app.py              # FastAPI Web server & REST endpoints
│   ├── compiler.py         # Voice/Video-to-SKILL.md compilation engine
│   ├── models.py           # Pydantic schema for submissions & skills
│   ├── teach_back.py       # Adversarial oral defense & fidelity scoring
│   ├── validator.py        # agentskills.io format & frontmatter validator
│   ├── verifier.py         # Person 2 license validator & cryptographic seal
│   └── static/
│       └── index.html      # Responsive Tailwind Web UI
├── data/
│   └── samples/
│       └── sample_transcripts.py  # Pre-loaded field demonstrations
├── skills_commons/         # Public repository of verified Agent Skills
│   ├── industrial-rotary-sensor-calibration/
│   ├── solar-inverter-arc-flash-reset/
│   └── agriculture-soil-salinity-tdr-probe/
├── requirements.txt        # Project dependencies
├── LICENSE                 # Apache-2.0 Open Source License
├── run.py                  # Main entrypoint
└── README.md
```
