from datasets import Dataset
from dotenv import load_dotenv
import openai
from ragas.llms.base import llm_factory
from ragas import evaluate
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._factual_correctness import FactualCorrectness
load_dotenv()

# data_sample_k7 = {
#   "question": ["""Act as an ontology engineer. Use the following content (examples, part of the ontology, and a list of guidelines) as a guide to translate the natural language rule you are given into a SWRL rule. 
#         The rule in natural language is the following: If a patient with Parkinson disease has a daily dosage plan with a specific dosage time and a missing dose event is observed, then send a notification to the doctor.
#         """
#   ],
#   "answer": ["""PD_Patient(?p) ^ hasDailyDosagePlan(?p, ?d) ^ DailyDosagePlan(?d) ^ hasDosageTime(?d, ?t) ^ DosageTime(?t) ^ PDpatientMissingDoseEventObservation(?e) -> NotifyDoctor(?n)"""],
#   "retrieved_contexts": [
#     [
#       """
#         http://w3id.org/Wear4PDmove/onto#PDpatientMissingDoseEventObservation
#         onto:PDpatientMissingDoseEventObservation rdf:type owl:Class ; rdfs:subClassOf onto:RecognizedEvent ; rdfs:comment "Missing dose event observation for PD Patient" ; rdfs:label "PD patient Missing Dose Event Observation" .
#         http://w3id.org/Wear4PDmove/onto#Patient
#         onto:Patient rdf:type owl:Class ; rdfs:subClassOf schema:Person ; rdfs:comment "Any kind of patient" ; rdfs:label "Patient" .
#         http://w3id.org/Wear4PDmove/onto#PersonalHealthRecord
#         onto:PersonalHealthRecord rdf:type owl:Class ; rdfs:comment "Personal Health Record of a patient" ; rdfs:label "Personal Health Record" .
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#AlertingNotification
#         onto:AlertingNotification rdf:type owl:Class ; rdfs:subClassOf core:ActuatingFunction ; rdfs:comment "Alerting Notification Function for event" ; rdfs:label "Alerting Notification Function" .
#         http://w3id.org/Wear4PDmove/onto#DailyDosagePlan
#         onto:DailyDosagePlan rdf:type owl:Class ; rdfs:subClassOf onto:MedicalPrescription , [ rdf:type owl:Restriction ; owl:onProperty onto:hasDosageTime ; owl:someValuesFrom onto:DosageTime ] ; rdfs:comment "Daily dosage plan for patient (4 times one day)" ; rdfs:label "Daily Dosage Plan" .
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#hasDosageTime
#         onto:hasDosageTime rdf:type owl:ObjectProperty ; rdfs:subPropertyOf core:hasTime ; rdfs:domain onto:DailyDosagePlan ; rdfs:range onto:DosageTime ; rdfs:comment "the dosing time of a patient"@en ; rdfs:label "has Dosage Time"@en .
#         http://w3id.org/Wear4PDmove/onto#hasPersonalHealthRecord
#         onto:hasPersonalHealthRecord rdf:type owl:ObjectProperty ; owl:inverseOf onto:recordBelongsToPatient ; rdfs:domain onto:Patient ; rdfs:range onto:PersonalHealthRecord ; rdfs:comment "patient has a health record"@en ; rdfs:label "has Personal Health Record"@en .
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#NotifyDoctor
#         onto:NotifyDoctor rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification ; rdfs:comment "Notify doctor for event (alert notification)" ; rdfs:label "Notify Doctor" .
#         http://w3id.org/Wear4PDmove/onto#NotifyNurse
#         onto:NotifyNurse rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification .
#         http://w3id.org/Wear4PDmove/onto#NotifyRelatives
#         onto:NotifyRelatives rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification .
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#Diagnosis
#         onto:Diagnosis rdf:type owl:Class ; rdfs:subClassOf onto:PersonalHealthRecord ; rdfs:comment "diagnosis of disease of a patient in one appointment" ; rdfs:label "Diagnosis" .
#         http://w3id.org/Wear4PDmove/onto#DosageTime
#         onto:DosageTime rdf:type owl:Class ; rdfs:subClassOf core:Time ; rdfs:comment "Dosage time on datetime" ; rdfs:label "Dosage Time (time in one day)" .
#         http://w3id.org/Wear4PDmove/onto#MedicalPrescription
#         onto:MedicalPrescription rdf:type owl:Class ; rdfs:subClassOf onto:PersonalHealthRecord ; rdfs:comment "Medical Prescription for Patient" ; rdfs:label "Medical Prescription" .
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#RecognizedEvent
#         onto:RecognizedEvent rdf:type owl:Class ; rdfs:subClassOf sosa:Observation ; rdfs:comment "An observation of a recognized event for a PD Patient" ; rdfs:label "PD patient recognized event observation" .
#         http://w3id.org/Wear4PDmove/onto#SketchingActivity
#         onto:SketchingActivity rdf:type owl:Class ; rdfs:subClassOf http://www.case.edu/MDO#ActivitiesofDailyLiving , [ rdf:type owl:Restriction ; owl:onProperty core:isMeasuredByDevice ; owl:someValuesFrom onto:SmartWatch ] ; rdfs:comment "An activity followed by the patient during his free time, using his hands (sketching)."@en ; rdfs:label "Sketching Activity"@en . 
#       """,
#       """
#         http://w3id.org/Wear4PDmove/onto#PD_Patient
#         onto:PD_Patient rdf:type owl:Class ; rdfs:subClassOf onto:Patient , [ rdf:type owl:Restriction ; owl:onProperty onto:hasPersonalHealthRecord ; owl:someValuesFrom onto:PersonalHealthRecord ] ; rdfs:comment "PD patient" ; rdfs:label "PD Patient" .
#         http://w3id.org/Wear4PDmove/onto#PDpatientFalllingEventObservation
#         onto:PDpatientFalllingEventObservation rdf:type owl:Class ; rdfs:subClassOf onto:RecognizedEvent ; rdfs:comment "Falling event observation for PD Patient" ; rdfs:label "PD patient Fallling Event Observation" .
#       """
#     ]
#   ],
#   "ground_truth": ["""PD_Patient(?p) ^ DailyDosagePlan(?ddp) ^ hasPersonalHealthRecord(?p, ddp) ^ DosageTime(?dt) ^ hasDosageTime(?ddp, ?dt) ^ PDpatientMissingDoseEventObservation(?mdeo) ^ NotifyDoctor(?nd) -> sendNotification(?nd, true)"""]
# }




