'''
Housing cost per square foot analysis over time
'''

import numpy as np
import matplotlib.pyplot as plt

def construct_state_dict(file):
    state_dict = {} #{states:{city:[costs]}}
    for line in file:
        line = line.lower()
        line = line.split(',')
        if line[2] != 'state':
            if line[2] not in state_dict:
                state_dict[line[2]] = {}
            state_dict[line[2]][line[1]] = construct_city_housing_list(line)
    return state_dict

def construct_city_housing_list(file_line_list):
    city_housing_list = []
    for i in range(6, len(file_line_list)):
        if file_line_list[i] != '':
            city_housing_list.append(int(file_line_list[i]))
    return city_housing_list
        
def analyze_city(city_costs):
    x_vals = np.arange(2018 - len(city_costs)/12, 2018 - 1/12, 1/12)
    for i in range(2):   
        try:
            assert len(x_vals) == len(city_costs)
        except:
            x_vals = np.arange(2018 - len(city_costs)/12, 2018, 1/12)
    plt.plot(x_vals, city_costs, 'r-')
    plt.ylabel('Cost per Square Foot ($)')
    plt.xlabel('Year')
    plt.title('Cost of Housing vs. Year')
    plt.axis([2018-len(city_costs)/12 - 1/12, 2018, 0, max(city_costs) + 10])
    plt.show()
    
#=============================================================================
def main():
    file = open('..\\data\\med_housePrice_per_squareFoot.csv', 'r')
    state_cities = construct_state_dict(file)
    print('Welcome to Housing Cost Analyzer.')
    while True:
        state = input('Enter the state abbreviation or type "exit" to exit: ')
        if state.lower() == 'exit':
            break
        elif state.lower() in state_cities:
            city = input('Enter the city name or type "exit" to exit: ')
            if city.lower() in state_cities[state]:
                analyze_city(state_cities[state][city])
            elif city.lower() == 'exit':
                break
            else:
                print('That is not a valid city.')
        else:
            print('That is not a valid state.')
    print('Goodbye!')
    
if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        