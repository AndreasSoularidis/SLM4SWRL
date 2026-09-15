from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

class OntologyAnalyzer:
  def __init__(self, path: str):
    g = Graph()
    self.ontology = g.parse(path)


  def get_classes(self, withUri: bool = False) -> list:
    q_classes = prepareQuery("""
      SELECT ?class
      WHERE {
          ?class a owl:Class .
          FILTER(isIRI(?class))
      }
    """)

    classes_list = []
    for row in self.ontology.query(q_classes):
      if withUri:
        classes_list.append(f"{self.ontology.compute_qname(row[0])[2]}:{self.ontology.compute_qname(row[0])[2]}") 
      else:
        classes_list.append(self.ontology.compute_qname(row[0])[2])
    return classes_list 
  

  def get_object_properties(self, withUri: bool = False) -> list:
    q_object_props = prepareQuery("""
      SELECT ?prop ?domain ?range
      WHERE {
          ?prop a owl:ObjectProperty .
          OPTIONAL { ?prop rdfs:domain ?domain . }
          OPTIONAL { ?prop rdfs:range ?range . }
      }
      ORDER BY ?prop
    """)
    obj_properties_list = []
    for row in self.ontology.query(q_object_props):
      prop_name = self.ontology.compute_qname(row.prop)[2] if not withUri else f"{self.ontology.compute_qname(row.prop)[0]}:{self.ontology.compute_qname(row.prop)[2]}"
      if withUri:
        domain_name = f"{self.ontology.compute_qname(row.domain)[0]}:{self.ontology.compute_qname(row.domain)[2]}" if row.domain else "ANY"
        range_name = f"{self.ontology.compute_qname(row.range)[0]}:{self.ontology.compute_qname(row.range)[2]}" if row.range else "ANY"
      else:
        domain_name = self.ontology.compute_qname(row.domain)[2] if row.domain else "ANY"
        range_name = self.ontology.compute_qname(row.range)[2] if row.range else "ANY"
      
      obj_properties_list.append(f"- {prop_name} (domain: {domain_name}, range: {range_name})")
    return obj_properties_list
  

  def get_data_properties(self, withUri: bool = False) -> list:
    q_data_props = prepareQuery("""
      SELECT ?prop ?domain ?range
      WHERE {
          ?prop a owl:DatatypeProperty .
          OPTIONAL { ?prop rdfs:domain ?domain . }
          OPTIONAL { ?prop rdfs:range ?range . }
      }
      ORDER BY ?prop
    """)

    data_properties_list = []
    for row in self.ontology.query(q_data_props):
      prop_name = self.ontology.compute_qname(row.prop)[2] if not withUri else f"{self.ontology.compute_qname(row.prop)[0]}:{self.ontology.compute_qname(row.prop)[2]}"
      if withUri:
        domain_name = f"{self.ontology.compute_qname(row.domain)[0]}:{self.ontology.compute_qname(row.domain)[2]}" if row.domain else "ANY"
        range_name = f"{self.ontology.compute_qname(row.range)[0]}:{self.ontology.compute_qname(row.range)[2]}" if row.range else "ANY"
      else:
        domain_name = self.ontology.compute_qname(row.domain)[2] if row.domain else "ANY"
        range_name = self.ontology.compute_qname(row.range)[2] if row.range else "ANY"
      
      data_properties_list.append(f"- {prop_name} (domain: {domain_name}, range: {range_name})")
    return data_properties_list
  
  
  def get_ontology_summary(self, withUri : bool = False) -> str:
    """
    Queries the rdflib Graph to extract a concise summary of the ontology's
    classes, object properties, and data properties.
    """
    summary = "### Ontology Schema ###\n\n"
    
    summary += (
      "@prefix : <http://example.org/job-ontology#> .\n"
      "@prefix gr: <http://example.org/greek-terms#> .\n"
      "@prefix job: <http://example.org/job-ontology#> .\n"
      "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
      "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
      "@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n"
      "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
      "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
      "@base <http://example.org/job-ontology#> .\n\n"
    )
    

    # Format Classes
    summary += "## Classes (Entities you can create):\n"
    for cls in self.get_classes(withUri):
      summary += f"- {cls}\n"
      
    # Format Object Properties
    summary += "\n## Object Properties (Relationships between entities):\n"
    for prop in self.get_object_properties(withUri):
      summary += f"{prop}\n"
      
    # Format Data Properties
    summary += "\n## Data Properties (Attributes of entities):\n"
    for prop in self.get_data_properties(withUri):
      summary += f"{prop}\n"
      
    summary += "######################\n\n"
    
    return summary