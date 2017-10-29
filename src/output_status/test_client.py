import xmlrpc.client
import src.irulez.log as log

logger = log.get_logger('button')

logger.debug("Before 1")
with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as proxy:
    for x in range(0, 16):
        logger.info(str(proxy.pin_status("DEMO", x)))


logger.debug("After 1")

logger.debug("Before 2")
proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000/")
multi_call = xmlrpc.client.MultiCall(proxy)
for x in range(0, 16):
    multi_call.pin_status("DEMO", 0)
result = multi_call()
logger.debug("After 2")
logger.info(str(tuple(result)))


logger.debug("Before 3")
with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as proxy:
    status = proxy.arduino_status("DEMO")
logger.debug(status)
logger.debug("After 3")
