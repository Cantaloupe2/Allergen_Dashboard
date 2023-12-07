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
st.title("Allergen Data Dashboard")

add_sidebar = st.sidebar.selectbox("Page",("1","2"))

print('streamlit file')
diet_data = pd.read_csv('diet_data_no_names.csv')

# create a list of the "Date \nContacted" column in diet_data and name it dates
dates = diet_data['Date \nContacted']
diet_data['dates'] =dates


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

#######################################################
  
  

sns.set_theme(style="white")

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(matrix, dtype=bool))

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(11, 11))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
fig = px.imshow(matrix,text_auto=True)

# find most common value
allergen_max = ndf.sum().idxmax()
second_most_df = ndf.sum()
second_most_df[allergen_max]=0
allergen_max2 = second_most_df.sum().idxmax()

# find most correlated values
sol = (matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(bool))
                  .stack()
                  .sort_values(ascending=False))
for index, value in sol.items():
  allergen1 = index[0]
  allergen2 = index[1]
  break

#######################################################
col1, col2 = st.columns([1,2])
with col1:
  allergen = "Peanuts"
  average_allergies = 2.5
  hall = "Landon"
  st.subheader(f"Response Summary")
  st.write(f"Most Common Dietary Issue: **{allergen_max}**")
  st.write(f"Second Most Common Dietary Issue: **{allergen_max2}**")
  st.write(f"Most Correlated Dietary Issues: **{allergen1}** and **{allergen2}**")
  st.write(f"Students list an average of **{average_allergies}** allergies.")
  st.write(f"Correlation matrix indicates **{hall}** may have an abnormally high number of **{allergen}** allergies")
with col2:
  st.plotly_chart(fig)
#with col3:
#  st.write("123456")
