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
sdvxin_api = os.getenv("SDVXIN_API")

mongo_url = os.getenv("MONGO_URL")
mongo_db = os.getenv("MONGO_DB")
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")

send_start_message = os.getenv("SEND_START_MESSAGE")
send_shutdown_message = os.getenv("SEND_SHUTDOWN_MESSAGE")

superusers: list[str] = json.loads(os.getenv("SUPERUSERS"))
supergroups: list[str] = json.loads(os.getenv("SUPERGROUPS"))
