import pandas as pd
import streamlit as st
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
import plotly.express as px

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("MSU-Culinary Visualizations")

add_sidebar = st.sidebar.selectbox("Page",("1","2"))

print('streamlit file')
diet_data = pd.read_csv('diet_data_no_names.csv')

# create a list of the "Date \nContacted" column in diet_data and name it dates
dates = diet_data['Date \nContacted']
diet_data['dates'] =dates

if add_sidebar == "1":

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
  #st.write(yearsdf.value_counts().sort_index())
  #st.bar_chart(yearsdf.value_counts())




  #########
  
  
  # df = pd.read_csv('diet_data_no_names.csv')
  # sdf=df.drop(['Major','RCPD','Other','Notes','Dining Accommodation',
  #             'Specialist','Intial Concern','Hall (Living/Eating)',
  #             'Class Type','Date \nContacted'], axis=1)
  
  #cdf=sdf.dropna(how='all')
  #cdf
  
  #ndf = cdf.fillna(0)
  
  #columns_to_convert = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
  #                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
  #                      'Vegetarian','Halal','Kosher']

  #for col in columns_to_convert:
  #    ndf[col] = ndf[col].replace('x', 1)
      
  #matrix = ndf.corr()
  #print(matrix)

  #################################################

df = diet_data
sdf=df.drop(['Major','RCPD','Other','Notes','Dining Accommodation',
             'Specialist','Intial Concern','Hall (Living/Eating)',
             'Class Type','dates', 'Date \nContacted'], axis=1)
cdf=sdf.dropna(how='all')

ndf = cdf.fillna(0)
columns_to_convert = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
                      'Vegetarian','Halal','Kosher']

for col in columns_to_convert:
    ndf[col] = ndf[col].replace('x', 1)
    ndf[col] = ndf[col].replace(' ',0)
matrix = ndf.corr()
matrix = px.matrix.medals_wide(indexed=True)
st.write(matrix)

#######
  
  

sns.set_theme(style="white")

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(matrix, dtype=bool))

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(11, 11))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
fig = px.imshow(matrix)

#st.pyplot(plot.get_figure())

if add_sidebar == "2":
  col1, col2 = st.columns([1,2])
  with col1:
    allergen = "Peanuts"
    average_allergies = 2.5
    hall = "Landon"
    st.write(f"Most Common Alergen: **{allergen}**")
    st.write(f"Most Correlated Alergens: **{allergen}** and **{allergen}**")
    st.write(f"Students list an average of **{average_allergies}** allergies.")
    st.write(f"Correlation matrix indicates **{hall}** may have an abnormally high number of **{allergen}** allergies")
  with col2:
    st.plotly_chart(fig)
  #with col3:
  #  st.write("123456")
