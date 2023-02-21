import pandas as pd
import os
import json
import openai
import time

from collections import namedtuple
from tqdm import tqdm
    
BATCH_SIZE = 5
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

with open('openai_key.txt') as f:
    openai.api_key = f.read()

def update_json_params(params):
    # Convert the params to a list of dictionaries
    params_dict = [p._asdict() for p in params]

    json_file = 'experiment_parameters.json'
    # Load the existing JSON file
    with open(f"{DIR_PATH}/../data/{json_file}", 'r') as f:
        data = json.load(f)
    # Update the data with the new params
    for p_d in params_dict:
        if p_d["param_name"] in data:
                # Check if the entire namedtuple is identical
                if data[p_d["param_name"]] == p_d:
                    print(f"***** WARNING: Param Set with name {p_d['param_name']} already exists and is identical. *****")
                else:
                    print(f"***** ERROR: Param Set with name {p_d['param_name']} already exists and is not identical. *****")
                    return False
        data.update({p_d["param_name"]: p_d})

    # Write the updated data back to the JSON file
    with open(f"{DIR_PATH}/../data/{json_file}", 'w') as f:
        json.dump(data, f, indent=4)
    return True

def run_experiments(params):
    for param in params:
        print(f"Processing param {param.param_name}")
        for num in tqdm(range(0, param.runs)):
            data_path = f"{DIR_PATH}/../data/{param.input_path}"

            fileObject = open(data_path, "r")
            text = fileObject.read()
            convos = text.split("\n\n\n\n")

            for i in tqdm(range(0, len(convos), BATCH_SIZE)):
                end = min(len(convos), i+BATCH_SIZE)
                data = convos[i:end]
                finished_running = False
                while not finished_running:
                    try:
                        for j, prompt in enumerate(param.prompt_seq):
                            # prompt_batch = list(zip([prompt]*(len(data)), data))
                            prompt_batch = [f"{prompt}\n\n{d}\n" for d in data]
                            resp = openai.Completion.create(model=param.model,
                                                                prompt=prompt_batch,
                                                                temperature=0.7,
                                                                max_tokens=1024,
                                                                top_p=1,
                                                                frequency_penalty=0,
                                                                presence_penalty=0)
                            data = [resp.choices[i].text.replace('\n', '') for i in range(len(data))]

                        ft_model = "davinci:ft-personal:summary-classifier-2023-01-22-02-04-52"
                        resp = openai.Completion.create(model=ft_model, prompt=data, max_tokens=1)
                        preds = [resp.choices[i].text for i in range(len(data))]
                        finished_running = True
                    except openai.error.RateLimitError:
                        sleep_time = 5
                        print(f"Hit the rate limit! Pausing script for {sleep_time} seconds")
                        time.sleep(sleep_time)
                
                # add result to data_df
                for i, d in enumerate(data):
                    data_df = pd.concat([data_df, pd.DataFrame({
                        "param": [param.param_name],
                        "convo_num": [i],
                        "summary": [d],
                        "classification": [preds[i]]
                    })], ignore_index=True)
   
        # Write out after every run through the convos in case code crashes midway through
        data_df.to_csv(f"./experiment_results/{param.output_file_name}")


data_df = pd.DataFrame(columns=["param", "convo_num", "summary", "classification"])
Param = namedtuple('Param', ['param_name', 'prompt_seq', 'model', 'runs', 'input_path', 'output_file_name'])

param1 = Param("1", ["Summarize this text message conversation between me and you in second person:"],
               "text-davinci-003", 10, "renamed_cleaned_transcripts.txt")
# param2 = Param("2", ["Summarize the following conversation between the BOT and the USER:",
#                "Convert from third to first person:",
#                "Convert from first person to second person:"], 
#                "text-davinci-002", 20, "cleaned_transcripts.txt")
param = Param("MegaPrompt", ["Write a reply from the perspective of the therapist summarizing the conversation so far. Focus on the client's feelings and experiences, and show that you understand and accept what they're going through. Summarize what the client said in a way that acknowledges their emotions and perspective. Encourage the client to think about the reasons they want to change, and summarize these reasons in a way that's clear and easy to understand. This means highlighting any statements or goals related to quitting smoking, cutting back, or reducing negative effects. End with an open-ended question that encourages the client to think more about their commitment to change by asking a question that doesn't have a simple yes or no answer, and that invites the client to reflect on what they've shared. The conversation is as follows:"],
              "text-davinci-003", 1, "therapist_client_transcripts.txt", "2_21_1_mega_prompt.csv")
params = [
            param
         ]

if update_json_params(params):
    run_experiments(params)
