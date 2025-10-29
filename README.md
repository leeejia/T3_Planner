# **$T^3$ Planner: A Self-Correcting LLM Framework for Robotic Motion Planning with Temporal Logic**

## Overview
This repository contains the code implementation for our paper: [$T^3$ Planner: A Self-Correcting LLM Framework for Robotic Motion Planning with Temporal Logic](https://arxiv.org/pdf/2510.16767)
The framework decomposes spatio-temporal task constraints via three modules, each of which stimulates an LLM to generate candidate trajectory sequences and examines their feasibility via a Signal Temporal Logic (STL) verifier until one that satisfies complex spatial, temporal, and logical constraints is found.

![]

## Installation

1.  **Clone the repository**

2.  **Create and activate a Python virtual environment**

3.  **Install dependencies**

4.  **Configure environment variables**
    Create `.env` file and fill in the necessary configurations, such as your API keys.
    ```env
    # .env
    SCENARIO="household"
    Ge_MODEL="deepseek"
    HOUSEHOLD_DATA_FILE=".\test_dataset\household\test.jsonl"
    # Add your LLM API key
    # OPENAI_API_KEY="your-api-key-here"
    ```

## Usage

Execute the corresponding main file for the scenario you wish to run.

-   **Run the Household scenario:**
    ```bash
    python main_household.py
    ```


After execution, the results (including logs, plots, and JSONL files) will be saved in the `result/<SCENARIO>/<MODEL>` directory.

