\# Clinical Privacy Gateway — Project Workflow



\## 1. Purpose



The Clinical Privacy Gateway protects sensitive clinical information before it is processed by a downstream Large Language Model (LLM).



The gateway sits between the application submitting clinical text and the downstream model.



Its primary workflow is:



```text

Clinical Text

&#x20;    |

&#x20;    v

PHI Detection

&#x20;    |

&#x20;    v

PHI Validation

&#x20;    |

&#x20;    v

De-identification

&#x20;    |

&#x20;    v

Protected Mapping

&#x20;    |

&#x20;    v

LLM Processing

&#x20;    |

&#x20;    v

Response Rehydration

&#x20;    |

&#x20;    v

API Response

```



The fundamental privacy requirement is:



> \*\*The downstream LLM must receive de-identified text rather than raw PHI.\*\*



\---



\## 2. End-to-End Workflow



The complete processing pipeline consists of the following stages:



1\. Request submission

2\. Input validation

3\. PHI detection

4\. PHI validation

5\. PHI de-identification

6\. Protected mapping

7\. LLM processing

8\. Response rehydration

9\. API response



\---



\## 3. Stage 1 — Request Submission



A client application sends clinical text to the Clinical Privacy Gateway through the FastAPI API.



Example request content:



```text

Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.

```



The client does not communicate directly with the downstream LLM.



Instead:



```text

Client

&#x20; |

&#x20; v

Clinical Privacy Gateway

&#x20; |

&#x20; v

Downstream LLM

```



This allows the gateway to enforce the privacy controls before model processing.



\---



\## 4. Stage 2 — API Input Validation



The API layer receives the request and validates the incoming data.



The gateway ensures that the request contains usable clinical text before continuing with the PHI protection pipeline.



Invalid or empty input is rejected instead of being passed through the processing pipeline.



This provides an initial input boundary before PHI detection begins.



\---



\## 5. Stage 3 — PHI Detection



The PHI detector analyzes the clinical text and identifies potentially sensitive entities.



The detection system combines:



```text

Microsoft Presidio

&#x20;       +

Custom PHI Recognizers

```



Examples of detected entities include:



```text

PERSON

LOCATION

DATE\_TIME

EMAIL\_ADDRESS

PHONE\_NUMBER

MEDICAL\_RECORD\_NUMBER

ACCOUNT\_NUMBER

HEALTH\_PLAN\_BENEFICIARY\_NUMBER

```



Example:



```text

Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.

```



Detected entities:



```text

PERSON

&#x20;   Marcus Whitfield



DATE\_TIME

&#x20;   14 March 1978



LOCATION

&#x20;   Boston

```



At this stage, detections are candidates for PHI protection.



They are not immediately sent to the de-identification layer.



\---



\## 6. Stage 4 — PHI Validation



The detected entities are passed to the PHI validation layer.



The validator improves detection quality before de-identification.



The validation process includes:



```text

Confidence Score Filtering

&#x20;         |

&#x20;         v

Overlap Resolution

&#x20;         |

&#x20;         v

Identifier Prioritization

&#x20;         |

&#x20;         v

Accepted PHI Detections

```



\### Confidence Filtering



Detections below the configured minimum confidence score can be rejected.



This helps reduce weak or unreliable detections.



\### Overlap Resolution



Multiple recognizers may identify overlapping portions of the same text.



The validator resolves these conflicts and selects the appropriate detection.



\### Identifier Prioritization



Custom clinical identifiers can be prioritized when they overlap with generic Presidio detections.



For example:



```text

MRN PCG-4471902

```



should be treated as:



```text

MEDICAL\_RECORD\_NUMBER

```



rather than allowing a weaker overlapping detection to take precedence.



\---



\## 7. Stage 5 — PHI De-identification



After validation, accepted PHI entities are replaced with controlled placeholder tokens.



Example input:



```text

Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.

```



Protected output:



```text

Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



The clinical meaning and surrounding text are preserved while the original sensitive values are removed from the text that will be sent to the LLM.



\---



\## 8. Stage 6 — Protected Mapping



When PHI is replaced, the gateway maintains a mapping between the generated placeholder tokens and the original values.



Example:



```text

Patient\_001       -> Marcus Whitfield

DATE\_001          -> 14 March 1978

LOCATION\_001      -> Boston

```



The mapping is maintained inside the gateway's controlled processing layer.



The downstream LLM receives the protected text but does not receive the original PHI mapping.



Conceptually:



```text

&#x20;                 Gateway

&#x20;                    |

&#x20;       +------------+------------+

&#x20;       |                         |

