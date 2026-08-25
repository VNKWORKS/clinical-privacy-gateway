<a id="readme-top"></a>

# Clinical Privacy Gateway

A privacy-preserving API gateway for detecting and de-identifying Protected Health Information (PHI) in clinical text before it reaches a downstream Large Language Model (LLM).

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Presidio](https://img.shields.io/badge/Microsoft%20Presidio-PHI%20Detection-5C2D91?style=for-the-badge)](https://microsoft.github.io/presidio/)
[![Pytest](https://img.shields.io/badge/Pytest-26%20Tests%20Passing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## Table of Contents

- [About the Project](#about-the-project)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Supported PHI](#supported-phi)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Example](#example)
- [Security and Privacy](#security-and-privacy)
- [Evaluation](#evaluation)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Development Workflow](#development-workflow)
- [License](#license)
- [Author](#author)

---

## About the Project

Clinical and healthcare text can contain sensitive information such as patient names, dates of birth, locations, medical record numbers, account numbers, insurance identifiers, email addresses, and phone numbers.

Sending this information directly to a downstream language model can unnecessarily expose sensitive data.

**Clinical Privacy Gateway** addresses this problem by placing a privacy layer between the application handling clinical text and the downstream LLM.

The gateway follows the principle:

> **Detect → Validate → De-identify → Process → Rehydrate**

The primary security requirement is:

> **Raw PHI must not be sent to the downstream LLM.**

This project is implemented as a Python-based REST API and includes PHI detection, validation, controlled masking, mapping, LLM abstraction, rehydration, security tests, and evaluation metrics.

---

## Problem Statement

A conventional clinical AI workflow may look like:

```text
Clinical Text
     |
     v
Foundation Model / LLM
     |
     v
Generated Response
````

If the original clinical text contains PHI, sensitive information may cross the downstream model boundary.

The goal of this project is to introduce a privacy gateway:

```text
Clinical Application
        |
        | Raw clinical text
        v
+---------------------------+
|   Clinical Privacy        |
|        Gateway             |
|                           |
|  1. Detect PHI            |
|  2. Validate detections   |
|  3. De-identify PHI       |
+---------------------------+
        |
        | De-identified text
        v
+---------------------------+
|      Downstream LLM       |
+---------------------------+
        |
        | LLM response
        v
+---------------------------+
|       Rehydrator          |
+---------------------------+
        |
        v
   Final Response
```

The intended privacy boundary is:

```text
RAW PHI
   |
   X
   |
   +---------------------> Downstream LLM
          blocked
```

Instead:

```text
RAW CLINICAL TEXT
        |
        v
   PHI DETECTION
        |
        v
    VALIDATION
        |
        v
 DE-IDENTIFICATION
        |
        v
 MASKED TEXT
        |
        v
       LLM
        |
        v
 LLM RESPONSE
        |
        v
   REHYDRATION
        |
        v
 FINAL RESPONSE
```

---

## Solution

The gateway detects potential PHI, validates the detections, replaces sensitive values with controlled placeholders, sends only the masked text to the downstream LLM, and then rehydrates approved placeholders after model processing.

### Original clinical text

```text
Patient Marcus Whitfield was born on 14 March 1978 and lives in Boston.
MRN PCG-4471902.
```

### Masked text sent to the LLM

```text
Patient Patient_001 was born on DATE_001 and lives in LOCATION_001.
MEDICAL_RECORD_NUMBER_001.
```

The downstream LLM therefore receives the clinical context without receiving the original sensitive values.

### LLM response

```text
Clinical summary: Patient Patient_001 was born on DATE_001 and
lives in LOCATION_001. MEDICAL_RECORD_NUMBER_001.
```

### Final response after controlled rehydration

```text
Clinical summary: Patient Marcus Whitfield was born on 14 March 1978
and lives in Boston. MRN PCG-4471902.
```

The key privacy property is that the LLM-processing stage operates on the de-identified representation.

---

## Key Features

### PHI Detection

Uses Microsoft Presidio Analyzer together with project-specific recognizers.

### Custom Clinical Identifiers

The project includes custom recognition support for:

* Medical Record Number
* Account Number
* Health Plan Beneficiary Number
* Insurance Member ID

### PHI Validation

Detected entities are validated using:

* Confidence score filtering
* Entity prioritization
* Overlap and conflict resolution

### Controlled De-identification

Detected PHI is replaced with controlled placeholders before downstream model processing.

### Mapping

The gateway maintains a mapping between generated placeholders and their corresponding original values.

### Rehydration

Approved placeholders can be restored after the LLM has completed processing.

### Configurable LLM Provider

The LLM layer is abstracted behind an LLM client interface and factory.

The current implementation supports:

* Mock LLM for local development and testing
* Configurable OpenAI LLM client

### Security Testing

The project contains explicit security tests verifying that raw PHI is not passed to the LLM.

### Evaluation

A dedicated evaluation module measures:

* True Positives
* False Positives
* False Negatives
* Precision
* Recall
* F1 Score

---

## Architecture

The application is organized around a privacy boundary between the clinical application and the downstream LLM.

```text
                         CLINICAL APPLICATION
                                |
                                | Raw clinical text
                                v
                    +-------------------------+
                    |   FastAPI API Layer     |
                    +-------------------------+
                                |
                                v
                    +-------------------------+
                    |      PHI Detector       |
                    |                         |
                    | Presidio + Custom       |
                    | Recognizers             |
                    +-------------------------+
                                |
                                v
                    +-------------------------+
                    |     PHI Validator       |
                    |                         |
                    | Confidence filtering    |
                    | Entity prioritization   |
                    | Conflict resolution     |
                    +-------------------------+
                                |
                                v
                    +-------------------------+
                    |     Deidentifier        |
                    |                         |
                    | PHI -> Placeholder      |
                    +-------------------------+
                                |
                                | Masked clinical text
                                v
                    +-------------------------+
                    |      LLM Client         |
                    |                         |
                    | Mock / OpenAI           |
                    +-------------------------+
                                |
                                | LLM response
                                v
                    +-------------------------+
                    |       Rehydrator        |
                    |                         |
                    | Placeholder -> PHI      |
                    +-------------------------+
                                |
                                v
                         FINAL RESPONSE
```

### Privacy Boundary

The most important architectural rule is:

```text
                         PRIVACY BOUNDARY
                                |
                                v

Raw PHI ---> Detection ---> Validation ---> Masking ---> LLM

                         RAW PHI DOES NOT CROSS
                         THE LLM BOUNDARY
```

---

## Workflow

The complete processing workflow is:

```text
1. Client submits clinical text
             |
             v
2. PHI Detection
             |
             v
3. PHI Validation
             |
             v
4. De-identification
             |
             v
5. PHI Mapping
             |
             v
6. Only masked text is sent to LLM
             |
             v
7. LLM generates response
             |
             v
8. Response is rehydrated
             |
             v
9. Final response returned
```

### Step 1 — Receive

The API receives clinical text from the client.

### Step 2 — Detect

The PHI detector analyzes the input and identifies possible sensitive entities.

### Step 3 — Validate

The validator applies confidence filtering and resolves conflicting or overlapping detections.

### Step 4 — De-identify

Validated PHI values are replaced with controlled placeholders.

### Step 5 — Create Mapping

The gateway maintains the relationship between placeholders and original values.

### Step 6 — Process

Only the de-identified text is passed to the downstream LLM.

### Step 7 — Receive

The LLM returns a response containing the placeholders.

### Step 8 — Rehydrate

Approved placeholders are restored using the mapping.

### Step 9 — Return

The final response is returned to the API client.

---

## Supported PHI

The current project and evaluation include the following categories:

| PHI Type                         | Example                                         |
| -------------------------------- | ----------------------------------------------- |
| `PERSON`                         | Marcus Whitfield                                |
| `LOCATION`                       | Boston                                          |
| `DATE_TIME`                      | 14 March 1978                                   |
| `MEDICAL_RECORD_NUMBER`          | MRN PCG-4471902                                 |
| `ACCOUNT_NUMBER`                 | AC-2026-123456                                  |
| `HEALTH_PLAN_BENEFICIARY_NUMBER` | HP-2026-445566                                  |
| `EMAIL_ADDRESS`                  | [marcus@example.com](mailto:marcus@example.com) |
| `PHONE_NUMBER`                   | 617-555-0182                                    |

The actual entities detected at runtime depend on the configured Presidio recognizers and custom recognizers.

---

## Technology Stack

| Technology                  | Purpose                         |
| --------------------------- | ------------------------------- |
| Python 3.10+                | Application development         |
| FastAPI                     | REST API framework              |
| Pydantic                    | Request and response validation |
| Microsoft Presidio          | PHI detection                   |
| Custom Presidio Recognizers | Domain-specific PHI detection   |
| Pytest                      | Automated testing               |
| Uvicorn                     | ASGI application server         |
| Configurable LLM Client     | Downstream LLM integration      |
| Git                         | Version control                 |
| GitHub                      | Repository hosting and review   |

---

## Project Structure

```text
clinical-privacy-gateway/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── core/
│   │
│   ├── models/
│   │
│   ├── recognizers/
│   │
│   ├── schemas/
│   │
│   ├── security/
│   │
│   ├── services/
│   │   ├── deidentifier.py
│   │   ├── gateway.py
│   │   ├── llm_client.py
│   │   ├── llm_factory.py
│   │   ├── mock_llm.py
│   │   ├── openai_llm.py
│   │   ├── phi_detector.py
│   │   ├── phi_validator.py
│   │   └── rehydrator.py
│   │
│   └── main.py
│
├── configs/
│
├── docs/
│
├── evaluation/
│   └── evaluate_phi.py
│
├── scripts/
│
├── tests/
│   ├── api/
│   ├── integration/
│   ├── security/
│   └── unit/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Getting Started

## Prerequisites

The project requires:

* Python 3.10 or newer
* Git
* PowerShell, Command Prompt, or another terminal

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

---

## Clone the Repository

```powershell
git clone https://github.com/VNKWORKS/clinical-privacy-gateway.git
cd clinical-privacy-gateway
```

---

## Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install project dependencies:

```powershell
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Configure the required environment variables in `.env`.

For local testing, the project can use the mock LLM provider.

If an external LLM provider is configured, provide its credentials through environment variables.

> Never commit `.env` or API keys to the repository.

The repository intentionally contains `.env.example` rather than real credentials.

---

# Running the Application

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

---

# API Documentation

The primary API endpoints are versioned under:

```text
/api/v1
```

---

## Health Check

### Endpoint

```text
GET /health
```

Example:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

The health endpoint verifies that the service is running.

---

## De-identify Endpoint

### Endpoint

```text
POST /api/v1/deidentify
```

This endpoint detects and de-identifies PHI without sending the text to the downstream LLM.

### Request

```json
{
  "text": "Patient Marcus Whitfield lives in Boston."
}
```

### PowerShell Example

```powershell
$payload = @{
    text = "Patient Marcus Whitfield lives in Boston."
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/deidentify" `
    -Method Post `
    -ContentType "application/json" `
    -Body $payload
```

### Response

```json
{
  "masked_text": "Patient Patient_001 lives in LOCATION_001.",
  "mapping_id": "mapping-id",
  "entities_detected": 2
}
```

The exact mapping ID is generated at runtime.

---

## Process Endpoint

### Endpoint

```text
POST /api/v1/process
```

This endpoint executes the complete privacy-preserving workflow:

```text
Detect
   |
   v
Validate
   |
   v
De-identify
   |
   v
LLM Processing
   |
   v
Rehydrate
```

### Request

```json
{
  "text": "Patient Marcus Whitfield was born on 14 March 1978 and lives in Boston. MRN PCG-4471902."
}
```

### PowerShell Example

```powershell
$payload = @{
    text = "Patient Marcus Whitfield was born on 14 March 1978 and lives in Boston. MRN PCG-4471902."
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/process" `
    -Method Post `
    -ContentType "application/json" `
    -Body $payload
```

### Response Structure

```json
{
  "masked_text": "Patient Patient_001 was born on DATE_001 and lives in LOCATION_001. MEDICAL_RECORD_NUMBER_001.",
  "llm_response": "Clinical summary: Patient Patient_001 was born on DATE_001 and lives in LOCATION_001. MEDICAL_RECORD_NUMBER_001.",
  "final_response": "Clinical summary: Patient Marcus Whitfield was born on 14 March 1978 and lives in Boston. MRN PCG-4471902.",
  "mapping_id": "mapping-id"
}
```

The exact response wording and mapping ID may vary depending on the configured LLM provider.

---

# Example

Consider the following clinical text:

```text
Patient Marcus Whitfield was born on 14 March 1978 and lives in Boston.
MRN PCG-4471902.
Account Number: AC-2026-123456.
Health Plan Beneficiary Number: HP-2026-445566.
Email marcus@example.com.
Phone 617-555-0182.
```

The gateway detects the sensitive entities.

A representative masked representation is:

```text
Patient Patient_001 was born on DATE_001 and lives in LOCATION_001.
MEDICAL_RECORD_NUMBER_001.
ACCOUNT_NUMBER_001.
HEALTH_PLAN_BENEFICIARY_NUMBER_001.
Email EMAIL_ADDRESS_001.
Phone PHONE_NUMBER_001.
```

Only the masked representation is passed to the LLM.

The LLM can therefore process the clinical context without requiring the original patient identifiers.

After processing, approved placeholders can be rehydrated using the gateway mapping.

---

# Security and Privacy

Security is the central design objective of this project.

## Raw PHI Protection

The gateway is designed so that raw PHI is processed before downstream LLM access:

```text
Raw Clinical Text
        |
        v
PHI Detection
        |
        v
Validation
        |
        v
De-identification
        |
        v
Masked Clinical Text
        |
        v
LLM
```

The prohibited path is:

```text
Raw Clinical Text
        |
        v
LLM
```

## Validation

The PHI validator applies a minimum confidence threshold and resolves overlapping detections.

Project-specific clinical identifiers are prioritized so that stronger domain-specific detections are not unnecessarily replaced by weaker generic recognizers.

## Mapping

The mapping mechanism associates generated placeholders with the original values required for controlled rehydration.

## Rehydration

Rehydration occurs after LLM processing rather than before it.

This maintains the privacy boundary during downstream model processing.

## Environment Secrets

Secrets such as API keys must be stored in environment variables and should never be committed to Git.

The `.gitignore` configuration protects local environment files from accidental repository commits.

## Security Tests

The project includes explicit tests verifying:

* Raw PHI does not reach the LLM.
* Masked text is passed to the LLM.
* PHI is rehydrated only after model processing.
* Unknown placeholders are not blindly restored.
* Mapping records can be saved and retrieved.
* Mapping records can be deleted.
* Missing mappings are handled safely.
* Multiple PHI types are protected together.

> This project demonstrates a privacy-preserving engineering architecture. It is not a claim of HIPAA certification or complete regulatory compliance.

---

# Evaluation

The project includes a dedicated PHI detection evaluation script:

```text
evaluation/evaluate_phi.py
```

Run the evaluation with:

```powershell
python -m evaluation.evaluate_phi
```

## Current Evaluation Results

The current evaluation produced:

| Metric          | Result |
| --------------- | -----: |
| True Positives  |      8 |
| False Positives |      1 |
| False Negatives |      0 |
| Precision       | 0.8889 |
| Recall          | 1.0000 |
| F1 Score        | 0.9412 |

### Interpretation

**Precision — 0.8889**

The detector produced a high proportion of expected entity categories relative to the total predicted categories in the evaluation cases.

**Recall — 1.0000**

All expected entity categories in the current evaluation cases were detected.

**F1 Score — 0.9412**

The F1 score provides a combined measure of precision and recall.

### Evaluation Scope

The current evaluation contains six representative test cases covering:

* Person
* Location
* Date and time
* Medical record number
* Account number
* Health plan beneficiary number
* Email address
* Phone number

These results should be interpreted as project-level evaluation results rather than as a production clinical benchmark because the evaluation dataset is intentionally small.

---

# Testing

Run the complete automated test suite:

```powershell
python -m pytest -v
```

Current result:

```text
26 passed
```

## Test Categories

### API Tests

The API test suite verifies:

* Health endpoint
* De-identification endpoint
* Empty input validation
* Process endpoint privacy behavior

### Security Tests

The security test suite verifies:

* Raw PHI never reaches the LLM
* Gateway rehydrates LLM responses
* Mapping IDs are returned
* Mapping records can be saved
* Mapping records can be retrieved
* Mapping records can be deleted
* Missing mappings are rejected
* Multiple PHI types are protected

### Unit Tests

Unit tests cover:

* Account number recognition
* Health plan beneficiary recognition
* Insurance member ID recognition
* Medical record number recognition
* PHI detector integration
* Presidio entity detection
* PHI validation
* Rehydration behavior

### Integration Tests

Integration tests include LLM client construction and integration behavior.

---

# Running Evaluation and Tests Together

A recommended local verification sequence is:

```powershell
python -m evaluation.evaluate_phi
python -m pytest -v
```

Expected evaluation summary:

```text
Precision      : 0.8889
Recall         : 1.0000
F1 Score       : 0.9412
```

Expected test result:

```text
26 passed
```

---

# Limitations

This repository is an engineering prototype demonstrating a privacy-preserving clinical text processing architecture.

Important limitations include:

* PHI detection is not guaranteed to be perfect.
* False positives and false negatives can occur.
* The current evaluation dataset is small.
* Real clinical documents may contain complex or previously unseen identifiers.
* Production deployment would require authentication and authorization controls.
* Production systems would require secure encryption and key management.
* Production systems would require appropriate monitoring and audit controls.
* Data retention policies would need to be defined for production environments.
* Regulatory compliance requires organizational, administrative, technical, and legal controls beyond this application.

The project should therefore be considered a demonstration of the architecture and engineering approach rather than a production-ready clinical compliance solution.

---

# Future Improvements

Potential future improvements include:

* Expand the PHI evaluation dataset.
* Add per-entity precision, recall, and F1 metrics.
* Add additional clinical PHI recognizers.
* Improve confidence calibration.
* Add authentication and authorization.
* Encrypt mapping storage.
* Add privacy-safe audit logging.
* Add Docker deployment.
* Add CI/CD pipelines.
* Add performance and load testing.
* Add production monitoring.
* Add additional LLM providers.
* Add document-level de-identification.
* Add configurable masking strategies.
* Add stronger mapping lifecycle and retention controls.

---

# Development Workflow

The recommended development workflow is:

```text
Modify Code
    |
    v
Run Targeted Tests
    |
    v
Run Full Test Suite
    |
    v
Run PHI Evaluation
    |
    v
Review Git Diff
    |
    v
Commit Changes
    |
    v
Push to GitHub
```

Useful commands:

```powershell
python -m pytest -v
python -m evaluation.evaluate_phi
git diff --check
git status
```

Before committing:

```powershell
git add .
git diff --cached --check
git diff --cached --stat
git commit -m "your commit message"
git push
```

---

# License

No dedicated open-source license is currently included in this repository.

If this project is intended for public open-source distribution, an appropriate license should be added.

---

# Author

**VNKWORKS**

Project repository:

[https://github.com/VNKWORKS/clinical-privacy-gateway](https://github.com/VNKWORKS/clinical-privacy-gateway)

---

<p align="center">
  <a href="#readme-top">Back to top</a>
</p>
