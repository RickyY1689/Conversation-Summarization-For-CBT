import os
import pandas as pd
import openai

from enum import Enum

class Preds(Enum):
    YES = 1
    NO = 0

def zero_shot():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    dir_path = os.path.dirname(os.path.realpath(__file__))

    test_df = pd.read_csv(f"{dir_path}/../data/righting_reflex.csv", header=None, names=['text', 'label'])
    preds = []
    labels = []
    for _, row in test_df.iterrows():
        text = row['text']
        label = row['label']
        response = openai.Completion.create(model="text-davinci-002",
                                            prompt=f"Is the following statement giving advice? Answer yes or no.\n{text}\nAnswer:\n",
                                            temperature=0.3,
                                            max_tokens=2,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0)
        
        pred = response.choices[0].text.replace('\n', '')
        pred = Preds[pred.upper()].value
        
        print(f"Testing: {text} | Pred: {pred} | Label: {label}")
        preds.append(pred)
        labels.append(label)

    err = [abs(pred - label) for pred, label in zip(preds, labels)]
    acc = 1 - sum(err)/len(err)
    print(f"Accuracy: {acc}")

def few_shot(k, samples=2):
    # Running Cross Validation k Times
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(f"{dir_path}/../data/righting_reflex.csv", header=None, names=['text', 'label'])
    
    acc_list = []
    for i in range(0, k):
        print(f"-------- Run {i} --------")
        train_df = pd.concat([df[df['label']==1].sample(n=samples, random_state=i), df[df['label']==0].sample(n=samples, random_state=i)])
        test_df = df.drop(set(train_df.index))
        preds = []
        labels = []
        prompt = "Is the following statement commanding someone? Answer 0 or 1.\n"
        for _, row in train_df.iterrows():
            prompt += f"'{row['text']}': {row['label']}\n"
        
        for _, row in test_df.iterrows():
            text = row['text']
            label = row['label']
            response = openai.Completion.create(model="text-davinci-002",
                                                prompt=f"{prompt}'{row['text']}':\n",
                                                temperature=0.3,
                                                max_tokens=2,
                                                top_p=1,
                                                frequency_penalty=0,
                                                presence_penalty=0)
            
            pred = response.choices[0].text.replace('\n', '')
            pred = int(pred)
            
            print(f"Testing: {text} | Pred: {pred} | Label: {label}")
            preds.append(pred)
            labels.append(label)
        err = [abs(pred - label) for pred, label in zip(preds, labels)]
        acc = 1 - sum(err)/len(err)
        acc_list.append(acc)
    
    print(f"Accuracies: {acc_list} | Mean Accuracy: {sum(acc_list)/len(acc_list)}")
    
few_shot(3, samples=1)
# zero_shot()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.Completion.create(
#   model="text-davinci-002",
#   prompt="'You feel that you should quit smoking due to it's negative impacts on your health.': 0\n'You want to quit smoking, and you know that it will require willpower.': 0\n'You would like to stop smoking among your friends.': 0\n'Finally, you realize that making this change will require discipline.': 0\n'You enjoy smoking because it relieves stress, but you do not like the health risks associated with it.': 0\n'You mentioned a substitute smoking habit could make quitting easier for you.': 0\n'You need to quit smoking because it's unhealthy.': 1\n'I suggest that you find a substitute smoking habit.': 1\n'You should try nicotine patches to help with alleviate your desire to smoke.': 1\n'I think you need to bolster your willpower if you hope to stick to this new routine.': 1\n'I tell you that you need to stop smoking.': 1\n'If you want to mend your relationship with your family you need to quit smoking.': 1\n'You feel that you should quit smoking due to it's negative impacts on your health.':\n",
#   temperature=0.7,
#   max_tokens=2,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
# breakpoint()