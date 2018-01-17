from traitlets.config.loader import load_pyconfig_files
import os.path

def load_config():
    if os.path.isfile('~/.vsmlib/vsmlib_config.py'):
        c = load_pyconfig_files(['vsmlib_config.py'], '~/.vsmlib')
        return c
    else:
        raise ValueError('configuration file not find, please put create one in ~/.vsmlib/vsmlib_config.py')
        exit(0)
    # check the default config folder

