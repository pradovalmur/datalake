import os
from environment import Environment
from project import project

active_environment = Environment[os.environ['ENVIRONMENT']]
