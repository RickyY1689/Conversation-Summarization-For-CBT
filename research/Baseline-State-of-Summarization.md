# Analysis of the Baseline Summarization

## Data

20 randomly sampled transcripts were taken from the MI Bot V5.1 document. The initial introduction of the Bot and it's purpose was removed such that the first message in each conversation was:

> BOT: To start, what is the thing you like most about smoking?

## Analysis of Results

## The Good

There are certainly instances where the current pipeline shows this endeavor's potential with multiple summarizations outputted that are done in the style of MI. It also preserves the reflections and affirmations that occur within the conversation.

> You like smoking because it gives you a buzz, but you dislike that it is bad for your health. You want to change your smoking habit by reducing the number of cigarettes you smoke gradually, and you believe that your life will improve by making this change. You will need to make a detailed plan with the exact number of cigarettes you are allowed to smoke each day.

> You are trying to quit smoking and the bot is asking you questions about it. You enjoy smoking, but don't like how expensive it is or how it makes you smell. You would like to change your smoking habit by smoking less and eventually quitting. To do this, you will need to reduce the amount of cigarettes you smoke each day.

## The Bad

There are a number of issues that exist within the results.

1. The output will sometimes take in the last parts of the conversation which is always the same and involves the Bot thanking the User. **This should be removed in a preprocessing step** in the future to avoid these issues.

   > You enjoy smoking because it makes you happy, but you don't like the smell of cigarettes on your clothes. You want to reduce your consumption of cigarettes. What do you need to do to reduce your consumption? You need to first reduce your consumption and then cut it out altogether. Thanks for the conversation.

2. Sometimes the output will reference the Bot and the User instead of I/You respectively, even though it may abide by the first person narrative voice. A potential resolution may involve **preprocessing the chat and replace Bot and User with I and You respectively**. This may "trick" the bot into ensuring the pronouncs are correct.

   > You are trying to quit smoking, and the bot is trying to help. You say that you like smoking because it fills the time, is a stress release, or is social. The bot says that you enjoy the fact that smoking helps you cope with stressful situations. You say that you dislike the health consequences of smoking. The bot says that you want to quit smoking completely. You say that you are not willing to put in the effort. The bot says that you need to find other ways to cope with your smoking habit.

3. In a number of cases, the summarization is very dense in nature. However, this may be an issue whereby rerunning the pipeline on the same input may yield different results. Since this issue occurs at the summarization level, **summary quality metrics could be run on the initial output and if it fails to meet a minimum threshold it is run again for some $n$ iterations**.

   > You are trying to quit smoking and the bot is helping by asking questions about why you want to quit and what your goals are.

   > You and I discuss the positives and negatives of smoking, with you ultimately expressing a desire to change your smoking habit due to the cost. I encourage this change and offer some advice on steps you can take to make it happen.

4. Cases of the righting-reflex although not as common as initially expected to pop up as well. **Righting-reflex classification may help with resolving this issue**.

   > You enjoy smoking because it makes you happy, but you don't like the smell of cigarettes on your clothes. You want to reduce your consumption of cigarettes. What do you need to do to reduce your consumption? You need to first reduce your consumption and then cut it out altogether. Thanks for the conversation.

General thoughts for improvement:

- Is there potential in taking an extractive summarizer to trim out the "fat" (ie.  "That's great to hear, thanks for letting me know!" type messages) and then running an abstractice summarization afterwards?
  - Can swap the extractive summarizer with classical preprocessing (go with this)
- Temperature should vary based on the prompt
  - The initial summarization may call for lower temperatures while the later prompts rearranging pronouns and POV may call for higher temperatures
- Is there any merit in evaluating against chat log datasets?
  - The domain difference may be too large to prove useful
    - Might be useful when it comes to finetuning?