&#x20;       v                         v

&#x20; Protected Text             PHI Mapping

&#x20;       |                         |

&#x20;       |                         |

&#x20;       v                         |

&#x20;      LLM                       |

&#x20;       |                         |

&#x20;       +----------+--------------+

&#x20;                  |

&#x20;                  v

&#x20;             Rehydration

```



This separation is a key part of the privacy architecture.



\---



\## 9. Stage 7 — LLM Processing



Only the de-identified text is passed to the configured LLM provider.



The LLM receives:



```text

Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



The LLM does not receive:



```text

Marcus Whitfield

14 March 1978

Boston

```



The LLM can therefore process the clinical context without requiring direct access to the original sensitive identifiers.



\---



\## 10. Stage 8 — Response Rehydration



After the LLM generates a response, the gateway passes the response through the rehydration layer.



The rehydrator looks for known placeholder tokens and restores their corresponding original values using the protected mapping.



Example LLM response:



```text

Clinical summary: Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



Rehydrated response:



```text

Clinical summary: Patient Marcus Whitfield was born on

14 March 1978 and lives in Boston.

```



Rehydration occurs after LLM processing.



Therefore, the original PHI does not need to be exposed to the downstream model.



\---



\## 11. Stage 9 — API Response



The final processed response is returned to the requesting client application.



Conceptually:



```text

Client Request

&#x20;     |

&#x20;     v

Clinical Privacy Gateway

&#x20;     |

&#x20;     +--> PHI Detection

&#x20;     |

&#x20;     +--> PHI Validation

&#x20;     |

&#x20;     +--> De-identification

&#x20;     |

&#x20;     +--> LLM Processing

&#x20;     |

&#x20;     +--> Rehydration

&#x20;     |

&#x20;     v

Final API Response

```



The processing transaction may also be associated with a mapping identifier.



The mapping identifier identifies the relevant mapping transaction without exposing the PHI mapping itself.



\---



\# 12. Complete Example



Consider the following clinical input:



```text

Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.

```



\### Step 1 — Detect



The detector identifies:



```text

PERSON

&#x20;   Marcus Whitfield



DATE\_TIME

&#x20;   14 March 1978



LOCATION

&#x20;   Boston

```



\### Step 2 — Validate



The validator checks:



```text

Confidence

Overlapping detections

Identifier priority

```



The accepted entities are:



```text

PERSON

DATE\_TIME

LOCATION

```



\### Step 3 — De-identify



The gateway replaces the PHI:



```text

Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



\### Step 4 — Store Mapping



The gateway maintains:



```text

Patient\_001       -> Marcus Whitfield

DATE\_001          -> 14 March 1978

LOCATION\_001      -> Boston

```



\### Step 5 — Send to LLM



The LLM receives:



```text

Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



It does not receive the original values.



\### Step 6 — LLM Generates Response



Example:



```text

Clinical summary: Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.

```



\### Step 7 — Rehydrate



The gateway restores the known placeholders:



```text

Clinical summary: Patient Marcus Whitfield was born on

14 March 1978 and lives in Boston.

```



\### Step 8 — Return Response



The final response is returned to the client application.



\---



\# 13. Security-Critical Workflow



The most important part of the workflow is the LLM boundary.



```text

&#x20;                ORIGINAL PHI

&#x20;                     |

&#x20;                     v

&#x20;             +---------------+

&#x20;             | PHI Detection  |

&#x20;             +-------+-------+

&#x20;                     |

&#x20;                     v

&#x20;             +---------------+

&#x20;             | PHI Validation |

&#x20;             +-------+-------+

&#x20;                     |

&#x20;                     v

&#x20;             +---------------+

&#x20;             | De-identify    |

&#x20;             +-------+-------+

&#x20;                     |

&#x20;                     | SAFE TEXT ONLY

&#x20;                     v

&#x20;             =================

&#x20;              LLM BOUNDARY

&#x20;             =================

&#x20;                     |

&#x20;                     v

&#x20;             +---------------+

&#x20;             |      LLM      |

&#x20;             +-------+-------+

&#x20;                     |

&#x20;                     | Response

&#x20;                     v

&#x20;             +---------------+

&#x20;             |  Rehydration   |

&#x20;             +-------+-------+

&#x20;                     |

&#x20;                     v

&#x20;               API Response

```



The privacy boundary prevents the downstream model from receiving the original PHI during normal processing.



\---



\# 14. API Processing Paths



The gateway exposes different API operations for different processing purposes.



\## De-identification Path



The de-identification path is used when the client needs the detected PHI to be replaced with safe placeholders.



```text

