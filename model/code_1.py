import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

"""
PRE-PROCESSING HISTORICAL DATA
"""

# Define a function to extract the year in inflation
def extract_year(year):
    # Split year by dashes
    parts = year.split('-')
    # Get the first part, then split by spaces and take the first part
    year_part = parts[0]
    return year_part.strip() # Strip any leading/trailing spaces

historical_polls = pd.read_csv("pres_pollaverages_1968-2016.csv")
inflation_by_year = pd.read_csv("united-states-inflation-rate-cpi.csv")

inflation_by_year['date'] = inflation_by_year['date'].apply(extract_year)
print(inflation_by_year)

historical_polls['state'] = historical_polls['state'].str.lower()

print(inflation_by_year.iloc[0])
print(inflation_by_year['inflation'])

# merge inflation rates and historical polls dataset
historical_polls['inflation'] = 0
for i in range(len(historical_polls)):
    historical_df_year = historical_polls['cycle'][i]
    indices = inflation_by_year.index[inflation_by_year['date'] == str(historical_df_year)].tolist()
    historical_polls['inflation'][i] = str(inflation_by_year['inflation'][indices[0]])

# ---------------------------------------------------

# Define a function to extract the last name
def extract_last_name(full_name):
    # Split the full name by comma
    parts = full_name.split(',')
    # Get the first part, then split by spaces and take the last part
    last_name = parts[0].split()[-1]
    return last_name.strip()  # Strip any leading/trailing spaces

# Apply the function to the 'Name' column
historical_polls['candidate_name'] = historical_polls['candidate_name'].apply(extract_last_name)
historical_polls['candidate_name'] = historical_polls['candidate_name'].str.lower()

# ---------------------------------------------------


# Found dataset on MIT for presidential election results by state 1976-2016
# MIT Election Data and Science Lab, 2017, "U.S. President 1976–2020", https://doi.org/10.7910/DVN/42MVDX, 
# Harvard Dataverse, V7, UNF:6:MkQHX147hJCgscG5IqK77g== [fileUNF]

election_results = pd.read_csv("1976-2020-president.csv")

# ---------------------------------------------------

election_results['pct'] = election_results['candidatevotes'] / election_results['totalvotes']
election_results['state'] = election_results['state'].str.lower()

# Define a function to extract the part before the comma
def extract_last_name(full_name):
     if isinstance(full_name, str):
        return full_name.split(',')[0]
     else:
        return ""

# Apply the function to the 'Name' column
election_results['candidate'] = election_results['candidate'].apply(extract_last_name)
election_results['candidate'] = election_results['candidate'].str.lower()

election_results.head()

# ---------------------------------------------------

# merge dataframes on year, state, party
# merge pct-estimate and pc-actual datasets
election_polls_vs_results = pd.merge(historical_polls, election_results, left_on=['candidate_name','state','cycle'], right_on=['candidate','state','year'], how='inner')
election_polls_vs_results = election_polls_vs_results[['cycle','state','candidate_name','modeldate','pct_estimate','pct_trend_adjusted','party_simplified','pct', 'inflation']]

election_polls_vs_results['pct_estimate'] = election_polls_vs_results['pct_estimate'].fillna(0)/100
election_polls_vs_results.head()

# ---------------------------------------------------

x = election_polls_vs_results[['pct_estimate', 'inflation']]
y = election_polls_vs_results['pct'].fillna(0)

""""
# plot original dataset
fig, ax = plt.subplots()

ax.scatter(x, y, vmin=0, vmax=1)

ax.set(xlim=(0, 1), xticks=np.arange(0,0.1),
       ylim=(0, 1), yticks=np.arange(0,0.1))

plt.title('Original Election Dataset')
plt.show()

r_squared = r2_score(x, y)
print("R-squared value (original election dataset):", r_squared)
"""

# ---------------------------------------------------

historical_polls = pd.read_csv("pres_pollaverages_1968-2016.csv")
historical_polls['state'] = historical_polls['state'].str.lower()

# Define a function to extract the last name
def extract_last_name(full_name):
    # Split the full name by comma
    parts = full_name.split(',')
    # Get the first part, then split by spaces and take the last part
    last_name = parts[0].split()[-1]
    return last_name.strip()  # Strip any leading/trailing spaces

# Apply the function to the 'Name' column
historical_polls['candidate_name'] = historical_polls['candidate_name'].apply(extract_last_name)
historical_polls['candidate_name'] = historical_polls['candidate_name'].str.lower()

# ---------------------------------------------------

# There appears to be a large set of outliers with relatively high polling pct and very low actual pct
# Possibly due to candidates that ended up dropping out of the race, but still received votes

