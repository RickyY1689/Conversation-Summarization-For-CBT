# Designing a Minimum Viable Summarization Generator

## Purpose

The goal by the end of this experiment is to have generated a prompt or prompt pipeline utilizing GPT3 to generate a "good enough" summary.

We will define a "good enough" summary as the following:

- Covers the majority of points the user has brought up and the reflections from the bot
- Has no anaphora issues (User, Bot, I, You, etc.)
- Does not give a surface level summary (ie "You and I are discussing smoking...")

This is our desired summary outcome.

While we would like to avoid things like the righting reflex as described in [Righting-Reflex-Classification](Righting-Reflex-Classification.md) these issues fall out of scope during the pursuit of an MVP.

**Goal:** Create a prompt or prompt pipeline with a 95%> hitrate or desired summaries.

## Experiments

### Baseline Results

**Data:** [transcripts.txt](../data/transcripts.txt)

**Results File Name:** [Summarization Baseline](../experiment_results/summarization_baseline.json)

**Baseline Hitrate:** 45%

The results of the baseline are summarized and analyzed in [Baseline-State-of-Summarization](Baseline-State-of-Summarization.md).

### Experiment 1 - Preprocess Text Transcripts

**Data:** [cleaned_transcripts.txt](../data/cleaned_transcripts.txt)

**Results File Name:** [12_3_1_MVP.json](../experiment_results/12_3_1_MVP.json)

**Hitrate:** 65%

**Parameters**:

