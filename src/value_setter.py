import os
import logging

if 'appdata' not in os.environ:
    mainDir = 'ArtificianWorld/'
    indicatorDir = mainDir + 'indicators/'
    inputsDir = mainDir + 'inputs/'
    imagesDir = mainDir + 'images/'
    archiveDir = mainDir + 'archive/'
    loggingDir = mainDir + 'logging/'
else:
    mainDir = os.environ['appdata'] + '\\ArtificialWorld\\'
    indicatorDir = mainDir + 'indicators\\'
    inputsDir = mainDir + 'inputs\\'
    imagesDir = mainDir + 'images\\'
    archiveDir = mainDir + 'archive\\'
    loggingDir = mainDir + 'logging\\'

# Configure logging
logging.basicConfig(
    filename=os.path.join(mainDir, 'directory_creation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def createDirs():
    """
    Creates the required directories if they do not exist.

    Directories:
        - mainDir: Base directory for the application.
        - indicatorDir: Directory for storing indicator files.
        - inputsDir: Directory for input files.
        - imagesDir: Directory for image files.
        - archiveDir: Directory for archived files.
        - loggingDir: Directory for log files.

    Logs:
        - Logs the creation of directories.
        - Logs warnings if a directory already exists.
        - Logs errors if directory creation fails.
    """
    dirs = [mainDir, indicatorDir, inputsDir, imagesDir, archiveDir, loggingDir]
    for dir in dirs:
        dir_path = dir.strip('\\')  # Normalize directory path
        try:
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)  # Use makedirs to create intermediate directories if needed
                logging.info(f"Created required directory: {dir_path}")
                print(f"Created required directory: {dir_path}")
            else:
                logging.warning(f"Directory already exists: {dir_path}")
        except OSError as e:
            logging.error(f"Failed to create directory {dir_path}: {e}")
            print(f"Error: Could not create directory {dir_path}. Check logs for details.")

createDirs()
