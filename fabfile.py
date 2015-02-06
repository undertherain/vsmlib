import fabric
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import *

from jinja2 import Template, BaseLoader, TemplateNotFound
import fnmatch
import os

env.hosts = ['localhost']

env.user = "web"
env.group = "web"
env.superuser = "web"

#env.project_name = 'nightwind'
#env.use_ve=True

@task
def clean():
    print("cleaning")
    with lcd("preprocess"):
        local("make clean")
    local("find . -name \"*.pyc\" -delete")
    local("find . -name \"__pycache__\" -delete")
