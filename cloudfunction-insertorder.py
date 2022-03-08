

"""Background Cloud Function to be triggered by Pub/Sub.
Args:
     event (dict):  The dictionary with data specific to this type of
                    event. The `@type` field maps to
                     `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                    The `data` field maps to the PubsubMessage data
                    in a base64-encoded string. The `attributes` field maps
                    to the PubsubMessage attributes if any is present.
     context (google.cloud.functions.Context): Metadata of triggering event
                    including `event_id` which maps to the PubsubMessage
                    messageId, `timestamp` which maps to the PubsubMessage
                    publishTime, `event_type` which maps to
                    `google.pubsub.topic.publish`, and `resource` which is
                    a dictionary that describes the service API endpoint
                    pubsub.googleapis.com, the triggering topic's name, and
                    the triggering event type
                    `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
Returns:
    None. The output is written to Cloud Logging.
"""

import base64
import json
from google.cloud import spanner


# Your Cloud Spanner instance ID.
instance_id = "bitf-dev"
#
# Your Cloud Spanner database ID.
database_id = "bitf"

# Instantiate a client.
spanner_client = spanner.Client()

# Get a Cloud Spanner instance by ID.
instance = spanner_client.instance(instance_id)

# Get a Cloud Spanner database by ID.
database = instance.database(database_id)

def main_pubsub(event, context):
print("""This Function was triggered by messageId {} published at {} to {}
""".format(context.event_id, context.timestamp, context.resource["name"]))

# Print out the data from Pub/Sub, to prove that it worked
order = json.loads(base64.b64decode(event['data']))
#format insert
insert_stmt = "INSERT TradeOrders (SessionUUID,OrderUUID,CoinUUID,PlayerUUIDL,Placed, Ask,Price,UnitSize,Cancelled,Filled) VALUES {{'{}' ,'{}' ,'{}' ,'{}' ,'{}',{} ,{} ,{} ,{}, {}}}"
insert_stmt = insert_stmt.format(order['SessionUUID'],order['OrderUUID'],order['CoinUUID'],order['PlayerUUID'],order['Placed'],order['Ask'],order['Price'],order['UnitSize'],order['Cancelled'],order['Filled'])

database.run_in_transaction(insert_order, insert_stmt)
row_ct = transaction.execute_update(insert_stmt)

def insert_order(transaction,stmt):
row_ct = transaction.execute_update(stmt)
print("{} record(s) inserted.".format(row_ct))
