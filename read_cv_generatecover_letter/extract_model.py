# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="openai-community/gpt2", tokenizer="gpt2")

prompt = "Who is the best football player in the world?"

result = pipe(prompt, max_length=100, num_return_sequences=1, do_sample=True)

print(result[0]['generated_text'])

pipe.save_pretrained("chatbotModel")