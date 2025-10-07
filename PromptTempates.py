class CustomPromptTemplates:
  RAG_template = """
  Act as an ontology engineer. Use the following content (examples, part of the ontology, and common mistakes) as a guide to translate the natural language rule you are given into a SWRL rule. 
    EXAMPLES

    Example 1
    Rule in natural language: IF a Person Has a Sibling who Is a Man, THEN the Person Has a Brother.
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: IF a Person Has a Phone Number that starts with '+', THEN the Person Has an International Phone Number.
    SWRL rule: Person(?p) ^ PhoneNumber(?number) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  IF a Person Has an Age greater than 17, THEN the Person is an Adult and Has IdCard.
    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ Age(?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)

    Example 4
    Rule in natural language:  IF a Publication Has two different Authors, THEN those Authors have Cooperated With each other.
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

    Example 5
    Rule in natural language: IF a Researcher Has Published more than 10 papers in a Top-Tier Conference, THEN the Researcher is a Prominent Researcher and Has a High Citation Impact.
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?p) ^ Conference(?p) ^ topTierConference(?p) ^ swrlb:greaterThan(count(?p), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r)

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
  
  
  mistral_template = """USER: Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
    PART OF ONTOLOGY 

    {context}

    END OF ONTOLOGY

    The rule in natural language is the following: {question}
    Give only the final SWRL rule
    ASSISTANT:
  """

  llama_template = """Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
    PART OF ONTOLOGY 

    {context}

    END OF ONTOLOGY

    The rule in natural language is the following: {question}
    Give only the final SWRL rule
  """

  phi_template = """Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
    PART OF ONTOLOGY 

    {context}

    END OF ONTOLOGY

    The rule in natural language is the following: {question}
    Give only the final SWRL rule
  """

  qwen_template = """Below are some instructions that describe some tasks. Write responses that appropriately complete each request.

  USER: Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
  PART OF ONTOLOGY 

  {context}

  END OF ONTOLOGY

  The rule in natural language is the following: {question}
  Give only the final SWRL rule

  ASSISTANT: """

  qwen_template2 = """Below are some instructions that describe some tasks. Write responses that appropriately complete each request.

  USER: Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
  PART OF ONTOLOGY 

  {context}

  END OF ONTOLOGY

  The rule in natural language is the following: {question}
  Give only the final SWRL rule

  ASSISTANT: """

  
  @staticmethod
  def rules_in_nl(start=0, end=10):
    sar_rules = [
      "If a mission is related to a specific incident and that incident has a priority level of 'high', then the mission should also be assigned as a 'high' priority.",
      "If an incident is identified and a vulnerable object is also identified, then it can be inferred that the vulnerable object is involved in that incident.",
      "If an incident is involved within a dataset, and that dataset was produced by a task and that task is related with a media item, then the location of incident is the same with the location of media item.",
      "If an incident has an impact, and that impact affects a vulnerable object, then the incident's severity level is classified as 'high'.",
      "If a responder is assigned to a mission, and that mission is related to an incident and the location of the incident is known, then the location of responder is the same with the location of the incident.",
      "If an incident is detected and the confidence of this detection is greater than 0.9 and vulnerable objects are also detected, then the priority of the incident is set to 'high' and the detected vulnerable objects are involved in this incident.",
      "If a measurement of a climate parameter is taken at a specific location, and an incident occurs at that same location, then that measurement can be associated with that incident.",
      "If a detection has a start time and an end time, and its total duration is calculated to be greater than 60 minutes, then the severity of the incident is 'high'.",
      "If a vulnerable object and an incident are detected, and this incident has an impact, then the vulnerable object is impacted by that impact.",
      "If an incident is detected and the risk of the detection is greater than 0.8 and the confidence of the detection is less than 0.5, then the incident has priority 'Requires Verification' and a responder is assigned to identification mission.",
    ]

    return sar_rules[start:end]
  
  @staticmethod
  def pd_rules_in_nl(start=0, end=10):
    sar_rules = [
      "If a patient with Parkinson’s disease has a daily dosage plan with a specific dosage time and a missing dose is observed, then send a notification to the doctor.",
      "If a patient with Parkinson’s disease has tremor and bradykinesia of upper limb and performs a walking activity that is measured by a smart watch and a patient falling event is observed, then send a notification to the doctor.",
      "If a patient has tremor and bradykinesia of upper limp, then that patient should be classified as a patient with Parkinson’s disease.",
      "If a patient with Parkinson’s disease has a falling event observation and that observation happened 30 minutes after dosing, then send a notification alert to the doctor.",
      "If tremor is observed after dosing in a patient with Parkinson’s disease and a missing dose event is recognized, and a notification is sent to the doctor, then instances of PD patient observations are automatically classified as 'PD patient Missing Dose Event Observations'.",
      "If an observation for bradykinesia of the upper limb is made after dosing and bradykinesia is detected, a missing dose event is recognized, then a missing dosing event a notification is identified, and a  Notification to the doctor is sent. ",
      "If there is a falling event observation, then send notification alert to the doctor, nurse and the relative.",
      "If an individual is monitored and the low-level event of tremor and bradykinesia is identified, and this individual has a health record with a dosing plan of Dopamine, then must be a PD patient",
      "If the missing dosing (high-level) event has been recognized more than 2 times, then send notification to the doctor for action",
      "If dose is planned every 4 hours (based on the health record), and a low-level event of tremor and bradykinesia is identified within the boundaries of this interval, send notification to the doctor for action (increase dosing).",
    ]

    return sar_rules[start:end]

  def get_rag_data(index):
    data = [
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentPriority  :rdfs:range  :string
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMissionEnd  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:range  :string
      :hasMissionStart  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:range  :string
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isAssignedMission  :owl:inverseOf  :isAssignedToResponder
      :isAssignedMission  :rdfs:domain  :Responder
      :isAssignedMission  :rdfs:range  :Mission
      :isAssignedToResponder  :rdfs:domain  :Mission
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :relatesToIncident  :owl:inverseOf  :relatesToMission
      :relatesToIncident  :rdfs:domain  :Mission
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      :relatesToMission  :rdfs:range  :Mission
      """,
      """
      :Asset  :rdfs:subClassOf  :VulnerableObject
      :LivingBeing  :rdfs:subClassOf  :VulnerableObject
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:range  :VulnerableObject
      :hasImpactOn  :rdfs:range  :VulnerableObject
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:domain  :VulnerableObject
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :involvesParticipant  :rdfs:range  :VulnerableObject
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isImpactedBy  :rdfs:domain  :VulnerableObject
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:domain  :VulnerableObject
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      """,

      """
      :AudioItem  :rdfs:subClassOf  :MediaItem
      :DataAnalysis  :rdfs:subClassOf  :Task
      :ImageItem  :rdfs:subClassOf  :MediaItem
      :TextItem  :rdfs:subClassOf  :MediaItem
      :VideoItem  :rdfs:subClassOf  :MediaItem
      :belongsToCollection  :rdfs:domain  :MediaItem
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :containedInDataset  :owl:inverseOf  :containsDetection
      :containedInDataset  :rdfs:domain  :Detection
      :containedInDataset  :rdfs:range  :Dataset
      :containsDetection  :rdfs:domain  :Dataset
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :hasAnalyzedMediaSource  :rdfs:domain  :MediaItem
      :hasDatasetResultsSource  :rdfs:domain  :Dataset
      :hasDisasterLocation  :rdfs:range  :Location
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:range  :Location
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMeasurementLocation  :owl:inverseOf  :isLocationOfMeasurement
      :hasMeasurementLocation  :rdfs:domain  :ClimateParameter
      :hasMeasurementLocation  :rdfs:range  :Location
      :hasMediaItemTimestamp  :rdfs:domain  :MediaItem
      :hasMediaItemTimestamp  :rdfs:range  :dateTime
      :hasMediaLocation  :owl:inverseOf  :isLocationOfMediaItem
      :hasMediaLocation  :rdfs:domain  :MediaItem
      :hasMediaLocation  :rdfs:range  :Location
      :hasRadius  :rdfs:domain  :Location
      :hasRawMediaSource  :rdfs:domain  :MediaItem
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :owl:inverseOf  :isLocationOfReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:range  :Location
      :hasResponderLocation  :owl:inverseOf  :isLocationOfResponder
      :hasResponderLocation  :rdfs:domain  :Responder
      :hasResponderLocation  :rdfs:range  :Location
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInDataset  :rdfs:range  :Dataset
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfDisaster  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfMeasurement  :rdfs:domain  :Location
      :isLocationOfMediaItem  :rdfs:domain  :Location
      :isLocationOfMediaItem  :rdfs:range  :MediaItem
      :isLocationOfReport  :rdfs:domain  :Location
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isLocationOfResponder  :rdfs:domain  :Location
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :lat  :rdfs:domain  :Location
      :long  :rdfs:domain  :Location
      :producedByTask  :owl:inverseOf  :taskProducesDataset
      :producedByTask  :rdfs:domain  :Dataset
      :producedByTask  :rdfs:range  :Task
      :relatesTo  :rdfs:domain  :MediaItem
      :relatesTo  :rdfs:range  :MediaItem
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMediaItem  :owl:inverseOf  :relatesToTask
      :relatesToMediaItem  :rdfs:domain  :Task
      :relatesToMediaItem  :rdfs:range  :MediaItem
      :relatesToMission  :rdfs:domain  :Incident
      :relatesToTask  :rdfs:domain  :MediaItem
      :relatesToTask  :rdfs:range  :Task
      :sensorProducesDataset  :rdfs:domain  :Sensor
      :sensorProducesDataset  :rdfs:range  :Dataset
      :taskProducesDataset  :rdfs:domain  :Task
      :taskProducesDataset  :rdfs:range  :Dataset
      """,
      """
      :Asset  :rdfs:subClassOf  :VulnerableObject
      :LivingBeing  :rdfs:subClassOf  :VulnerableObject
      :causedByDisaster  :owl:inverseOf  :causesDisasterImpact
      :causedByDisaster  :rdfs:domain  :ImpactType
      :causedByIncident  :rdfs:domain  :ImpactType
      :causedByIncident  :rdfs:range  :IncidentType
      :causesDisasterImpact  :rdfs:domain  :NaturalDisasterType
      :causesDisasterImpact  :rdfs:range  :ImpactType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :causesIncidentImpact  :rdfs:range  :ImpactType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:range  :VulnerableObject
      :hasImpactOccurrence  :rdfs:domain  :ImpactType
      :hasImpactOccurrence  :rdfs:range  :Impact
      :hasImpactOn  :owl:inverseOf  :isImpactedBy
      :hasImpactOn  :rdfs:domain  :Impact
      :hasImpactOn  :rdfs:range  :VulnerableObject
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :owl:inverseOf  :isImpactOfIncident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:range  :Impact
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:range  :string
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:domain  :VulnerableObject
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :involvesParticipant  :rdfs:range  :VulnerableObject
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:domain  :Impact
      :isImpactOfIncident  :rdfs:range  :Incident
      :isImpactedBy  :rdfs:domain  :VulnerableObject
      :isImpactedBy  :rdfs:range  :Impact
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfImpactType  :rdfs:domain  :Impact
      :isOfImpactType  :rdfs:range  :ImpactType
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:domain  :VulnerableObject
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      """,
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :hasDisasterLocation  :rdfs:range  :Location
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:range  :Location
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMeasurementLocation  :owl:inverseOf  :isLocationOfMeasurement
      :hasMeasurementLocation  :rdfs:domain  :ClimateParameter
      :hasMeasurementLocation  :rdfs:range  :Location
      :hasMediaLocation  :owl:inverseOf  :isLocationOfMediaItem
      :hasMediaLocation  :rdfs:domain  :MediaItem
      :hasMediaLocation  :rdfs:range  :Location
      :hasMissionEnd  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:range  :string
      :hasMissionStart  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:range  :string
      :hasRadius  :rdfs:domain  :Location
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :owl:inverseOf  :isLocationOfReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:range  :Location
      :hasResponderLocation  :owl:inverseOf  :isLocationOfResponder
      :hasResponderLocation  :rdfs:domain  :Responder
      :hasResponderLocation  :rdfs:range  :Location
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isAssignedMission  :owl:inverseOf  :isAssignedToResponder
      :isAssignedMission  :rdfs:domain  :Responder
      :isAssignedMission  :rdfs:range  :Mission
      :isAssignedToResponder  :rdfs:domain  :Mission
      :isAssignedToResponder  :rdfs:range  :Responder
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfDisaster  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfMeasurement  :rdfs:domain  :Location
      :isLocationOfMediaItem  :rdfs:domain  :Location
      :isLocationOfReport  :rdfs:domain  :Location
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isLocationOfResponder  :rdfs:domain  :Location
      :isLocationOfResponder  :rdfs:range  :Responder
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :lat  :rdfs:domain  :Location
      :long  :rdfs:domain  :Location
      :relatesToIncident  :owl:inverseOf  :relatesToMission
      :relatesToIncident  :rdfs:domain  :Mission
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      :relatesToMission  :rdfs:range  :Mission
      """,
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :containedInDataset  :owl:inverseOf  :containsDetection
      :containedInDataset  :rdfs:domain  :Detection
      :containsDetection  :rdfs:domain  :Dataset
      :containsDetection  :rdfs:range  :Detection
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:range  :float
      :hasDetectionEnd  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:range  :float
      :hasDetectionStart  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:range  :dateTime
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentPriority  :rdfs:range  :string
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMissionPriority  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:range  :string
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :incidentDetectedBy  :rdfs:range  :Detection
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:range  :Detection
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      """,
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :characterizedByParameterType  :rdfs:range  :ClimateParameterType
      :characterizesDisasterType  :rdfs:domain  :ClimateParameterType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :hasClimateParameterMeasurement  :owl:inverseOf  :relatesToNaturalDisaster
      :hasClimateParameterMeasurement  :rdfs:domain  :NaturalDisaster
      :hasClimateParameterMeasurement  :rdfs:range  :ClimateParameter
      :hasClimateParameterOccurrence  :owl:inverseOf  :isOfClimateParameterType
      :hasClimateParameterOccurrence  :rdfs:domain  :ClimateParameterType
      :hasClimateParameterOccurrence  :rdfs:range  :ClimateParameter
      :hasDisasterLocation  :rdfs:range  :Location
      :hasIncidentClimateParameter  :owl:inverseOf  :isClimateParameterOfIncident
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentClimateParameter  :rdfs:range  :ClimateParameter
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:range  :Location
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMeasurementLocation  :owl:inverseOf  :isLocationOfMeasurement
      :hasMeasurementLocation  :rdfs:domain  :ClimateParameter
      :hasMeasurementLocation  :rdfs:range  :Location
      :hasMeasurementTimestamp  :rdfs:domain  :ClimateParameter
      :hasMeasurementTimestamp  :rdfs:range  :dateTime
      :hasMediaLocation  :owl:inverseOf  :isLocationOfMediaItem
      :hasMediaLocation  :rdfs:domain  :MediaItem
      :hasMediaLocation  :rdfs:range  :Location
      :hasRadius  :rdfs:domain  :Location
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :owl:inverseOf  :isLocationOfReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:range  :Location
      :hasResponderLocation  :owl:inverseOf  :isLocationOfResponder
      :hasResponderLocation  :rdfs:domain  :Responder
      :hasResponderLocation  :rdfs:range  :Location
      :hasUnit  :rdfs:domain  :ClimateParameter
      :hasValue  :rdfs:domain  :ClimateParameter
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isClimateParameterOfIncident  :rdfs:domain  :ClimateParameter
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfDisaster  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:domain  :Location
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfMeasurement  :rdfs:domain  :Location
      :isLocationOfMeasurement  :rdfs:range  :ClimateParameter
      :isLocationOfMediaItem  :rdfs:domain  :Location
      :isLocationOfReport  :rdfs:domain  :Location
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isLocationOfResponder  :rdfs:domain  :Location
      :isOfClimateParameterType  :rdfs:domain  :ClimateParameter
      :isOfClimateParameterType  :rdfs:range  :ClimateParameterType
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :lat  :rdfs:domain  :Location
      :long  :rdfs:domain  :Location
      :observes  :rdfs:range  :ClimateParameter
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      :relatesToNaturalDisaster  :rdfs:domain  :ClimateParameter
      """,
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :containedInDataset  :owl:inverseOf  :containsDetection
      :containedInDataset  :rdfs:domain  :Detection
      :containsDetection  :rdfs:domain  :Dataset
      :containsDetection  :rdfs:range  :Detection
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:range  :float
      :hasDetectionEnd  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:range  :float
      :hasDetectionStart  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:range  :dateTime
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:range  :string
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :incidentDetectedBy  :rdfs:range  :Detection
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:range  :Detection
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      """,
      """
      :Asset  :rdfs:subClassOf  :VulnerableObject
      :LivingBeing  :rdfs:subClassOf  :VulnerableObject
      :causedByDisaster  :owl:inverseOf  :causesDisasterImpact
      :causedByDisaster  :rdfs:domain  :ImpactType
      :causedByIncident  :rdfs:domain  :ImpactType
      :causedByIncident  :rdfs:range  :IncidentType
      :causesDisasterImpact  :rdfs:domain  :NaturalDisasterType
      :causesDisasterImpact  :rdfs:range  :ImpactType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :causesIncidentImpact  :rdfs:range  :ImpactType
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:range  :VulnerableObject
      :hasImpactOccurrence  :rdfs:domain  :ImpactType
      :hasImpactOccurrence  :rdfs:range  :Impact
      :hasImpactOn  :owl:inverseOf  :isImpactedBy
      :hasImpactOn  :rdfs:domain  :Impact
      :hasImpactOn  :rdfs:range  :VulnerableObject
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :owl:inverseOf  :isImpactOfIncident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:range  :Impact
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :incidentDetectedBy  :rdfs:domain  :Incident
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:domain  :VulnerableObject
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :involvesParticipant  :rdfs:range  :VulnerableObject
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:domain  :Impact
      :isImpactOfIncident  :rdfs:range  :Incident
      :isImpactedBy  :rdfs:domain  :VulnerableObject
      :isImpactedBy  :rdfs:range  :Impact
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isOfImpactType  :rdfs:domain  :Impact
      :isOfImpactType  :rdfs:range  :ImpactType
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:domain  :VulnerableObject
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      """,
      """
      :causedByIncident  :rdfs:range  :IncidentType
      :causesIncidentImpact  :rdfs:domain  :IncidentType
      :containedInDataset  :owl:inverseOf  :containsDetection
      :containedInDataset  :rdfs:domain  :Detection
      :containsDetection  :rdfs:domain  :Dataset
      :containsDetection  :rdfs:range  :Detection
      :derivedFrom  :rdfs:domain  :Incident
      :derivedFrom  :rdfs:range  :Incident
      :detectsIncident  :owl:inverseOf  :incidentDetectedBy
      :detectsIncident  :rdfs:domain  :Detection
      :detectsIncident  :rdfs:range  :Incident
      :detectsParticipant  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:domain  :Detection
      :hasDetectionConfidence  :rdfs:range  :float
      :hasDetectionEnd  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:domain  :Detection
      :hasDetectionRisk  :rdfs:range  :float
      :hasDetectionStart  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:domain  :Detection
      :hasDetectionTimestamp  :rdfs:range  :dateTime
      :hasIncidentClimateParameter  :rdfs:domain  :Incident
      :hasIncidentImpact  :rdfs:domain  :Incident
      :hasIncidentLocation  :rdfs:domain  :Incident
      :hasIncidentOccurrence  :rdfs:domain  :IncidentType
      :hasIncidentOccurrence  :rdfs:range  :Incident
      :hasIncidentPriority  :rdfs:domain  :Incident
      :hasIncidentPriority  :rdfs:range  :string
      :hasIncidentSeverity  :rdfs:domain  :Incident
      :hasMissionEnd  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:domain  :Mission
      :hasMissionPriority  :rdfs:range  :string
      :hasMissionStart  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:domain  :Mission
      :hasMissionStatus  :rdfs:range  :string
      :hasReportID  :rdfs:domain  :IncidentReport
      :hasReportLocation  :rdfs:domain  :IncidentReport
      :hasResponderLocation  :owl:inverseOf  :isLocationOfResponder
      :hasResponderLocation  :rdfs:domain  :Responder
      :hasResponderLocation  :rdfs:range  :Location
      :incidentDetectedBy  :rdfs:domain  :Incident
      :incidentDetectedBy  :rdfs:range  :Detection
      :involvedInDataset  :owl:inverseOf  :involvesIncident
      :involvedInDataset  :rdfs:domain  :Incident
      :involvedInIncident  :rdfs:range  :Incident
      :involvesIncident  :rdfs:domain  :Dataset
      :involvesIncident  :rdfs:range  :Incident
      :involvesParticipant  :rdfs:domain  :Incident
      :isAssignedMission  :owl:inverseOf  :isAssignedToResponder
      :isAssignedMission  :rdfs:domain  :Responder
      :isAssignedMission  :rdfs:range  :Mission
      :isAssignedToResponder  :rdfs:domain  :Mission
      :isAssignedToResponder  :rdfs:range  :Responder
      :isClimateParameterOfIncident  :rdfs:range  :Incident
      :isImpactOfIncident  :rdfs:range  :Incident
      :isLocationOfIncident  :rdfs:range  :Incident
      :isLocationOfReport  :rdfs:range  :IncidentReport
      :isLocationOfResponder  :rdfs:domain  :Location
      :isLocationOfResponder  :rdfs:range  :Responder
      :isOfIncidentType  :rdfs:domain  :Incident
      :isOfIncidentType  :rdfs:range  :IncidentType
      :participantDetectedBy  :rdfs:range  :Detection
      :relatesToIncident  :owl:inverseOf  :relatesToMission
      :relatesToIncident  :rdfs:domain  :Mission
      :relatesToIncident  :rdfs:range  :Incident
      :relatesToMission  :rdfs:domain  :Incident
      :relatesToMission  :rdfs:range  :Mission
      """
    ]

    return data[index]
  
  # sar_rules = [
  #     "If a mission is related to a specific incident and that incident has a priority level of 'high', then the mission should also be assigned as a 'high' priority.",
  #     "If a detection activity identifies both an incident and a vulnerable object, then it can be inferred that the vulnerable object is involved in that incident.",
  #     "If an incident is involved within a dataset, and that dataset was produced by a task and that task is related with a media item, then the location of incident is the same with the location of media item.",
  #     "If an incident has an impact, and that impact affects a vulnerable object, then the incident's severity level is classified as 'high'.",
  #     "If a responder is assigned to a mission, and that mission is related to an incident at a known location, then the location of responder can be inferred to be the same as the location  of incident.",
  #     "If a detection activity identifies an incident and the confidence level of this detection is greater than 0.9 and vulnerable objects are also detected, then the priority of the incident is set to 'high' and the detected vulnerable objects are involved in this incident.",
  #     "If a climate parameter measurement is taken at a specific location, and an incident occurs at that same location, then that climate parameter measurement can be formally associated with the incident.",
  #     "If a detection event has a start time and an end time, and its total duration is calculated to be greater than 60 minutes, then the severity of the incident is 'high'.",
  #     "If a detection activity identifies a vulnerable object and also identifies an incident, and this incident has an impact, then it can be inferred that the vulnerable object is impacted by that impact.",
  #     "If a detection activity identifies an incident with a detection risk level greater than 0.8 and the confidence of the detection is less than 0.5, then the incident has priority 'Requires Verification' and a responder is assigned to identification mission.",
  #   ]