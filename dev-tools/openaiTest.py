# Author: Jeff Schloemer
# Date: 12/28/2022

import openai
import os

key = os.getenv("OPENAI_API_KEY")
useopenai = ""
if (key is None):
    useopenai = False
    print("No OPENAI API Key Found - All external queries will be stopped")
else:    
    openai.api_key = key
    useopenai = True
    
if (useopenai):
    init="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with Unknown.\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: "
    prompt="What are uses for AI in satellites?"
    fin = "\nA:"
    total = init + prompt + fin
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=total,
                temperature=0,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\n"]
            )
    print(response)
    print(response['choices'][0]['text'])
