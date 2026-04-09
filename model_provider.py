class ModelProvider:
  def __init__(self):
    self.models = {
      "mistral": "mistral:7b",
      "mistral-instruct": "mistral-SWRL-3:latest",
      "llama": "llama3.1:8b",
      "llama-instruct": "llama3.1-SWRL-3:latest",
      "qwen": "qwen2.5:7b",
      "qwen-instruct": "swot/qwen2.5-instruct:lastest",
      "openai": "ft:gpt-4o-2024-08-06:personal:recipe-ner:BMAvb5Vd",
      "phi-large": "phi3:14b",
      "phi-instruct": "swot/phi-3.5-mini-instruct:new",
      "phi4-instruct": "swot/phi-4-instruct:latest",
      "gemma": "gemma2:9b",
      "gemma-instruct": "swot/codegemma-instruct"
    }

  def get_model(self, name):
    return self.models.get(name)
