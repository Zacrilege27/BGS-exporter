from prometheus_client import start_http_server
import time

from config import load_config
from state_store import load_state
from metrics import set_up, publish_system_metrics
from spansh_client import SpanshClient
from normalizer import normalize_spansh_system


def main():
    print("Loading config...")
    config = load_config("config.yml")
    print("Config loaded.")

    print("Loading state...")
    state = load_state(config["storage"]["state_file"])
    print(f"State loaded: {state}")

    client = SpanshClient(
        timeout=config["polling"]["request_timeout_seconds"]
    )

    faction_name = config["faction"]["name"]
    primary_systems = config["systems"]["primary"]

    port = config["exporter"]["listen_port"]
    print(f"Starting exporter on port {port}")
    start_http_server(port)
    print("Metrics server started.")

    while True:
        try:
            set_up(1)

            for system_entry in primary_systems:
                system_name = system_entry["name"]
                system_id64 = int(system_entry["id64"])

                if not system_id64:
                    print(f"Skipping {system_name}: missing id64")
                    continue

                print(f"Fetching {system_name} ({system_id64})")
                raw = client.get_system(system_id64)
                normalized = normalize_spansh_system(raw, faction_name)

                print(
                    f"{normalized['system_name']}: "
                    f"influence={normalized['faction_influence']}, "
                    f"rank={normalized['faction_rank']}, "
                    f"controller={normalized['system_controller']}, "
                    f"stations={normalized['controlled_station_count']}"
                )

                publish_system_metrics(normalized)

        except Exception as e:
            print(f"Error: {e}")
            set_up(0)

        time.sleep(config["polling"]["interval_seconds"])


if __name__ == "__main__":
    main()