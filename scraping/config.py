from configparser import ConfigParser


def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for param in parameters:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


if __name__ == '__main__':
    config = load_config()
    print(config)
