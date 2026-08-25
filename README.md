<a id="readme-top"></a>



<!-- PROJECT SHIELDS -->



\[!\[Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)

\[!\[Presidio](https://img.shields.io/badge/Microsoft-Presidio-5C2D91?style=for-the-badge)](https://microsoft.github.io/presidio/)

\[!\[Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)](https://pytest.org/)

\[!\[Status](https://img.shields.io/badge/Status-Working-2EA44F?style=for-the-badge)](#project-status)



<!-- PROJECT LOGO -->



<br />

<div align="center">



&#x20; <h1 align="center">Clinical Privacy Gateway</h1>



&#x20; <p align="center">

&#x20;   A privacy-preserving gateway for protecting clinical text before downstream foundation-model processing.

&#x20;   <br />

&#x20;   <br />

&#x20;   <a href="https://github.com/VNKWORKS/clinical-privacy-gateway">View Repository</a>

&#x20;   \&middot;

&#x20;   <a href="#demo">View Demo</a>

&#x20;   \&middot;

&#x20;   <a href="#evaluation">View Evaluation</a>

&#x20;   \&middot;

&#x20;   <a href="#documentation">View Documentation</a>

&#x20; </p>

</div>



\---



\## Table of Contents



<details>

&#x20; <summary>Contents</summary>



\- \[About the Project](#about-the-project)

&#x20; - \[Problem Statement](#problem-statement)

&#x20; - \[Project Objective](#project-objective)

&#x20; - \[Key Features](#key-features)

\- \[System Architecture](#system-architecture)

\- \[Privacy Workflow](#privacy-workflow)

\- \[PHI Detection](#phi-detection)

\- \[Technology Stack](#technology-stack)

\- \[Project Structure](#project-structure)

\- \[Getting Started](#getting-started)

&#x20; - \[Prerequisites](#prerequisites)

&#x20; - \[Installation](#installation)

&#x20; - \[Environment Configuration](#environment-configuration)

&#x20; - \[Run the Application](#run-the-application)

\- \[API Documentation](#api-documentation)

&#x20; - \[Health Check](#health-check)

&#x20; - \[De-identification API](#de-identification-api)

&#x20; - \[Secure Processing API](#secure-processing-api)

\- \[Usage](#usage)

&#x20; - \[Example Input](#example-input)

&#x20; - \[Masked Output](#masked-output)

&#x20; - \[Final Output](#final-output)

\- \[LLM Integration](#llm-integration)

\- \[Security and Privacy](#security-and-privacy)

\- \[Evaluation](#evaluation)

\- \[Testing](#testing)

\- \[Demo](#demo)

\- \[Documentation](#documentation)

\- \[Project Status](#project-status)

\- \[Limitations](#limitations)

\- \[Future Improvements](#future-improvements)

\- \[Contributing](#contributing)

\- \[License](#license)

\- \[Contact](#contact)



</details>



\---



\## About the Project



Clinical and healthcare text can contain sensitive information such as patient names, dates, locations, medical record numbers, account numbers, insurance identifiers, email addresses, and phone numbers.



When clinical text is processed by a downstream language model, sending the original text directly to the model can expose sensitive information.



\*\*Clinical Privacy Gateway\*\* addresses this problem by placing a privacy layer between the source application and the downstream language model.



The gateway detects PHI, validates the detections, replaces sensitive values with controlled placeholders, sends only the de-identified text to the LLM, and rehydrates approved placeholders after model processing.



\### Core Principle



> \*\*Detect → Validate → Mask → Process → Rehydrate\*\*



The architecture is designed around the requirement that the downstream LLM should receive \*\*masked clinical text rather than raw PHI\*\*.



\---



\## Problem Statement



A typical clinical AI workflow can look like:



```text

Clinical Text

&#x20;    |

&#x20;    v

Foundation Model

&#x20;    |

&#x20;    v

Generated Response
