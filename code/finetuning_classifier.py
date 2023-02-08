import pandas as pd
import os
import json
import openai

input_path = "1_10_1_temp_0.6.json"
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = f"{dir_path}/../experiment_results/{input_path}"

with open(f'{dir_path}/../openai_key.txt') as f:
        openai.api_key = f.read()

with open(data_path, 'r') as f:
    data = json.load(f)

for k in data.keys():
    print("--------")
    print(data[k]['2']['result'])

    ft_model = "davinci:ft-personal:summary-classifier-2023-01-22-02-04-52"
    res = openai.Completion.create(model=ft_model, prompt=data[k]['2']['result'], max_tokens=1)
    print(res['choices'][0]['text'])