class PortId(str):
    def __new__(cls, port_id: str):
        if len(port_id) == 0:
            raise ValueError(f"BlockInstanceId cannot be empty (received '{port_id}')")

        if ' ' in port_id:
            raise ValueError(f"PortId cannot contain whitespace (received '{port_id}')")

        if '::' in port_id:
            raise ValueError(f"PortId cannot contain '::' (received '{port_id}')")

        if '[' in port_id or ']' in port_id:
            raise ValueError(f"PortId cannot contain '[' or ']' (received '{port_id}')")

        return super().__new__(cls, port_id)
