import os
env = os.environ.get("APP_ENV", "dev")

print("LOADING SETTINGS", env)

if env == "dev":
    from .dev import *
if env == "demo":
    from .demo import *

print("Data dir was set to", DATA_DIR)
