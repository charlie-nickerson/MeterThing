// src/stores/deviceStore.ts
import { writable } from 'svelte/store';

interface Device {
  name: string;
  device_profile_name: string;
  dev_eui: string;
}

interface DeviceConfig {
  label: string;
  devices: string[];
  selected: string;
  deviceMap: {
    [name: string]: string;
  };
}

interface DeviceTypes {
  [key: string]: DeviceConfig;
}

function createDeviceStore() {
  const { subscribe, set, update } = writable<DeviceTypes>({});
  let initPromise: Promise<void> | null = null;

  const initialize = async () => {
    // If already initializing, return the existing promise
    if (initPromise) {
      return initPromise;
    }

    initPromise = new Promise(async (resolve, reject) => {
      try {
        console.log('Fetching devices from API...');
        const response = await fetch('/api/devices/list');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API response:', data);
        
        if (!Array.isArray(data.result)) {
          throw new Error('Invalid data format received from API');
        }
        
        const deviceTypes = data.result.reduce((acc: DeviceTypes, device: Device) => {
          const type = device.device_profile_name;
          if (!acc[type]) {
            acc[type] = {
              label: type,
              devices: [],
              selected: '',
              deviceMap: {}
            };
          }
          acc[type].devices.push(device.name);
          acc[type].deviceMap[device.name] = device.dev_eui;
          return acc;
        }, {});
        
        console.log('Final deviceTypes:', deviceTypes);
        set(deviceTypes);
        resolve();
      } catch (error) {
        console.error('Failed to fetch devices:', error);
        set({});  // Reset store on error
        reject(error);
      } finally {
        initPromise = null;  // Clear the promise so we can retry
      }
    });

    return initPromise;
  };

  return {
    subscribe,
    set,
    update,
    initialize
  };
}

export const deviceTypes = createDeviceStore();