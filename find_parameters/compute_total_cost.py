def compute_total_cost(interest_rate, lifetime_list, capital_cost_list):
    years = [int(capital_cost['year']) for capital_cost in capital_cost_list]
    total_cost_list = []
    for year in years:
        lifetime_value = [lifetime_elem['value'] for lifetime_elem in lifetime_list if int(lifetime_elem['year'])<=year][-1]
        ANF = (((1+interest_rate)**(lifetime_value))*interest_rate)/(((1+interest_rate)**(lifetime_value))-1)
        capital_cost_value = [capital_cost_elem['value'] for capital_cost_elem in capital_cost_list if int(capital_cost_elem['year'])<=year][-1]
        total_cost_list.append({'year': year, 'value': capital_cost_value*(ANF+1)})

    return total_cost_list
