from build_in_functions import iterate_mapping
from write_to_csv import seperator_to_csv


def create_region_file(regions_data, cwd):
    region_list = []
    region_list.append(['#blockwise'])
    unique_regions = iterate_mapping(regions_data,"map(&join(``,['/include(./regions/',@,'.csv)']),unique(timeseries[? timeindex_start== `{}`].region[]))".format('2016-01-01T00:00:00'))
    for region in unique_regions:
        region_list.append([region])

    seperator_to_csv(region_list, cwd + '/Region.csv')