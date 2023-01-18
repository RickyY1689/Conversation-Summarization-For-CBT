# Brief Temperature Experiment

## Motivation

In [Designing-An-MVP.md](Designing-An-MVP.md), Experiment 4 changed the model temperature without proper documented experimentation. This brief experiment aims to rectify this and study the effects of temperature starting with Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]. The hope is to find results that help justify the decision to drop the temperature 

## Temperature Variation Experiments

### Temperature 0.1

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.1.json](../experiment_results/1_10_1_temp_0.1.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 45%

> You were having a conversation with someone about their smoking habit. You enjoy combining smoking and cannabis, but you are aware of the health implications. You would like to change the amount you smoke and you believe that by doing so, you can improve your overall health. To make this change, you plan to slowly reduce the amount of cigarettes you smoke daily.
>
> You discussed your likes and dislikes about smoking with another person, and the changes you wanted to make. You wanted to reduce your smoking gradually and quit altogether, believing that it would improve your life. To do this, you need to create a detailed plan with an exact number of cigarettes you are allowed to smoke each day.

Large amounts of the results struggled with either ambiguous naming (ie. "someone", "a person", "myself", "them") and contained phrases such as "you were/are having a conversation". There were also tense issues present.

### Temperature 0.2

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.2.json](../experiment_results/1_10_1_temp_0.2.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 55%

Issues with wrong tenses were gone however still many cases of ambiguous naming.

### Temperature 0.3

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.3.json](../experiment_results/1_10_1_temp_0.3.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 60%

Cases here continued to struggle with ambiguous naming and mentions of "conversations".

### Temperature 0.4

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.4.json](../experiment_results/1_10_1_temp_0.4.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 85%

Ambiguous naming seemed to all be resolved, issues pertaining the mention of "conversations" remained.

### Temperature 0.5

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.5.json](../experiment_results/1_10_1_temp_0.5.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 85%

Results similar to temperature 0.4

### Temperature 0.6

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.6.json](../experiment_results/1_10_1_temp_0.6.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 80%

Results similar to temperature 0.4

### Temperature 0.7

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.7.json](../experiment_results/1_10_1_temp_0.7.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 85%

Results similar to temperature 0.4

### Temperature 0.8

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.8.json](../experiment_results/1_10_1_temp_0.8.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 85%

Results similar to temperature 0.4

### Temperature 0.9

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_0.9.json](../experiment_results/1_10_1_temp_0.9.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 95%

Results similar to temperature 0.4, only one mention of "conversation" that did not make contextual sense.

### Temperature 1

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_temp_1.0.json](../experiment_results/1_10_1_temp_1.0.json)

**Parameters:** Experiment 3 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:** 80%

Results similar to temperature 0.4

### Analysis of Results

In general it seemed that temperatures greater than 0.3 resulted in desirable results with higher temperatures containing seemingly more creative and better articulated sentences but also seemed to contain more "righting-reflex" type sentences. However these observations remain loose as they were adjacent to the main objective when reviewing the results.

## Temperature Consistency Experiments

**Data:** [renamed_cleaned_transcripts.txt](../data/renamed_cleaned_transcripts.txt)

**Results File Name:** [1_10_1_MVP_0.json](../experiment_results/1_10_1_MVP_0.json), [1_10_1_MVP_1.json](../experiment_results/1_10_1_MVP_1.json), [1_10_1_MVP_2.json](../experiment_results/1_10_1_MVP_2.json), [1_10_1_MVP_3.json](../experiment_results/1_10_1_MVP_3.json), [1_10_1_MVP_4.json](../experiment_results/1_10_1_MVP_4.json)

**Parameters:** Experiment 5 from [Designing-An-MVP.md][Dsigning-An-MVP.md]

**Hitrate:**  100%, 95%, 100%, 100%, 100%

### Analysis of Results

To ensure this temperature experiment has been reliable the consistency of a given temperature should be tested. To save time and cost testing was done on a a single temperature value (0.5) and indicates the results to be highly consistent however did differ between runs with the summaries for each transcript never being exactly the same.

## Conclusion

While there seems to be some uncertainty regarding which temperature value to use between [0.4, 1] due to the similar levels of performance it seems to justify that running with either 0.5 or 0.7 for a MVP is acceptable.

[Dsigning-An-MVP.md]: 