import os
import json
import openai
import time
import re

with open('openai_key.txt') as f:
    openai.api_key = f.read()

input_path = "renamed_cleaned_transcripts.txt"
output_path = "1_10_1.json"
postprocessing = False

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = f"{dir_path}/../data/{input_path}"

fileObject = open(data_path, "r")
text = fileObject.read()
convos = text.split("\n\n\n\n")

prompt_seq = ["Summarize the following conversation between you and me:",
              "Convert from third to first person:",
              "Convert from first person to second person:"]
res_dict = {}

for temp in range(10, 11, 1):
    output_path = f"1_10_1_temp_{float(temp/10)}.json"
    print(f"Testing temp at {float(temp/10)}")
    postprocessing = False

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = f"{dir_path}/../data/{input_path}"
    for i, convo in enumerate(convos):
        if i%10==0 and i!=0:
            time.sleep(10)
        data = convo
        res_dict[i] = {"data": data}
        print(f"------------ Convo Number #{i+1} ------------")
        for j, prompt in enumerate(prompt_seq):
            response = openai.Completion.create(model="text-davinci-003",
                            prompt=f"{prompt}\n\n{data}\n",
                            temperature=float(temp/10),
                            max_tokens=256,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0)
            
            data = response.choices[0].text.replace('\n', '')
            res_dict[i][j] = {}
            res_dict[i][j]["prompt"] = prompt
            res_dict[i][j]["result"] = data
            print(f"{prompt}")
            print(f"{data}")

        if postprocessing:
            postprocessed_data = data

            if "conversation" in postprocessed_data[0:postprocessed_data.find(".")]:
                postprocessed_data = postprocessed_data[postprocessed_data.find(".")+2:]

            conversion_dict = {"I":	"you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself", "am": "are", "the other individual": "me"}
            def replace(match):
                return conversion_dict[match.group(0)]
            # for key, value in conversion_dict.items():
            postprocessed_data = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in conversion_dict), replace, postprocessed_data)
            postprocessed_data = ". ".join([p.capitalize() for p in postprocessed_data.split(". ")])
            
            res_dict[i][j+1] = {}
            res_dict[i][j+1]["prompt"] = "Postprocessing Step"
            res_dict[i][j+1]["result"] = postprocessed_data
            
    # Directly from dictionary
    with open(f'{dir_path}/../experiment_results/{output_path}', 'w') as outfile:
        json.dump(res_dict, outfile)