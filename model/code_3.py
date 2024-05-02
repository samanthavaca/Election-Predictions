import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt

dem_dictionary = {}
rep_dictionary = {}
lib_dictionary = {}

def trainModel(year):
    '''
    Pre-processing data
    '''

    print("YEAR BEING RUN!!")
    print(year)
    # 1. Clear all empty candidates
    # 2. Remove any other parties, other than Democrats/Republicans/Independent
    # 3. Calculate votes / total votes (percentage votes per state)
    # 4. Make a new column- add the percentage that each candidate got

    # Read in presidential data from 1976-2020
    pres_data = pd.read_csv("new_data/1976-2020-president.csv")

    pres_data = pres_data[((pres_data['party_simplified'] == "DEMOCRAT") | (pres_data['party_simplified'] == "REPUBLICAN") | (pres_data['party_simplified'] == "LIBERTARIAN"))]
    # print(pres_data)

    # Creating a new column for the percentage of votes
    pres_data['percent_votes'] = 0
    pres_data['percent_votes'] = pres_data['candidatevotes'] / pres_data['totalvotes']
    print(pres_data)

    # 5. Clean the unemployment data
    unemploy = pd.read_csv("new_data/unemployment-per-state.csv")

    # Percent (%) of Labor Force Unemployed in State/Area

    # Percent by state by month by year
    # State/Area,Year,Month

    # 6. Add it to the pres_data
    pres_data['unemployment'] = 0

    #unemploy = unemploy[(unemploy['Month'] == 3)]
    # Group by 'State' and 'Year' and calculate the mean unemployment
    average_unemployment = unemploy.groupby(['State/Area', 'Year'])['percent-unemployed'].mean().reset_index()

    # Rename the column to clarify it's the average
    # print(unemploy)
    unemploy = average_unemployment

    print(unemploy)

    pres_data['year'] = pres_data['year'].astype(float)
    unemploy['Year'] = unemploy['Year'].astype(float)
    unemploy['State/Area'] = unemploy['State/Area'].str.upper()

    # Combine both of the datasets
    pres_data = pd.merge(pres_data, unemploy, how='inner', left_on=['year', 'state'], right_on=['Year', 'State/Area'])

    """
    # 5. Clean the income data
    income_data = pd.read_csv("personal-income.csv")
    melted_income = pd.melt(income_data, id_vars=['GeoFips', 'GeoName', ], value_vars=['1994:Q1', '1994:Q2', '1994:Q3', '1994:Q4', '1995:Q1', '1995:Q2', '1995:Q3', '1995:Q4', '1996:Q1', '1996:Q2', '1996:Q3', '1996:Q4', '1997:Q1', '1997:Q2', '1997:Q3', '1997:Q4', '1998:Q1', '1998:Q2', '1998:Q3', '1998:Q4', '1999:Q1', '1999:Q2', '1999:Q3', '1999:Q4', '2000:Q1', '2000:Q2', '2000:Q3', '2000:Q4', '2001:Q1', '2001:Q2', '2001:Q3', '2001:Q4', '2002:Q1', '2002:Q2', '2002:Q3', '2002:Q4', '2003:Q1', '2003:Q2', '2003:Q3', '2003:Q4', '2004:Q1', '2004:Q2', '2004:Q3', '2004:Q4', '2005:Q1', '2005:Q2', '2005:Q3', '2005:Q4', '2006:Q1', '2006:Q2', '2006:Q3', '2006:Q4', '2007:Q1', '2007:Q2', '2007:Q3', '2007:Q4', '2008:Q1', '2008:Q2', '2008:Q3', '2008:Q4', '2009:Q1', '2009:Q2', '2009:Q3', '2009:Q4', '2010:Q1', '2010:Q2', '2010:Q3', '2010:Q4', '2011:Q1', '2011:Q2', '2011:Q3', '2011:Q4', '2012:Q1', '2012:Q2', '2012:Q3', '2012:Q4', '2013:Q1', '2013:Q2', '2013:Q3', '2013:Q4', '2014:Q1', '2014:Q2', '2014:Q3', '2014:Q4', '2015:Q1', '2015:Q2', '2015:Q3', '2015:Q4', '2016:Q1', '2016:Q2', '2016:Q3', '2016:Q4', '2017:Q1', '2017:Q2', '2017:Q3', '2017:Q4', '2018:Q1', '2018:Q2', '2018:Q3', '2018:Q4', '2019:Q1', '2019:Q2', '2019:Q3', '2019:Q4', '2020:Q1', '2020:Q2', '2020:Q3', '2020:Q4', '2021:Q1', '2021:Q2', '2021:Q3', '2021:Q4', '2022:Q1', '2022:Q2', '2022:Q3', '2022:Q4', '2023:Q1', '2023:Q2', '2023:Q3', '2023:Q4'], var_name='Year', value_name='Income')
    
    filtered_income = melted_income[~melted_income['Year'].str.contains('Q1|Q2|Q3')]
    filtered_income = filtered_income[~filtered_income['GeoName'].str.contains('United States|New England|Mideast|Great Lakes|Plains|Southeast|Southwest|Rocky Mountain|Far West *')]
    filtered_year = filtered_income['Year'].str.replace(':? ?Q4', '', regex=True)
    filtered_income['Year'] = filtered_year
    filtered_income['GeoName'] = filtered_income['GeoName'].str.upper()
    #filtered_income['Income'] = filtered_income['Income'] * 0.4
    print(filtered_income)

    pres_data['year'] = pres_data['year'].astype(int)
    filtered_income['Year'] = filtered_income['Year'].astype(int)

    print(pres_data)

    pres_data = pd.merge(pres_data, filtered_income, how='inner', left_on=['year', 'state'], right_on=['Year', 'GeoName'])

    """

    """
    # 5. Clean the income data
    cpi_data = pd.read_csv("cpi.csv")

    cpi_data = cpi_data[(cpi_data['quarter'] == 4)]
    
    cpi_data['state'] = cpi_data['state'].str.upper()
    print(cpi_data)

    #pres_data['year'] = pres_data['year'].astype(int)
    #cpi_data['year'] = cpi_data['year'].astype(int)

    print(pres_data)
    
    pres_data = pd.merge(pres_data, cpi_data, how='inner', left_on=['year', 'state'], right_on=['year', 'state'])
    """ 

    # Good year: 1992pres_data = pd.merge(pres_data, filtered_income, how='inner', left_on=['year', 'state'], right_on=['Year', 'GeoName'])
    # 1988 is the most even split, but results are not correct
    pres_data = pres_data[(pres_data['year'] >= 1992)]

    # 7. Extract test data from 2020
    pres_data_2020 = pres_data[pres_data['year'] == 2020.0].copy()
    pres_data = pres_data[pres_data['year'] != 2020.0]

    print(pres_data)

    print("2020 data")
    print(pres_data_2020)


    '''
    Train the model
    '''

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    from joblib import dump

    x = pres_data['percent-unemployed']
    y = pres_data['percent_votes']

    X = np.array(x).reshape(-1, 1)
    Y = np.array(y).reshape(-1, 1)

    # 8. Define function to train linear regression model for each party by state
    def train_linear_regression_by_state(data, party):
        state_models = {}
        state_mses = {}
        for state, state_data in data.groupby('state'):
            relevant_data = state_data[state_data['party_simplified'] == party]
            X = relevant_data[['percent-unemployed']]
            y = relevant_data['percent_votes']
            if len(y) > 1:  # Skip states with insufficient data for the party
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                state_models[state] = model
                state_mses[state] = mse
        return state_models, state_mses

    # 9. Train linear regression models for each party by state
    parties = ['DEMOCRAT', 'REPUBLICAN', 'LIBERTARIAN']
    all_state_models = {}
    all_state_mses = {}
    for party in parties:
        state_models, state_mses = train_linear_regression_by_state(pres_data, party)
        all_state_models[party] = state_models
        all_state_mses[party] = state_mses

    """
    # Print mean squared error for each party by state - for testing purposes
    for party, state_mses in all_state_mses.items():
        print(f"Mean squared error for {party} models by state:")
        for state, mse in state_mses.items():
            print(f"{state}: {mse}")
    """

    '''
    Make predictions depending on the year
    '''

    if year == 2024:
        # 10. Make predictions using trained models for each party by state
        unemploy_data_24 = pd.read_csv("unemployment-per-state-2024.csv")
        party_predictions = {}
        for party, state_models in all_state_models.items():
            party_predictions[party] = {}
            for state, model in state_models.items():
                state_data = unemploy_data_24[unemploy_data_24['state'] == state]
                X = state_data[['percent-unemployed']]
                predictions = model.predict(X)
                party_predictions[party][state] = predictions

    if year == 2020:
        # 10. Make predictions using trained models for each party by state
        party_predictions = {}
        for party, state_models in all_state_models.items():
            party_predictions[party] = {}
            for state, model in state_models.items():
                state_data = pres_data_2020[pres_data_2020['state'] == state]
                X_new = state_data[['percent-unemployed']]
                predictions = model.predict(X_new)
                party_predictions[party][state] = predictions

    dem_dictionary = {}
    rep_dictionary = {}
    lib_dictionary = {}

    # 11. Print predictions for each party by state (for 2020) - for testing purposes
    for party, state_predictions in party_predictions.items():
        # print(f"Predicted percent votes for {party} by state:")
        if (party == 'DEMOCRAT'):
            for state, predictions in state_predictions.items():
                dem_dictionary[state] = predictions[0]
                # print(f"{state}: {predictions}")
        if (party == 'REPUBLICAN'):
            for state, predictions in state_predictions.items():
                rep_dictionary[state] = predictions[0]
                # print(f"{state}: {predictions}")
        if (party == 'LIBERTARIAN'):
            for state, predictions in state_predictions.items():
                lib_dictionary[state] = predictions[0]
                # print(f"{state}: {predictions}")
    #print("*** Predicted percent votes for Republicans by state: ***")
    #print(rep_dictionary)

    # 12. Print actual data for each party (2020 data) - for testing purposes
    #print("\n*** Actual percent votes for each party by state: ***")
    selected_columns = pres_data_2020[['state', 'party_simplified', 'percent_votes']]
    #print(selected_columns)

    dem_electoral = 0
    rep_electoral = 0

    electoral_votes = pd.read_csv("2024_Electoral_College.csv") # number of electoral votes per state

    for state in dem_dictionary:
        if dem_dictionary.get(state) > rep_dictionary.get(state, 0):
            total_value = electoral_votes[electoral_votes['State'] == state]
            dem_electoral += int(total_value['Total'].iloc[0])
        else:
            total_value = electoral_votes[electoral_votes['State'] == state]
            rep_electoral += int(total_value['Total'].iloc[0])
    
    return dem_dictionary, rep_dictionary, dem_electoral, rep_electoral

    # Questions to consider next: How are we going to use this percentage data? How does this predict on 2024 data?

trainModel(2024)

def get_dem_results(year):
    return trainModel(year)[0]

def get_dem_votes(year):
    return trainModel(year)[2]

def get_rep_results(year):
    return trainModel(year)[1]

def get_rep_votes(year):
    return trainModel(year)[3]

def get_lib_results():
    print("Getting lib results")
    if lib_dictionary:
        return lib_dictionary
    else:
        trainModel()
        return lib_dictionary