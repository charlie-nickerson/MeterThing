# backend/app.py
from fastapi import FastAPI
from chirpstack_client import ChirpStackClient, load_config

app = FastAPI()
config = load_config('chirpstack_config.json')

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