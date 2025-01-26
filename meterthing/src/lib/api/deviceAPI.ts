interface ChirpstackDevice {
  name: string;
  device_profile_name: string;
  dev_eui: string;
}

export async function fetchDevices() {
  const response = await fetch('/api/devices/list');
  const data = await response.json();
  return data.result.map((device: ChirpstackDevice) => ({
    name: device.name,
    type: device.device_profile_name,
    devEui: device.dev_eui
  }));
}