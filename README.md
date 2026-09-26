# SLM4SWRL Framework
SLM-assisted generation of SWRL rules from Natural Language (NL)

## What is SLM4SWRL
The SLM4SWRL is an SLM-based (Graph)RAG-enhanced framework for translating NL rules into Semantic Web Language (SWRL) rules.
The framework allows users to utilize LLMs (e.g., ChatGPT) and SLMs (e.g., Llama3.1, Mistralv0.3, Miinstral3, Gemma2, and Qwen2.5) that run locally via Ollama

## Architecture 

![SLM4SWRL_architecture](https://github.com/user-attachments/assets/4f81bb59-c2e5-4191-b0cb-48d9412fb189)

## Evaluation
The proposed framework was evaluated in two domains, Search and Rescue (SAR) and Parkinson's Disease (PD).
To this end, two ontologies (beAWARE ontology and Wear4PDmove ontology were used. 

### An Ontology fragment in a Graph format from the SAR domain (beAWARE ontology)
<img width="1962" height="932" alt="image" src="https://github.com/user-attachments/assets/8f1b1d2d-fbb5-491b-b80a-2ccb8b3ae2f3" />

For the sake of experimentation, for each domain 10 rules in NL were manually crafted based on the used ontologies

### Rules in NL 
#### SAR domain
* If a mission is related to a specific incident and that incident has a priority level of 'high', then the mission should also be assigned as a 'high' priority
* If an incident is identified and a vulnerable object is also identified, then it can be inferred that the vulnerable object is involved in that incident.
* If an incident is involved within a dataset, and that dataset was produced by a task and that task is related with a media item, then the location of incident is the same with the location of media item."
* If an incident has an impact, and that impact affects a vulnerable object, then the incident's severity level is classified as 'high'.
* If a responder is assigned to a mission, and that mission is related to an incident and the location of the incident is known, then the location of responder is the same with the location of the incident."
* If an incident is detected and the confidence of this detection is greater than 0.9 and vulnerable objects are also detected, then the priority of the incident is set to 'high' and the detected vulnerable objects are involved in this incident."
* If a measurement of a climate parameter is taken at a specific location, and an incident occurs at that same location, then that measurement can be associated with that incident."
* If a detection has a start time and an end time, and its total duration is calculated to be greater than 60 minutes, then the severity of the incident is 'high'.
* If a vulnerable object and an incident are detected, and this incident has an impact, then the vulnerable object is impacted by that impact.
* If an incident is detected and the risk of the detection is greater than 0.8 and the confidence of the detection is less than 0.5, then the incident has priority 'Requires Verification' and a responder is assigned to identification mission.

#### PD domain
* If a patient with Parkinson disease has a daily dosage plan with a specific dosage time and a missing dose event is observed, then send a notification to the doctor.
* If a patient with Parkinson disease has tremor and bradykinesia of upper limb and performs a walking activity that is measured by a smart watch and a patient falling event is observed, then send a notification to the doctor."
* If a patient has tremor and bradykinesia of upper limp, then that patient should be classified as a patient with Parkinson disease.
* If a patient with Parkinson disease has a falling event observation and that observation happened 30 minutes after dosing, then send a notification alert to the doctor.
* If a patient with Parkinson disease has  tremor and that tremor is observed after a dosage time then a notification is sent to the relatives and a missing dose event observation is recognized.
* If a patient with Parkinson disease has bradykinesia of the upper limb and this observation  is made after dosing, then send a  notification to relatives and a missing dosing event observation is identified.
* If a falling event observation is identified for a patient with Parkinson disease, then send a notification alert to the nurse and the relative.
* If a person is monitored and the low-level events of tremor and  bradykinesia of the upper limb are identified, and this person has a medical prescription that contains Dopamine, then it is most likely to be a patient with Parkinson disease.
* If a missing dosing event has been observed for a patient with Parkinson disease more than 2 times, then send notification to the doctor for action.
* If a patient with Parkinson disease has a dose plan every 4 hours, and tremor and bradykinesia of the upper limb is identified within the boundaries of this interval then send notification to the doctor for action.

### Prompt Engineering
The framework follows the Few-Shot Prompt Engineering technique.
```` code
  Act as an ontology engineer. Use the following content (examples, part of the ontology, and a list of guidelines) as a guide to translate the natural language rule you are given into a SWRL rule. 
  EXAMPLES
    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)
    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)
    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ Age(?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)
    Example 4
    Rule in natural language: if a publication has two different authors, then those authors have cooperated with each other.
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)
    Example 5
    Rule in natural language: if a researcher has published more than 10 papers in a Top-Tier conference, then the researcher is a prominent researcher and has a high citation impact.
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?c) ^ Conference(?c) ^ topTierConference(?c) ^ swrlb:greaterThan(count(?c), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)
  END OF EXAMPLES
  PART OF ONTOLOGY 
    {context}
  END OF ONTOLOGY
  
  COMMON GUIDELINES

  Please try to implement the following guidelines:
  1: Variables e.g., (?something) used in Conclusions must be present in Conditions. So create as many variables as needed in Conditions. 
  2: Each atom must have exactly one variable if it represents class.
  3: Each atom must have exactly two variables if it represents object property.
  4: Each concept must be represented by a class and must be present in Conditions.

  END OF COMMON GUIDELINES

  The rule in natural language is the following: {question}
  Give only the final SWRL rule
  """
````
#### For GraphRAG configuration the context has the following format

````code
:causedByIncident  rdfs:range  :IncidentType .
:causesIncidentImpact  rdfs:domain  :IncidentType .
:derivedFrom  rdfs:domain  :Incident .
:derivedFrom  rdfs:range  :Incident .
:detectsIncident  owl:inverseOf  :incidentDetectedBy .
:detectsIncident  rdfs:domain  :Detection .
:detectsIncident  rdfs:range  :Incident .
:hasIncidentClimateParameter  rdfs:domain  :Incident .
:hasIncidentImpact  rdfs:domain  :Incident .
:hasIncidentLocation  rdfs:domain  :Incident .
:hasIncidentOccurrence  rdfs:domain  :IncidentType .
:hasIncidentOccurrence  rdfs:range  :Incident .
:hasIncidentPriority  rdfs:domain  :Incident .
:hasIncidentPriority  rdfs:range  :string .
:hasIncidentSeverity  rdfs:domain  :Incident .
:hasMissionEnd  rdfs:domain  :Mission .
:hasMissionPriority  rdfs:domain  :Mission .
:hasMissionPriority  rdfs:range  :string .
:hasMissionStart  rdfs:domain  :Mission .
:hasMissionStatus  rdfs:domain  :Mission .
:hasMissionStatus  rdfs:range  :string .
:incidentDetectedBy  rdfs:domain  :Incident .
:involvedInDataset  owl:inverseOf  :involvesIncident .
:involvedInDataset  rdfs:domain  :Incident .
:involvedInIncident  rdfs:range  :Incident .
:involvesIncident  rdfs:domain  :Dataset .
:involvesIncident  rdfs:range  :Incident .
:involvesParticipant  rdfs:domain  :Incident .
:isAssignedMission  owl:inverseOf  :isAssignedToResponder .
:isAssignedMission  rdfs:domain  :Responder .
:isAssignedMission  rdfs:range  :Mission .
:isAssignedToResponder  rdfs:domain  :Mission .
:isClimateParameterOfIncident  rdfs:range  :Incident .
:isImpactOfIncident  rdfs:range  :Incident .
:isLocationOfIncident  rdfs:range  :Incident .
:isOfIncidentType  rdfs:domain  :Incident .
:isOfIncidentType  rdfs:range  :IncidentType .
:relatesToIncident  rdfs:domain  :Mission .
:relatesToIncident  rdfs:range  :Incident .
:relatesToMission  rdfs:domain  :Incident .
:relatesToMission  rdfs:range  :Mission .
````

### Metrics

#### SAR Domain
<img width="2047" height="1305" alt="SAR_1" src="https://github.com/user-attachments/assets/6f54458e-7a95-4136-af5f-9a1e3f2a2f02" />
<img width="2047" height="1311" alt="SAR_2" src="https://github.com/user-attachments/assets/c8abf3ca-68fc-4f79-946e-73c631dc52aa" />

#### PD Domain
<img width="1934" height="1299" alt="PD_2" src="https://github.com/user-attachments/assets/4ad5d6d0-60ca-4edf-b2d2-6b5dbb46450e" />
<img width="1941" height="1288" alt="PD_1" src="https://github.com/user-attachments/assets/142a5ea2-48a2-4823-b814-c618c531e932" />

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
#### Important Node
Ollama and Neo4j are required for running the framework
