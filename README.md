# MeterThing

This Repository contains the code used to build my MeterThing website. It includes both the backend written in python using FastAPI and the frontend built with svelte. This README is used to explain how everything fits together and how to run the project.

# ChirpStack API Credentials Setup Tutorial

This tutorial will guide you through the process of setting up your API credentials file for ChirpStack, which is necessary for interacting with the ChirpStack API programmatically.

## Prerequisites

- Access to a ChirpStack server instance
- Administrative permissions to create API keys
- Basic knowledge of JSON file format
- Must have Node JS version 22.14.0 or higher installed
## Step 1: Create an API Key in ChirpStack

1. Log in to your ChirpStack web interface
2. Navigate to **API Keys** section (usually found under your user profile or in the administration panel)
3. Click on **Add API Key**
4. Enter a name for your API key (e.g., "My Application Integration")
5. Select the appropriate access rights for your needs
6. Click **Create API Key**
7. **Important**: Copy the generated API token immediately, as it will only be shown once

## Step 2: Create Your Configuration File

1. Create a new file named `chirpstack_config.json` in your project directory
2. Open the file in a text editor
3. Add the following JSON structure:

```json
{
    "server_address": "[SERVER_IP_OR_HOSTNAME]:[PORT]",
    "api_token": "[YOUR_API_TOKEN]",
    "tenant_id": "[YOUR_TENANT_ID]",
    "application_id": "[YOUR_APPLICATION_ID]",
    "device_eui": "[YOUR_DEVICE_EUI]"
}
```

## Step 3: Fill in Your Configuration Details

Replace the placeholders with your actual values:

- **server_address**: The IP address or hostname of your ChirpStack server, including the port number
- **api_token**: The API token generated in Step 1
- **tenant_id**: Your tenant ID (found in the ChirpStack web interface under Tenants)
- **application_id**: The ID of the application you want to work with (found under Applications)
- **device_eui**: The EUI of your LoRaWAN device


## Additional Resources

- [ChirpStack Documentation](https://www.chirpstack.io/docs/)
- [ChirpStack API Reference](https://www.chirpstack.io/docs/chirpstack/api/index.html)
- [LoRaWAN Device Management Best Practices](https://www.chirpstack.io/docs/guides/device-management.html)

# HOW TO RUN

## Install Fast API endpoint:
`cd backend`
`pip install -r requirements.txt`
`pip install fastapi uvicorn`

## Start the Fast API endpoint:
`cd backend`
`uvicorn app:app --reload --port 8000`

## Run the server
`cd meterthing`
`npm run dev`

I'll help you understand how your code works by breaking down the flow from backend to frontend. Let me explain the entire system architecture and how data moves through it.

# Understanding ChirpStack Integration: A Complete Overview

### The Backend Foundation: FastAPI and ChirpStack Client

The backend system starts with two main Python files: `app.py` and `chirpstack_client.py`. The `app.py` file creates a FastAPI endpoint that serves as a bridge between your frontend and the ChirpStack server.

When a request comes to `/api/devices/list`, your FastAPI server:
1. Loads configuration from `chirpstack_config.json`
2. Creates a ChirpStack client instance
3. Retrieves devices using gRPC communication
4. Transforms the device data into a simplified format
5. Returns this data as a JSON response

The `ChirpStackClient` class in `chirpstack_client.py` handles the low-level communication with the ChirpStack server using gRPC. It uses your API token and server address to authenticate and retrieve device information.

### The Frontend Architecture: Svelte and Stores

Your frontend uses Svelte's store system to manage device data. Here's how the data flows:

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

# Understanding Async/Await in Web Development

## Introduction

When building modern web applications, particularly those involving IoT devices and real-time data, one of the most important concepts to understand is asynchronous programming using `async/await`. This guide will explain what these keywords mean, why they're essential, and how they work in practice.

## The Restaurant Analogy

To understand `async/await`, imagine you're at a busy restaurant. When you order food, the waiter follows an efficient process:

1. Takes your order
2. Submits it to the kitchen 
3. Serves other tables while your food is being prepared
4. Returns when the food is ready

This is exactly how `async/await` works in programming. It allows your code to handle other tasks while waiting for slow operations (like getting data from a server) to complete. Without this capability, your application would be like a waiter who can only serve one table at a time, standing idle while waiting for each order to be prepared.

## Understanding Async/Await in Practice

Let's look at a real-world example from a Svelte component that loads IoT device data:

```typescript
onMount(async () => {
  // First action when the component loads
  console.log('Component mounted');
  
  // Wait for device data to load
  await deviceTypes.initialize();
  
  // Once data is loaded, we can use it
  console.log('Store initialized:', $deviceTypes);
});
```

In this code, the `async` keyword tells JavaScript that this function will perform operations that take time to complete. The `await` keyword marks specific points where we need to wait for something to finish before moving on.

## How Async Works in API Calls

Here's how async operations work when fetching data from an API:

```typescript
const initialize = async () => {
  try {
    // Wait for the API response
    const response = await fetch('/api/devices/list');
    
    // Wait for the JSON data to be extracted
    const data = await response.json();
    
    // Update the application with the new data
    store.set(deviceTypes);
  } catch (error) {
    console.error('Failed to fetch devices:', error);
  }
};
```

Each `await` keyword marks a point where the code needs to pause and wait for an operation to complete. However, this pause doesn't block the rest of your application - other code can continue running, just like our waiter can serve other tables while waiting for one order to be prepared.

## Async in Backend Development

The concept of async operations extends to backend development as well. Here's an example using FastAPI:

```python
@app.get("/api/devices/list")
async def list_devices():
    try:
        # Create a client to communicate with IoT devices
        client = ChirpStackClient(config['server_address'], 
                                config['api_token'], 
                                config['application_id'])
        
        # Get the device data
        devices = client.get_devices()
        
        # Process the data into a useful format
        device_list = []
        for device in devices.result:
            device_list.append({
                "name": device.name,
                "device_profile_name": device.device_profile_name,
                "dev_eui": device.dev_eui
            })
            
        return {"result": device_list}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
```

## Why Async/Await Matters

Async programming is crucial in modern web development for several reasons:

1. **Responsiveness**: Your application stays interactive even while waiting for slow operations to complete.

2. **Efficiency**: Multiple operations can happen simultaneously, like a waiter handling multiple tables.

3. **Better User Experience**: Users don't experience freezes or delays while waiting for data to load.

4. **Resource Management**: Your application can make better use of system resources by not blocking while waiting for operations to complete.

This is particularly important in IoT applications where you're dealing with:
- Network communications that may have varying response times
- Multiple devices sending data simultaneously
- Real-time data updates that shouldn't freeze the interface
- Complex operations that take time to complete

## Best Practices

When working with async/await, keep these guidelines in mind:

1. Always wrap async operations in try/catch blocks to handle errors gracefully
2. Use async/await consistently throughout your application
3. Remember that async functions always return a Promise
4. Consider the user experience when designing async operations
5. Use loading indicators to show users when operations are in progress

## Conclusion

Understanding async/await is fundamental to building modern web applications, especially those involving IoT devices and real-time data. By allowing your code to handle multiple operations efficiently without blocking, async/await enables you to create responsive, user-friendly applications that can handle complex operations smoothly.

Remember: just as a good restaurant needs efficient waiters who can handle multiple tables simultaneously, a good web application needs efficient async operations to handle multiple tasks concurrently. This approach ensures your application stays responsive and provides a smooth user experience, even when dealing with complex device communications and data processing.