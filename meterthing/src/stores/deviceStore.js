import { readable, writable } from 'svelte/store';

export const deviceTypes = writable({
  temp: {
    label: "Temperature Device",
    devices: ["Temp1", "Temp2", "Temp3", "All Devices"],
    selected: null
  },
  turb: {
    label: "Turbidity Device", 
    devices: ["Turb1", "Turb2", "Turb3", "All Devices"],
    selected: null
  },
  detect: {
    label: "Water Detection Devices",
    devices: ["Detect1", "Detect2", "Detect3", "All Devices"],
    selected: null
  }
});