from typing import Any


def _safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def normalize_spansh_system(raw: dict, watched_faction: str) -> dict:
    record = raw.get("record", {})

    system_name = record.get("name", "")
    controller = record.get("controlling_minor_faction")
    controller_state = record.get("controlling_minor_faction_state")
    updated_at = record.get("updated_at")

    faction_presences = _safe_list(record.get("minor_faction_presences"))
    stations = _safe_list(record.get("stations"))

    # Sort by influence descending so we can compute rank.
    sorted_factions = sorted(
        faction_presences,
        key=lambda f: f.get("influence", 0.0),
        reverse=True,
    )

    watched_presence = None
    watched_rank = None

    for idx, faction in enumerate(sorted_factions, start=1):
        if faction.get("name") == watched_faction:
            watched_presence = faction
            watched_rank = idx
            break

    watched_station_names = []
    for station in stations:
        if station.get("controlling_minor_faction") == watched_faction:
            watched_station_names.append(station.get("name", ""))

    return {
        "timestamp_utc": updated_at,
        "system_name": system_name,
        "system_controller": controller,
        "system_controller_state": controller_state,
        "faction_present": watched_presence is not None,
        "faction_name": watched_faction,
        "faction_influence": (
            watched_presence.get("influence", 0.0) if watched_presence else 0.0
        ),
        "faction_rank": watched_rank if watched_rank is not None else 0,
        "faction_state": watched_presence.get("state", "None") if watched_presence else "None",
        "faction_pending_states": (
            watched_presence.get("pending_states", []) if watched_presence else []
        ),
        "faction_allegiance": watched_presence.get("allegiance") if watched_presence else None,
        "faction_government": watched_presence.get("government") if watched_presence else None,
        "controlled_station_count": len(watched_station_names),
        "controlled_stations": watched_station_names,
        "all_factions_sorted": [
            {
                "name": faction.get("name"),
                "influence": faction.get("influence", 0.0),
                "state": faction.get("state", "None"),
            }
            for faction in sorted_factions
        ],
    }