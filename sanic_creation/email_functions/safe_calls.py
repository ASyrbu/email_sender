async def async_safe_call(_function, *args):
    try:
        responses = await _function(*args)
        return responses
    except Exception as error_msg:
        print(f"ASYNC SAFE CALL ERR: {error_msg}")
        return None, 500


def safe_call(_function, *args):
    try:
        responses = _function(*args)
        return responses
    except Exception as error_msg:
        print(f"SAFE CALL ERR: {error_msg}")
        return None, 500