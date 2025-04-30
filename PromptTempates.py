class CustomPromptTemplates:
  ontology_template = """
  Act as an ontology engineer. Use the following content (part of the ontology) as a guide to translate the natural language rule you are given into a SWRL rule. 
    PART OF ONTOLOGY 

    {context}

    END OF ONTOLOGY

    The rule in natural language is the following: {question}
    Give only the final SWRL rule
  """

  
  @staticmethod
  def rules_in_nl():
    easy_rule = """if gas is recognized at coordinates and fire is recognized at these coordinates and agents is nearby to these coordinates, then send an alert to these agents, and the agents must abort mission."""
    medium_rule = """if a person is recognized at coordinates and has heart rate less than 30 pulses per minute and the location in these coordinates is safe, then send to thsese coordinates a search and rescue team."""
    hard_rule = """if house on fire is recognized at coordinates and person has Voice Sign 'help', then send alert to fire station, send to these coordinates a search and rescue team, send to these coordinates a flying drone agent and send to these coordinates a spot robot agent."""
    
    prompt1 = easy_rule
    prompt2 = medium_rule
    prompt3 = hard_rule

    return [prompt1, prompt2, prompt3] 