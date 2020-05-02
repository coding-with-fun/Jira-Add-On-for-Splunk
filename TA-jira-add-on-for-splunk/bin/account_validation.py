import requests
from requests.auth import HTTPBasicAuth
from splunktaucclib.rest_handler.endpoint.validator import Validator


class JiraAccount(object):
    def __init__(self, account_name, username, password, url):
        """
        Initialize JiraAccount object
        :param account_name: Account name
        :param username: User name
        :param password: Password for the user name
        :param url: Jira URL
        """
        self.account_name = account_name
        self.username = username
        self.password = password
        self.jira_url = url.strip("").strip("https://")
        self.jira_url = "http://{}/rest/api/2/issue/createmeta".format(
            self.jira_url)

    def validate(self):
        """
        Validate the account credentials and return status code
        corresponding to the Client Name

        :return: Status code
        """

        response = requests.get(self.jira_url, auth=HTTPBasicAuth(
            self.username, self.password))
        response.raise_for_status()


class AccountValidator(Validator):
    """
    This class extends base class of Validator.
    """

    def validate(self, value, data):
        """
        We define Custom validation here for verifying credentials
        when storing account information.
        """
        try:
            Jira_account = JiraAccount(data.get("account_name"), data.get(
                "username"), data.get("password"), data.get("jira_url"))
            Jira_account.validate()

            self.put_msg("Authenticated!")

        except Exception as e:
            self.put_msg("Please enter valid account information" + str(e))
            return False

        return True
