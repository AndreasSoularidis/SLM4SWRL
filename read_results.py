from datasets import Dataset
from dotenv import load_dotenv
import openai
from ragas.llms import llm_factory
from ragas import evaluate
from ragas.metrics._context_recall import ContextRecall
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._factual_correctness import FactualCorrectness
load_dotenv()
import json
import re

path = './results/Updated-Phase2-SAR-ministral_14b.jsonl'

with open(path, "r", encoding="utf-8") as f:
  for line in f:
    record = json.loads(line)

    # Full prompt content
    human_content = record["inputs"]["messages"][0][0]["kwargs"]["content"]

    # Model response (strip ```swrl code fences if present)
    raw_response = record["outputs"]["generations"][0][0]["text"]
    swrl_rule = re.sub(r"^```swrl\s*|\s*```$", "", raw_response.strip())

    # Extract NL rule (after "The rule in natural language is the following:")
    nl_match = re.search(
        r"The rule in natural language is the following:\s*(.*?)(?=\s*Give only|\Z)",
        human_content,
        re.DOTALL,
    )
    nl_rule = nl_match.group(1).strip() if nl_match else None

    # Extract ontology context (between PART OF ONTOLOGY and END OF ONTOLOGY)
    ontology_match = re.search(
        r"PART OF ONTOLOGY\s*(.*?)\s*END OF ONTOLOGY",
        human_content,
        re.DOTALL,
    )
    ontology_context = ontology_match.group(1).strip() if ontology_match else None

    data_sample_k5 = {
      "question": [nl_rule],
      "answer": [swrl_rule],
      "retrieved_contexts": [
      [
        ontology_context.join(",")
      ]
      ],
      "ground_truth": ["""Detection(?d) ^ Incident(?i) ^ detectsIncident(?d, ?i) ^ hasDetectionRisk(?d, ?dr) ^ swrlb:greaterThan(?dr, 0.8) ^ hasDetectionConfidence(?d, ?dc) ^ swrlb:lessThan(?dc, 0.5) ^ Mission(?m) ^ Responder(?r) -> hasIncidentPriority(?i, "request verification"^^rdf:PlainLiteral) ^ isAssignedMission(?r, ?m)"""]
    }
    client = openai.AsyncOpenAI()
    llm = llm_factory("gpt-4o-mini", client=client)
    dataset = Dataset.from_dict(data_sample_k5)

    score = evaluate(dataset, metrics=[ContextRecall(), Faithfulness(), FactualCorrectness()], llm=llm)
    

    print("NL RULE:  ", nl_rule)
    print("SWRL RULE:", swrl_rule)
    print("ONTOLOGY: ", ontology_context)
    print("RAGAS EVAL: ", score)
    print("---")
    break
