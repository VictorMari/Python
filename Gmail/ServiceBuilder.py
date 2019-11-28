import pickle
import os.path as path
import base64
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from apiclient import errors

def generateGmailBuild():
    with open("token.pickle", 'rb') as token:
        creds = pickle.load(token)
        if creds and creds.valid:
            return build('gmail', 'v1', credentials=creds)
        if creds or not creds.valid:
            creds.refresh(Request())
        else:
            print("Creds not found")

def getEmailList(Service, **kwargs):
    try:
        response = Service.users().messages().list(**kwargs).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            kwargs['pageToken'] = response['nextPageToken']
            response = Service.users().messages().list(**kwargs).execute()
            if 'messages' in response:
                messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print(f"An error has occurred {error}")

def getEmail(Service, **kwargs):
    try:
        response = Service.users().messages().get(**kwargs).execute()
        return response
    except errors.HttpError as error:
        print(f"Error occurred {error}")

def getAttachment(Service, **kwargs):
    try:
        response = Service.users().messages().attachments().get(**kwargs).execute()
        return response
    except errors.HttpError as error:
        print(f"Error occurrend {error}")

def saveEmailAttachments(email, **kwargs):
    for part in email['payload']['parts']:
        attachment_data = None
        if part['filename'] != "":
            if 'attachmentId' in part['body']:
                params = {
                    "userId": "me",
                    "messageId": email['id'],
                    "id": part['body']['attachmentId']
                }
                attachment = getAttachment(kwargs['service'], **params)
                attachment_data = base64.urlsafe_b64decode(attachment['data'])
            
            destination = path.join(kwargs['path'], part['filename'])
            with open(destination, "wb") as file:
                file.write(attachment_data)


def main():
    Service = generateGmailBuild()
    params = {
        "userId": "me",
        "q": "from:franciscomd87@hotmail.com"}
    mail_params = {
        "userId": "me",
        "id": "159e6d5f1cbd0d3a"
    }
    attachment_params = {
        "userId": "me",
        "messageId": "159e6d5f1cbd0d3a",
        "id": "ANGjdJ96QvcxUTg3HJvbXasOrwa30q4N4xXjRtOcsqj_yvDr7q8z941Goajuu72Ua_wF0cBFQDKE_jpVr45dJpia1bDiQfipGilmKmlB50fROK4AnvSyIAD4QA2YmvRZUZSKPmJXstHNUB4llrqaic_nfZN-sp41IPdSq8NU068YINqPnRroUPcxNl8etLdBvfFjAApUUUjIqNDymvyTbHE0liyuZRUPaktGH63ZyNLbSJXyXDbxffcQ4BCsO5aDbwEHaMtKszLDDHGUSyuvYuIrVXbyaAScnd4lk8hL1AX47FGRERS8lpETS1n3FoI"
    }
    attachment_Downloader = {
        "service": Service,
        "path": "C:\\Users\\vmari\\Documents\\Attachments"
    }
    emails = getEmailList(Service, **params)
    emails = map(lambda e: getEmail(Service, userId='me', id=e['id']), emails)
    for email in emails:
        saveEmailAttachments(email, **attachment_Downloader)
if __name__ == '__main__':
    main()

