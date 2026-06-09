import json


path = 'G:\\Το Drive μου\\PhD - Drive\\SLM4SWRL\\Experiments\\Experiment Files\\SAR\\Phase2-SAR-llama.jsonl'
with open(path, "r", encoding="utf-8") as f:
  for line in f:
    record = json.loads(line)
    
    # Human content
    human_content = record["inputs"]["messages"][0][0]["kwargs"]["content"]
    
    # Model response
    response = record["outputs"]["generations"][0][0]["text"]
    
    print("HUMAN:", human_content)
    print("RESPONSE:", response)
    print("---")