try:
    # The first line of local.py should be "from default import *", then it 
    # can override those settings it sees fit.
    from StatReader.local_settings import *
except ImportError:
    from StatReader.default_settings import *
