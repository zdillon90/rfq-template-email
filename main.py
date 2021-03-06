from __future__ import print_function

import os.path
from re import sub
import json
from email.mime.text import MIMEText
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


template = """
Account:
Model(s):
Directional Quote [D] or Production [P]:
# of Models to Quote (Quantity):
Quantities to quote of each Model:
Technology:
Material:
Finish:
Expected Lead Time:
Additional Instructions/Comments:
End Use:
"""


def create_message(sender, to, subject, message_text, message_id, thread_id):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['Subject'] = subject
    message['threadId'] = thread_id
    message['In-Reply-To'] = message_id
    message['References'] = message_id
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode(), 'threadId': thread_id}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)


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
            t_data = service.users().threads().get(
                userId='me', id=thread_id).execute()
            n_msgs = len(t_data['messages'])
            with open('output.json', 'w') as outfile:
                json.dump(t_data, outfile)

            if n_msgs == 1:
                print(thread_id)
                msg = t_data['messages'][0]['payload']
                subject = ''
                from_email = ''
                to_email = ''
                message_id = ''
                for header in msg['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                for header in msg['headers']:
                    if header['name'] == 'From':
                        from_email = header['value']
                        break
                for header in msg['headers']:
                    if header['name'] == 'To':
                        to_email = header['value']
                        break
                for header in msg['headers']:
                    if header['name'] == 'Message-ID':
                        message_id = header['value']
                        break
                # TODO: Add reply to email here
                print(subject)
                print(message_id)
                template_msg = create_message(
                    from_email, to_email, subject, template, message_id, thread_id)
                send_message(service, 'me', template_msg)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
