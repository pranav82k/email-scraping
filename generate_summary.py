# To generate a summary of the extracted information, you can use NLP tools like GPT or spaCy. Here's an example of
# how to generate a summary using GPT-2:

from dotenv import load_dotenv
import os
import openai

# Load the variables from the .env file
load_dotenv()

# Pass the API key from environment
openai.api_key = os.getenv('OPEN_API_KEY')


def generate_summary(text):
    prompt = f"Please summarize the following text:\n{text}\n\nSummary:"
    response = openai.Completion.create(
        # engine="text-davinci-002",
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # return response
    summary = response.choices[0].text.strip()
    return summary
