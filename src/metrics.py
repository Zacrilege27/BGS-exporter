from prometheus_client import Gauge

EXPORTER_UP = Gauge("bgs_exporter_up", "Exporter health")

SYSTEM_FETCH_SUCCESS = Gauge(
    "bgs_system_fetch_success",
    "Whether the system fetch succeeded",
    ["system"],
)

FACTION_PRESENT = Gauge(
    "bgs_faction_present",
    "Whether the watched faction is present in the system",
    ["system", "faction"],
)

FACTION_INFLUENCE = Gauge(
    "bgs_faction_influence",
    "Influence of the watched faction in the system",
    ["system", "faction"],
)

FACTION_RANK = Gauge(
    "bgs_faction_rank",
    "Rank of the watched faction by influence in the system",
    ["system", "faction"],
)

SYSTEM_CONTROLLED = Gauge(
    "bgs_system_controlled",
    "Whether the watched faction controls the system",
    ["system", "faction"],
)

CONTROLLED_STATION_COUNT = Gauge(
    "bgs_controlled_station_count",
    "Number of stations in the system controlled by the watched faction",
    ["system", "faction"],
)

FACTION_STATE = Gauge(
    "bgs_faction_state",
    "State flag for the watched faction",
    ["system", "faction", "state"],
)

FACTION_PENDING_STATE = Gauge(
    "bgs_faction_pending_state",
    "Pending state flag for the watched faction",
    ["system", "faction", "state"],
)


def set_up(value: int):
    EXPORTER_UP.set(value)


def publish_system_metrics(normalized: dict):
    system = normalized["system_name"]
    faction = normalized["faction_name"]

    SYSTEM_FETCH_SUCCESS.labels(system=system).set(1)
    FACTION_PRESENT.labels(system=system, faction=faction).set(
        1 if normalized["faction_present"] else 0
    )
    FACTION_INFLUENCE.labels(system=system, faction=faction).set(
        normalized["faction_influence"]
    )
    FACTION_RANK.labels(system=system, faction=faction).set(
        normalized["faction_rank"]
    )
    SYSTEM_CONTROLLED.labels(system=system, faction=faction).set(
        1 if normalized["system_controller"] == faction else 0
    )
    CONTROLLED_STATION_COUNT.labels(system=system, faction=faction).set(
        normalized["controlled_station_count"]
    )

    current_state = normalized["faction_state"] or "None"
    FACTION_STATE.labels(system=system, faction=faction, state=current_state).set(1)

    for pending_state in normalized["faction_pending_states"]:
        FACTION_PENDING_STATE.labels(
            system=system,
            faction=faction,
            state=pending_state,
        ).set(1)