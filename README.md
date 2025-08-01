# Objective Ethics Framework (OEF)

The Objective Ethics Framework (OEF) is a coordination architecture designed to embed structured, auditable, and adaptive ethical reasoning into AI systems. Unlike traditional top-down approaches that impose static moral principles, the OEF enables real-time routing, prioritization, and justification of ethical decisions using modular tools, heuristics, and recursive oversight.

This repository contains the full OEF whitepaper, visual routing diagram, glossary, and supporting resources for public reference and non-commercial development.

---

## 🔍 What Is the OEF?

The OEF is not a moral framework. It is a coordination system that:
- Assigns ethical evaluation tiers via contextual triage
- Routes decisions through logic modules, ethical processors, or human review
- Coordinates evidence, heuristics, and recursion
- Audits outcomes and supports long-term adaptive refinement

It is designed to work with any ethical input—bioethics, legal norms, or discipline-specific heuristics—without originating its own values.

---

## 📘 Whitepaper Contents

- Section 1: Why Ethics Needs a Rebuild
- Section 2: The Failure of Top-Down Ethics
- Section 3: From Principles to Practice
- Section 4: Structured Well-Being & Tiered Evaluation
- Sections 5–14: Ethical Tenets, Heuristics, System Architecture
- Appendix A: Glossary
- Appendix B: Limitations & Future Development

---

## 🧭 Visual: Tier Routing Overview

Each tier routes decisions differently based on context and risk:

- **Tier 1:** System Logic → Execution  
- **Tier 2:** EAP → System Logic → Execution  
- **Tier 3:** EAP → Logic → RAP → Execution  
- **Tier 4:** EAP → Logic → RAP → Human  
- **Tier 5:** Direct to Human Oversight  

Color-coded diagram included in `/visuals`.

---

## Code Module Descriptions
🔸 oef_core_structure.py
Purpose
Implements the core mechanics of the OEF decision-making process, including tier assignment (DEP), ethical routing (EAP, RAP), and feedback mechanisms. This file acts as the operational backbone of the framework.

Functionality
- Encapsulates ethical context via the EthicalDecision class
- Assigns ethical tiers based on urgency, scope, and context
- Routes decisions through modular ethical pathways using OEFProcessor
- Outputs traceable justifications for audit, adaptation, and system transparency

Use Case
Ideal for use in embedded ethical agents, simulations, or as a back-end component in AI systems requiring transparent, tiered ethical evaluation.

🔸 oef_scenario_processor.py
Purpose
A sandbox tool for testing how different scenarios are processed through the OEF routing architecture. Enables stress-testing, validation, and scenario-based iteration.

Functionality
- Provides predefined test scenarios across tiers 1–5
- Injects ethical decisions into the core processor
- Outputs routing decisions, justifications, and data used
- Demonstrates how pressure loops and modular pathways operate under varied constraints

Use Case
Best used for evaluating how the OEF performs under real-world or hypothetical conditions. Useful for developers, researchers, and ethics reviewers wanting to observe decision processing behavior.


---

## 📝 License

Unless otherwise noted, all code and content in this repository is released under the
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.
You are free to share and adapt the material for non-commercial purposes, as long as proper credit is given and derivative works are distributed under the same license.

👉 Read the license here

This license is also explicitly embedded in the whitepaper itself.

---

## ✍️ Author

**Haley Harper**  
Lead Ethics, Kraken Core  
📫 hello@kraken-core.com  
🔗 [kraken-core.com](https://kraken-core.com)

---

## 🤝 Citation & Use

If referencing the OEF in publications, please cite the full whitepaper or contact the author for integration guidance. Any use of the framework in live systems should adhere to the embedded transparency and traceability requirements described in Sections 7–10.
