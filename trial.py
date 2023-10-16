from flask import Flask, render_template, request
import requests
import json
import pandas as pd
import webbrowser
import subprocess
import os

app = Flask(__name__)
# base_url = "https://iics-icinq1.informaticacloud.com/ma/api/v2"
all_activity_log_data = []

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
credentials = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        base_url = request.form['base_url']
        orgId = request.form['orgId']
        typev = request.form['typev']
        selected_options = request.form.getlist("options")
        DataF = list(selected_options)

        credentials = {
            "username": username,
            "password": password
        }
        if (base_url[-1] == '/'):
            base_url += "ma/api/v2"
        else:
            base_url += "/ma/api/v2"

        trial(base_url, credentials, typev, DataF,orgId)

        project_path = os.getcwd()
        project_path += r'\filtered_data.xlsx'
        return project_path + " Successfully Created"

    return render_template('index.html')


def login_and_get_session_id(base_url, credentials):
    login_url = f"{base_url}/user/login"

    try:
        response = requests.post(login_url, headers=headers, json=credentials)
        response.raise_for_status()
        data = response.json()
        session_id = data.get("icSessionId")
        server_url = data.get("serverUrl")

        if session_id:
            print("--", session_id)
            return session_id, server_url
        else:
            print("Session ID not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Login Request failed: {e}")
        return None


def get_activity_log(session_id, server_url,orgId):
    all_activity_log_data=[]
    IICS_URL = server_url.replace("saas", "")
    activity_log_url = f"{server_url}/api/v2/activity/activityLog"

    max = 1000
    batch = int(max / 50)
    start = 0

    while start <= batch:
        url = IICS_URL + "jls-di/api/v1/Orgs('" + {orgId} + "')/JobLogEntries?$filter=" \
                                                                             "(assetType eq 'MTT')" + "&$skip=" + str(start * 200) + "&$top=200"

        api_header = {'Content-Type': 'application/json',
                       'IDS-SESSION-ID': session_id,
                       'Accept': 'application/json'}

        response = requests.request(url, headers=api_header)

        # response2 = requests.get(activity_log_url, headers=api_headers)

        response.raise_for_status()

        data = response.json()
        all_activity_log_data.append(data)

    return all_activity_log_data


def trial(base_url, credentials, typev, DataF,orgId):
    session_id, server_url = login_and_get_session_id(base_url, credentials)
    print(server_url)

    if session_id:
        activity_log = get_activity_log(session_id, server_url,orgId)

        if activity_log:
            # print(json.dumps(activity_log, indent=4))
            filtered_df = [entry for entry in activity_log if
                           entry["type"] == typev and entry["state"] == 1]
            df = pd.DataFrame(filtered_df)

            df["objectName_runId"] = df["objectName"] + "_" + df["runId"].astype(str)
            df["startTime"] = pd.to_datetime(df["startTime"])
            df["endTime"] = pd.to_datetime(df["endTime"])
            df["startTime"] = df["startTime"].dt.tz_localize(None)
            df["endTime"] = df["endTime"].dt.tz_localize(None)

            df["duration"] = (df["endTime"] - df["startTime"]).dt.total_seconds()
            df["RowsPerSecond"] = df["successTargetRows"] / df["duration"]

            # filtered_df = df[df['type'] == 'MTT']
            # filtered_df = df[df['state'] == 1]
            # filtered_df = df[
            #       ['objectName_runId','type', 'state', 'startTime', 'endTime', 'duration', 'successTargetRows','runContextType']]
            filtered_df = df[DataF]

            output_file = "filtered_data.xlsx"
            filtered_df.to_excel(output_file, engine='openpyxl')

            print(f"Filtered data saved to {output_file}")

        else:
            print("Failed to retrieve the activity log.")
    else:
        print("Login failed. Session ID not obtained.")


def openURL():
    webbrowser.open('http://localhost:3000')


if __name__ == '__main__':
    openURL()
    app.run(debug=True, host='localhost', port=3000)


