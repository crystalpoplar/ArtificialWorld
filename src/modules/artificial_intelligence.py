import traceback
import logger

mainLog = logger.mainLog

def build_user_tool(function_name: str, function_description: str, args={}) -> dict:
    """
    Builds a user tool configuration for a function.

    Parameters:
        function_name (str): The name of the function.
        function_description (str): A description of the function's purpose.
        args (dict): A dictionary of arguments where each key is the argument name, and the value is a dictionary
                     containing the argument's description and optional enum values.

    Returns:
        dict: A dictionary representing the tool configuration.
    """
    mainLog.info(f"Building user tool for function: {function_name}")

    try:
        # Initialize the tool structure
        tool = {
            "type": "function",
            "function": {
                "name": function_name,
                "description": function_description,
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }

        # Populate the parameters' properties
        for arg_name, arg_details in args.items():
            tool["function"]["parameters"]["properties"][arg_name] = {
                "type": arg_details.get("type", "string"),
                "description": arg_details.get("description", "No description provided")
            }
            # Add enum values if provided
            if "enum" in arg_details:
                tool["function"]["parameters"]["properties"][arg_name]["enum"] = arg_details["enum"]

        mainLog.info(f"Successfully built user tool for function: {function_name}")
        return tool

    except Exception as e:
        mainLog.error(f"Error building user tool for function: {function_name}")
        mainLog.error(traceback.format_exc())
        return {}
