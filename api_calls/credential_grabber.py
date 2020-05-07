import yaml

class GrabCredentials(object):

    def __init__(self, credential_yaml):

        self.credential_yaml = credential_yaml

        self.app_token = None

        self.user = None

        self.password = None

    def populate_credentials(self):

        with open(self.credential_yaml, 'r') as file:

            credentials = yaml.load(file, Loader=yaml.FullLoader)

#        assert set(['email', 'password', 'appToken']) in credentials

        for key in credentials:

            assert credentials[key] is not None, "Missing {missing} in credential file".format(missing=key)

        self.app_token = credentials['appToken']

        self.user = credentials['user']

        self.password = credentials['password']

credential_grabber = GrabCredentials("api_calls/.credentials.yml")

credential_grabber.populate_credentials()

