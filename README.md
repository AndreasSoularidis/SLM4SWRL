# SLM2SWRL
SLM-assisted generation of SWRL rules from natural language

## What is SLM2SWRL
The SLM2SWRL is an SLM-based GraphRAG enhanced framework for translating natural language (NL) rules into Semantic Web Language (SWRL) rules.
The framework allows the users to utilize LLMs (e.g., ChatGPT, Llama, Gemini, etc.) and SLMs that runs locally via Ollama (e.g., Mistral, Llama-3.1).

## Research Methodology
### Utilized (Experimental) Ontology

### Rules in NL 
⦁	Rule 1: if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission.
⦁	Rule 2: if a person is recognized at coordinates and has heart rate less than 30 pulses per minute and the location in these coordinates is safe, then send to thsese coordinates a search and rescue team.
⦁	Rule 3: if house on fire is recognized at coordinates and person has Voice Sign 'help', then send alert to fire station, send to these coordinates a search and rescue team, send to these coordinates a flying drone agent and send to these coordinates a spot robot agent.


#### Important Node
Starting October 2nd, 2024, gpt-4o will point to the gpt-4o-2024-08-06 snapshot [Link](https://platform.openai.com/docs/models/gpt-4o)

## Guick Install
Python 3.10
For Windows
```bash
py -m venv .venv
```
```bash
.venv\Scripts\activate
```
```bash
py -m pip install -r requirements.txt
```

For Unix/macOS
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
python3 -m pip install -r requirements.txt
```
