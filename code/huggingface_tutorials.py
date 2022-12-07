from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

# Chosing a model from the model hub
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Generating Text
generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)
print(generator("Three Rings for the Elven-kings under the sky, Seven for the Dwarf-lords in their halls of stone", 
                max_length=30,
                num_return_sequences=2))

# Mask filling
unmasker = pipeline(task="fill-mask")
unmasker("This course will teach you all about <mask> models.", top_k=2)