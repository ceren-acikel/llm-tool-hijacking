# ToolGPT: Evaluating Metadata Manipulation Attacks in Tool-Augmented LLM Agents

This repository contains the implementation and experimental artifacts developed for a bachelor thesis on security and privacy risks in tool-augmented LLM agents.

The objective of the project is to evaluate whether metadata-level manipulation can influence tool selection in LLM agents and whether these biased selections can propagate into execution-layer compromise.

## Project Structure

- `data/` – experiment data and query files
- `data_example/` – tool definitions, schemas, and example resources
- `ds_configs/` – configuration files for the execution environment
- `preprocess/` – preprocessing utilities
- `scripts/` – helper scripts for setup and experiment support
- `toolbench/` – main source code directory containing the adapted ToolBench pipeline
- `malicious_beacon_q1.jsonl` – beacon log generated during Q1 runs
- `malicious_beacon_q2.jsonl` – beacon log generated during Q2 runs
- `README_base_toolllm.md` – reference copy of the original ToolLLM documentation
- `.env.example` – example environment file for API key configuration

## Experimental Setup

The project extends the ToolLLM framework with a controlled experimental setup for metadata-induced tool hijacking.

Malicious near-clone tools are introduced with overlapping descriptions, matching parameter schemas, and equivalent primary functionality.  
The main manipulated property is tool naming, in order to test metadata-induced selection bias.

In addition, each malicious tool contains an embedded beacon-style payload that records execution locally without performing real exfiltration.

## LLM Backend and Extensibility

The experiment pipeline is built on an adapted ToolBench architecture and extended for the controlled evaluation conducted in this thesis.

The main thesis-specific modifications include:

- restriction of the tool pool for controlled evaluation
- integration of malicious near-clone tools
- metadata-level manipulation through alternative tool naming
- beacon-based execution logging for malicious tool calls
- trust annotation via `security_level`
- new query sets for baseline and amplified conditions
- patched runner scripts for reproducible Q1 and Q2 execution

## Running the Experiments

Before execution, install the required dependencies and configure the necessary API keys through a local `.env` file.

Install dependencies:

```bash
pip install -r requirements.txt
```

Then add the required API keys to your .env file.

Run the experiment scripts from the repository root.

Run Q1:
```bash
python3 toolbench/run_Q1.py
```

Run Q2:
```bash
python3 toolbench/run_Q2.py
```

## Outputs

Experiment outputs are written to:

- `toolbench/tooleval/results/`

Beacon logs are stored separately in the repository root:

- `malicious_beacon_q1.jsonl`  
- `malicious_beacon_q2.jsonl`

These outputs are used to analyze malicious tool selection behavior and execution-layer activation under the two query conditions.

## License and Attribution

This repository builds on ToolLLM.  
Credit for the original framework remains with the ToolLLM authors.

All additional modifications implemented for the bachelor thesis experiments, including malicious tool integration, beacon-based execution instrumentation, trust annotation, retrieval logging, and experiment configuration, were developed in this repository for academic research purposes.
