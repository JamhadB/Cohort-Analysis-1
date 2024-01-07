import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import seaborn as sns
import matplotlib.pyplot as plt

# upload and preview data

print('Data Preview')

data = pd.read_csv("cohorts.csv")
print(data.head())

print('------------------------')

# determine if data has any null values

# print('Missing Values')
# missing_values = data.isnull().sum()
# print(missing_values)

# print('------------------------')

# determine datatypes of all columns

# print('Data Types')
# data_types = data.dtypes
# print(data_types)

# print('------------------------')

# date column from string -> datetime format

data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Display stats for dataset

print('Data Description')

desc_stats = data.describe()
print(desc_stats)

print('------------------------')

pio.templates.default = "plotly_white"

# trend analysis for new & returning users

fig = go.Figure()
#
# fig.add_trace(go.Scatter(x=data['Date'], y=data['New users'], mode='lines+markers', name='New Users')) # New Users
#
# fig.add_trace(go.Scatter(x=data['Date'], y=data['Returning users'], mode='lines+markers', name='Returning Users')) # Returning Users
#
# fig.update_layout(title='Trend of New and Returning Users Over Time',
#                              xaxis_title='Date',
#                              yaxis_title='Number of Users') # Update layout
#
# fig.show()

# print('------------------------')

# trend analysis of duration over time

# fig = px.line(data_frame=data, x='Date', y=['Duration Day 1', 'Duration Day 7'], markers=True, labels={'value': 'Duration'})
# fig.update_layout(title='Trend of Duration (Day 1 and Day 7) Over Time',
#                   xaxis_title='Date',
#                   yaxis_title='Duration',
#                   xaxis=dict(tickangle=-45))
#
# fig.show()

# examining the correlation between variables with a correlation matrix

# correlation_matrix = data.corr() # create matrix
#
# plt.figure(figsize=(10,8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Correlation Matrix of Variables')
# plt.show()

# Grouping data by week (cohorts)

data['Week'] = data['Date'].dt.isocalendar().week

# calcuating weekly averages

print('Weekly Averages')

weekly_averages = data.groupby('Week').agg({
    'New users':'mean',
    'Returning users':'mean',
    'Duration Day 1':'mean',
    'Duration Day 7': 'mean'
}).reset_index()

print(weekly_averages.head())
print('----------------------')

fig1 = px.line(weekly_averages, x='Week', y=['New users', 'Returning users'], markers=True,
               labels={'value':'Average Number of Users'}, title='Weekly Average of New vs. Returning Users')
fig1.update_xaxes(title='Week of the Year')
fig1.update_yaxes(title='Average Number of Users')

fig2 = px.line(weekly_averages, x='Week', y=['Duration Day 1', 'Duration Day 7'], markers=True,
               labels={'value':'Average Duration'}, title='Weekly Average of Duration (Day 1 vs. Day 7)')
fig2.update_xaxes(title='Week of the Year')
fig2.update_yaxes(title='Average Duration')

fig1.show()
fig2.show()

# Creating the cohort martix

cohort_matrix = weekly_averages.set_index('Week')

plt.figure(figsize=(12, 8))
sns.heatmap(cohort_matrix, annot=True, cmap='coolwarm', fmt='.1f')
plt.title('Cohort Matrix of Weekly Averages')
plt.ylabel('Week of the Year')
plt.show()
