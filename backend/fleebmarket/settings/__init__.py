import os

env = os.environ.get("APP_ENV", "dev")

print("Loading settings for", env, "environment.")

if env == "dev":
    from .dev import *
if env == "demo":
    from .demo import *
