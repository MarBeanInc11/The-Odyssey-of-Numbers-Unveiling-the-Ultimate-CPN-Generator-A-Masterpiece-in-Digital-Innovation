# Configuration settings for the CPN generator

# You can add any settings specific to the environment here.

import os

# Load environment variables if any
MIN_CPN_NUMBER = os.environ.get("MIN_CPN_NUMBER", 100000000)
MAX_CPN_NUMBER = os.environ.get("MAX_CPN_NUMBER", 999999999)
