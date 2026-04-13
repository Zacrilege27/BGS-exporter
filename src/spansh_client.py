import requests


class SpanshClient:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.base_url = "https://spansh.co.uk/api"

    def get_system(self, system_id64: int) -> dict:
        url = f"{self.base_url}/system/{system_id64}"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()