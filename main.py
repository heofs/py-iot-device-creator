import argparse
import io
import os
import sys
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud import iot_v1
from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

project_id = "henofs-project"
cloud_region = "europe-west1"
registry_id = "sensor-register"
service_account_json = "./service_account.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json


def create_rs256_device(device_id, certificate_file):
    """Create a new device with the given id, using RS256 for
    authentication."""
    # [START iot_create_rsa_device]
    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': device_id,
        'credentials': [{
            'public_key': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    return client.create_device(parent, device_template)
    # [END iot_create_rsa_device]


def list_devices():
    """List all devices in the registry."""
    # [START iot_list_devices]
    print('Listing devices')

    client = iot_v1.DeviceManagerClient()
    registry_path = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(parent=registry_path))
    for device in devices:
        print('Device: {} : {}'.format(device.num_id, device.id))

    return devices
    # [END iot_list_devices]


print(list_devices())
