# MeterThing
Just another repo to test out Chirpstack integration. My goal is to make a python rest API

# HOW TO RUN

## Install Fast API endpoint:
`cd backend`
`pip install fastapi uvicorn`

## Start the Fast API endpoint:
`uvicorn app:app --reload --port 8000`

## Run the server
`cd meterthing`
`npm run dev`

I'll help you understand how your code works by breaking down the flow from backend to frontend. Let me explain the entire system architecture and how data moves through it.

# Understanding Your ChirpStack Integration: A Complete Overview

### The Backend Foundation: FastAPI and ChirpStack Client

Your backend system starts with two main Python files: `app.py` and `chirpstack_client.py`. The `app.py` file creates a FastAPI endpoint that serves as a bridge between your frontend and the ChirpStack server.

When a request comes to `/api/devices/list`, your FastAPI server:
1. Loads configuration from `chirpstack_config.json`
2. Creates a ChirpStack client instance
3. Retrieves devices using gRPC communication
4. Transforms the device data into a simplified format
5. Returns this data as a JSON response

The `ChirpStackClient` class in `chirpstack_client.py` handles the low-level communication with the ChirpStack server using gRPC. It uses your API token and server address to authenticate and retrieve device information.

### The Frontend Architecture: Svelte and Stores

Your frontend uses Svelte's powerful store system to manage device data. Here's how the data flows:

1. The `deviceStore.ts` file creates a custom store using Svelte's `writable` store:
```typescript
function createDeviceStore() {
  const store = writable<DeviceTypes>({});
  // ... initialization logic
  return {
    subscribe: store.subscribe,
    initialize
  };
}
```

2. The store's `initialize` function fetches data from your backend API and organizes it by device type:
```typescript
const deviceTypes = data.result.reduce((acc: DeviceTypes, device: Device) => {
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
```

3. Your Svelte component connects to this store using:
```typescript
import { deviceTypes } from "../../stores/deviceStore";
```

### The UI Component

Your Svelte component uses reactive statements and the store to render a dynamic form:

```svelte
onMount(async () => {
  await deviceTypes.initialize();
});
```

When the component mounts, it initializes the store, which triggers the API call. The `$` prefix in `$deviceTypes` is Svelte's auto-subscription syntax - it automatically handles subscribing and unsubscribing to the store.

The template section creates a form that:
1. Checks if device types exist (`{#if $deviceTypes}`)
2. Iterates through each device type (`{#each Object.entries($deviceTypes) as [type, config]}`)
3. Creates a select dropdown for each type, populated with that type's devices
4. Uses two-way binding with `bind:value` to keep the UI and store in sync

### API Communication Setup

Your `vite.config.ts` sets up a development proxy that forwards API requests to your FastAPI backend:

```typescript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',
    changeOrigin: true
  }
}
```

This means when your frontend makes a request to `/api/devices/list`, it actually goes to `http://127.0.0.1:8000/api/devices/list` during development.

### The Complete Data Flow

1. User loads the page
2. Component mounts and calls `deviceTypes.initialize()`
3. Initialize function makes an API request to `/api/devices/list`
4. Request is proxied to your FastAPI backend
5. Backend creates ChirpStack client and retrieves devices
6. Data flows back to frontend
7. Store processes and organizes the data
8. Svelte reactively updates the UI with the new data
9. User sees dropdowns populated with their devices, organized by type

This architecture creates a clean separation of concerns while maintaining reactive data flow throughout your application.