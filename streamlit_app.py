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
