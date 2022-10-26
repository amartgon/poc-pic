import os

DEFAULTS = {'DB_NAME': 'pic',
            'COLLECTION_NAME': 'equipos',
            'ARCHIVE_URL': f'mongodb://usr:pass1@archived-atlas-online-archive-63447e82d4032850be4f5c49-y3nia.a.query.mongodb.net/?ssl=true&authSource=admin',            
            'CLUSTER_URL': f'mongodb+srv://usr:pass1@cluster0.y3nia.mongodb.net/?retryWrites=true&w=majority&readPreference=nearest&compressors=zstd',
            'FEDERATED_URL': f'mongodb://usr:pass1@atlas-online-archive-63447e82d4032850be4f5c49-y3nia.a.query.mongodb.net/?ssl=true&authSource=admin'}


def init_defaults_from_env():
    for key in DEFAULTS.keys():
        value = os.environ.get(key)
        if value:
            DEFAULTS[key] = value


# get the settings from the environment variables
init_defaults_from_env()
