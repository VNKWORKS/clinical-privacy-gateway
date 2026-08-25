\# Clinical Privacy Gateway — Architecture



\## 1. System Overview



The Clinical Privacy Gateway is designed as a privacy boundary between clinical applications and downstream Large Language Models.



The system ensures that detected Protected Health Information (PHI) is replaced with safe placeholder tokens before clinical text is sent to an LLM.



The original PHI is retained only inside the application's controlled mapping layer and is restored after LLM processing.



\---



\## 2. High-Level Architecture



```text

&#x20;                        Clinical Application

&#x20;                                 |

&#x20;                                 | Clinical Text

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |     FastAPI API Gateway     |

&#x20;                   |                             |

&#x20;                   |  POST /api/v1/deidentify    |

&#x20;                   |  POST /api/v1/process       |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       PHI Detector          |

&#x20;                   |                             |

&#x20;                   | Microsoft Presidio          |

&#x20;                   | Custom PHI Recognizers       |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       PHI Validator          |

&#x20;                   |                             |

&#x20;                   | Score Filtering              |

&#x20;                   | Conflict Resolution           |

&#x20;                   | Identifier Prioritization     |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       Deidentifier          |

&#x20;                   |                             |

&#x20;                   | PHI -> Safe Tokens           |

&#x20;                   |                             |

&#x20;                   | Marcus Whitfield             |

&#x20;                   |        -> Patient\_001        |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 | SAFE / DE-IDENTIFIED TEXT

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       LLM Client Layer       |

&#x20;                   |                             |

&#x20;                   | Configurable Provider         |

&#x20;                   | Mock / OpenAI                 |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       LLM Processing         |

&#x20;                   |                             |

&#x20;                   | Receives ONLY masked text    |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 | LLM Response

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |        Rehydrator            |

&#x20;                   |                             |

&#x20;                   | Safe Token -> Original PHI   |

&#x20;                   +-------------+---------------+

&#x20;                                 |

&#x20;                                 v

&#x20;                   +-----------------------------+

&#x20;                   |       API Response           |

&#x20;                   |                             |

&#x20;                   | Final Clinical Response      |

&#x20;                   +-----------------------------+







&#x20;                   PRIVACY BOUNDARY

&#x20;                        |

&#x20;                        v



Original PHI

&#x20;   |

&#x20;   v

+------------------+

| PHI Detection    |

+------------------+

&#x20;   |

&#x20;   v

+------------------+

| PHI Validation   |

+------------------+

&#x20;   |

&#x20;   v

+------------------+

| De-identification|

+------------------+

&#x20;   |

&#x20;   | SAFE TEXT ONLY

&#x20;   v

+------------------+

|      LLM         |

+------------------+



Original PHI never crosses

the LLM boundary.



Step 1 — Request



A client submits clinical text to the API.



Example:



Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.

Step 2 — PHI Detection



The PHI detector analyzes the text and identifies entities such as:



PERSON

DATE\_TIME

LOCATION



For example:



Marcus Whitfield

14 March 1978

Boston

Step 3 — PHI Validation



Detected entities are passed through the PHI validator.



The validator performs:



minimum confidence score filtering

overlapping entity resolution

identifier prioritization

selection of the most appropriate PHI detection



This reduces false-positive detections from overlapping recognizers.



Step 4 — De-identification



Detected PHI is replaced with deterministic placeholder tokens.



Example:



Original:



Patient Marcus Whitfield was born on 14 March 1978

and lives in Boston.



Becomes:



Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.



The mapping is maintained internally.



Example:



Patient\_001  -> Marcus Whitfield

DATE\_001     -> 14 March 1978

LOCATION\_001 -> Boston

Step 5 — LLM Processing



Only the masked text is sent to the configured LLM provider.



The LLM receives:



Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.



It does not receive:



Marcus Whitfield

14 March 1978

Boston

Step 6 — Response Rehydration



The LLM response is passed to the rehydration layer.



Safe tokens are replaced with their original values.



Example:



LLM response:



Clinical summary: Patient Patient\_001 was born on DATE\_001

and lives in LOCATION\_001.



Becomes:



Clinical summary: Patient Marcus Whitfield was born on

14 March 1978 and lives in Boston.

Step 7 — API Response



The API returns the processed result together with the mapping identifier.



The mapping identifier allows the processing transaction to be referenced without exposing the mapping itself.
