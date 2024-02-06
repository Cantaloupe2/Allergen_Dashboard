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
from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Dietary Concerns Dashboard")

# add_sidebar = st.sidebar.selectbox("Page",("1","2"))

print('streamlit file')
diet_data = pd.read_csv('diet_data_no_names.csv')

# create a list of the "Date \nContacted" column in diet_data and name it dates
dates = diet_data['Date \nContacted']
diet_data['dates'] =dates


  #################################################

df = diet_data
#######################################################
# Convert Date times to correct format if not already
def format_date(date_str):
    date_str = str(date_str)
    try:
        # Attempt to parse the date
        parsed_date = datetime.strptime(date_str, '%m/%d/%y')
        # st.write(parsed_date.strftime('%m/%d/%y'))
        return parsed_date.strftime('%m/%d/%y')
    except ValueError:
        # If parsing fails, try another format
        try:
            parsed_date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
            # parsed_date.strftime('%m/%d/%y')
            return parsed_date.strftime('%m/%d/%y')
        except ValueError:
            # Handle the case where the date is not in the expected formats
            # st.write(date_str)
            return date_str

# Apply the formatting function to the 'date' column
df['dates'] = df['dates'].apply(format_date)
###########################################################
# convert mess of strings to X marks
columns_to_check = df.columns

# Iterate over each row and column
for index, row in df.iterrows():
    for column in columns_to_check:
        # Check if the column name is in the string for the current row (case-sensitive)
        if column in str(row[column]):
            # If present, mark the column with 'x'
            df.at[index, column] = 'x'
        if str(row[column]) == 'x':
            dummy = 0
        else:
            # If not present, mark the column with ''
            df.at[index, column] = ''

#############################################################

sdf=df.drop(['Major','RCPD','Other','Notes','Dining Accommodation',
             'Specialist','Intial Concern','Hall (Living/Eating)',
             'Class Type','dates', 'Date \nContacted'], axis=1)
cdf=sdf.dropna(how='all')

ndf = cdf.fillna(0)
columns_to_convert = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
                      'Vegetarian','Halal','Kosher']

total_allergens = 0 
for col in columns_to_convert:
    ndf[col] = ndf[col].replace('x', 1)
    ndf[col] = ndf[col].replace(' ',0)
    ndf[col] = ndf[col].replace('',0)
    total_allergens = total_allergens + ndf[col].sum()
average_allergens = total_allergens/len(ndf)
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
allergen_max2 = second_most_df.idxmax()

# find most correlated values
sol = (matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(bool))
                  .stack()
                  .sort_values(ascending=False))
flag = 0
for index, value in sol.items():
  if flag == 2:
    break
  if flag == 1:
    allergen3 = index[0]
    allergen4 = index[1]
  if flag == 0:
    allergen1 = index[0]
    allergen2 = index[1]
  flag = flag + 1

  


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
  st.write(f"Second Most Correlated Dietary Issues: **{allergen3}** and **{allergen4}**")
  st.write(f"Students list an average of **{str(average_allergens)[0:3]}** allergies.")
with col2:
  st.subheader(f"Dietary Concerns Correlation Matrix")
  st.plotly_chart(fig)


stacked_df = pd.read_csv("linechart_data.csv")
#fig = px.line(x = stacked_df["Year"], y = stacked_df["Prop"], color = stacked_df["allergy"])
stacked_df["Year"] = pd.to_numeric(stacked_df["Year"], errors='coerce')
stacked_df["Prop"] = pd.to_numeric(stacked_df["Prop"], errors='coerce')
fig2 = px.line(x = stacked_df["Year"], y = stacked_df["Prop"], color = stacked_df["allergy"])
fig2.update_layout(
    xaxis_title="Year",
    yaxis_title="Proportion",
    legend_title="Dietary Concern",
)

dates_ndf = ndf
dates_ndf["dates"] = df["dates"]

# create a list of the "Date \nContacted" column in diet_data and name it dates
dates_series = dates_ndf['dates']
# remove NaN values from dates
for i in range(len(dates_series)):
  if type(dates_series.iloc[i]) != str:
    dates_series.iloc[i] = "00"
#dates_series = [date for date in dates_series if type(date) == str]

# # take the last 2 digits of each element in dates and name it years
years = [date[-2:] for date in dates_series]
# convert to years
for i in range(len(years)):
  years[i] = int(years[i])+2000

# st.write(dates_ndf)
# for i in range(len(dates_ndf)):
#   dates_ndf.loc[i,"dates"] = int(str(dates_ndf.loc[i,"dates"])[-1])*100
dates_ndf["years"]= years
by_year = dates_ndf["years"].value_counts()
by_year = by_year.sort_index()
by_year = by_year[by_year.index >=2014]



# Total Plot
fig3 = px.line(x = by_year.index, y = by_year)
fig3.update_layout(
    xaxis_title="Year",
    yaxis_title="Responses",
)
# st.write(stacked_df)
# st.write(by_year)
# total_concerns = []
# for i in range(len(stacked_df)):
#   total_concerns.append(stacked_df.iloc[i,"Prop"]*by_year[stacked_df.iloc[i,"Year"]])

# non proportional dietary condition plot
fig4 = px.line(x = stacked_df["Year"], y = stacked_df["Count"], color = stacked_df["allergy"])
fig4.update_layout(
    xaxis_title="Year",
    yaxis_title="Responses",
    legend_title="Dietary Concern",
)

st.subheader("Responses Time Data")

tab1, tab2, tab3 = st.tabs(["Total","By Dietary Concern", "By Dietary Concern (Proportions)"])

tab1.plotly_chart(fig3)

tab2.plotly_chart(fig4)

tab3.plotly_chart(fig2)



###########################################################
neighorhoods = pd.read_csv("neighborhood_data.csv")


neighorhoods['Year'] = '20' + neighorhoods['Date \nContacted'].str.split('/').str[-1]


neighborhood_list = np.array(["south","north","east","brody","rivertrail"])
grouped_years = neighorhoods.groupby("Year")
data_2014 = grouped_years.get_group("2014")

fig5 = px.bar(x = neighborhood_list,y = neighorhoods["Neighborhood"].value_counts())
fig5.update_layout(
    xaxis_title="Neighborhood",
    yaxis_title="Count",
)
st.subheader("Response Locations")
st.write(fig5)
