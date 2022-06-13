from google_oauth.config import Config
import requests
# Function for retrieving Google's provider configuration.
def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()