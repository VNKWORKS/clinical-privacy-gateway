# ClinicalShield Secure PHI Deidentification Gateway

## 1. Project Overview

ClinicalShield is a secure clinical text de-identification gateway designed to protect patient identifiers before clinical text is sent to a foundation language model.

The gateway accepts raw clinical text, detects protected health information (PHI), replaces identifiers with consistent pseudonyms or transformed values, securely maintains the required mapping, forwards only the de-identified text to a downstream foundation model, and safely rehydrates the model response when appropriate.

The primary engineering objective is to balance two competing requirements:

1. Prevent identifier leakage.
2. Preserve the clinical meaning required by downstream language-model applications.

The project is designed around the principle that both excessive leakage and excessive removal are failures.

---

## 2. Problem Statement

Healthcare organizations may want to use foundation language models for clinical summarization, question answering, and other clinical NLP tasks.

However, identifiable patient information should not be exposed to an external foundation model.

A simple redaction system can remove identifiers but may also remove information that is important for clinical reasoning.

For example:

Raw:

"Marcus Whitfield presented with right L5 radiculopathy after the collision."

A useful de-identification system should preserve the medical meaning while removing the identifying information.

Possible output:

"Patient_A presented with right L5 radiculopathy after the collision."

The project therefore focuses on privacy protection while preserving downstream clinical utility.

---

## 3. Target Outcome

The final system will provide the following end-to-end workflow:

Raw Clinical Text
        |
        v
PHI Detection
        |
        v
PHI Validation and Conflict Resolution
        |
        v
Secure De-identification
        |
        +--------------------+
        |                    |
        v                    v
Masked Clinical Text     Secure Mapping
        |
        v
Foundation LLM
        |
        v
LLM Response
        |
        v
Rehydration Security Check
        |
        v
Rehydrated Response

The complete workflow will be demonstrated using a synthetic clinical document.

---

## 4. Core Interfaces

The system will expose two core operations.

### De-identification

```text
deidentify(text) -> (masked_text, mapping)