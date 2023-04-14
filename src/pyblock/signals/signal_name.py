class SignalName(str):
    def __new__(cls, signal_name: str):
        if len(signal_name) == 0:
            raise ValueError(f"SignalName cannot be empty (received '{signal_name}')")

        if ' ' in signal_name:
            raise ValueError(f"SignalName cannot contain whitespace (received '{signal_name}')")

        if '::' in signal_name:
            raise ValueError(f"SignalName cannot contain '::' (received '{signal_name}')")

        if '[' in signal_name or ']' in signal_name:
            raise ValueError(f"SignalName cannot contain '[' or ']' (received '{signal_name}')")

        return super().__new__(cls, signal_name)
