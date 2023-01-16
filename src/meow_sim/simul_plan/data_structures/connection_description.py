from dataclasses import dataclass


@dataclass
class ConnectionDescription:
    id: str
    from_block: str
    from_port: str
    to_block: str
    to_port: str