```python
prompt_seq = ["Summarize the following conversation between the BOT and the USER:",
              "Convert from third to first person:",
              "Convert from first person to second person:"]
openai.Completion.create(model="text-davinci-002",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.7,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

We will remove the fluff from the text transcripts from the bot so that the model will only be shown the things we want it to focus on. Given the Bot asks 5 questions with each question followed by a User reply and a Bot reflection, we will cut down each transcript to 15 messages each.

While the issues revolving anaphora were decreased some of the initial summaries became extractive without any change in the prompt.

### Experiment 2 - Moving to DaVinci-003

**Data:** [cleaned_transcripts.txt](../data/cleaned_transcripts.txt)

**Results File Name:** [12_3_2_MVP.json](../experiment_results/12_3_2_MVP.json)

**Incorporations from Prior Experiments:** Preprocess Text

**Hitrate:** 80%

**Parameters**:

```python
prompt_seq = ["Summarize the following conversation between the BOT and the USER:",
              "Convert from third to first person:",
              "Convert from first person to second person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.7,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```



During this experiment, OpenAI presented a new publicly available version of GPT-3 called DaVinci-003. Prior to this, all experiments were run on DaVinvi-002. It is worthwhile to see if there are any differences in the results when using this model. 

Using DaVinci-003 removed both surface level summaries and extractive summaraies however the issue of pronoun issues still exist.

> You like the feeling and physical act of smoking, but you don't like the smell. You don't want to make a change in your smoking habit, but the bot emphasizes the need for discipline and persistence if you are to make a change. The bot suggests that to smoke less, you would keep yourself busy in other ways. The bot acknowledges this, highlighting that it is not just a matter of smoking less, but also of staying busy in other ways.

However there may be a couple of potential easy fixes to this"

1. By modifying the chat transcripts to replace "BOT" and "USER" and "I" and "You" respectively would remove bot and user from the input, hopefully making it easier for the final output to properly select the correct pronouns.

2. Replacing "the bot" and "the user" in the final output with "You" and "I" may also resolve these issues. The last two sentences are indeed redundant but we will not worry about this during the design of an MVP. Now, assuming that GPT3 is able to correct grammar, we may add another prompt to the pipeline to fix the grammar.

Since method 2 would result in more prompts slowing down overall runtime, method 1 seems more appropriate to pursue first.

### Experiment 3 - Converting Texter Names to "Me" and "You"

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [12_3_3_MVP.json](../experiment_results/12_3_3_MVP.json)

**Incorporations from Prior Experiments:** Preprocess Text, DaVinci-003

##### **Baseline Hitrate:** 90%

**Parameters**:

```python
prompt_seq = ["Summarize the following conversation between you and me:",
              "Convert from third to first person:",
              "Convert from first person to second person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.7,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

After experimenting with a couple different permutations of pronouns it seemed that "me" and "you" instead of "bot" and "user" yeilded the best results. This made a marked improvement in the results of the summary as the removal of bot and user seemed to result in better pronouns present.

There were some minor issues in the summaries that did not meet expectations:

- Some summaries had a sentence contained an initial starting sentence saying something along the lines of "I'm having a conversation with you about smoking"

  > You were having a conversation with someone about their smoking habit. They discussed the things they liked and disliked about smoking and indicated that they would like to make a conscious choice to quit smoking. You discussed the potential impact of this change and the steps needed to make it, which they determined to be a matter of willpower.

  > You centered our conversation around the topic of smoking. You stated that you enjoyed the flavor and relaxation associated with smoking, but you were concerned about the health damage it caused. You wanted to reduce the number of cigarettes you smoked, believing that this would result in better health and odor. Finally, you acknowledged that making this change would require discipline.

  - These can easily be resolved by parsing the end result and if the first sentence contains the word "conversation" remove that sentence, we don't want to parse every sentences since in future sentences "conversation" may be used in a different context and should be kept

- Some summaries ended up using "they" instead of "you"

  > You were having a conversation with someone about their smoking habit. They discussed the things they liked and disliked about smoking and indicated that they would like to make a conscious choice to quit smoking. You discussed the potential impact of this change and the steps needed to make it, which they determined to be a matter of willpower.

  - It would be too dangerous to replace all occurances of "they" to "you" as it's likely "they" will be used many times in different contexts and replacing these would destroy the summary
  - However, looking at the improved summary outputs, the prompt "Convert from first person to second person:" at this point is just manually changing every "I" into "You", this can be done through hardcoding allowing us to both drop a prompt in the pipeline speeding things up and also ensuring all "I"s are properly converted into "You" and not "They"

  - Expected Result:

    ```json
    {"prompt": "Convert from third to first person:",
    "result": "I enjoy the feeling and physical act of smoking, but I dislike the smell. I don't want to make a change, but I do realize that it will require discipline and persistence. To make the change, I need to take steps to keep myself busy in other ways."},{
    "prompt": "Convert from first person to second person:",
    "result": "You enjoy the feeling and physical act of smoking, but you dislike the smell. You don't want to make a change, but you do realize that it will require discipline and persistence. To make the change, you need to take steps to keep yourself busy in other ways."}
    ```

  - Buggy Result:

    ```json
    {"prompt": "Convert from third to first person:",
    "result": "I was having a conversation with someone about my smoking habit. I 	   discussed the things I liked and disliked about smoking and indicated that I would like to make a conscious choice to quit smoking. We discussed the potential impact of this change and the steps needed to make it, which I determined to be a matter of willpower."},{
    "prompt": "Convert from first person to second person:",
    "result": "You were having a conversation with someone about their smoking habit. They discussed the things they liked and disliked about smoking and indicated that they would like to make a conscious choice to quit smoking. You discussed the potential impact of this change and the steps needed to make it, which they determined to be a matter of willpower."}
    ```

### Experiment 4 - Simplifying Prompt Sequence and Text Postprocess

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [12_3_4_MVP.json](../experiment_results/12_3_4_MVP.json)

**Incorporations from Prior Experiments:** Preprocess Text, DaVinci-003, Converting Texter Names

**Hitrate:** 100%

**Parameters**:

```python
prompt_seq = ["Summarize the following conversation between you and me:",
              "Convert from third to first person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.5,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

Added postprocessing steps:

- Code was added to check for whether the first sentence mentions "conversation":

  ```python
  if "conversation" in postprocessed_data[0:postprocessed_data.find(".")]:
      postprocessed_data = postprocessed_data[postprocessed_data.find(".")+2:]
  ```

- Code was also added to convert pronouns listed in the conversion dictionary:

  ```python
  conversion_dict = {"I":	"you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself", "am": "are", "the other individual": "me"}
  ```

This experiment also dropped temperature to `0.5` as a summarization task should not warrent such high temperatures. Using this new pipeline, the generated results were all considered to fit the criteria of "good enough" defined in the **Purpose** section.

One issue to note is that one summary was written in past tense which didn't make as much sense, but this should be something that is tackled after an MVP is settled upon

> From Result {1}
>
> You liked the feeling smoking gave you and the physical act of smoking, but you disliked the smell. You wanted to make a change in your smoking habit, but you realized that it would require discipline and persistence. To make the change, you knew you would need to keep yourself busy in other ways.

### Experiment 5 - Experimentation Via Single Prompt

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Incorporations from Prior Experiments:** Preprocess Text, DaVinci-003, Converting Texter Names

**Results File Name:** [12_4_1_MVP.json](../experiment_results/12_4_1_MVP.json)

**Hitrate:** 100%

**Parameters**:

```python
prompt_seq = ["Summarize this text message conversation between me and you in second person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.5,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

There is a motivation to see if it is possible to concatonate these prompts into one singular prompt. Not only will this make the GPT3 inference process faster, it will also cost less tokens to run. The results varied drastically based on the prompt. For instance "Summarize this text message conversation between me and you in the perspective of you:" yeilded a hitrate of 0% with completly unuseable summaries.

Playing around with the prompts let to the one used in this experiment that showed promise when tested with a smaller subset of the data. Running on the overall dataset gave great results with all summaries meeting the metrics set out in **Purpose**. Unlike **Experiment 4**, there were no issues with past or present tense.

A strong reminder for the power that is present in GPT3 that all the extra work and thought could be done in this singular prompt.

### Experiment 6 - Experimentation Via Single Prompt

**Data:** [cleaned_transcripts.txt](../data/cleaned_transcripts.txt)

**Incorporations from Prior Experiments:** Preprocess Text, DaVinci-003

**Results File Name:** [12_4_2_MVP.json](../experiment_results/12_4_2_MVP.json)

**Hitrate:** 95%

**Parameters**:

```python
prompt_seq = ["Summarize this text message conversation between me and you in second person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.5,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

Issue showed up where the Bot was referenced.

### Experiment 7 - Experimentation Via Single Prompt

**Data:** [transcripts.txt](../data/transcripts.txt)

**Incorporations from Prior Experiments:** DaVinci-003

**Results File Name:** [12_4_3_MVP.json](../experiment_results/12_4_3_MVP.json)

**Hitrate:** 50%

**Parameters**:

```python
prompt_seq = ["Summarize this text message conversation between me and you in second person:"]
openai.Completion.create(model="text-davinci-003",
                         prompt=f"{prompt}\n\n{data}\n",
                         temperature=0.5,
                         max_tokens=256,
                         top_p=1,
                         frequency_penalty=0,
                         presence_penalty=0)
```

Issues where the bot was referenced, surface level summarization, and nonsensicle sentences with incorrect pronoun usage were all present.

## Conclusion

It is clear that preprocessing the text helped remove noise and allow GPT3 to better focus on the important messages, in a way this was a form of extractive summarization. 

Additionally, it was evident that there exists cleaver postprocessing steps along with smarter prompt engineering that went a long way in improving the quality of the summaries. However, it was shown that GPT3 itself was sufficient in acting as an MVP with a single prompt after some experimentation without any need for postprocessing steps or a multiprompt setup. Preprocessing however did seemed to help as seen by **Experiment 6 and 7**.

## Next Steps

Now that an MVP has been designed there are three logical next steps in my opinion:

1. Continuing improving the quality of the summaries

   - This is of course the most obvious one and would entail adding a last sentence to see if the user would like to add anything, checking for righting reflexes and working on a resolution, and so on

2. Attempting to fine-tune a smaller model by using our current MVP to generate the training data

   - A more experimental idea which could yield some very interesting results
   - The inspiration here comes from *knowledge distilation* when a large model is trained and a smaller model is then trained by attempting to fit its layers onto the layers of the larger model in a 1 to $n$ manner
   - The implementation here would be different and wouldn't be actual *knowledge distilation*

3. Attempt the MVP on more sophisticated chat transcripts

   - We've previously discussed that the current chat transcripts are not the latest transcripts, with the new model having more sophistication
   - It would be worthwhile to see how well our MVP performs in this more complex environment

4. ###### If we want to ever go back to exploring a prompt pipeline, [ChatGPT](https://openai.com/blog/chatgpt/) could be a strong solution due to its abilitiy to infer on prior messages

```python
fauci_df.loc[(fauci_df["user"].isin(["realdonaldtrump", "antknowsmaui"]) & bool(set(fauci_df["user"]) & set(["realdonaldtrump", "antknowsmaui"])))].head(25)

```

