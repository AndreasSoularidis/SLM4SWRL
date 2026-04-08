class CustomPromptTemplates:
  graph_examples = """
    EXAMPLES

    Example 1
    Rule in natural language: IF a Person Has a Sibling who Is a Man, THEN the Person Has a Brother.
    PART OF ONTOLOGY
    :hasSibling  :rdfs:domain :Person
    :hasSibling  :rdfs:range :Person
    :hasBrother  :rdfs:domain :Person
    :hasBrother  :rdfs:range :Person
    :isMan :rdfs:domain :Person
    :isMan :rdfs:range xsd:boolean
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ isMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: IF a Person Has a Phone Number that starts with '+', THEN the Person Has an International Phone Number.
    PART OF ONTOLOGY
    :hasPhoneNumber :rdfs:domain :Person
    :hasPhoneNumber :rdfs:range :PhoneNumber
    :hasInternationalPhoneNumber :rdfs:domain :Person
    :hasInternationalPhoneNumber :rdfs:range xsd:boolean
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ PhoneNumber(?number) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  IF a Person Has an Age greater than 17, THEN the Person is an Adult and Has IdCard.
    PART OF ONTOLOGY
    :hasAge :rdfs:domain :Person
    :hasAge :rdfs:range xsd:integer
    :hasIdCard :rdfs:domain :Person
    :hasIdCard :rdfs:range :IdCard
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)

    Example 4
    Rule in natural language:  IF a Publication Has two different Authors, THEN those Authors have Cooperated With each other.
    PART OF ONTOLOGY
    :hasAuthor :rdfs:domain :Publication
    :hasAuthor :rdfs:range :Author
    :differentFrom :rdfs:domain :Author
    :differentFrom :rdfs:range :Author
    :cooperatedWith :rdfs:domain :Author
    :cooperatedWith :rdfs:range :Author
    END OF ONTOLOGY 
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

    Example 5
    Rule in natural language: IF a Researcher Has Published more than 10 papers in a Top-Tier Conference, THEN the Researcher is a Prominent Researcher and Has a High Citation Impact.
    PART OF ONTOLOGY
    :hasPublished :rdfs:domain :Researcher
    :hasPublished :rdfs:range :Conference
    :hasHighCitationImpact :rdfs:domain :Researcher
    :hasHighCitationImpact :rdfs:range xsd:boolean
    END OF ONTOLOGY 
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?p) ^ Conference(?p) ^ topTierConference(?p) ^ swrlb:greaterThan(count(?p), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)

    END OF EXAMPLES
  """
  
  prompt = """
  Act as an ontology engineer. Use the following content (examples, part of the ontology, and common mistakes) as a guide to translate the natural language rule you are given into a SWRL rule. 
  EXAMPLES
    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
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

  alpaca_prompt = """
  Below is an instruction that describes a task, paired with an input that provides further context.
  ### Instruction:
  Act as an ontology engineer. Use the following content (examples, part of the ontology, and common mistakes) as a guide to translate the natural language rule you are given into a SWRL rule. 
  EXAMPLES
  Example 1
  Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
  SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

  Example 2
  Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
  SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

  Example 3
  Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
  SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

  Example 5
  Rule in natural language: if a researcher has published more than 10 papers in a Top-Tier conference, then the researcher is a prominent researcher and has a high citation impact.
  SWRL rule: Researcher(?r) ^ hasPublished(?r, ?c) ^ Conference(?c) ^ topTierConference(?c) ^ swrlb:greaterThan(count(?c), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)
  END OF EXAMPLES
  ### Input:
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
  ### Response:
  
  """
  

  @staticmethod
  def sar_rules_in_nl(start=0, end=10):
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
    pd_rules = [
      "If a patient with Parkinson’s disease has a daily dosage plan with a specific dosage time and a missing dose event is observed, then send a notification to the doctor.",
      "If a patient with Parkinson’s disease has tremor and bradykinesia of upper limb and performs a walking activity that is measured by a smart watch and a patient falling event is observed, then send a notification to the doctor.",
      "If a patient has tremor and bradykinesia of upper limp, then that patient should be classified as a patient with Parkinson’s disease.",
      "If a patient with Parkinson’s disease has a falling event observation and that observation happened 30 minutes after dosing, then send a notification alert to the doctor.",
      "If tremor is observed after dosing in a patient with Parkinson’s disease and a missing dose event is recognized, and a notification is sent to the doctor, then instances of PD patient observations are automatically classified as PD patient Missing Dose Event Observations.",
      "If an observation for bradykinesia of the upper limb is made after dosing and bradykinesia of upper limb is detected, then a missing dosing event a notification is identified, and a sent send Notification to the doctor is sent.",
      "If a falling event observation is identified for a patient with Parkinson’s disease, then send notification alert to the nurse and the relative.",
      "If an individual is monitored and the low-level event of tremor and  bradykinesia is identified, and this individual has a health record with a dosing plan of Dopamine, then it is most likely to be a PD patient.",
      "If a missing dosing event has been observed more than 2 times, then send notification to the doctor for action.",
      "If a patient with Parkinson’s disease has a dose plan every 4 hours, and tremor and bradykinesia of upper limb is identified within the boundaries of this interval then send notification to the doctor for action."
    ]

    return pd_rules[start:end]