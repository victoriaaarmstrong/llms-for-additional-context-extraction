import pandas as pd
from create_prompts import *
from transformers import pipeline, set_seed
import openai
from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

## file we want to use
FILE = "single-filled.xlsx"

## amount of money we don't want to go over on any single run
LIMIT = 10.00

## price per token for different models input and output
FOUR_INPUT = 0.00003
FOUR_OUTPUT = 0.00006
THREE_FIVE_INPUT = 0.000001
THREE_FIVE_OUTPUT = 0.000002


def estimate_cost(text, price):
    """
    Estimates the number of tokens in a given chunk of text, and then calculates the total estimated cost of that text
    :param text:
    :return:
    """

    token_estimate = (text.count(" ") + 1)*(3/4)
    cost_estimate = token_estimate*price

    return cost_estimate


## read in the conversations
df = pd.read_excel(FILE)

## create a new df to save results in
results = pd.DataFrame(columns = ['Conversation', 'Main', 'Context', 'Zero-Output', 'One-Output', 'Few-Output'])

client = OpenAI()

## initialize the amount of money spent for each run
money_spent = 0.00

## iterate over each data point in the testing set
for i in range(len(df)):

    ## make sure we're sitll under our spend limit (it's not a hard max so if we go one pass over that's fine)
    if money_spent < LIMIT:

        print("Starting test point " + str(i) + "...")
        ## extract the conversation
        conversation = df.loc[i, 'Full-Text']

        ## put values into temporary df that gets appended to the results each time
        temp = pd.DataFrame(columns = ['Conversation', 'Main', 'Context', 'Zero-Output', 'One-Output', 'Few-Output'])
        temp.loc[0] = [conversation, df.loc[i, 'Main'], df.loc[i, 'Context'], "", "", ""]

        ## fill the three different prompts with the conversation
        zero, one, few = fill_primary_prompt(conversation)

        ## calculate and add on the input costs
        money_spent += (estimate_cost(zero, FOUR_INPUT) + estimate_cost(one, FOUR_INPUT) + estimate_cost(few, FOUR_INPUT))

        ## generate the output from the LLM
        zero_output = client.chat.completions.create(
          model="gpt-4",
          messages=[
            {
              "role": "user",
              "content": zero,
            }
          ],
          temperature=1,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        one_output = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": one,
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        few_output = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": few,
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        ## calculate and add on output costs
        money_spent += (estimate_cost(zero_output.choices[0].message.content, FOUR_OUTPUT) + estimate_cost(one_output.choices[0].message.content, FOUR_OUTPUT) + estimate_cost(few_output.choices[0].message.content, FOUR_OUTPUT))

        ## save to temporary df
        temp['Zero-Output'] = zero_output.choices[0].message.content
        temp['One-Output'] = one_output.choices[0].message.content
        temp['Few-Output'] = few_output.choices[0].message.content

        ## append temp df as a row to the results
        results = pd.concat([results, temp], ignore_index=True)
        #results = results.append(temp)
        print("Finishing test point " + str(i) + "...\n\n")

    else:
        ## reset the index to avoid funky key errors
        results = results.reset_index()

        ## save what's been collected of the results to an excel file
        results.to_excel('results-stopped-early.xlsx', index=False)

        print('exceeded desired spend limit, process terminated and data saved as is')
        exit(-1)


## reset the index to avoid funky key errors
results = results.reset_index()

## save the resuls to an excel file
results.to_excel('results.xlsx', index=False)
print('successfully generated results for all data points with estimated total spend: ' + str(money_spent))