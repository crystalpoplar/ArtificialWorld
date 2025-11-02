import logging
import concurrent_log_handler
import value_setter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
mainLog = logging.getLogger(__name__)

handler=concurrent_log_handler.ConcurrentRotatingFileHandler(value_setter.loggingDir+'main.log', 'a', maxBytes=50000, backupCount=5)
handler.setLevel(logging.INFO)
mainLog.addHandler(handler)
