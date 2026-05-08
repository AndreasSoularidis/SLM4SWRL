class CustomPromptTemplates:
  retreiver_system = """
  You are an expert Knowledge/Ontology Engineer.
  Your task is to extract nouns or short phrases that appear in the input text and are present in the context. 
  Output only the list of concept names, no explanations, no reasoning, no OWL or RDF, no text other than the list. 
  Each concept must exactly match or be semantically equivalent to an ontology label.  
  """

  retreiver_prompt = """
    Context:\n{context}\n
    Text:\n{question}\n
  """

  prompt = """
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