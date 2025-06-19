# SLM4SWRL Framework
SLM-assisted generation of SWRL rules from natural language

## What is SLM4SWRL
The SLM4SWRL is an SLM-based GraphRAG-enhanced framework for translating natural language (NL) rules into Semantic Web Language (SWRL) rules.
The framework allows the users to utilize LLMs (e.g., ChatGPT, Llama, Gemini, etc.) and SLMs that runs locally via Ollama (e.g., Mistral, Llama-3.1).

![SLM4SWRL_architecture](https://github.com/user-attachments/assets/4f81bb59-c2e5-4191-b0cb-48d9412fb189)

## Research Methodology
### Experimental Ontology in a Graph format from the Search and Rescue (SAR) domain

![ontology](https://github.com/user-attachments/assets/8f892065-cbe0-4462-ad28-6957375c0625)

### Experimental Rules in NL 
* Rule 1: if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission.
* Rule 2: if a person is recognized at coordinates and has heart rate less than 30 pulses per minute and the location in these coordinates is safe, then send to thsese coordinates a search and rescue team.
* Rule 3: if house on fire is recognized at coordinates and person has Voice Sign 'help', then send alert to fire station, send to these coordinates a search and rescue team, send to these coordinates a flying drone agent and send to these coordinates a spot robot agent.

### Prompt Engineering

#### Example
Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. \
PART OF ONTOLOGY 

isRecognizedAt (domain: Gas, range: Coordinates) \
hasGasLevel (domain: Gas, range: xsd:Integer) \
hasLatitude (domain: Coordinates, range: xsd:Double) \
hasLongitude (domain: Coordinates, range: xsd:Double) \
hasCoordinates (domain: House, range: Coordinates) \
hasCoordinates (domain: Location, range: Coordinates) \
hasCoordinates (domain: Person, range: Coordinates) \
isNearby (domain: Agent, range: Coordinates) \
isRecognizedAt (domain: Fire, range: Coordinates) \
isRecognizedAt (domain: Gas, range: Coordinates) \
sendTo (domain: Agent, range: Coordinates) \
isRecognizedAt (domain: Fire, range: Coordinates) \
HasFireIntensity (domain: Fire, range: xsd:Integer) \
sendAlert (domain: Alert, range: Fire Station) \
sendAlert (domain: Alert, range: Agent) \
sendAlert (domain: Alert, range: Fire Station) \
hasParticipants (domain: Mission, range: Agent) \
abortMission (domain: Agent, range: Mission) 

END OF ONTOLOGY 

The rule in natural language is the following: if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission. Give only the final SWRL rule

#### Response
Gas(?gas) ∧ Fire(?fire) ∧ Coordinates(?coordinates) ∧ isRecognizedAt(?gas, ?coordinates) ∧ isRecognizedAt(?fire, ?coordinates) ∧ Agent(?agent) ∧ Alert(?alert) ∧ hasParticipants(?mission, ?agent) ∧ isNearby(?agent, ?coordinates) → sendAlert(?alert, ?fireStation) ∧ abortMission(?agent, ?mission)

### Metrics

![metrics](https://github.com/user-attachments/assets/aa7796dc-9949-4967-a515-f42cd9ef7829)

#### Important Node
Ollama and Neo4j are required for running the framework

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

## Neo4j 
```bash
CALL n10s.graphconfig.init();
```
```bash
CALL n10s.rdf.import.fetch("https://raw.githubusercontent.com/beAWARE-project/ontology/master/beAWARE_ontology.owl","RDF/XML");
```
