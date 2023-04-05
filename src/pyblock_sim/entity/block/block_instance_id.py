class BlockInstanceId(str):
    def __new__(cls, instance_id: str):
        if len(instance_id) == 0:
            raise ValueError(f"BlockInstanceId cannot be empty (received '{instance_id}')")

        if ' ' in instance_id:
            raise ValueError(f"BlockInstanceId cannot contain whitespace (received '{instance_id}')")

        if '::' in instance_id:
            raise ValueError(f"BlockInstanceId cannot contain '::' (received '{instance_id}')")

        if '[' in instance_id or ']' in instance_id:
            raise ValueError(f"BlockInstanceId cannot contain '[' or ']' (received '{instance_id}')")

        return super().__new__(cls, instance_id)
