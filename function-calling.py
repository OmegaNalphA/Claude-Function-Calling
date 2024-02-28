ANTHROPIC_API_KEY = "YOUR_API_KEY"

from anthropic import Anthropic
import re
from typing import List, Dict

client = Anthropic(api_key=ANTHROPIC_API_KEY)


# Define a few functions
def addition(a: int, b: int):
    print("Calling addition!", a, b, a + b)
    return a + b


def subtraction(a: int, b: int):
    print("Calling subtraction!", a, b, a - b)
    return a - b


# Define the user's question
USER_PROMPT = "I have 100 apples. I then sell 10 apples. I called my supplier, and they sent me a shipment of 20 apples. How many apples do I have at the end?"


# Function Descriptions
ADDITION_FUNCTION_DESCRIPTION = """
You have access to the "addition" function. This function takes two integers and adds them together, then returns the result.
You can call this function any time by writing <addition>{{FIRST_NUMBER}}, {{SECOND_NUMBER}}</addition>. This will trigger a calculator that will return the mathematical result.

Below is an example:

Human: What is 101 + 202?

Assistant: <addition>101, 202</addition><function_result>303</function_result>
"""

SUBTRACTION_FUNCTION_DESCRIPTION = """
You have access to the "subtraction" function. This function takes two integers and subtracts the second number from the first, then returns the result.
You can call this function any time by writing <subtraction>{{FIRST_NUMBER}}, {{SECOND_NUMBER}}</addition>. This will trigger a calculator that will return the mathematical result.

Below is an example:

Human: What is 101 - 202?

Assistant: <subtraction>101, 202</subtraction><function_result>-101</function_result>
"""

# Register the functions in your function template
FULL_PROMPT = f"""
You are a capable calculating assistant. Your clients will be asking you questions about calculations they need assistance with. Right now, the client has a query: "{USER_PROMPT}"
If you are uncertain about how to answer the question, simply say you do not know.

You have access to a few functions to help you do these calculations. Read through these functions, and think through which ones you would use to solve the client's query.
<functions>
{ADDITION_FUNCTION_DESCRIPTION}
---
{SUBTRACTION_FUNCTION_DESCRIPTION}
</functions

Think through the problem step by step.
First, analyze the functions above, and rationalize what functions would be relevant to the query.
Then, use a scratchpad and write out what functions would be relevant and how you would use them in <scratchpad> tags.
Finally, output your answer and put it in an <answer> tag. An example is below:

<example>
Human: What is 101 + 202 - 3?

Assistant: <addition>101, 202</addition><function_result>303</function_result><subtraction>303, 3</subtraction><function_result>300</function_result><answer>300</answer>
</example>

Now, answer the user's query: {USER_PROMPT}
"""

FUNCTION_DICT = {"addition": addition, "subtraction": subtraction}


# Define a function to call Claude and set up the stop sequences
def query(message_history: List[Dict[str, str]]) -> str:
    assistant_content = ""
    while True:
        message = client.messages.create(
            max_tokens=1024,
            model="claude-2.1",
            messages=message_history
            + [{"role": "assistant", "content": assistant_content}],
            stop_sequences=["</addition>", "</subtraction>"],
            temperature=0,
        )
        curr_content = message.content[0].text
        print(assistant_content)
        print(curr_content)

        if message.stop_reason == "stop_sequence":
            stop_sequence = ""
            stop_sequence_find = re.search(r"</(.*?)>", message.stop_sequence)
            if stop_sequence_find:
                stop_sequence = stop_sequence_find.group(1)
            else:
                return "Unknown stop sequence, stopping"
            if stop_sequence in FUNCTION_DICT:
                print(stop_sequence)
                latest_function = curr_content[curr_content.rfind(stop_sequence) :]
                numbers = re.findall(r"\-?\d+", latest_function)
                if len(numbers) == 2:
                    result = FUNCTION_DICT[stop_sequence](
                        int(numbers[0]), int(numbers[1])
                    )
                    assistant_content += (
                        curr_content
                        + f"</{stop_sequence}><function_result>{result}</function_result>"
                    )
        elif message.stop_reason == "end_turn":
            assistant_content += curr_content
            return assistant_content
        else:
            return "Unknown error, stopping"


# Call Claude
message_history = [{"role": "user", "content": FULL_PROMPT}]

assistant_response = query(message_history)

answer = re.search(r"<answer>(.*?)</answer>", assistant_response, re.DOTALL)
if answer:
    print("---")
    print(answer.group(1))
else:
    print("No answer provided")
