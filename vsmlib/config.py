from traitlets.config.loader import load_pyconfig_files
import os.path

def load_config():
    # check the default config folder
    default_dir = os.path.expanduser("~/.vsmlib/")
    if os.path.isfile(os.path.join(default_dir, 'vsmlib_config.py')):
        c = load_pyconfig_files(['vsmlib_config.py'], default_dir)
        return c
    else:
        raise ValueError('configuration file not find, please create one in ~/.vsmlib/vsmlib_config.py')
        exit(0)

