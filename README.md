# JIRA client

Tool to access JIRA using the CLI.

## Usage from source

Run `python client.py`

## Install to run from container
jira-client is available as a Docker container from dockerhub in muccg/jiracli. 
The jiracli script will fetch and run the container when invoked.

``` sh
$ sudo -L https://raw.githubusercontent.com/muccg/jira-client/master/jiracli > /usr/local/bin/jiracli
$ sudo chmod +x /usr/local/bin/jiracli
```
Now run `jiracli`, the container will be fecthed from dockerhub if not available locally.

If used for the first time, you will be asked for your JIRA credentials. The credentials will be saved for future requests in HOME_DIR/.ccgjira

## Functionality
This is initial version of the client with limited functionality that follows the workflow:
* Retrieve all available projects for a logged in user and list them,
* User selects a project,
* User provides search term,
* Matching tickets are displayed,
* User can choose if tag/label matching tickets with serach term.
