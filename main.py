from __future__ import print_function

import os.path
from re import sub

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def send_email():
    # Reply to the specific thread with the RFQ template
    pass


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        threads = service.users().threads().list(
            userId='me', q='to:zach@shapeways.com from:zdillon90@gmail.com subject:rfq-test').execute().get('threads', [])
        for thread in threads:
            thread_id = thread['id']
            tdata = service.users().threads().get(
                userId='me', id=thread_id).execute()
            nmsgs = len(tdata['messages'])

            if nmsgs == 1:
                # TODO: Add reply to email here
                send_email(thread_id)

                msg = tdata['messages'][0]['payload']
                subject = ''
                print(thread_id)
                for header in msg['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                if subject:
                    print('%s (%d messages)' % (subject, nmsgs))
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
