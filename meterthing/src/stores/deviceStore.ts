import { writable } from 'svelte/store';
import { fetchDevices } from '../lib/api/deviceAPI';

interface Device {
  name: string;
  device_profile_name: string;
  dev_eui: string;
}

interface DeviceConfig {
  label: string;
  devices: string[];
  selected: string;
}

interface DeviceTypes {
  [key: string]: DeviceConfig;
}

function createDeviceStore() {
  const store = writable<DeviceTypes>({});

  const initialize = async () => {
    try {
      const response = await fetch('/api/devices/list');
      const data = await response.json();
      console.log('API response:', data);
      
      const deviceTypes = data.result.reduce((acc: DeviceTypes, device: Device) => {
        console.log('Processing device:', device);
        const type = device.device_profile_name;
        if (!acc[type]) {
          acc[type] = {
            label: type,
            devices: [],
            selected: ''
          };
        }
        acc[type].devices.push(device.name);
        return acc;
      }, {});
      
      console.log('Final deviceTypes:', deviceTypes);
      store.set(deviceTypes);
    } catch (error) {
      console.error('Failed to fetch devices:', error);
    }
  };

  return {
    subscribe: store.subscribe,
    initialize
  };
}


export const deviceTypes = createDeviceStore();