# Getting rid of drastic outliers in the data with high pct estimate and low actual pct.
election_pvr_cleaned =  election_polls_vs_results[election_polls_vs_results['pct_estimate'] < election_polls_vs_results['pct']*5]
election_pvr_cleaned['pct_estimate'] = election_pvr_cleaned['pct_estimate'].apply(pd.to_numeric, errors='coerce')
election_pvr_cleaned = election_pvr_cleaned[(election_pvr_cleaned['pct_estimate'] <= 0.9)]

# Tried adding weights
#print(type(election_pvr_cleaned['inflation']))
#election_pvr_cleaned['inflation'] = election_pvr_cleaned['inflation'].astype(float) * 1000

print(election_pvr_cleaned['inflation'])

x = election_pvr_cleaned[['pct_estimate', 'inflation']]
y = election_pvr_cleaned['pct'].fillna(0)

""""
# plot cleaned dataset
fig, ax = plt.subplots()

ax.scatter(x, y, vmin=0, vmax=1)

ax.set(xlim=(0, 1), xticks=np.arange(0,0.1),
       ylim=(0, 1), yticks=np.arange(0,0.1))

plt.title('Cleaned Election Dataset')
plt.show()

r_squared = r2_score(x, y)
print("R-squared value (cleaned election dataset):", r_squared)
"""

"""
MACHINE LEARNING - LINEAR REGRESSION
"""

# Make prediction of actual pct based on predicted pct

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from joblib import dump

X = np.array(x)
print(X.shape)
Y = np.array(y)
print(Y.shape)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Choose a model (Linear Regression)
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

# We can save the model to be used elsewhere
dump(model, 'pres_election_polls_vs_real_predict.joblib')


"""
PRE-PROCESSING 2020 DATA
"""

cpi_2020 = 1.2336 # Average inflation rate in 2020

polls_2020 = pd.read_csv("presidential_poll_averages_2020.csv")
def extract_last_name(full_name):
    # Split the full name by whitespace
    parts = full_name.split()
    # Exclude suffixes like "Jr.", "Sr.", etc., if present
    if parts[-1] in ['Jr.', 'Sr.', 'II', 'III', 'IV']:
        last_name = parts[-2]  # Take the second last part as the last name
    else:
        last_name = parts[-1]  # Otherwise, take the last part as the last name
    return last_name


# Apply the function to the 'Name' column
polls_2020['candidate_name'] = polls_2020['candidate_name'].apply(extract_last_name)
polls_2020['candidate_name'] = polls_2020['candidate_name'].str.lower()

polls_2020['inflation'] = cpi_2020

x_2020 = np.array(polls_2020[['pct_estimate', 'inflation']])
pred_2020 = model.predict(x_2020) # Use linear regression model to predict 2020 election results
polls_2020['pred_pct'] = pred_2020/100
polls_2020['state'] = polls_2020['state'].str.lower()

print(pred_2020)

actual_2020 = election_results[election_results['year'] == 2020 ] # Actual 2020 election results

actual_vs_predicted_2020_elections = pd.merge(polls_2020, actual_2020, left_on=['candidate_name','state','cycle'], right_on=['candidate','state','year'], how='inner')
actual_vs_predicted_2020_elections['Net pred pct'] = actual_vs_predicted_2020_elections['pct'] - actual_vs_predicted_2020_elections['pred_pct']

sum_net_pred = actual_vs_predicted_2020_elections['Net pred pct'].sum()
avg_net_pred = sum_net_pred/26924

"""
According to our model, who would win in 2020?
"""

predicted_2020_averages = actual_vs_predicted_2020_elections.groupby(['state', 'candidate_name']).agg({'pred_pct': 'mean'})
predicted_2020_averages.reset_index(inplace=True)

pred_2020_election = predicted_2020_averages.pivot_table(index='state', columns='candidate_name', values='pred_pct')
pred_2020_election.reset_index(inplace=True)

error = 0
biden_count = pred_2020_election[pred_2020_election['biden']>pred_2020_election['trump']+error]
trump_count = pred_2020_election[pred_2020_election['trump']>=pred_2020_election['biden']+error]

electoral_votes = pd.read_csv("2024_Electoral_College.csv")
electoral_votes['State'] = electoral_votes['State'].str.lower()

biden_electoral = pd.merge(biden_count, electoral_votes, left_on='state', right_on = 'State', how='left')
biden_electoral_votes = biden_electoral['Total'].sum()
print("In 2020, Biden would have won: " + str(biden_electoral_votes))

trump_electoral = pd.merge(trump_count, electoral_votes, left_on='state', right_on = 'State', how='left')
trump_electoral_votes = trump_electoral['Total'].sum()
print("In 2020, Trump would have won: " + str(trump_electoral_votes))