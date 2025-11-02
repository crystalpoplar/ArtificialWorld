import requests

def post_data_to_api(new_data, filepath, api_url):
    """
    Sends data to a specified API endpoint via a POST request.

    Args:
        new_data (Any): The data to be sent to the API.
        filepath (str): The file path associated with the data.
        api_url (str): The URL of the API endpoint.

    Returns:
        requests.Response: The response object returned by the API.

    Raises:
        requests.RequestException: If the request fails due to network issues or invalid responses.
    """
    # Prepare the payload to be sent in the POST request
    apiData = {
        'data': new_data,
        'path': filepath
    }
    try:
        # Send the POST request to the API endpoint with the JSON payload
        response = requests.post(api_url, json=apiData)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.RequestException as e:
        # Log or handle exceptions as needed
        print(f"Error posting data to API: {e}")
        raise
