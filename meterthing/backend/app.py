# backend/app.py
from fastapi import FastAPI
from chirpstack_client import ChirpStackClient, load_config
from datetime import datetime



app = FastAPI()
config = load_config('chirpstack_config.json')

@app.get("/api/temperature/data")
async def get_temperature_data(start_date: str, end_date: str, device_id: str = "a8610a35392c6605"):
    print(f"Received request for temperature data: {start_date} to {end_date}")
    try:
        client = ChirpStackClient(config['server_address'], config['api_token'], config['application_id'])
        client.load_aws_credentials()
        
        # Convert string dates to datetime and set time to start/end of day
        start = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        end = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        
        print(f"Querying temperature data from {start} to {end}")
        
        # Query temperature data
        data = client.query_temperature_data(
            start_time=start,
            end_time=end,
            device_id=device_id
        )
        
        print(f"Found {len(data)} temperature readings")
        return {"result": data}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    
@app.get("/api/devices/list")
async def list_devices():
    print("Received request to /api/devices/list")
    try:
        client = ChirpStackClient(config['server_address'], config['api_token'], config['application_id'])
        devices = client.get_devices()
        device_list = []
        for device in devices.result:
            device_list.append({
                "name": device.name,
                "device_profile_name": device.device_profile_name,
                "dev_eui": device.dev_eui
            })
        print(f"Returning devices: {device_list}")
        return {"result": device_list}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise