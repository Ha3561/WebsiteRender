import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"]

 


def get_credentials():
    """Retrieve credentials from token.json or initiate OAuth 2.0 flow."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, prompt='consent')  # Prompt user to consent to new scopes
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_n_events(n):
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=int(n),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", []) #stores events in

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start, duration, name, and ID of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event["summary"]
            event_id = event["id"]

            # Calculate duration
            start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_time = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
            duration = end_time - start_time

            print(f"{start} ({event_id}): {summary} (Duration: {duration})")

    except HttpError as error:
        print(f"An error occurred: {error}")


def delete_event(event_id):
    """Delete a specific event from the user's calendar."""
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Event deleted successfully.")
    except HttpError as error:
        print(f"An error occurred: {error}") 


def get_series_id():
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=1,  # Just retrieve one event
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if events:
            # Extract the series ID from the first event
            series_id = events[0].get("recurringEventId")
            if series_id:
                return series_id
            else:
                print("The event is not recurring.")
        else:
            print("No events found.")
    except HttpError as error:
        print(f"An error occurred: {error}") 


def create_event():
    title = input("Enter event title: ")
    location = input("Enter event location: ")
    invitees = input("Enter invitees (separated by commas if multiple): ")
    google_meet = input("Enter Google Meet link or leave blank for no link: ")

    start_time_str = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
    end_time_str = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")

    # Validate start and end date input
    try:
        start_time = datetime.datetime.fromisoformat(start_time_str)
        end_time = datetime.datetime.fromisoformat(end_time_str)
    except ValueError:
        print("Invalid date format. Please enter dates in YYYY-MM-DD HH:MM:SS format.")
        return

    if end_time <= start_time:
        print("End time should be after start time. Please enter valid dates.")
        return

    # Optionally, ask for recurrence parameters
    recurrence = input("Do you want to make this event recurring? (Y/N): ")
    if recurrence.upper() == 'Y':
        recurrence_type = input("Enter recurrence type (daily/weekly/monthly): ")
        if recurrence_type.lower() == 'daily':
            interval = input("Enter repeat interval in days: ")
            recurrence = f"RRULE:FREQ=DAILY;INTERVAL={interval}"
        elif recurrence_type.lower() == 'weekly':
            interval = input("Enter repeat interval in weeks: ")
            days = input("Enter days of the week to repeat (e.g., MO,TU,WE): ")
            recurrence = f"RRULE:FREQ=WEEKLY;INTERVAL={interval};BYDAY={days}"
        elif recurrence_type.lower() == 'monthly':
            interval = input("Enter repeat interval in months: ")
            recurrence = f"RRULE:FREQ=MONTHLY;INTERVAL={interval}"
        elif recurrence_type.lower() == 'count':
            count = input("Enter the number of times to repeat: ")
            interval = input("Enter repeat interval in days: ")
            recurrence = f"RRULE:FREQ=DAILY;INTERVAL={interval};COUNT={count}"
        else:
            print("Invalid recurrence type. Event will not be recurring.")
            recurrence = None
    else:
        recurrence = None

    # Create event or return if not recurring
    if recurrence:
        # Create recurring event with valid input
        print("Creating recurring event...")
        # Call function to create event using the validated inputs
    else:
        # Create single event with valid input
        print("Creating single event...")
 





def main():
    # Delete an event 
    #get_n_events(10)
    #delete_event("cpij2phh6hgm8b9m6kp64b9k6srj2bb160q66b9hcgr30cr56gs3idppc8_20240313T133000Z")

    # Get upcoming events
    #get_series_id()
    #print(get_n_events(10)) 

    create_event()
     


if __name__ == "__main__":
    main()
