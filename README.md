# Claude-Function-Calling
Easy way to use reliable function calling with Claude 2.1

## Description
This repository contains an approach to extend Claude 2.1's capabilities by integrating custom function calling within the conversational flow. By leveraging the Anthropic API, we showcase how to dynamically invoke predefined Python functions — such as addition and subtraction — directly from within Claude's responses.

## How to use
1. Clone the repository locally.
2. `pip install anthropic`
3. Replace the `API_KEY` in `function-calling.py` with your own API key.
4. Run `python function-calling.py` to start. 

## Example
```
User: I have 100 apples. I then sell 10 apples. I called my supplier, and they sent me a shipment of 20 apples. How many apples do I have at the end?

Assistant:
<scratchpad>
Original number of apples: 100
Number of apples sold: 10  
Number of apples shipped: 20

To calculate the final number of apples, I need to:
1) Subtract the number of apples sold (10) from the original number (100) 
2) Add the number of apples shipped (20)
</scratchpad>

<subtraction>100, 10
subtraction
Calling subtraction! 100 10 90
<scratchpad>
Original number of apples: 100
Number of apples sold: 10  
Number of apples shipped: 20

To calculate the final number of apples, I need to:
1) Subtract the number of apples sold (10) from the original number (100) 
2) Add the number of apples shipped (20)
</scratchpad>

<subtraction>100, 10</subtraction><function_result>90</function_result
>
<addition>90, 20
addition
Calling addition! 90 20 110
<scratchpad>
Original number of apples: 100
Number of apples sold: 10  
Number of apples shipped: 20

To calculate the final number of apples, I need to:
1) Subtract the number of apples sold (10) from the original number (100) 
2) Add the number of apples shipped (20)
</scratchpad>

<subtraction>100, 10</subtraction><function_result>90</function_result>
<addition>90, 20</addition><function_result>110</function_result
>

<answer>110</answer>
---
110
```