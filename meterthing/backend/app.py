# backend/app.py
from fastapi import FastAPI
from chirpstack_client import ChirpStackClient, load_config
from datetime import datetime



app = FastAPI()
config = load_config('chirpstack_config.json')

# Define request model
class CreateDeviceRequest(BaseModel):
    device_profile_id: str
    name: str
    dev_eui: str
    description: str = ""
    join_eui: str = "0000000000000000"
    is_disabled: bool = False
    skip_fcnt_check: bool = True
    tags: Optional[Dict[str, str]] = None
    variables: Optional[Dict[str, str]] = None

@app.post("/api/devices/create")
async def create_device(device_data: CreateDeviceRequest):
    print(f"Received request to create device: {device_data.name}")
    try:
        client = ChirpStackClient(config['server_address'], config['api_token'], config['application_id'])
        
        response = client.create_device(
            application_id=config['application_id'],
            device_profile_id=device_data.device_profile_id,
            name=device_data.name,
            dev_eui=device_data.dev_eui,
            description=device_data.description,
            join_eui=device_data.join_eui,
            is_disabled=device_data.is_disabled,
            skip_fcnt_check=device_data.skip_fcnt_check,
            tags=device_data.tags,
            variables=device_data.variables
        )
        
        print(f"Device created successfully: {device_data.name}")
        return {"status": "success", "message": f"Device {device_data.name} created successfully"}
    except Exception as e:
        print(f"Error creating device: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating device: {str(e)}")

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

@app.get("/api/water/data")
async def get_water_data(start_date: str, end_date: str, device_id: str = "a8610a3432436a0f"):
    print(f"Received request for water detection data: {start_date} to {end_date}")
    try:
        client = ChirpStackClient(config['server_address'], config['api_token'], config['application_id'])
        client.load_aws_credentials()
        
        start = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        end = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        
        print(f"Querying water detection data from {start} to {end}")
        
        data = client.query_water_data(
            start_time=start,
            end_time=end,
            device_id=device_id
        )
        
        print(f"Found {len(data)} water detection readings")
        return {"result": data}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise