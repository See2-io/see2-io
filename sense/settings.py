"""
See2 Sense settings.


For more information on this file, see
https://github.com/see2-io/docs/sense/settings.md

"""

import os
from see2_io.settings import BASE_DIR

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ENRON_DATA_ROOT = os.path.join(BASE_DIR, 'sense/enron_emails/data/')
ENRON_DATA_COLLECTION = os.path.join(ENRON_DATA_ROOT, 'collection/')
ENRON_DATA_SIM = os.path.join(ENRON_DATA_ROOT, 'sim/')

# Enron Email Simulation config
ENRON_SIM_START = 0
ENRON_SIM_STOP = 251299
ENRON_SIM_PERIOD = 500