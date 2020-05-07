import pandas as pd
import datetime
from api_calls.credential_grabber import GrabCredentials
from sodapy import Socrata

# File specified file for credentials
credential_path = "api_calls/.credentials.yml"

credential_grab = GrabCredentials(credential_path)

# get credentials from hidden yaml
credential_grab.populate_credentials()

# Unauthenticated client only works with public raw_data sets. Note 'None'
# in place of application token, and no username or password:

client = Socrata("raw_data.cityofchicago.org",
                 credential_grab.app_token,
                 username=credential_grab.user,
                 password=credential_grab.password)

results = client.get("yhhz-zm2v")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#get current date

current_date = datetime.date.today()

results_df.to_csv("raw_data/chicago_covid_data {date}.csv".format(date=current_date))