Client

&#x20; |

&#x20; v

POST /api/v1/deidentify

&#x20; |

&#x20; v

PHI Detection

&#x20; |

&#x20; v

PHI Validation

&#x20; |

&#x20; v

De-identification

&#x20; |

&#x20; v

Protected Text

```



\---



\## Full Processing Path



The full processing path performs the complete privacy-preserving LLM workflow.



```text

Client

&#x20; |

&#x20; v

POST /api/v1/process

&#x20; |

&#x20; v

PHI Detection

&#x20; |

&#x20; v

PHI Validation

&#x20; |

&#x20; v

De-identification

&#x20; |

&#x20; v

LLM Processing

&#x20; |

&#x20; v

Response Rehydration

&#x20; |

&#x20; v

Final Response

```



\---



\# 15. Failure Handling



The system is designed to reject invalid processing conditions rather than silently continuing.



Examples include:



```text

Empty request text

&#x20;       |

&#x20;       v

Request rejected

```



```text

Missing mapping

&#x20;       |

&#x20;       v

Rehydration error

```



```text

Invalid or unsupported processing input

&#x20;       |

&#x20;       v

API validation failure

```



The test suite verifies several of these conditions.



\---



\# 16. Testing Workflow



The project uses multiple levels of testing.



```text

&#x20;                Test Suite

&#x20;                    |

&#x20;       +------------+------------+

&#x20;       |            |            |

&#x20;       v            v            v

&#x20;     Unit         API       Security

&#x20;     Tests       Tests        Tests

&#x20;       |            |            |

&#x20;       +------------+------------+

&#x20;                    |

&#x20;                    v

&#x20;             Integration Tests

&#x20;                    |

&#x20;                    v

&#x20;             Evaluation Script

&#x20;                    |

&#x20;                    v

&#x20;            Precision / Recall

```



The current test suite contains:



```text

26 automated tests

```



All current tests pass.



The PHI detection evaluation currently reports:



```text

True Positives  : 8

False Positives : 1

False Negatives : 0



Precision       : 0.8889

Recall          : 1.0000

F1 Score        : 0.9412

```



These metrics are based on the evaluation cases currently included in the repository.



\---



\# 17. Workflow Summary



The complete workflow can be summarized as:



```text

1\. Client submits clinical text

&#x20;                |

&#x20;                v

2\. API validates the request

&#x20;                |

&#x20;                v

3\. PHI detector identifies sensitive entities

&#x20;                |

&#x20;                v

4\. Validator filters and prioritizes detections

&#x20;                |

&#x20;                v

5\. De-identification replaces PHI with safe tokens

&#x20;                |

&#x20;                v

6\. Original values are maintained in controlled mapping

&#x20;                |

&#x20;                v

7\. Only protected text is sent to the LLM

&#x20;                |

&#x20;                v

8\. LLM generates a response

&#x20;                |

&#x20;                v

9\. Rehydrator restores known placeholders

&#x20;                |

&#x20;                v

10\. Final response is returned to the client

```



\---



\# 18. Core Design Principle



The entire workflow is built around one central principle:



> \*\*Protect sensitive information before model processing, and restore it only after model processing when required.\*\*



This allows the gateway to separate:



```text

Clinical Context

```



from:



```text

Sensitive Identifiers

```



while still allowing the downstream model to process the useful clinical content.



\---



\# 19. Workflow at a Glance



```text

&#x20;                 +----------------------+

&#x20;                 | Clinical Application |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            | Original Text

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |   FastAPI Gateway    |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |    PHI Detection     |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |    PHI Validation    |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |  De-identification   |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            | Safe Text

&#x20;                            v

&#x20;                 ========================

&#x20;                      LLM BOUNDARY

&#x20;                 ========================

&#x20;                            |

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |   LLM Processing     |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            | Response

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |     Rehydrator       |

&#x20;                 +----------+-----------+

&#x20;                            |

&#x20;                            v

&#x20;                 +----------------------+

&#x20;                 |    API Response      |

&#x20;                 +----------------------+

```



\---



\## 20. Final Workflow Guarantee



The gateway is designed so that:



```text

Original Clinical Text

&#x20;       |

&#x20;       v

PHI Protection

&#x20;       |

&#x20;       v

De-identified Text

&#x20;       |

&#x20;       v

LLM

```



rather than:



```text

Original Clinical Text

&#x20;       |

&#x20;       v

LLM

```



The privacy-preserving workflow is therefore:



> \*\*Detect → Validate → De-identify → Process → Rehydrate\*\*
