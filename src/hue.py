import logger
import main

LOG = logger.mainLog

def getBridgeIp():
    """
    Retrieves the IP address of the Philips Hue Bridge from the automation.json file.
    If the IP address is not found, prompts the user to enter it.

    Returns:
        str: The IP address of the Philips Hue Bridge.
    """
    if not is_enabled():
        LOG.warning("Philips Hue automation is not enabled.")
        return None
    LOG.info("Retrieving Philips Hue Bridge IP address.")
    automationJson = getJsonDict('automation.json')
    if 'Bridge IP' not in automationJson:
        LOG.warning("Bridge IP not found in automation.json. Prompting user for input.")
        automationJson['Bridge IP'] = textPrompt('Enter in IP Address of Bridge')
        updateJsonFile(automationJson, 'automation.json')
        LOG.info(f"Bridge IP updated to: {automationJson['Bridge IP']}")
    return automationJson['Bridge IP']
