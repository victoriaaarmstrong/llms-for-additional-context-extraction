import pandas as pd
import json
import random

## play with this variable to generate more instances of the same template
NUM = 5

## read in the templates
df = pd.read_excel("single-domain-master.xlsx")
df = df.dropna()

## make a new DataFrame to hold the filled templates
filled_data = pd.DataFrame(columns = ['Domain', 'Path', 'Question', 'Template', 'Value1-Type', 'Value2-Type', 'Main', 'Context', 'Number-Sentences', 'Reverse', 'Full-Text', 'Value1', 'Value2'])

## for every template
for i in range(len(df)):

    num_selected = 0

    ## open the correct json file for this template
    with open(df.loc[i, 'Path'], 'r') as f:
        vals = json.load(f)

    ## use this template NUM times depending on how many variations you want.
    while num_selected < NUM:
        ## copy the row
        temp = df.loc[i].copy(deep=True)

        ## check that you actually have a Value1
        if df.loc[i,'Value1-Type'] != "N":

            ## get the value options to fill from and randomly select one
            value1_list = vals[df.loc[i, 'Value1-Type']]
            v1 = random.choice(value1_list)

            ## replace value1 with the selected value
            temp['Template'] = temp['Template'].replace('value1', v1)
            temp['Main'] = temp['Main'].replace('value1', v1)
            temp['Context'] = temp['Context'].replace('value1', v1)


        ## check that you actually have a Value 2
        if df.loc[i, 'Value2-Type'] != "N":

            ## get the value option sto fill from and randomly select one
            value2_list = vals[df.loc[i, 'Value2-Type']]
            v2 = random.choice(value2_list)

            ## replace value2 with the selected value
            temp['Template'] = temp['Template'].replace('value2', v2)
            temp['Main'] = temp['Main'].replace('value2', v2)
            temp['Context'] = temp['Context'].replace('value2', v2)

        ## generate and append the Q&A pair
        text = "Agent: " + temp['Question'] + "\nUser: " + temp['Template']

        ## add on the new generated data to the row
        temp['Full-Text'] = text
        temp['Value1'] = v1
        temp['Value2'] = v2

        ## add to storage df
        filled_data = filled_data.append(temp)

        num_selected += 1

## reset the index to avoid funky key errors
filled_data = filled_data.reset_index()


## need to return the list? save somewhere?
filled_data.to_excel('single-filled.xlsx', index=False)
