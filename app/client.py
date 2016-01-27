import config
import utils

if not utils.validate_credentials():
    print "Please check your credentials"
    exit(0)

projects = utils.get_request_auth(config._PROJECTS)

print "\nProjects"
if projects:
    for project in projects:
        print " - %s (%s)" % (project["name"], project["key"])

project_key = raw_input("\nProject key: ")
search_term = raw_input("Search term (optional): ")
ticket_id = raw_input("Ticket ID (optional): ")

params = {}
params["jql"] = "project=%s" % project_key

if search_term:
    params["jql"] = params["jql"] + " AND text~'%s'" % search_term
if ticket_id:
    params["jql"] = params["jql"] + " AND issue='%s'" % ticket_id

params["maxResults"] = config._MAX_SEARCH_RESULTS
params["fields"] = ["summary",]

search_result =  utils.get_request_auth(config._SEARCH, params)

if "issues" in search_result and len(search_result["issues"]) != 0:
    print "\nTicket found:"
    issues = search_result["issues"]
    for issue in issues:
        print "%s -> %s" % (issue["key"], issue["fields"]["summary"])
        
    print "\nWould you liket to tag/label the above ticket(s) with '%s'?" % search_term
    prompt = raw_input("Proceed? [y/n] ")
    if prompt == "n":
        pass
    elif prompt == "y":
        for index, issue in enumerate(issues, start=1):
            payload = utils.add_label_payload(search_term)
            if utils.put_request_auth(config._ISSUE_BY_KEY % issue["key"], payload):
                utils.print_progress(index, len(issues))
else:
    print "\nNo tickets"

print "\n\nSee you next time!"
print "Have a good day!"
