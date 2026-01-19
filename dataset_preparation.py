import json

def transform_to_alpaca_format(path):
  dataset_path = path.split('/')[:-1]
  dataset_name = path.split('/')[-1].split('.')[0]
  extension = path.split('/')[-1].split('.')[-1]
  
  with open(path, 'r', encoding='utf-8') as file:
    instances = json.load(file)

  alpaca_format_data = []
  for index, _ in enumerate(instances):
    alpaca_format_data.append({
      "instruction": instances[index]['conversations'][0]['content'],
      "input": instances[index]['conversations'][1]['content'],
      "output": instances[index]['conversations'][2]['content']
    })

  print(f"Total instances converted: {len(alpaca_format_data)}")

  destination_path = f"{'/'.join(dataset_path)}/{dataset_name}_alpaca.{extension}"
  with open(destination_path, 'w', encoding='utf-8') as f:
    json.dump(alpaca_format_data, f, ensure_ascii=False, indent=4)

transform_to_alpaca_format('./Dataset and Notebooks/dataset_v5_extended.json')