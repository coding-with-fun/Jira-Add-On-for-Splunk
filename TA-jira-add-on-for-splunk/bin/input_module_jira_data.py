# encoding = utf-8

import os
import sys
import time
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth
from account_validation import AccountValidator


def validate_input(helper, definition):
    """
    Implement your own validation logic to
    validate the input stanza configurations
    """
    pass


def collect_events(helper, ew):
    """
    Implement your data collection logic here
    """
    global_account = helper.get_arg('global_account')

    key = str(helper.get_input_stanza_names())
    username = global_account.get('username')
    password = global_account.get('password')
    jira_url = global_account.get('jira_url')
    time_now = str(time.strftime('%Y/%m/%d %H:%M'))
    last_time = helper.get_check_point(key)

    if not last_time:
        last_time = "1998/01/01 00:00"
    else:
        last_time = str(last_time)

    jira_url = "http://" + str(jira_url) + "/rest/api/2/search"
    params = {'maxResults': 1000,
              'jql': "updated >= '{0}' AND updated <= '{1}'".format(
                  str(last_time),
                  str(time_now))}

    helper.log_info("Params = {}".format(params))
    response = requests.get(url=jira_url, params=params,
                            auth=HTTPBasicAuth(username, password))

    r_json = response.json()
    helper.log_info("Data is {}".format(r_json))
    for issue in r_json["issues"]:
        event = helper.new_event(json.dumps(issue), time=None, host=None,
                                 index="jira_data", source=None,
                                 sourcetype=None, done=True,
                                 unbroken=True)

        ew.write_event(event)

    helper.save_check_point(key, time_now)