data_sample_k5 = {
  "question": ["""Act as an ontology engineer. Use the following content (examples, part of the ontology, and a list of guidelines) as a guide to translate the natural language rule you are given into a SWRL rule. 
        The rule in natural language is the following: If a patient with Parkinson disease has a daily dosage plan with a specific dosage time and a missing dose event is observed, then send a notification to the doctor.
        """
  ],
  "answer": ["""Patient(?p) ^ hasParkinsonDisease(?p, true) ^ DailyDosagePlan(?d) ^ hasPersonalHealthRecord(?p, ?phr) ^ PersonalHealthRecord(?phr) ^ hasDailyDosagePlan(?phr, ?d) ^ hasDosageTime(?d, ?dt) ^ DosageTime(?dt) ^ PDpatientMissingDoseEventObservation(?e) ^ hasPatient(?e, ?p) -> NotifyDoctor(?n)"""],
  "retrieved_contexts": [
    [
      """
        http://w3id.org/Wear4PDmove/onto#PDpatientMissingDoseEventObservation
        onto:PDpatientMissingDoseEventObservation rdf:type owl:Class ; rdfs:subClassOf onto:RecognizedEvent ; rdfs:comment "Missing dose event observation for PD Patient" ; rdfs:label "PD patient Missing Dose Event Observation" .
        http://w3id.org/Wear4PDmove/onto#Patient
        onto:Patient rdf:type owl:Class ; rdfs:subClassOf schema:Person ; rdfs:comment "Any kind of patient" ; rdfs:label "Patient" .
        http://w3id.org/Wear4PDmove/onto#PersonalHealthRecord
        onto:PersonalHealthRecord rdf:type owl:Class ; rdfs:comment "Personal Health Record of a patient" ; rdfs:label "Personal Health Record" .
      """,
      """
        http://w3id.org/Wear4PDmove/onto#AlertingNotification
        onto:AlertingNotification rdf:type owl:Class ; rdfs:subClassOf core:ActuatingFunction ; rdfs:comment "Alerting Notification Function for event" ; rdfs:label "Alerting Notification Function" .
        http://w3id.org/Wear4PDmove/onto#DailyDosagePlan
        onto:DailyDosagePlan rdf:type owl:Class ; rdfs:subClassOf onto:MedicalPrescription , [ rdf:type owl:Restriction ; owl:onProperty onto:hasDosageTime ; owl:someValuesFrom onto:DosageTime ] ; rdfs:comment "Daily dosage plan for patient (4 times one day)" ; rdfs:label "Daily Dosage Plan" .
      """,
      """
        http://w3id.org/Wear4PDmove/onto#hasDosageTime
        onto:hasDosageTime rdf:type owl:ObjectProperty ; rdfs:subPropertyOf core:hasTime ; rdfs:domain onto:DailyDosagePlan ; rdfs:range onto:DosageTime ; rdfs:comment "the dosing time of a patient"@en ; rdfs:label "has Dosage Time"@en .
        http://w3id.org/Wear4PDmove/onto#hasPersonalHealthRecord
        onto:hasPersonalHealthRecord rdf:type owl:ObjectProperty ; owl:inverseOf onto:recordBelongsToPatient ; rdfs:domain onto:Patient ; rdfs:range onto:PersonalHealthRecord ; rdfs:comment "patient has a health record"@en ; rdfs:label "has Personal Health Record"@en .
      """,
      """
        http://w3id.org/Wear4PDmove/onto#NotifyDoctor
        onto:NotifyDoctor rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification ; rdfs:comment "Notify doctor for event (alert notification)" ; rdfs:label "Notify Doctor" .
        http://w3id.org/Wear4PDmove/onto#NotifyNurse
        onto:NotifyNurse rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification .
        http://w3id.org/Wear4PDmove/onto#NotifyRelatives
        onto:NotifyRelatives rdf:type owl:Class ; rdfs:subClassOf onto:AlertingNotification .
      """,
      """
        http://w3id.org/Wear4PDmove/onto#Diagnosis
        onto:Diagnosis rdf:type owl:Class ; rdfs:subClassOf onto:PersonalHealthRecord ; rdfs:comment "diagnosis of disease of a patient in one appointment" ; rdfs:label "Diagnosis" .
        http://w3id.org/Wear4PDmove/onto#DosageTime
        onto:DosageTime rdf:type owl:Class ; rdfs:subClassOf core:Time ; rdfs:comment "Dosage time on datetime" ; rdfs:label "Dosage Time (time in one day)" .
        http://w3id.org/Wear4PDmove/onto#MedicalPrescription
        onto:MedicalPrescription rdf:type owl:Class ; rdfs:subClassOf onto:PersonalHealthRecord ; rdfs:comment "Medical Prescription for Patient" ; rdfs:label "Medical Prescription" .
      """
    ]
  ],
  "ground_truth": ["""PD_Patient(?p) ^ DailyDosagePlan(?ddp) ^ hasPersonalHealthRecord(?p, ddp) ^ DosageTime(?dt) ^ hasDosageTime(?ddp, ?dt) ^ PDpatientMissingDoseEventObservation(?mdeo) ^ NotifyDoctor(?nd) -> sendNotification(?nd, true)"""]
}





client = openai.AsyncOpenAI()
llm = llm_factory("gpt-4o-mini", client=client)
dataset = Dataset.from_dict(data_sample_k5)

score = evaluate(dataset, metrics=[ContextRecall(), Faithfulness(), FactualCorrectness()], llm=llm)
print(score)