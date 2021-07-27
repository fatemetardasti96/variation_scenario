def create_domestic_limit_bloc(inp, domestic_limit):
    limit_csv = []
    limit_csv.append(['#comment', 'limited primary energy for {}'.format(inp)])
    start_date = '{}-01-01_00:00'.format(domestic_limit[0]['year'])
    ##TODO what should be the end date in doemstic limit?
    end_date = '{}-01-01_00:00'.format(domestic_limit[-1]['year']+1)
    base = 1E10
    #convert PJ to GW
    limit_csv.append(['base', '#type', 'DVP_const', '#data', start_date, base, end_date, 0])
    
    value_row = ["value", "#type", 'DVP_const', "#data"]
    for i, elem in enumerate(domestic_limit):
        year, value = elem['year'], elem['value']
        value = 1000*value/3.6
        start_date = '{}-01-01_00:00'.format(year)
        try:
            end_date = '{}-01-01_00:00'.format(domestic_limit[i+1]['year']-1)
        except:
            end_date = '{}-01-01_00:00'.format(domestic_limit[-1]['year']+1)
        ##TODO: end value should be 0?    
        value_row.extend([start_date, value, end_date, 0])
    limit_csv.append(value_row)

    limit_csv.append(['#endtable'])
    return limit_csv
