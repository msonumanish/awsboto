import os
import logging
import pyinotify
import boto3
from boto3.s3.transfer import S3Transfer

logging.basicConfig(filename='example.log', level=logging.INFO)

# Create an S3 client and transfer object
s3 = boto3.client('s3')
transfer = S3Transfer(s3)

# Define a class to handle the events
class TxtEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        if event.pathname.endswith('.tsbak'):
            filepath = os.path.join(event.path, event.name)
            logging.info(f"New file created: {filepath}")
            bucket_name = 'your-bucket-name'
            key_name = os.path.basename(filepath)
            callback = self.get_callback(filepath)
            transfer.upload_file(filepath, bucket_name, key_name, callback=callback)
            logging.info(f"File {key_name} uploaded to S3 bucket {bucket_name}")

    def get_callback(self, filepath):
        file_size = os.path.getsize(filepath)
        progress_size = 0
        def callback(bytes_transferred):
            nonlocal progress_size
            progress_size += bytes_transferred
            percent_complete = int((progress_size / file_size) * 100)
            logging.info(f"Uploaded {percent_complete}% of {file_size} bytes")
        return callback

# Create an instance of the notifier
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, TxtEventHandler())

# Define the directory to watch
watch_directory = "/path/to/watch"

# Define the events to watch for
mask = pyinotify.IN_CREATE

# Add the directory to the watch list
wdd = wm.add_watch(watch_directory, mask, rec=True, auto_add=True)

# Start the notifier loop
logging.info("Watching directory for new .tsbak files...")
notifier.loop()
