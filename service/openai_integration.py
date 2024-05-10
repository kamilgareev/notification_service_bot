import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI


def get_parsed_user_message(user_message):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    system_message = ("You are an assistant that converts user message into the following format: \
                          {'text': (what a user asks to notify about),\
                          'time': (when a user asks to notify them, provide the notification\
                           time in 'YYYY-MM-DD HH:MM:SS' format, as current date and time use %s),\
                          'time_seconds': (provide the notification time period in seconds; the 'seconds' value should\
                           be an integer))}"
                      % datetime.now(tz=timezone.utc))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_message}],
    )
    return eval(completion.choices[0].message.content)
