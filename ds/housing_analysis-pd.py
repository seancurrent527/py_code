'''
Housing cost per square foot analysis over time
'''

import pandas as pd
import numpy as np
import scipy.stats as stat
import matplotlib.pyplot as plt
        
def analyze_state(country_costs, state):        
    state_filter = country_costs['State'] == state.upper()
    state_costs = country_costs[state_filter]
    return state_costs
        
def analyze_city(state_costs, city):
    city_filter = state_costs['RegionName'] == city.title()
    city_costs = state_costs[city_filter]
    return city_costs
    
def plot_data(costs):
    avg_costs = costs.mean()[2:]
    x_vals = np.arange(2018 - len(avg_costs)/12, 2018 - 1/12, 1/12)
    plt.plot(x_vals, list(avg_costs), 'r-')
    plt.ylabel('Cost per Square Foot ($)')
    plt.xlabel('Year')
    plt.title('Cost of Housing vs. Year')
    plt.axis([2018-len(avg_costs)/12 - 1/12, 2018, 0, avg_costs.max() + 10])
    plt.show()
    
def plot_correlation(cost1, cost2):
    avg_costs1 = cost1.mean()[2:]
    avg_costs2 = cost2.mean()[2:]
    x_vals = np.arange(2018 - len(avg_costs1)/12, 2018 - 1/12, 1/12)
    plt.plot(x_vals, avg_costs1, 'b--', x_vals, avg_costs2, 'r--')
    plt.ylabel('Cost per Square Foot ($)')
    plt.xlabel('Year')
    plt.title('US - Blue vs State - Red')
    plt.axis([2018-len(avg_costs1)/12 - 1/12, 2018, 0, max(avg_costs1.max(), avg_costs2.max()) + 10])
    plt.show()
    
def calculate_correlation(cost1, cost2):
    correlation, prob = stat.pearsonr(list(cost1.mean()[2:]), list(cost2.mean()[2:]))
    print('The correlation between US data and state data is', correlation**2)
    
def state_correlations(country_costs):
    '''
    DO NOT USE. Large runtime.
    '''
    states = {x for x in country_costs['State']}
    state_correlations = {}
    for state in states:
        cost2 = country_costs[country_costs['State'] == state.upper()]
        correlation, prob = stat.pearsonr(list(country_costs.mean()[2:]), list(cost2.mean()[2:]))
        state_correlations[state] = correlation**2
    max_corr, min_corr = max(state_correlations.values()), min(state_correlations.values())
    for key, val in state_correlations.items():
        if val == max_corr:
            max_state = key
        elif val == min_corr:
            min_state = key
    print('The state with the maximum correlation is', (max_state, max_corr))
    print('The state with the minimum correlation is', (min_state, min_corr))
    
    
#=============================================================================
def main():
    country_costs = pd.read_csv('..\\data\\med_housePrice_per_squareFoot.csv')
    print('Welcome to Housing Cost Analyzer.')
    while True:
        choice = input('Choose one: (view data, view correlations) ')
        if choice.lower() == 'view data':    
            print('Data viewer initialized.')
            if input('Would you like to see a plot of average US housing values? ').lower()\
            in ('y','yes'):
                plot_data(country_costs)
            while True:
                try:
                    state = input('Enter a state abbreviation or type "exit" to exit: ')
                    if state == 'exit' or state == 'skip':
                        break
                    state_costs = analyze_state(country_costs, state)
                    if input('Would you like to see a plot of average state housing values? ').lower()\
                    in ('y','yes'):
                        plot_data(state_costs)
                    if input('Would you like to view a city in the state? ').lower()\
                    in ('y','yes'):
                        city = input('Enter the city name or type "exit" to exit: ')
                        if city == 'exit' or city == 'skip':
                            break
                        city_costs = analyze_city(state_costs, city)
                        plot_data(city_costs)
                        
                except ValueError:
                    print('That is not an acceptable state abbreviation.')
                    continue
        
        elif choice.lower() == 'view correlations':
            print('Correlation analysis initiated.')
         
            while True:
                try:
                    #state_correlations(country_costs)
                    state = input('Enter a state abbreviation or type "exit" to exit: ')
                    if state == 'exit' or state == 'skip':
                        break
                    state_costs = analyze_state(country_costs, state)
                    calculate_correlation(country_costs, state_costs)
                    plot_correlation(country_costs, state_costs)
                        
                except ValueError:
                    print('That is not an acceptable state abbreviation.')
                    continue
        
        elif choice.lower() == 'exit':
            break
            
        else:
            print('That is not a valid choice. Please choose either'\
             + ' (view data, view correlations) or type "exit" to exit.')

    
    print('Goodbye!')
    
    
if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
