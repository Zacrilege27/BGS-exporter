import requests


class EliteBGSClient:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.base_url = "https://elitebgs.app/api/ebgs/v5"

    def get_system(self, system_name: str) -> dict:
        url = f"{self.base_url}/systems"
        params = {
            "name": system_name,
        }
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()