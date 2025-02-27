import json
import os

import dotenv

dotenv.load_dotenv()

df_api = os.getenv("DIVING_FISH_API")
lx_api = os.getenv("LXNS_API")
fanyu_api = os.getenv("FANYU_API")
wahlap_arcade_api = os.getenv("WAHLAP_ARCADES_API")
df_token = os.getenv("DIVING_FISH_TOKEN")
lx_token = os.getenv("LXNS_TOKEN")

superusers: list[str] = json.loads(os.getenv("SUPERUSERS"))
supergroups: list[str] = json.loads(os.getenv("SUPERGROUPS"))