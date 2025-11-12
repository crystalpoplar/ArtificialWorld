import flask
from notify_run import Notify
import logger
import file_management

notify = Notify(endpoint='https://notify.run/t7M6m7zJ3fos7p7X1lJY')

# Initialize Flask app and logger
app = flask.Flask(__name__)
listenerLog = logger.mainLog
listenerLog.info('Listener has started')

@app.route('/api', methods=['POST'])
def post_json():
    """
    Endpoint to update a JSON file with new data.

    This function receives a POST request with JSON data containing the path to the JSON file
    and the data to be updated. It updates the JSON file with the provided data and returns a response.

    Returns:
        Response: A JSON response indicating the update status.
    """
    # Log the received request
    listenerLog.info('Received POST request to /api endpoint')
    
    # Extract data from the request
    new_data = flask.request.json
    data = new_data['data']
    path = new_data['path']
    
    # Log the details of the request
    listenerLog.info(f"Updating JSON file at path: {path} with data: {data}")
    
    # Update the JSON file
    try:
        with open(path, 'w') as f:
            f.write(str(data))
    except OSError as e:
        listenerLog.error(f"Error updating JSON file: {e}")
        response = False
        notify.send(f"Error updating JSON file: {e}")
    except Exception as e:
        listenerLog.error(f"Error updating JSON file: {e}")
        response = False
    else:
        response = True
    response = file_management.updateJsonFile(data, path)
    response = {
        'update': response
    }
    
    # Log the response
    listenerLog.info(f"Response: {response}")

    return flask.jsonify(response), 201

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)