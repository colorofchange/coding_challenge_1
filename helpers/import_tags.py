import re
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from templates_app.models import Tag
from django.conf import settings

sheet = None
SPREADSHEET_ID = "1XcosQGeuQ_YfUQm-rt_7In-WAcCSqy_Tdzth7Rv12HM"
batch = []

OTHER = 0
OWNER = 1
HELP = 2
DEPARTMENT = 3
ISSUE = 4
ASK = 5
ENTITY = 6
TARGETING = 7
CAMP = 8

def ProcessAndCreateTags(range_name, tag_type_adding):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=range_name).execute()
    values = result.get('values', [])[1:]
    if values:
        for row in values:
            if tag_type_adding=='OWN':
                original_data = row[1].strip()
                stripped_data = re.split("OWNER|Owner", row[1])[1].strip()

            elif tag_type_adding=='HELP':
                original_data = row[1].strip()
                stripped_data = re.split("HELPER|Helper", row[1])[1].strip()

            elif tag_type_adding=='DEPT':
                original_data = row[1].strip()
                if "@" in original_data:
                    stripped_data = row[1].split("@")[1].strip()
                else:
                    stripped_data = original_data

            elif (tag_type_adding=='I'):
                original_data = row[1].strip()
                stripped_data = row[1].split("*")[1].strip()

            elif (tag_type_adding=='ASK'):
                original_data = row[1].strip()
                stripped_data = row[1].strip()[1:-1]
            
            elif (tag_type_adding=='ENT'):
                original_data = row[1].strip()
                stripped_data = row[1].strip()[1:-1]

            elif (tag_type_adding=='TGT'):
                original_data = row[1].strip()
                stripped_data = row[1].split("!")[1].strip()   

            elif (tag_type_adding=='CAMP'):
                if(int(row[2]) >= 10):
                    original_data = row[1].strip()
                    if "camp" in original_data.lower():
                        stripped_data = re.split("CAMP|Camp|camp|CaMP", row[1])[1].strip()
                    else:
                        stripped_data = original_data

            elif (tag_type_adding=='OTH'):
                original_data = row[1].strip()
                stripped_data = original_data

            if not Tag.objects.filter(name=stripped_data, tag_type=tag_type_adding, source_name=original_data).exists():
                print(stripped_data)
                batch.append(Tag(name=stripped_data, tag_type=tag_type_adding, source_name=original_data))

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_console(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# ProcessAndCreateTags("owner_tags!A:B", settings.TAGS[OWNER][0])
# ProcessAndCreateTags("helper_tags!A:B", settings.TAGS[HELP][0])
# ProcessAndCreateTags("department_tags!A:B", settings.TAGS[DEPARTMENT][0])
# ProcessAndCreateTags("issue_tags!A:B", settings.TAGS[ISSUE][0])
# ProcessAndCreateTags("ask_tags!A:B", settings.TAGS[ASK][0])
# ProcessAndCreateTags("entity_tags!A:B", settings.TAGS[ENTITY][0])
# ProcessAndCreateTags("targeting_tags!A:B", settings.TAGS[TARGETING][0])
# ProcessAndCreateTags("camp_tags!A:C", settings.TAGS[CAMP][0])
# ProcessAndCreateTags("other_tags!A:B", settings.TAGS[OTHER][0])

Tag.objects.bulk_create(batch) 