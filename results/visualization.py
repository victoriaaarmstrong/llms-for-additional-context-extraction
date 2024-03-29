import pandas as pd

########################
## Plots from Table 3 ##
########################

## Sentences pie chart
sentences = pd.DataFrame({'sentences': [16, 2]},
                  index=['One Sentence', 'Two Sentences'])
sentences_image = sentences.plot.pie(y='sentences', colors=['deepskyblue','tomato'], legend=True, labeldistance=None, autopct='%1.1f%%')
sentences_image.set_ylabel("")
sentences_image.figure.savefig('sentences.jpg', bbox_inches='tight')

## Reversed pie chart
reversed = pd.DataFrame({'reversed': [11, 7]},
                  index=['Yes', 'No'])
reversed_image = reversed.plot.pie(y='reversed', colors=['deepskyblue','tomato'], legend=True, labeldistance=None, autopct='%1.1f%%')
reversed_image.set_ylabel("")
reversed_image.figure.savefig('reversed.jpg', bbox_inches='tight')

## Single reversed pie chart
single_reversed = pd.DataFrame({'single-reversed': [6, 10]},
                  index=['Correctly Classified', 'Incorrectly Classified'])
single_reversed_image = single_reversed.plot.pie(y='single-reversed', colors=['deepskyblue','tomato'], legend=True, labeldistance=None, autopct='%1.1f%%')
single_reversed_image.set_ylabel("")
single_reversed_image.figure.savefig('single_reversed.jpg', bbox_inches='tight')

#######################
## Plots for Results ##
#######################

## read in the CSV with aggregate results
df = pd.read_csv('results.csv')

## get the total right for each domain
df['Unsuccessful'] = 50 - df['Successful']

## separate out all of the different domains
restaurant = df.loc[df['Domain'] == 'Restaurant']
hotel = df.loc[df['Domain'] == 'Hotel']
train = df.loc[df['Domain'] == 'Train']
restaurant_hotel = df.loc[df['Domain'] == 'Restaurant-Hotel']
restaurant_train = df.loc[df['Domain'] == 'Restaurant-Train']
hotel_train = df.loc[df['Domain'] == 'Hotel-Train']

## restaurant graph
restaurant_image = restaurant.plot.bar(x='X-Shot', stacked=True, title="Restaurant", color=['deepskyblue','tomato'])
restaurant_image.legend(loc='lower right')
restaurant_image.set_xlabel("")
restaurant_image.figure.savefig('restaurant_results.jpg', bbox_inches='tight')


## hotel graph
hotel_image = hotel.plot.bar(x='X-Shot', stacked=True, title="Hotel", color=['deepskyblue','tomato'])
hotel_image.legend(loc='lower right')
hotel_image.set_xlabel("")
hotel_image.figure.savefig('hotel_results.jpg', bbox_inches='tight')

## train graph
train_image = train.plot.bar(x='X-Shot', stacked=True, title="Train", color=['deepskyblue','tomato'])
train_image.legend(loc='lower right')
train_image.set_xlabel("")
train_image.figure.savefig('train_results.jpg', bbox_inches='tight')

## restaurant-hotel graph
restaurant_hotel_image = restaurant_hotel.plot.bar(x='X-Shot', stacked=True, title="Restaurant-Hotel", color=['deepskyblue','tomato'])
restaurant_hotel_image.legend(loc='lower right')
restaurant_hotel_image.set_xlabel("")
restaurant_hotel_image.figure.savefig('restaurant_hotel_results.jpg', bbox_inches='tight')

## restaurant-trian graph
restaurant_train_image = restaurant_train.plot.bar(x='X-Shot', stacked=True, title="Restaurant-Train", color=['deepskyblue','tomato'])
restaurant_train_image.legend(loc='lower right')
restaurant_train_image.set_xlabel("")
restaurant_train_image.figure.savefig('restaurant_train_results.jpg', bbox_inches='tight')

## hotel-train graph
hotel_train_image = hotel_train.plot.bar(x='X-Shot', stacked=True, title="Hotel-Train", color=['deepskyblue','tomato'])
hotel_train_image.legend(loc='lower right')
hotel_train_image.set_xlabel("")
hotel_train_image.figure.savefig('hotel_train_results.jpg', bbox_inches='tight')
"""
