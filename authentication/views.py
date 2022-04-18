from asyncio import exceptions
from django.http import HttpResponse
from django.shortcuts import render
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
# Create your views here.
import os
import google_apis_oauth
import datetime
from django.shortcuts import HttpResponseRedirect

# The url where the google oauth should redirect
# after a successful login.
REDIRECT_URI = 'http://localhost:8000/google_oauth/callback/'

# Authorization scopes required
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path of the "client_id.json" file
JSON_FILEPATH = os.path.join(os.getcwd(), '/Google-Calendar-Integration/client_secret.json')

def RedirectOauthView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)

def CallbackView(request):
    stringified_token=dict()
    try:
        # Get user credentials
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )
        stringified_token = google_apis_oauth.stringify_credentials(
            credentials)
    except:
        # print(exceptions)#exceptions.InvalidLoginException:
        pass
    creds,refreshed= google_apis_oauth.load_credentials(stringified_token)

    # Using credentials to access Upcoming Events
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list.execute()
    calendar_id=calendar_list['items'][0]['id']#'primary'
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 1000 events')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def home(request):
    return render(request,"fr/index.html")