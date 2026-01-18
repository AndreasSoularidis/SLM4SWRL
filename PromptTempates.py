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

  ttl_examples = """
    EXAMPLES

    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    PART OF ONTOLOGY
    example_ontology:hasSibling rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range example_ontology:Person ;
      rdfs:label "has sibling" .
    example_ontology:IsMan rdf:type owl:DatatypeProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range xsd:boolean ;
      rdfs:label "is man" .
    example_ontology:hasBrother rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range example_ontology:Person ;
      rdfs:label "has brother" .
    example_ontology:Person rdf:type owl:Class ;
      rdfs:label "Person" .
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    PART OF ONTOLOGY
    example_ontology:hasPhoneNumber rdf:type owl:DatatypeProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range xsd:string ;
      rdfs:label "has phone number" .
    example_ontology:hasInternationalPhoneNumber rdf:type owl:DatatypeProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range xsd:boolean ;
      rdfs:label "has international phone number" .
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
    PART OF ONTOLOGY
    example_ontology:hasIdCard rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range example_ontology:IdCard ;
      rdfs:label "has ID Card" .
    example_ontology:hasAge rdf:type owl:DatatypeProperty ;
      rdfs:domain example_ontology:Person ;
      rdfs:range xsd:boolean ;
      rdfs:label "has age" .
    example_ontology:Person rdf:type owl:Class ;
      rdfs:label "Person" .
    example_ontology:IdCard rdf:type owl:Class ;
      rdfs:label "ID Card" .
    example_ontology:Adult rdf:type owl:Class ;
      rdfs:subClassOf example_ontology:Person ;
      rdfs:label "Adult" .
    END OF ONTOLOGY

    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)

    Example 4
    Rule in natural language:  If a publication has two different authors, then those authors have cooperated with each other.
    PART OF ONTOLOGY
    example_ontology:hasAuthor rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Publication ;
      rdfs:range example_ontology:Author ;
      rdfs:label "has author" .
    example_ontology:differentFrom rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Author ;
      rdfs:range example_ontology:Author ;
      rdfs:label "different from" .
    example_ontology:cooperatedWith rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Author ;
      rdfs:range example_ontology:Author ;
      rdfs:label "cooperated with" .
    END OF ONTOLOGY
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

    Example 5

    Rule in natural language: if a researcher has published more than 10 papers in a Top-Tier conference, then the researcher is a prominent researcher and has a high citation impact.
    PART OF ONTOLOGY
    example_ontology:hasPublished rdf:type owl:ObjectProperty ;
      rdfs:domain example_ontology:Researcher ;
      rdfs:range example_ontology:Conference ;
      rdfs:label "has published" .
    example_ontology:hasHighCitationImpact rdf:type owl:DatatypeProperty ;
      rdfs:domain example_ontology:Researcher ;
      rdfs:range xsd:boolean ;
      rdfs:label "has high citation impact" .
    example_ontology:Conference rdf:type owl:Class ;
      rdfs:label "Conference" .
    example_ontology:Researcher rdf:type owl:Class ;
      rdfs:label "Researcher" .
    example_ontology:TopTierConference rdf:type owl:Class ;
      rdfs:subClassOf example_ontology:Conference ;
      rdfs:label "Top-Tier Conference" .
    example_ontology:ProminentResearcher rdf:type owl:Class ;
      rdfs:subClassOf example_ontology:Researcher ;
      rdfs:label "Prominent Researcher" .
    END OF ONTOLOGY
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?c) ^ Conference(?c) ^ topTierConference(?c) ^ swrlb:greaterThan(count(?c), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)

    END OF EXAMPLES
  """

  owl_examples = """
    EXAMPLES

    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    PART OF ONTOLOGY
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasSibling">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:label>has sibling</rdfs:label>
    </owl:ObjectProperty>
    <owl:DatatypeProperty rdf:about="https://raw.githubusercontent.com/example_ontology#IsMan">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label>is man</rdfs:label>
    </owl:DatatypeProperty>
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasBrother">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:label>has brother</rdfs:label>
    </owl:ObjectProperty>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#Person">
        <rdfs:label>Person</rdfs:label>
    </owl:Class>
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    PART OF ONTOLOGY
    <owl:DatatypeProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasPhoneNumber">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:label>has phone number</rdfs:label>
    </owl:DatatypeProperty>
    <owl:DatatypeProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasInternationalPhoneNumber">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label>has international phone number</rdfs:label>
    </owl:DatatypeProperty>
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
    PART OF ONTOLOGY
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasIdCard">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#IdCard"/>
        <rdfs:label>has ID Card</rdfs:label>
    </owl:ObjectProperty>
    <owl:DatatypeProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasAge">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label>has age</rdfs:label>
    </owl:DatatypeProperty>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#Person">
        <rdfs:label>Person</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#IdCard">
        <rdfs:label>ID Card</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#Adult">
      <rdfs:subClassOf rdf:resource="https://raw.githubusercontent.com/example_ontology#Person"/>
        <rdfs:label>Adult</rdfs:label>
    </owl:Class>
    END OF ONTOLOGY

    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)

    Example 4
    Rule in natural language:  If a publication has two different authors, then those authors have cooperated with each other.
    PART OF ONTOLOGY
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasAuthor">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Publication"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Author"/>
        <rdfs:label>has author</rdfs:label>
    </owl:ObjectProperty>
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#differentFrom">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Author"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Author"/>
        <rdfs:label>different from</rdfs:label>
    </owl:ObjectProperty>
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#cooperatedWith">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Author"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Author"/>
        <rdfs:label>cooperated with</rdfs:label>
    </owl:ObjectProperty>
    END OF ONTOLOGY
    SWRL rule: Publication(?p) ^ Author(?y) ^ Author(?z) ^ hasAuthor(?p, ?y) ^ hasAuthor(?p, ?z) ^ differentFrom(?y, ?z) -> cooperatedWith(?y, ?z)

    Example 5

    Rule in natural language: if a researcher has published more than 10 papers in a Top-Tier conference, then the researcher is a prominent researcher and has a high citation impact.
    PART OF ONTOLOGY
    <owl:ObjectProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasPublished">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Researcher"/>
        <rdfs:range rdf:resource="https://raw.githubusercontent.com/example_ontology#Conference"/>
        <rdfs:label>has published</rdfs:label>
    </owl:ObjectProperty>
     <owl:DatatypeProperty rdf:about="https://raw.githubusercontent.com/example_ontology#hasHighCitationImpact">
        <rdfs:domain rdf:resource="https://raw.githubusercontent.com/example_ontology#Researcher"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>
        <rdfs:label>has high citation impact</rdfs:label>
    </owl:DatatypeProperty>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#Conference">
        <rdfs:label>Conference</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#Researcher">
        <rdfs:label>Researcher</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#TopTierConference">
      <rdfs:subClassOf rdf:resource="https://raw.githubusercontent.com/example_ontology#Conference"/>
        <rdfs:label>Top-Tier Conference</rdfs:label>
    </owl:Class>
    <owl:Class rdf:about="https://raw.githubusercontent.com/example_ontology#ProminentResearcher">
      <rdfs:subClassOf rdf:resource="https://raw.githubusercontent.com/example_ontology#Researcher"/>
        <rdfs:label>Prominent Researcher</rdfs:label>
    </owl:Class>
    END OF ONTOLOGY
    SWRL rule: Researcher(?r) ^ hasPublished(?r, ?c) ^ Conference(?c) ^ topTierConference(?c) ^ swrlb:greaterThan(count(?c), 10) -> ProminentResearcher(?r) ^ hasHighCitationImpact(?r, true)

    END OF EXAMPLES
  """

  manchester_examples = """
    EXAMPLES

    Example 1
    Rule in natural language: If a person has a sibling who is a man, then the person has a brother.
    PART OF ONTOLOGY
    ObjectProperty: example_ontology:hasSibling
      Annotations: 
        rdfs:label "has sibling"
      Domain: 
        example_ontology:Person
      Range: 
        example_ontology:Person

    DataProperty: example_ontology:isMan
      Annotations: 
        rdfs:label "is man"
      Domain: 
        example_ontology:Person
      Range: 
        xsd:boolean

    ObjectProperty: example_ontology:hasBrother
      Annotations: 
        rdfs:label "has brother"
      Domain: 
        example_ontology:Person
      Range: 
        example_ontology:Person

    Class: example_ontology:Person
      Annotations: 
        rdfs:label "Person",
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasSibling(?p, ?s) ^ Person(?s) ^ IsMan(?s, true) -> hasBrother(?p, ?s)

    Example 2
    Rule in natural language: if a person has a phone number that starts with '+', then the person has an international phone number.
    PART OF ONTOLOGY
     DataProperty: example_ontology:hasPhoneNumber
      Annotations: 
        rdfs:label "has phone number"
      Domain: 
        example_ontology:Person
      Range: 
        xsd:string

    DataProperty: example_ontology:hasInternationalPhoneNumber
      Annotations: 
        rdfs:label "has international phone number",
      Domain: 
        example_ontology:Person
      Range: 
        xsd:boolean
    END OF ONTOLOGY 
    SWRL rule: Person(?p) ^ hasPhoneNumber(?p, ?number) ^ swrlb:startsWith(?number, "+") -> hasInternationalPhoneNumber(?p, true)

    Example 3
    Rule in natural language:  if a person has age greater than 17, then the person is an adult and has id card.
    PART OF ONTOLOGY
    ObjectProperty: example_ontology:hasIdCard
      Annotations: 
        rdfs:label "has ID Card"
      Domain: 
        example_ontology:Person
      Range: 
        example_ontology:IdCard

    DataProperty: example_ontology:hasAge
      Annotations: 
        rdfs:label "has age"
      Domain: 
        example_ontology:Person
      Range: 
        xsd:boolean
    
    Class: example_ontology:Person
      Annotations: 
        rdfs:label "Person",

    Class: example_ontology:IdCard
      Annotations: 
        rdfs:label "ID Card",

    Class: example_ontology:Adult
      Annotations: 
        rdfs:label "Adult"

      SubClassOf: 
        example_ontology:Person
    END OF ONTOLOGY

    SWRL rule: Person(?p) ^ hasAge(?p, ?age) ^ swrlb:greaterThan(?age, 17) ^ IdCard(?id) -> Adult(?p) ^ hasIdCard(?p, ?id)
    END OF EXAMPLES
  """

  system = "Act as an ontology engineer. Use the following content (examples, part of the ontology, and common mistakes) as a guide to translate the natural language rule you are given into a SWRL rule. "
  
  guidelines = """
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

  def get_prompt(self, format):
    prompt = self.system
    if format == "ttl":
      prompt += self.ttl_examples
    elif format == "owl":
      prompt += self.owl_examples
    elif format == "manchester":
      prompt += self.manchester_examples
    elif format == "graph":
      prompt += self.graph_examples
    prompt += self.guidelines
    return prompt
  
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