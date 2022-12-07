# Using GPT3 For Text Classification

**Context:** [This paper](https://arxiv.org/pdf/2103.12407.pdf) goes over the various ways we can use GPT3 for text classification through the context of "Is this text sexist" and lays the outline for how to write such classification request prompts.

## Curiosity

I wondered if GPT3 could give me a good definition of the righting reflex. To provide a clear definition we may look towards an article on Motivational Interview:

> The [‘righting reflex’](https://books.google.co.th/books?id=oFFNAgAAQBAJ&pg=PA43&dq=righting+reflex+motivational+interviewing+in+education&hl=en&sa=X&ved=2ahUKEwjPsYKGo97sAhUCXisKHUEwB60Q6AEwAXoECAYQAg#v=snippet&q=righting reflex&f=false) is the desire to ‘fix’ or offer advice/information when someone presents you with a problem which requires change to be made.

Unfortunately, when queried to GPT3 the results were dissapointing. 

> Prompt: Describe the righting reflex within the field of motivational interviewing? 
>
> GPT3 Response: The righting reflex is the motivational interviewing technique of reflecting back to the client their own words and experiences in order to help them see the connections between their thoughts, feelings, and behaviors. This technique allows the therapist to avoid judgment and to explore the client's innermost thoughts and feelings.

> Prompt: What is the righting reflex in talk therapy?
>
> GPT3 Response: There is no such thing as a righting reflex in talk therapy.

> Prompt: Explain what righting reflex means in motivational interviewing:
>
> GPR3 Response: The righting reflex is the innate tendency of humans to seek restoration of equilibrium following a disturbance. This can be seen as a self-regulatory mechanism that motivates individuals to return to a state of balance or emotional well-being.

Of course, even if GPT3 could provide an acceptable answer it would by no means be indication of understanding rather impressive regurgitation.

## Experiment #1: Zero Shot

The paper structured its queries like so:

> Is the following text sexist? Answer yes or no. 
>
> ‘Women belong in the kitchen' 
>
> Answer: 
>
> Yes (<- GPT3 Response)

### Attempt #1

Following this structure I tried a multitude of potential righting reflex classification prompts. The question was changed to "Is the following text applying the righting reflex? Answer yes or no.".

Running this on a manually created dataset of 16 statements with a 50/50 split between righting reflex statements and MI-style reflections.

**Query:** Is the following text  applying the righting reflex? Answer yes or no.

**Accuracy:** 43.8%

### Attempt #2

Considering that GPT3 does not understand what a "righting reflex" is, it may be beneficial to describe the righting reflex rather than name it outright. This seemed to be a step in the right direction.

**Query:** Is the following statement giving advice? Answer yes or no.

**Accuracy:** 62.5%

### Attempt #3

From the results of Attempt #2 the query is strong at identifying righting reflex statements but sometimes labels reflection statements as True/Yes. This may be a problem with the query as advice can come in the form of reflection and affirmation (ie. You believe that by making changes to your smoking habit, you will be able to improve your health and smell). What makes advice fall into the righting reflex trap is when it is largely instructive and commanding.

**Query:** Is the following statement commanding someone? Answer yes or no.

**Accuracy:** 75%

## Experiment #2: Few Shot

Within the reference paper Few Shot performed the best and did better than single shot. Additionally, since our non-righting-reflex statements are not just random general statements but have their own qualities (affirmation, reflective) then it makes sense to teach the model these properties. Thus we should show a mix of both categories. 

Running without instruction even on low temperature yeilded responses that were not classification (ie. "You", "I").

### Attempt #1

Since we needed to run with instruction, the natural instruction was the query from attempt #3 in experiment 1. 

Now that there was a "training" set that was exposed to GPT3, we needed to ensure the performance was not a statistical anomoly due to the sampling results. Cross validation was implemented to increase confidence. The training set contained one positive and one negative instance. 

**Results from Cross Validation:**  75%, 75%, 92% | Mean 81%

## Takeaways

GPT3 definitely shows promise as a classification of righting-reflex detection. Although this tool itself  does not by itself achieve the goal of MI style summarization, it may lend itself in a variety of ways.

1. By detecting righting-reflex sentences within a summarization, we can extract those sentences out and aim to iteratively resolve them within the pipeline
2. Using this to identify the number of righting-reflex sentences within a summary could be the start to adding some quantitative metrics that can be used to assess summarization success, allowing the comparison of various pipeline approaches