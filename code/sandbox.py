# Trash code that is purely for testing and prototyping

import os
import openai

with open('openai_key.txt') as f:
    openai.api_key = f.read()

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Write a reply from the perspective of the therapist summarizing the conversation so far. Focus on the client's feelings and experiences, and show that you understand and accept what they're going through. Summarize what the client said in a way that acknowledges their emotions and perspective. Encourage the client to think about the reasons they want to change, and summarize these reasons in a way that's clear and easy to understand. This means highlighting any statements or goals related to quitting smoking, cutting back, or reducing negative effects. End with an open-ended question that encourages the client to think more about their commitment to change by asking a question that doesn't have a simple yes or no answer, and that invites the client to reflect on what they've shared. The conversation is as follows:\n\nTherapist: To start, what is the thing you like most about smoking?\nClient: I like the feeling I get from it of course, and also, I enjoy the physical act.\nTherapist: You enjoy the fact that smoking makes you feel calm and relaxed.\nTherapist: Did that make sense?\nClient: Yes\nTherapist: Now, what is the thing you like least about smoking?\nClient: The smell\nTherapist: You dislike the smell of cigarettes.\nTherapist: Did what I said make sense to you?\nClient: yes\nTherapist: Now, what is one thing about your smoking habit that you would like to change?\nClient: Nothing actually\nTherapist: You want to quit smoking completely.\nTherapist: Did that make sense?\nClient: no\nTherapist: What will it look like when you have made this change in your smoking habit?\nClient: I don't want to make a change.\nTherapist: You realize that making the change will require discipline and persistence.\nTherapist: Does this make sense to you?\nClient: yes\nTherapist: Finally, what are the steps you need to take to make this change?\nClient: Well, if I wanted to smoke less, I suppose I would possibly try to keep myself busy in other ways\nTherapist: You realize that it is not just a matter of smoking less, but also of staying busy in other ways.\nTherapist: Did that make sense?\nClient: yes\n\nIt sounds like the thought of changing your smoking habit brings up mixed feelings for you. You enjoy the feeling of calm and relaxation that smoking gives you, but you don't like the smell. You recognize that it will require discipline and persistence to make a change, but it is not something you are currently interested in doing. You are considering ways to keep yourself busy as an alternative to smoking. It sounds like you have thought through the pros and cons of changing, and have come to a decision that you are not ready to make a change right now. What would motivate you to make the change in the future?",
  temperature=0.7,
  max_tokens=900,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)