# Imports
import copy
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
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

#######################################################################################
#Pulling in the data from qualtrix pipeline
# Set up credentials
api_key = "AIzaSyD95Gh8QGvJVrW1GnU39NWLd2PS77xr5qE"  # Replace with your API key

# Authenticate using API key
service_account_file = "sonic-harbor-404423-c09f9b7f4fe5.json"
gc = gspread.service_account(filename=service_account_file)

# Open the Google Sheet by URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1GG1BuGn-u85zIaxM1Mo9ymgotqgY4k44fn3kKV-wbLY/edit?usp=sharing"  # Replace with your Google Sheets URL
sh = gc.open_by_url(spreadsheet_url)

# Select a specific worksheet
worksheet = sh.get_worksheet(0)  # Change the index accordingly

# Get all values from the worksheet as DataFrame
diet_data = get_as_dataframe(worksheet)

# Rename Column in round about way
dates = diet_data['Date \nContacted']
diet_data['dates'] =dates

# Create A separate Dataframe Named Df
df = diet_data

#######################################################
#Convert Date times to correct format if not already
def format_date(date_str):
    try:
        # Attempt to parse the date
        parsed_date = datetime.strptime(str(date_str), '%m/%d/%y')
        # st.write(parsed_date.strftime('%m/%d/%y'))
        return parsed_date.strftime('%m/%d/%y')
    except ValueError:
        # If parsing fails, try another format
        try:
            parsed_date = datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S")
            # parsed_date.strftime('%m/%d/%y')
            return parsed_date.strftime('%m/%d/%y')
        except ValueError:
            # Handle the case where the date is not in the expected formats
            return date_str

# Apply the formatting function to the 'date' column
df['dates'] = df['dates'].apply(format_date)

# remove nan values
df = df[df['dates'].notna()]

###########################################################
#convert mess of strings to X marks
columns_to_check = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
                      'Vegetarian','Halal','Kosher']
# Iterate over each row and column
for index, row in df.iterrows():
    for column in columns_to_check:
        # Check if the column name is in the string for the current row (case-sensitive)
        if str(column)[0:3] in str(row[column]):
            # If present, mark the column with 'x'
            df.at[index, column] = 'x'
            pass
        if str(df.at[index,column]) == 'x':
            pass
        else:
            # If not present, mark the column with ''
            df.at[index, column] = ''
#############################################################
#Create several modified dataframes
#drop entries with no date
df = df[df['dates'].notna()]
# Drop the non allergen columns
sdf=df.drop(['Major','RCPD','Other','Notes','Dining Accommodation',
             'Specialist','Intial Concern','Hall (Living/Eating)',
             'Class Type','dates', 'Date \nContacted'], axis=1)
# Drop columns where no allergen is listed (for correlation matrix)
cdf=sdf.dropna(how='all')
ndf = cdf.fillna(0)
# Fix how na values are counted for allergens
mod_ndf = df.dropna(how='all')
mod_ndf = mod_ndf.fillna(0)
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

for col in columns_to_convert:
    mod_ndf[col] = mod_ndf[col].replace('x', 1)
    mod_ndf[col] = mod_ndf[col].replace(' ',0)
    mod_ndf[col] = mod_ndf[col].replace('',0)
    total_allergens = total_allergens + mod_ndf[col].sum()
    
matrix = ndf.corr()

#######################################################
#Code for the info bar
  

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

##############################################################################################################  

#Implementing info bar#
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

#################################################################################################################
#stacked dataframe using preprogrammed data.#
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

##################################################################################################################
#Create a years column and plot dietary concerns by proportion with it.
dates_ndf = mod_ndf
dates_ndf["dates"] = df["dates"]
# create a list of the "Date \nContacted" column in diet_data and name it dates
dates_series = dates_ndf['dates']
# remove NaN values from dates
#for i in range(len(dates_series)):            recently removed this for loop
#  if type(dates_series.iloc[i]) != str:
    #dates_series.iloc[i] = "00"
#dates_series = [date for date in dates_series if type(date) == str]
# st.write(df["dates"])
# # take the last 2 digits of each element in dates and name it years
years = [date[-2:] for date in df['dates']]
#st.write(years)
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



################################################################################################################

#######################################################################################################
dates_ndf = dates_ndf.reset_index()
hall_column_string = 'Hall (Living/Eating)'
unique_years = dates_ndf['years'].unique()
unique_halls = dates_ndf[hall_column_string].unique()
valid_halls = ['Akers','Brody',"Case","Holden","Holmes",'Landon','Owen', 'Shaw', 'Snyder']
filtered_df = pd.DataFrame([], index=unique_years, columns=valid_halls)
###############################
allergen_columns = ['Eggs', 'Milk', 'Fish','Shellfish','Peanuts',
                      'Tree Nuts','Sesame','Soy','Wheat/Gluten','Vegan',
                      'Vegetarian','Halal','Kosher']
dictionary_template = {}
for val in allergen_columns:
    dictionary_template[val] = 0
###############################    
for i, hall in enumerate(valid_halls):
    for j, year in enumerate(unique_years):
        temp_dictionary = copy.deepcopy(dictionary_template)
        for k, allergen in enumerate(allergen_columns):
            allergen_count = 0
            for l, row in enumerate(dates_ndf[allergen]):
                if dates_ndf['years'][l] == year:
                    if dates_ndf[hall_column_string][l] == hall:
                        allergen_count += row
            temp_dictionary[allergen] = allergen_count
        filtered_df.iloc[j,i] = [temp_dictionary]
filtered_df = filtered_df.drop(2002)
##############################
import plotly.graph_objects as go
option = st.selectbox(
    'Select Hall',
    valid_halls)
hall_select = option
dict_list = []
for i, val in enumerate(filtered_df[hall_select]):
    dict_list.append(val[0])
data = dict_list
# Custom x-values
x_values = filtered_df.index

# Create a list of colors for each category
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#b03c9e', '#ff5733', '#4a4a4a']

# Create the trace for each category
traces = []
for i, (category, color) in enumerate(zip(data[0].keys(), colors)):
    trace = go.Bar(
        x=x_values,
        y=[d[category] for d in data],
        name=category,
        marker=dict(color=color),
        hoverinfo='y+name'
    )
    traces.append(trace)

# Create the figure
fig_subsec = go.Figure(data=traces)

# Add layout details
fig_subsec.update_layout(
    title=hall_select+" Hall Dietary Survey Data",
    xaxis=dict(title="Index",tickvals=x_values),
    yaxis=dict(title="Quantity"),
    barmode="stack"
)

# Show the figure
st.plotly_chart(fig_subsec)
#fig.show()
########################################################################################################

############################################################## Final Debugging
st.write(df)

