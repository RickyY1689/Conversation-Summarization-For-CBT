import os

def remove_noise(convo):
    cleaned_convo = []
    for i in range(0, len(convo)-1, 6):
        cleaned_convo.extend(convo[i:i+3])
    return cleaned_convo

def change_names(convo):
    cleaned_convo = [None] * len(convo)
    for i in range(0, len(convo)):
        cleaned_convo[i] = convo[i].replace("BOT", "me").replace("USER", "you")
    return cleaned_convo

input_file = "cleaned_transcripts.txt"
output_file = "renamed_cleaned_transcripts.txt"

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = f"{dir_path}/../data/{input_file}"
preprocess_func = change_names
fileObject = open(data_path, "r")
text = fileObject.read()
convos = text.split("\n\n\n\n")
cleaned_convos = []

for convo in convos:
    cleaned_convo = preprocess_func(convo.split("\n"))
    cleaned_convo = "\n".join(cleaned_convo)
    cleaned_convos.append(cleaned_convo)

with open(f'{dir_path}/../data/{output_file}', 'w') as f:
    f.write("\n\n\n\n".join(cleaned_convos))
