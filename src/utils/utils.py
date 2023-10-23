import datetime

def generate_log_file_name(scenario_name, settings, append_date=False):
    """
    Generates a log file name based on the given scenario name.

    Parameters:
    scenario_name (str): The name of the scenario for which the log file name is to be generated.
    settings (dict): The settings dictionary containing scenario configurations.
    append_date (bool): Flag indicating whether to append the current date and time to the log file name.

    Returns:
    str: The generated log file name.
    """
    try:
        number_of_slots = settings["scenarios"][scenario_name]["number_of_slots"]
        resource_blocks_per_slot = settings["scenarios"][scenario_name]["resource_blocks_per_slot"]
        ewma_time_constant = settings["scenarios"][scenario_name]["ewma_time_constant"]
        slot_duration_in_seconds = settings["scenarios"][scenario_name]["slot_duration_in_seconds"]
        capacity_calculator = settings["scenarios"][scenario_name]["capacity_calculator"]
        number_of_ues = _get_number_of_user_equipments(scenario_name, settings)
        scheduler_suffix = _get_scheduler_suffix(capacity_calculator)

        formatted_duration = _format_scientific_notation(slot_duration_in_seconds)
        # Construct the base log file name
        base_log_name = f"n{number_of_slots}_t{formatted_duration}_rb{resource_blocks_per_slot}_u{number_of_ues}_tau{ewma_time_constant}_{scheduler_suffix}"

        # If append_date is True, append the current date and time
        if append_date:
            current_datetime = datetime.datetime.now()
            date_suffix = current_datetime.strftime("%Y%m%d_%H%M%S")
            return f"{base_log_name}_{date_suffix}"
        else:
            return f"{base_log_name}"

    except KeyError as e:
        print(f"KeyError: {e}. Check if {scenario_name} and required keys exist in settings.")
        return f"error_log_{scenario_name}"  # Return a default error log file name

def _format_scientific_notation(number):
    """
    Formats a float number to scientific notation without a decimal point.

    Parameters:
    number (float): The float number to be formatted.

    Returns:
    str: The formatted scientific notation string without a decimal point.
    """
    # Convert the number to scientific notation
    sci_notation = format(number, ".0e")

    # Replace the decimal point with an empty string
    formatted_notation = sci_notation.replace('.', '')

    return formatted_notation

def _get_number_of_user_equipments(scenario_name, settings):
    """
    Gets the number of user equipments based on the given scenario name.

    Parameters:
    scenario_name (str): The name of the scenario for which the number of UEs is to be calculated.
    settings (dict): The settings dictionary containing scenario configurations.

    Returns:
    int: The number of user equipments.
    """
    try:
        user_equipments = settings["scenarios"][scenario_name]["user_equipments"]

        if isinstance(user_equipments, list):
            # Assuming each item in the list is a dictionary with a "mode" key and optionally a "number_of_ues" key
            fixed_ues = [ue for ue in user_equipments if ue["mode"].upper() == "FIXED"]
            other_ues = [ue for ue in user_equipments if ue["mode"].upper() != "FIXED"]
            return len(fixed_ues) + sum(ue.get("number_of_ues", 1) for ue in other_ues)

        elif isinstance(user_equipments, dict):
            # If user_equipments is a dictionary, return the value associated with the "number_of_ues" key
            return user_equipments.get("number_of_ues", 0)

        else:
            print(f"Unexpected data type for user_equipments in scenario {scenario_name}")
            return 0  # Return 0 as a default value in case of an error

    except KeyError as e:
        print(f"KeyError: {e}. Check if {scenario_name} and required keys exist in settings.")
        return 0  # Return 0 as a default value in case of an error

def _get_scheduler_suffix(capacity_calculator):
    """
    Determines the scheduler suffix based on the capacity_calculator value.

    Parameters:
    capacity_calculator (str): The name of the capacity calculator.

    Returns:
    str: The scheduler suffix.
    """
    # Define a mapping of capacity calculator names to scheduler suffixes
    scheduler_mapping = {
        "RoundRobinCapacityCalculator": "RR",
        "ProportionalFairCapacityCalculator": "PF"
        # Add more scheduler types as needed
    }

    # Get the scheduler suffix from the mapping, default to an empty string if not found
    return scheduler_mapping.get(capacity_calculator, "")
