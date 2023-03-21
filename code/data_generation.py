import pandas as pd
import os
import json
import openai
import time

from collections import namedtuple
from tqdm import tqdm
    
BATCH_SIZE = 10
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

def run_experiments_old(params, run_classifier):
    data_df = pd.DataFrame(columns=["param", "convo_num", "summary", "classification"])
    for param in params:
        print(f"Processing param {param.param_name}")
        for num in tqdm(range(0, param.runs)):
            data_path = f"{DIR_PATH}/../data/{param.input_paths}"

            fileObject = open(data_path, "r")
            text = fileObject.read()
            convos = text.split("\n\n\n\n")
            
            assert(len(convos)==20)
            
            for i in tqdm(range(0, len(convos), BATCH_SIZE)):
                end = min(len(convos), i+BATCH_SIZE)
                data = convos[i:end]
                finished_running = False
                while not finished_running:
                    try:
                        for j, prompt in enumerate(params.prompts):
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

                        if run_classifier:
                            ft_model = "davinci:ft-personal:summary-classifier-2023-01-22-02-04-52"
                            resp = openai.Completion.create(model=ft_model, prompt=data, max_tokens=1)
                            preds = [resp.choices[i].text for i in range(len(data))]
                        else:
                            preds = [None]*len(data)
                        finished_running = True
                    except openai.error.RateLimitError:
                        sleep_time = 5
                        print(f"Hit the rate limit! Pausing script for {sleep_time} seconds")
                        time.sleep(sleep_time)
                
                # add result to data_df
                for j, d in enumerate(data):
                    data_df = pd.concat([data_df, pd.DataFrame({
                        "param": [param.param_name],
                        "convo_num": [j+i],
                        "summary": [d],
                        "classification": [preds[j]]
                    })], ignore_index=True)
   
        # Write out after every run through the convos in case code crashes midway through
        data_df.to_csv(f"./experiment_results/{param.output_file_name}")

def run_experiments(params, run_classifier=False):
    data_df = pd.DataFrame()
    for param in params:
        for i in tqdm(range(0, len(param.prompts)), desc="Prompt Phases", position=0, leave=True):
            prompt_seq = param.prompts[i]
            if param.input_paths[i] is not None:
                data_path = f"{DIR_PATH}/../data/{param.input_paths[i]}"
                fileObject = open(data_path, "r")
                data = fileObject.read()
            else:
                data = None
            data_sub_df = send_batched_requests(param, prompt_seq, data, run_classifier)
            data_sub_df = data_sub_df.rename(columns={"summary": f"phase_{i}", "classification": f"classification_{i}"})
            if i == 0:
                data_df = data_sub_df.copy()
            else:
                data_df = data_df.join(data_sub_df.drop(["param", "convo_num"], axis=1))
        data_df.to_csv(f"./experiment_results/{param.output_file_name}")


def send_batched_requests(param, prompt_seq, input_data, run_classifier):
    data_df = pd.DataFrame(columns=["param", "convo_num", "summary", "classification"])
    for _ in tqdm(range(0, param.runs), desc="Rerun Progress",  position=1, leave=True):
        if input_data is not None:
            convos = input_data.split("\n\n\n\n")
            assert(len(convos) == param.data_samples)
        else:
            convos = None
        
        for i in tqdm(range(0, param.data_samples, BATCH_SIZE), desc="Datapoint Progress", position=2, leave=True):
            end = min(param.data_samples, i+BATCH_SIZE)
            if convos is not None:
                data = convos[i:end]
            finished_running = False
            while not finished_running:
                try:
                    for j, prompt in enumerate(prompt_seq):
                        # prompt_batch = list(zip([prompt]*(len(data)), data))
                        if convos is not None:
                            prompt_batch = [f"{prompt}\n\n{d}\n" for d in data]
                        else:
                            prompt_batch = [f"{prompt}\n" for _ in range(0, end-i)]
                        resp = openai.Completion.create(model=param.model,
                                                            prompt=prompt_batch,
                                                            temperature=0.7,
                                                            max_tokens=1024,
                                                            top_p=1,
                                                            frequency_penalty=0,
                                                            presence_penalty=0)
                        data = [resp.choices[i].text.replace('\n', '') for i in range(0, end-i)]

                    if run_classifier:
                        ft_model = "davinci:ft-personal:summary-classifier-2023-01-22-02-04-52"
                        resp = openai.Completion.create(model=ft_model, prompt=data, max_tokens=1)
                        preds = [resp.choices[i].text for i in range(len(data))]
                    else:
                        preds = [None]*len(data)
                    finished_running = True
                except openai.error.RateLimitError:
                    sleep_time = 5
                    print(f"Hit the rate limit! Pausing script for {sleep_time} seconds")
                    time.sleep(sleep_time)
            
            # add result to data_df
            for j, d in enumerate(data):
                data_df = pd.concat([data_df, pd.DataFrame({
                    "param": [param.param_name],
                    "convo_num": [j+i],
                    "summary": [d],
                    "classification": [preds[j]]
                })], ignore_index=True)

    # Write out after every run through the convos in case code crashes midway through
    return data_df


