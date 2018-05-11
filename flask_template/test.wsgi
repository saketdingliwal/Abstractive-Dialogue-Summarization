import sys

# Insert the path to flask folder
sys.path.insert(0, "/path/to/flask/folder")

# In case of non-standard library requirements. Install them in a virtual env and activate it.
# Uncomment the below two lines only if required

# activate_this="/path/to/virtual_env"+"/bin/activate_this.py"
# exec(open(activate_this).read())

from app import app
application = app
