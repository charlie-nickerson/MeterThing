# backend/chirpstack_client.py
import grpc
import json
import requests
from chirpstack_api import api
from google.protobuf.json_format import ParseDict

class ChirpStackClient:
    def __init__(self, server_address, api_token, application_id):
        self.server_address = server_address
        self.api_token = api_token
        self.application_id = application_id
        
    # Keep all your existing methods here
    def create_device(self, application_id, device_profile_id, name, dev_eui, description=""):
        # Your existing method
        pass

    def delete_device(self, dev_eui):
        # Your existing method
        pass

    def get_device_metrics(self, dev_eui, start_time=None, end_time=None, aggregation=None):
        # Your existing method
        pass

    def get_devices(self):
        try:
            channel = grpc.insecure_channel(self.server_address)
            client = api.DeviceServiceStub(channel)
            metadata = [("authorization", f"Bearer {self.api_token}")]
            req = api.ListDevicesRequest()
            req.application_id = self.application_id
            req.limit = 1000
            resp = client.List(req, metadata=metadata)
            return resp
        except Exception as e:
            print(f"Error: {e}")
            return None

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        raise

# Move the test code inside this if block
if __name__ == "__main__":
    # Your test code here
    config = load_config('chirpstack_config.json')
    client = ChirpStackClient(config['server_address'], config['api_token'])
    # ... rest of your test code