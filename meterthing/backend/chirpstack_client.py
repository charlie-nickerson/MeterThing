import grpc
import json
import os
import requests
import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from chirpstack_api import api
from google.protobuf.json_format import ParseDict

class ChirpStackClient:
    def __init__(self, server_address, api_token, application_id):
        self.server_address = server_address
        self.api_token = api_token
        self.application_id = application_id
        self.dynamodb = None
        
    def load_aws_credentials(self, credentials_file='credentials.json'):
        """Load AWS credentials from a JSON file and initialize DynamoDB connection"""
        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            
            # Set environment variables
            os.environ['AWS_ACCESS_KEY_ID'] = credentials['aws_access_key_id']
            os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['aws_secret_access_key']
            os.environ['AWS_DEFAULT_REGION'] = credentials['aws_region']
            
            # Initialize DynamoDB resource
            self.dynamodb = boto3.resource('dynamodb')
            
        except Exception as e:
            print(f"Error loading AWS credentials: {str(e)}")
            raise

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

    def query_temperature_data(self, start_time=None, end_time=None, device_id="a8610a35392c6605"):
        """
        Query temperature data from DynamoDB for a specific device and time range.
        
        Args:
            start_time (datetime): Start time for the query range
            end_time (datetime): End time for the query range
            device_id (str): Device ID to query for
            
        Returns:
            list: List of temperature readings
        """
        if not device_id:
            raise ValueError("device_id cannot be empty")
        
        if not self.dynamodb:
            raise RuntimeError("AWS credentials not loaded. Call load_aws_credentials() first")
        
        try:
            table = self.dynamodb.Table('TemperatureTable')
            
            # Default to last 24 hours if no time range specified
            if not start_time:
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=24)
            
            # Format timestamps as strings to match table format
            start_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Query parameters
            query_params = {
                'KeyConditionExpression': 
                    Key('DeviceID').eq(device_id) & 
                    Key('Timestamp').between(start_timestamp, end_timestamp),
                'ScanIndexForward': True  # True for ascending, False for descending
            }
            
            # Execute query
            response = table.query(**query_params)
            items = response['Items']
            
            # Handle pagination
            while 'LastEvaluatedKey' in response:
                query_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = table.query(**query_params)
                items.extend(response['Items'])
            
            return items
            
        except Exception as e:
            print(f"Error querying DynamoDB: {str(e)}")
            return []
        
    def query_water_data(self, start_time=None, end_time=None, device_id="a8610a3432436a0f"):
        """
        Query water detection data from DynamoDB for a specific device and time range.
        """
        if not device_id:
            raise ValueError("device_id cannot be empty")
        
        if not self.dynamodb:
            raise RuntimeError("AWS credentials not loaded. Call load_aws_credentials() first")
        
        try:
            table = self.dynamodb.Table('WaterDetectionTable')
            
            if not start_time:
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=24)
            
            start_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
            end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S')
            
            query_params = {
                'KeyConditionExpression': 
                    Key('DeviceID').eq(device_id) & 
                    Key('Timestamp').between(start_timestamp, end_timestamp),
                'ScanIndexForward': True
            }
            
            response = table.query(**query_params)
            items = response['Items']
            
            while 'LastEvaluatedKey' in response:
                query_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = table.query(**query_params)
                items.extend(response['Items'])
            
            return items
            
        except Exception as e:
            print(f"Error querying DynamoDB: {str(e)}")
            return []

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        raise

if __name__ == "__main__":
    # Test code
    config = load_config('chirpstack_config.json')
    client = ChirpStackClient(config['server_address'], config['api_token'], config['application_id'])
    
    # Load AWS credentials
    client.load_aws_credentials()
    
    # Test temperature query for the last hour
    end = datetime.now()
    start = end - timedelta(hours=1)
    
    results = client.query_temperature_data(
        start_time=start,
        end_time=end
    )
    
    for item in results:
        print(f"Time: {item['Timestamp']}, "
              f"Temperature: {item['Temperature']}, "
              f"DeviceID: {item['DeviceID']}")