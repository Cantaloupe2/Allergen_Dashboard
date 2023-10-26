import pandas as pd
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("MSU-Culinary Visualizations")

print('streamlit file')
diet_data = pd.read_csv('diet_data_no_names.csv')

# create a list of the "Date \nContacted" column in diet_data and name it dates
dates = diet_data['Date \nContacted']
diet_data['dates'] =dates = diet_data['Date \nContacted']

# print type of dates
print(type(dates[0]))
dates[0][-2:]
# remove NaN values from dates
dates = [date for date in dates if type(date) == str]

# # take the last 2 digits of each element in dates and name it years
years = [date[-2:] for date in dates]
yearsdf = pd.DataFrame(years)
# plot a histogram of years
import matplotlib.pyplot as plt
plt.hist(years)
# make apropriate labels
plt.xlabel('year')
plt.ylabel('frequency')
plt.title('year of contact')
plt.show()
st.pyplot()
st.write(yearsdf.value_counts().sort_index())
#st.bar_chart(yearsdf.value_counts())




#########

import pandas as pd

df = pd.read_csv('diet_data_no_names.csv')
sdf=df.drop(['Major','RCPD','Other','Notes','Dining Accommodation',
             'Specialist','Intial Concern','Hall (Living/Eating)',
             'Class Type','Date \nContacted'], axis=1)

cdf=sdf.dropna(how='all')
cdf

ndf = cdf.fillna(0)

columns_to_convert = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
                      'Vegetarian','Halal','Kosher']

for col in columns_to_convert:
    ndf[col] = ndf[col].replace('x', 1)
    
matrix = ndf.corr()
print(matrix)

from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="white")

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(matrix, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 11))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(matrix, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
st.pyplot()
