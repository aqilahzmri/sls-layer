try:
    import unzip_requirements
except ImportError:
    pass

import pandas as pd
import xlsxwriter
from openpyxl import load_workbook
import json
import pandas as pd
from datetime import datetime, timedelta, date
import uuid
import boto3
import os
from random import shuffle


TABLE_NAME= os.environ["TABLE_NAME"]
REGION= os.environ["REGION"]


dynamodb = boto3.resource("dynamodb",region_name= REGION)
table= dynamodb.Table(TABLE_NAME)

def split_numbers(input_file, num_of_sheets):
    # Load the original Excel file into a DataFrame
    original_data = pd.read_excel(input_file)

    # Randomize the order of rows
    rows = original_data.index.tolist()
    shuffle(rows)
    randomized_data = original_data.loc[rows].reset_index(drop=True)

    # Convert phone_number to strings to ensure it's saved as text. Helps to avoid unexpected formatting
    randomized_data['Phone_Number'] = randomized_data['Phone_Number'].apply(lambda x: str(int(x)))

    # Calculate the total number of rows
    total_rows = randomized_data.shape[0]

    # Calculate the base batch size and the remainder
    base_batch_size = total_rows // num_of_sheets
    remainder = total_rows % num_of_sheets

    # Create a list to store batch DataFrames
    batches_list = []

    # Loop through each batch and store it in the list
    start_idx = 0
    for i in range(num_of_sheets):
        batch_size = base_batch_size + 1 if i < remainder else base_batch_size
        end_idx = start_idx + batch_size
        batch = randomized_data.iloc[start_idx:end_idx].copy()  # Make a copy to avoid SettingWithCopyWarning
        batches_list.append(batch)
        start_idx = end_idx
    return batches_list

def hourUpload(initialTimestamp, split_batches):
    for sheet_index, batch_df in enumerate(split_batches, start=1):
        dt = datetime.strptime(initialTimestamp, '%Y-%m-%dT%H:%M:%S+08:00')
        t_list = []
        uid = []
        Schedule_ID = []

        for i in range(len(batch_df)):
            result1 = dt + timedelta(hours=sheet_index - 1, minutes=i)
            strf = datetime.strftime(result1, '%Y-%m-%dT%H:%M:%S+08:00')
            schedule_id = "Reschedule"
            t_list.append(strf)
            id = uuid.uuid4()
            uid.append(id)
            Schedule_ID.append(schedule_id)

        batch_df["Session_ID"] = uid
        batch_df["Phone_Number"] = "+" + batch_df["Phone_Number"].astype(str)
        batch_df["Policy_Number"]
        batch_df["Schedule_Call_Timestamp"] = t_list
        batch_df["Schedule_ID"] = Schedule_ID
        column_order = ["Session_ID", "Phone_Number", "Policy_Number", "Schedule_Call_Timestamp", "Schedule_ID"]
        batch_df = batch_df[column_order]

        json_x = batch_df.to_json(orient="records", default_handler=str)
        records = json.loads(json_x)

        B = 0
        for num in records:
            num["Session_ID"]
            num["Phone_Number"]
            num["Policy_Number"]
            num["Schedule_Call_Timestamp"]
            num["Schedule_ID"]
            response=table.put_item(Item=num)
            print(num)
            B += 1

        print(f'Batch {sheet_index}: {B} Data successfully uploaded !')

def get_file_from_s3(bucket_name, object_key):

    s3 = boto3.client("s3",region_name='ap-southeast-1')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_contents = response['Body'].read()
    print(file_contents)
    return file_contents


