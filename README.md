\# Multi-Agent Negotiation Simulator



\## Project Overview

The Multi-Agent Negotiation Simulator is a web-based platform designed to simulate negotiation scenarios involving multiple stakeholders with different goals, constraints, and personalities.



This module focuses on \*\*Scenario Selection and Agent Configuration\*\* for three negotiation scenarios.



\## Features

\- Select from three negotiation scenarios.

\- Automatically load scenario-specific agents and their configurations.

\- View each agent's role, description, goals, and constraints.

\- Configure agent personalities:

&#x20; - Aggressive

&#x20; - Collaborative

&#x20; - Risk-Averse

\- Validate and submit the configuration before starting a negotiation.

\- View negotiation results and conversation transcripts.

\- Support for vendor pricing, job offer, and project budget allocation scenarios.



\## Technology Stack



\### Frontend

\- React

\- Vite

\- JavaScript

\- CSS



\### Backend

\- Python

\- FastAPI

\- Uvicorn



\## Project Structure



```text

Team-2/

├── backend/

│   ├── main.py

│   ├── schemas.py

│   └── negotiation\_engine.py

├── frontend/

│   ├── src/

│   │   ├── App.jsx

│   │   ├── App.css

│   │   └── data/

│   │       └── scenarios.js

│   ├── package.json

│   └── vite.config.js

├── .gitignore

└── README.md

```



\## Getting Started



\### Prerequisites

\- Python 3.10 or later

\- Node.js and npm

\- Git



\### 1. Clone the Repository



```bash

git clone https://github.com/saiprasath13/Infosys-Springboard-Virtual-Internship-Team-2.git

cd Infosys-Springboard-Virtual-Internship-Team-2

```



\### 2. Start the Backend



Open a terminal in the project root:



```powershell

cd backend

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install fastapi uvicorn

uvicorn main:app --reload

```



Backend API: `http://127.0.0.1:8000`



API documentation: `http://127.0.0.1:8000/docs`



\### 3. Start the Frontend



Open a \*\*second terminal\*\* in the project root:



```powershell

cd frontend

npm install

npm run dev

```



Open the local URL shown in the terminal, usually `http://localhost:5173`.



\## Available Scenarios



1\. \*\*Vendor Pricing Negotiation\*\* — simulate negotiation between a buyer and a vendor.

2\. \*\*Job Offer Negotiation\*\* — simulate negotiation between a candidate and a recruiter.

3\. \*\*Project Budget Allocation\*\* — review and allocate a project budget among different teams.



\## Agent Personalities



\- \*\*Aggressive:\*\* prioritizes assertive negotiation.

\- \*\*Collaborative:\*\* prioritizes mutually beneficial outcomes.

\- \*\*Risk-Averse:\*\* prioritizes minimizing risk and protecting constraints.



\## Current Implementation Note



The negotiation engine currently uses rule-based simulation logic. LLM-powered autonomous negotiation is not yet implemented.



\## Team



\*\*Team 2 — Infosys Springboard Virtual Internship Program 7.0\*\*



Repository: \[GitHub](https://github.com/saiprasath13/Infosys-Springboard-Virtual-Internship-Team-2)

