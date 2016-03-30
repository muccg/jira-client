import logging
import config
import utils

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logging.info("Welcome to JIRA Client")
logging.info("Validatating credentials...")

if not utils.validate_credentials():
    logging.error("Please check your credentials")
    exit(0)

logging.info("All good :)")

project_key = raw_input("\nProject key: ")
file_name = raw_input("File name: ")

with open(file_name, 'r') as f:
    content = [x.strip('\n') for x in f.readlines()]

logging.info("Found %d ticket numbers in file %s" % (len(content), file_name) )

for ticket in content:
    params = {}
    params["jql"] = "project=%s" % project_key
    params["jql"] = params["jql"] + " AND issue='%s'" % ticket

    search_result =  utils.get_request_auth(config._SEARCH, params)

    if search_result:
        payload = utils.add_label_payload(ticket)
        utils.put_request_auth(config._ISSUE_BY_KEY % ticket, payload)
        logging.info("Ticket %s done" % ticket)
    else:
        logging.warn("Ticket %s not found" % ticket)
