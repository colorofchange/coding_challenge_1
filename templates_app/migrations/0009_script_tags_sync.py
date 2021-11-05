from django.db import migrations
import os.path
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ..models import Tag
from django.conf import settings


class Migration(migrations.Migration):

    def InsertSeedData(apps, schema_editor):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SPREADSHEET_ID = "1XcosQGeuQ_YfUQm-rt_7In-WAcCSqy_Tdzth7Rv12HM"
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

        batch = []

        # PROCESS OWNER TAGS
        RANGE_NAME = "owner_tags!A:B"
        TAG_TYPE = settings.TAGS[1][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = re.split("OWNER|Owner", row[1])[1].strip()
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

         # PROCESS HELPER TAGS
        RANGE_NAME = "helper_tags!A:B"
        TAG_TYPE = settings.TAGS[2][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = re.split("HELPER|Helper", row[1])[1].strip()
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS DEPARTMENT TAGS
        RANGE_NAME = "department_tags!A:B"
        TAG_TYPE = settings.TAGS[3][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                if "@" in original_data:
                    stripped_data = row[1].split("@")[1].strip()
                else:
                    stripped_data = original_data
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS ISSUE TAGS
        RANGE_NAME = "issue_tags!A:B"
        TAG_TYPE = settings.TAGS[4][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = row[1].split("*")[1].strip()
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS ASK TAGS
        RANGE_NAME = "ask_tags!A:B"
        TAG_TYPE = settings.TAGS[5][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = row[1].strip()[1:-1]
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS ENTITY TAGS
        RANGE_NAME = "entity_tags!A:B"
        TAG_TYPE = settings.TAGS[6][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = row[1].strip()[1:-1]
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS TARGETING TAGS
        RANGE_NAME = "targeting_tags!A:B"
        TAG_TYPE = settings.TAGS[7][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = row[1].split("!")[1].strip()
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS CAMP TAGS
        RANGE_NAME = "camp_tags!A:B"
        TAG_TYPE = settings.TAGS[8][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                if "camp" in original_data.lower():
                    stripped_data = re.split(
                        "CAMP|Camp|camp|CaMP", row[1])[1].strip()
                else:
                    stripped_data = original_data
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        # PROCESS OTHER TAGS
        RANGE_NAME = "other_tags!A:B"
        TAG_TYPE = settings.TAGS[0][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])[1:]
        if values:
            for row in values:
                original_data = row[1].strip()
                stripped_data = original_data
                batch.append(
                    Tag(name=stripped_data, tag_type=TAG_TYPE, source_name=original_data))

        Tag.objects.bulk_create(batch)

    dependencies = [
        ('templates_app', '0008_tag_source_type'),
    ]

    operations = [
        # migrations.RunPython(InsertSeedData)
    ]
