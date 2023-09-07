from src import app
import logging

bucket_name = 'reschedule-call-bucket'
object_key = 'unanswered/schedule_call.xlsx'
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def main(event,context):

    logger.info("Event : {}".format(event))
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(event['Records'])

    # Bucket = "reschedule-call-bucket"
    # Key = "schedule_call.xlsx"

    input_file = app.get_file_from_s3(bucket_name, object_key)
    
    num_of_sheets = 9
    app.split_numbers(input_file, num_of_sheets)


    initialTimestamp = "2030-08-31T09:00:00+08:00"
    split_batches = app.split_numbers(input_file, num_of_sheets)
    app.hourUpload(initialTimestamp,split_batches)


if __name__ == "__main__":
   main()



