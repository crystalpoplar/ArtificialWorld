def earlierTime(curtime: str, earlierMins: int) -> str:
    """
    Calculates the time that is a specified number of minutes earlier than the given time,
    with wrap-around support for times before 00:00.

    Parameters:
        curtime (str): The current time in "HH:MM" 24-hour format (e.g., "14:30").
        earlierMins (int): The number of minutes to subtract from curtime.

    Returns:
        str: The new time in "HH:MM" 24-hour format.

    Notes:
        - If the subtraction goes past midnight, the time wraps around to the previous day.
        - Input is assumed to be valid and in correct format.
    """
    # Split the input time string into hours and minutes
    hour, mins = map(int, curtime.split(':'))

    # Convert the current time to total minutes
    total_mins = hour * 60 + mins

    # Subtract the specified number of minutes and wrap around 24 hours if needed
    total_mins = (total_mins - earlierMins) % (24 * 60)

    # Calculate the new hour and minute values
    new_hour = total_mins // 60
    new_min = total_mins % 60

    # Return the formatted time string
    return f"{new_hour}:{str(new_min).zfill(2)}"

def laterTime(curtime: str, laterMins: int) -> str:
    """
    Calculates the time that is a specified number of minutes later than the given time,
    with wrap-around support for times after 23:59.

    Parameters:
        curtime (str): The current time in "HH:MM" 24-hour format (e.g., "14:30").
        laterMins (int): The number of minutes to add to curtime.

    Returns:
        str: The new time in "HH:MM" 24-hour format.

    Notes:
        - If the addition goes past midnight, the time wraps around to the next day.
        - Input is assumed to be valid and in correct format.
    """
    # Split the input time string into hours and minutes
    hour, mins = map(int, curtime.split(':'))

    # Convert the current time to total minutes
    total_mins = hour * 60 + mins

    # Add the specified number of minutes and wrap around 24 hours if needed
    total_mins = (total_mins + laterMins) % (24 * 60)

    # Calculate the new hour and minute values
    new_hour = total_mins // 60
    new_min = total_mins % 60

    # Return the formatted time string
    return f"{new_hour}:{str(new_min).zfill(2)}"

