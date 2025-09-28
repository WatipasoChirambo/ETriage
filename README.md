# ETriage

ETriage is a hospital triage system designed to help local communities manage patient intake efficiently. It allows patients to submit their symptoms, view triage status, and helps hospitals allocate resources and reduce congestion.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Patient registration and symptom submission.
- Severity classification of cases.
- Admin dashboard to view and manage triage cases.
- Real-time updates for hospital staff.
- Responsive web frontend for both staff and patients.

## Tech Stack
- **Frontend:** Vue 3, Vite
- **Backend:** FastAPI, Python 3.11
- **Database:** PostgreSQL 15
- **Containerization:** Docker & Docker Compose
- **Deployment:** Local development via Docker

## System Architecture
The system consists of three main components:
1. **Frontend:** Vue 3 application served on port 5173.
2. **Backend:** FastAPI application served on port 8000, connected to PostgreSQL.
3. **Database:** PostgreSQL database storing patient data and triage information.

The components are containerized using Docker, enabling easy deployment and environment consistency.

## Installation

### Prerequisites
- Docker & Docker Compose installed
- Git installed
- Python 3.11 installed (for local development)

### Clone the Repository
```bash
git clone git@github.com:WatipasoChirambo/ETriage.git
cd ETriage
