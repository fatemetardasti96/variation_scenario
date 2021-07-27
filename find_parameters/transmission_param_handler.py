import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO)


def handle_transmission_param(param, default, varname):
    if len(param) == 1:
        return param[0]
    elif not len(param):
        return default
    else:
        logging.info("please consider further adjustment")
        raise Exception("multiple {}: {}!".format(varname, param))