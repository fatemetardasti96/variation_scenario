import shutil

from build_in_functions import iterate_mapping


def create_config_files(regions_data, cwd):
    src = r'./start_auto_gen.sh'
    dst = cwd + '/start_auto_gen.sh'
    shutil.copy(src, dst, follow_symlinks=True)
    interest_rate = iterate_mapping(regions_data,"unique(scalars[? parameter_name == 'WACC'].value)")[0]

    g = open(cwd +'/ProgramSettings.dat','w')
    with open('./ProgramSettings.dat', 'r') as f:
        for line in f.readlines():
            if line.strip() == 'simulation_start=':
                line = line.strip() + '2016-01-01_00:00\n'
            elif line.strip() == 'simulation_end=':
                line = line.strip() + '2051-01-01_00:00\n'
            elif line.strip() == 'interest_rate=':
                line = line.strip() + str(interest_rate) + '\n'

            g.writelines(line)
    ##TODO
    # emission limit is different for years
    # if emission_limit != None:
    #     g.writelines('max_co2_emission_annual={}\n'.format(emission_limit))
    g.close()