Param = namedtuple('Param', ['param_name', 'prompts', 'model', 'runs', 'input_paths', 'data_samples', 'output_file_name'])

# Older Param structure meant to run via run_experiments_old(...)
# ParamOld = namedtuple('Param', ['param_name', 'prompts', 'model', 'runs', 'input_path', 'output_file_name'])
# 
# Example single phase single prompt
# param1 = ParamOld("1", ["Summarize this text message conversation between me and you in second person:"],
#                "text-davinci-003", 10, "renamed_cleaned_transcripts.txt")
# Example single phase multi prompt
# param2 = ParamOld("2", ["Summarize the following conversation between the BOT and the USER:",
#                "Convert from third to first person:",
#                "Convert from first person to second person:"], 
#                "text-davinci-002", 20, "cleaned_transcripts.txt")

# Example on the updated 
# param1 = Param("MPA1", 
#                [
#                 ["Write a reply from the perspective of the therapist. First, write a single sentence that informs the client you will now take a moment to summarize the conversation you've had to make sure you understand what the client has said. Now summarize the conversation so far keeping in mind the following guidelines. Focus on the client's feelings and experiences, and show that you understand and accept what they're going through. Summarize what the client said in a way that acknowledges their emotions and perspective. Encourage the client to think about the reasons they want to change, and summarize these reasons in a way that's clear and easy to understand. This means highlighting any statements or goals related to quitting smoking, cutting back, or reducing negative effects. Finishing by asking the client if anything was missed in your reply before ending this conversation. This question must not ask the client to discuss new topics and only serves to verify nothing was missed in your response. The conversation is as follows:"]
#                 ],
#                "text-davinci-003", 1, ["therapist_client_transcripts.txt"], 20, "3_20_MPA1.csv")

param1 = Param("MPA6", 
               [
                ["As a therapist provide a single sentence explaining to your client that you will now take a moment to summarize your conversation with them to ensure you understand what the client has said so far."], 
                ["Write a reply from the perspective of the therapist summarizing the conversation so far. Focus on the client's feelings and experiences, and show that you understand and accept what they're going through. Summarize what the client said in a way that acknowledges their emotions and perspective. Encourage the client to think about the reasons they want to change, and summarize these reasons in a way that's clear and easy to understand. This means highlighting any statements or goals related to quitting smoking, cutting back, or reducing negative effects. Finishing by asking the client if anything was missed in your reply before ending this conversation. This question must not ask the client to discuss new topics and only serves to verify nothing was missed in your response. The conversation is as follows:",
                 "You are rewriting a message from a therapist to their client. Assume the role of the therapist and rewrite every sentence in the message that begins with 'You' such that no rewritten sentence begins with 'You'. These rewritten sentences should instead begin with phrases similar to phrases like 'It sounds like you' or 'What I'm hearing is that'. Ensure the rewritten sentences still address the client. Sentences that do not start with 'You' must be left unchanged. The message is as follows:"
                 ],
                ],
               "text-davinci-003", 1, [None, "therapist_client_transcripts.txt"], 20, "3_20_MPA6.csv")

params = [
            param1,
         ]

if update_json_params(params):
    run_experiments(params)
