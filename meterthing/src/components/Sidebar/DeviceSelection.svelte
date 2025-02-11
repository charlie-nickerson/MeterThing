<!-- DeviceSelection.svelte -->
<script>
  import { deviceTypes } from "../../stores/deviceStore";
  import { onMount } from 'svelte';

  let initialized = false;
  let initializationError = null;

  async function initializeStore() {
    try {
      console.log('Initializing device store...');
      await deviceTypes.initialize();
      console.log('Store initialized:', $deviceTypes);
      initialized = true;
    } catch (error) {
      console.error('Failed to initialize device store:', error);
      initializationError = error.message;
    }
  }

  onMount(() => {
    console.log('DeviceSelection component mounted');
    if (!initialized) {
      initializeStore();
    }
  });

  function handleDeviceSelection(type, deviceName) {
    deviceTypes.update(store => {
      store[type].selected = deviceName;
      return store;
    });
  }

  $: if ($deviceTypes) {
    console.log('deviceTypes updated:', $deviceTypes);
  }
</script>

<form class="config-form">
  <div class="configurations-section">
    <h2>Chart Controls</h2>
    {#if initializationError}
      <div class="error-message">
        Failed to load devices: {initializationError}
      </div>
    {:else if !$deviceTypes || Object.keys($deviceTypes).length === 0}
      <div class="loading-message">
        Loading devices...
      </div>
    {:else}
      {#each Object.entries($deviceTypes) as [type, config]}
        <div class="form-group">
          <label for={type}>{config.label}</label>
          <select
            id={type}
            value={config.selected}
            on:change={(e) => handleDeviceSelection(type, e.target.value)}
          >
            <option value="">Select a device</option>
            {#each config.devices as name}
              <option value={name}>{name}</option>
            {/each}
          </select>
        </div>
      {/each}
    {/if}
  </div>
</form>

<style>
  .config-form {
    padding: 1rem;
    font-family: "Inter", sans-serif;
  }
  h2 {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 1.5rem;
    font-weight: 600;
    font-family: "Inter", sans-serif;
  }
  .form-group {
    margin-bottom: 1.25rem;
  }
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #e2e8f0;
    font-size: 0.875rem;
    font-weight: 500;
    font-family: "Inter", sans-serif;
  }
  select {
    width: 100%;
    padding: 0.5rem;
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 0.375rem;
    color: #e2e8f0;
    font-size: 0.875rem;
    font-family: "Inter", sans-serif;
    transition: all 0.15s ease;
  }
  select:hover {
    border-color: #475569;
  }
  select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
  }
  option {
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 0.5rem;
    font-family: "Inter", sans-serif;
  }
  .error-message {
    color: #ef4444;
    padding: 0.5rem;
    border-radius: 0.375rem;
    background-color: rgba(239, 68, 68, 0.1);
    margin-bottom: 1rem;
  }
  .loading-message {
    color: #94a3b8;
    text-align: center;
    padding: 1rem;
  }
</style>