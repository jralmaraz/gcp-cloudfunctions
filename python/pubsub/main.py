import base64
import json
import os

from google.cloud import pubsub_v1
from google.cloud import secretmanager
from google.auth import jwt
#from flask import abort

# Instantiates a Pub/Sub client

project_id = os.environ.get('project_id', 'Specified environment variable is not set.')
project_number = os.environ.get('project_number', 'Specified environment variable is not set.') 

# [START functions_pubsub_subscribe]
# Publishes a message to a Cloud Pub/Sub topic.
# Triggered from a message on a Cloud Pub/Sub topic.

def subscribe(event, context):
# Background Cloud Function to be triggered by Pub/Sub.
#     Args:
#          event (dict):  The dictionary with data specific to this type of
#                         event. The `@type` field maps to
#                          `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
#                         The `data` field maps to the PubsubMessage data
#                         in a base64-encoded string. The `attributes` field maps
#                         to the PubsubMessage attributes if any is present.
#          context (google.cloud.functions.Context): Metadata of triggering event
#                         including `event_id` which maps to the PubsubMessage
#                         messageId, `timestamp` which maps to the PubsubMessage
#                         publishTime, `event_type` which maps to
#                         `google.pubsub.topic.publish`, and `resource` which is
#                         a dictionary that describes the service API endpoint
#                         pubsub.googleapis.com, the triggering topic's name, and
#                         the triggering event type
#                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
#     Returns:
#         None. The output is written to Cloud Logging.
#     
    target_topic_name = os.environ.get('target_topic_name', 'Specified environment variable is not set.') 
    target_project_id = os.environ.get('target_project_id', 'Specified environment variable is not set.') 
    
    #print(f'This is how the message got here {event}')

    notification_payload = base64.b64decode(event['data']).decode('utf-8')

    #print(f'This is the decoded payload looks like {notification_payload}')

    notification_request = json.dumps(notification_payload)

    #print(f'This is the String serialised JSON Object {notification_request}')

    if not target_topic_name or not notification_payload:
        return ('Missing "topic" and/or "message" parameter.', 400)

    # Publishes a message
    try:
        print(f'Publishing message to topic {target_topic_name} on project {target_project_id}')
        publisher = pubsub_v1.PublisherClient()
        # References an existing topic
        topic_path = publisher.topic_path(target_project_id, target_topic_name)
        
        try:
            notification_request_encoded = notification_payload.encode()
            #print(f'This is the encoded notification that will be sent to SRE {notification_request_encoded}')
            publish_future = publisher.publish(topic_path, notification_request_encoded)
            publish_future.result()  # Verify the publish succeeded
            return 'Message published.'
        except Exception as e:
            print(e)
            return (e, 500)
    except Exception as e:
        print(e)
        return (e, 500)
