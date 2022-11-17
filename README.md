# Conversation Summarization In the Style of Motivational Interviewing

## Context

This work is done as part of my [undergraduate thesis for the University of Toronto's Engineering Science program](https://engineering.calendar.utoronto.ca/course/esc499y1). My thesis proposal can be found [here]("Thesis-Proposal.pdf").

## Experiments Log

The following are all documented experiments so far with the end goal being the creation of a model capable of outputting human-like-speach summarizing a given text conversation in the style of [Motivational Inverviewing (MI)](https://motivationalinterviewing.org/understanding-motivational-interviewing) a branch of Cognative Behavioural Therapy (CBT).

### Baseline Results - Nov 7th

- **Hypothesis:** Can we chain together a sequence of zero-shot GPT3 models with different prompts to build a meaningful pipeline?

- **Take-Aways:** Summarizes well but correct use of pronouns ("I" vs "You") are hit or miss and introduces varies instances of "righting reflex" or "expert trap" type comments.
- Results can be viewed [here](./experiment_results/baseline_pipeline_summarization.md)





