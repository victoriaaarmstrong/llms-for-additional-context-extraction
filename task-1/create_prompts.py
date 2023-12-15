

# from * import prompt_list
# or you could just store all the final prompts here? probably easier? then you can just import this whole file into main

FIRST_PROMPT_TEMPLATES = ["You will be given a conversation between a User and an Agent. The Agent will ask a direct question and the User answers the question. The User may also add extra context that wasn't asked of them, or they may not. Your task is to identify the Main Information and the Additional Context. These must be direct quotes from the conversation and have no additional text added. If there is no Additional Context found, you can label the additional context as 'None'.\n\nYour answer should look like\n\nMain Information: ...\nAdditional Context ...\n\nYour conversation is:\n\nplace_holder",
                        "You will be given a conversation between a User and an Agent. The Agent will ask a direct question and the User answers the question. The User may also add extra context that wasn't asked of them, or they may not. Your task is to identify the Main Information and the Additional Context. These must be direct quotes from the conversation and have no additional text added. If there is no Additional Context found, you can label the additional context as 'None'. One example is provided below.\n\nEXAMPLE 1\n\tAgent: How much money would you like to deposit?\n\tUser: I need to deposit $100 and I'd also like to pay off my credit card bill.\n\tMain Information: I need to deposit $100\n\tAdditional Context: I'd also like to pay off my credit card bill.\n\nYour conversation is: \n\nplace_holder",
                        "You will be given a conversation between a User and an Agent. The Agent will ask a direct question and the User answers the question. The User may also add extra context that wasn't asked of them, or they may not. Your task is to identify the Main Information and the Additional Context. These must be direct quotes from the conversation and have no additional text added. If there is no Additional Context found, you can label the additional context as 'None'. Three examples are provided below.\n\nEXAMPLE 1\n\tAgent: How much money would you like to deposit?\n\tUser: I need to deposit $100 and I'd also like to pay off my credit card bill.\n\n\tMain Information: I need to deposit $100\n\tAdditional Context: I'd also like to pay off my credit card bill.\n\nEXAMPLE 2\n\tAgent: What type of bank account would you like to open?\n\tUser: I just retired, so I think it'd be best to open a savings account.\n\n\tMain Information: it'd be best to open a savings account.\n\tAdditional Context: I just retired\n\nEXAMPLE 3\n\tAgent: Who would you like to authorize on your account?\n\tUser: I'd like to authorize my husband. He'll also need to open a new savings account.\n\n\tMain Information: I'd like to authorize my husband.\n\tAdditional Context: He'll also need to open a new savings account.\n\nYour conversation is:\n\nplace_holder"]

FOLLOW_UP_PROMPT = "Now that you have identified the Main Information and Additional Context, you must assign each of the main information and the additional context to a named variable below.\n\nvariable_place_holder\n\nTo recall, you identified:\n\noutput_place_holder"

VARIABLES = ['hotel-book-day\nhotel-people\nhotel-stay\nhotel-area\nhotel-name\nhotel-pricerange\nhotel-stars\n',
                  'restaurant_people\nrestaurant_day\nrestaurant_food_types\nrestaurant_names\nrestaurant_booking_time\n',
                  'train-people\ntrain-arriveBy\ntrain-day\ntrain-departure\ntrain-destination\ntrain-leaveAt\n']

def fill_primary_prompt(conversation):
    ## make sure that x_shot is 0 for 0 shot, 1 for 1 shot and 2 for few show and then you can just get the slectect prompt by selecting the right list indices.
    zero = FIRST_PROMPT_TEMPLATES[0].replace('place_holder', conversation)
    one = FIRST_PROMPT_TEMPLATES[1].replace('place_holder', conversation)
    few = FIRST_PROMPT_TEMPLATES[2].replace('place_holder', conversation)

    return zero, one, few

def fill_secondary_prompt(domain, output):

    if domain == 'Hotel':
        variable = VARIABLES[0]
    elif domain == 'Restaurant':
        variable = VARIABLES[1]
    elif domain == 'Train':
        variable = VARIABLES[2]
    else:
        print('You have entered an unsupported domain type.')
        return

    prompt = FOLLOW_UP_PROMPT.replace('variable_place_holder', variable)
    prompt = prompt.replace('output_place_holder', output)

    return prompt

def fill_secondary_prompt_dual(domain_1, domain_2, output):

    variable = ""
    if domain_1 == 'Hotel':
        variable += VARIABLES[0]
    elif domain_1 == 'Restaurant':
        variable += VARIABLES[1]
    elif domain_1 == 'Train':
        variable += VARIABLES[2]
    else:
        print('You have entered an unsupported domain type.')
        return

    if domain_2 == 'Hotel':
        variable += VARIABLES[0]
    elif domain_2 == 'Restaurant':
        variable += VARIABLES[1]
    elif domain_2 == 'Train':
        variable += VARIABLES[2]
    else:
        print('You have entered an unsupported domain type.')
        return

    prompt = FOLLOW_UP_PROMPT.replace('variable_place_holder', variable)
    prompt = prompt.replace('output_place_holder', output)

    return prompt

#print(fill_secondary_prompt('Hotel', 'Train', 'This is your variable list: variable_place_holder \n and this is your output: output_place_holder'))