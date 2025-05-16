from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="write a code to print fiboncaci sequence in python",
    config=types.GenerateContentConfig(
        system_instruction="You are a code generation AI assistant. You will be given instructions, you will generate the code in the best and optimal way. Validity and correctness of the code is most important. Then you will be given the response to the code, and you shall correct the code if needed to generate the correct output. Only output the code. The code needs to be able to be plugged in and run without any changes. Do not include any extra information that might break the code -- example: example usage, description, etc."
    )
)
print(response.text)
