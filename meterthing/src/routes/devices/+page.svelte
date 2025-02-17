<!-- src/routes/devices/+page.svelte -->
<script lang="ts">
    import { deviceTypes } from "../../stores/deviceStore";
    import { onMount } from "svelte";
    import { PlusCircle, Trash2 } from "lucide-svelte";
  
    let isLoading = true;
    let error: string | null = null;
  
    onMount(async () => {
      try {
        await deviceTypes.initialize();
      } catch (e) {
        error = e instanceof Error ? e.message : "Failed to load devices";
      } finally {
        isLoading = false;
      }
    });
  </script>
  
  <div class="device-config">
    <div class="content-wrapper">
      <div class="header">
        <h2>Device Configuration</h2>
        <button class="add-button">
          <PlusCircle size={20} />
          Add Device
        </button>
      </div>
  
      {#if isLoading}
        <div class="status-message">Loading devices...</div>
      {:else if error}
        <div class="status-message error">{error}</div>
      {:else}
        <div class="devices-grid">
          {#each Object.entries($deviceTypes) as [type, config]}
            <div class="device-type-card">
              <div class="card-header">
                <h3>{type}</h3>
                <span class="device-count">{config.devices.length} devices</span>
              </div>
              <div class="device-list">
                {#each config.devices as device}
                  <div class="device-item">
                    <span>{device}</span>
                    <button class="delete-button" title="Delete device">
                      <Trash2 size={16} />
                    </button>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
  
  <style>
    .device-config {
      flex: 1;
      padding: 2rem;
      overflow-y: auto;
      background: #121214;
    }
  
    .content-wrapper {
      max-width: 1400px;
      margin: 0 auto;
    }
  
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }
  
    h2 {
      color: #e2e8f0;
      font-size: 1.5rem;
      font-weight: 600;
      margin: 0;
    }
  
    .add-button {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: #3b82f6;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.375rem;
      font-size: 0.875rem;
      cursor: pointer;
      transition: background-color 0.2s;
    }
  
    .add-button:hover {
      background: #2563eb;
    }
  
    .devices-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
    }
  
    .device-type-card {
      background: #1f1f23;
      border-radius: 0.75rem;
      overflow: hidden;
      box-shadow: 0 2px 4px 0 rgb(0 0 0 / 0.4);
    }
  
    .card-header {
      padding: 1rem;
      background: #2d2d32;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    .card-header h3 {
      color: #e2e8f0;
      font-size: 1rem;
      font-weight: 500;
      margin: 0;
    }
  
    .device-count {
      color: #94a3b8;
      font-size: 0.875rem;
    }
  
    .device-list {
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
  
    .device-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem;
      background: #2d2d32;
      border-radius: 0.375rem;
      color: #e2e8f0;
    }
  
    .delete-button {
      background: transparent;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      padding: 0.25rem;
      border-radius: 0.25rem;
      transition: all 0.2s;
    }
  
    .delete-button:hover {
      color: #ef4444;
      background: rgba(239, 68, 68, 0.1);
    }
  
    .status-message {
      text-align: center;
      color: #94a3b8;
      padding: 2rem;
    }
  
    .status-message.error {
      color: #ef4444;
    }
  
    @media (max-width: 768px) {
      .device-config {
        padding: 1rem;
      }
  
      .header {
        flex-direction: column;
        gap: 1rem;
        align-items: stretch;
        text-align: center;
      }
    }
  </style>