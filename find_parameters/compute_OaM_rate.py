def compute_OaM_rate(interest_rate, lifetime_list, fixed_cost_list, capital_cost_list):
    years = [int(capital_cost['year']) for capital_cost in capital_cost_list]
    OaM_rate_list = []
    for year in years:
        lifetime_value = [lifetime_elem['value'] for lifetime_elem in lifetime_list if int(lifetime_elem['year'])<=year][-1]
        ANF = (((1+interest_rate)**(lifetime_value))*interest_rate)/(((1+interest_rate)**(lifetime_value))-1)
        capital_cost_value = [capital_cost_elem['value'] for capital_cost_elem in capital_cost_list if int(capital_cost_elem['year'])<=year][-1]
        fixed_cost_value = [fixed_cost_elem['value'] for fixed_cost_elem in fixed_cost_list if int(fixed_cost_elem['year'])<=year][-1]
        try:
            OaM_rate_value = float(fixed_cost_value)/float(capital_cost_value * ANF)
        except:
            OaM_rate_value = 0
        OaM_rate_list.append({'year': year, 'value': OaM_rate_value})

    return OaM_rate_list