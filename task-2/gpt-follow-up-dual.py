import pandas as pd
from create_prompts import *
from transformers import pipeline, set_seed
import openai
from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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
df = pd.read_excel("missing-dual-prompt.xlsx")

## create a new df to save results in
results = pd.DataFrame(columns = ['Domain-1', 'Domain-2', 'Output', 'Variable-Assignment'])

client = OpenAI()

## initialize the amount of money spent for each run
money_spent = 0.00

## iterate over each data point in the testing set
for i in range(len(df)):

    ## make sure we're sitll under our spend limit (it's not a hard max so if we go one pass over that's fine)
    if money_spent < LIMIT:

        print("Starting test point " + str(i) + "...")
        ## extract the conversation
        domain_1 = df.loc[i, 'Domain-1']
        domain_2 = df.loc[i, 'Domain-2']
        output = df.loc[i, 'Output']

        ## put values into temporary df that gets appended to the results each time
        temp = pd.DataFrame(columns = ['Domain-1', 'Domain-2', 'Output', 'Variable-Assignment'])
        temp.loc[0] = [df.loc[i, 'Domain-1'], df.loc[i, 'Domain-2'], df.loc[i, 'Output'], ""]

        ## fill the three different prompts with the conversation
        prompt = fill_secondary_prompt_dual(domain_1, domain_2, output)
        print(prompt)

        ## calculate and add on the input costs
        money_spent += estimate_cost(prompt, FOUR_INPUT) #+ estimate_cost(one, THREE_FIVE_INPUT) + estimate_cost(few, THREE_FIVE_INPUT))

        ## generate the output from the LLM
        result = client.chat.completions.create(
          model="gpt-4",
          messages=[
            {
              "role": "user",
              "content": prompt,
            }
          ],
          temperature=1,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )


        ## calculate and add on output costs
        money_spent += estimate_cost(result.choices[0].message.content, FOUR_OUTPUT) #+ estimate_cost(one_output.choices[0].message.content, THREE_FIVE_OUTPUT) + estimate_cost(few_output.choices[0].message.content, THREE_FIVE_OUTPUT))

        ## save to temporary df
        temp['Variable-Assignment'] = result.choices[0].message.content

        ## append temp df as a row to the results
        results = pd.concat([results, temp], ignore_index=True)

        #results = results.append(temp)
        print("Finishing test point " + str(i) + "...\n\n")

    else:
        ## reset the index to avoid funky key errors
        results = results.reset_index()

        ## save what's been collected of the results to an excel file
        results.to_excel('gpt-missing-dual-follow-up-stopped-early.xlsx', index=False)

        print('exceeded desired spend limit, process terminated and data saved as is')
        exit(-1)


## reset the index to avoid funky key errors
results = results.reset_index()

## save the resuls to an excel file
results.to_excel('gpt-missing-dual-follow-up-results.xlsx', index=False)
print('successfully generated results for all data points with estimated total spend: ' + str(money_spent))