import os
from dotenv import load_dotenv
from google import genai
import re
import ast
import json

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)


def generate_prompt(user_request, retrieved_cocktails, user_preferenses=None):
    prompt = (f"The user entered the following query: {user_request}. "
              f"The database contains information about such cocktails and information about them: {retrieved_cocktails}"
              f"Based on this data, display the answer to the user's request.")
    return prompt


def get_gemini_response(prompt):
    response = GEMINI_CLIENT.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response


def check_filters(user_query):
    prompt = f"""
        Extract filters from the following cocktail request. If the user does not directly say something, do not apply 
        the corresponding filter, but leave None.
        Respond in JSON with keys: alcoholic (true, false, None), glassType ('Cocktail glass', 'Collins glass', 
        'Highball glass', 'Whiskey sour glass', 'Shot glass', 'Coffee mug', 'Martini Glass', 'Old-fashioned glass',
         'Champagne flute', 'Irish coffee cup', 'Beer mug', 'Margarita glass', 'Mason jar', 'Balloon Glass', 
         'Punch bowl', or None), category ('Cocktail', 'Shot', 'Ordinary Drink','Other / Unknown', 'Coffee / Tea', 
         'Beer', 'Punch / Party Drink', 'Shake', 'Cocoa' or None).
         If there is more than one parameter (for example, several types of glasses), submit them in the python list 
         format, for example [Shot glass, Beer mug]

        Query: "{user_query}"
        """
    response = get_gemini_response(prompt)
    match = re.search(r"\{.*\}", response.text, re.DOTALL)
    if match:
        json_str = match.group(0)
        data = json.loads(json_str)
        print(data)
    else:
        print("JSON not found")
    print(response.text)
    return data
