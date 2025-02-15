<!-- // src/components/WaterDetectionTable.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { deviceTypes } from '../../stores/deviceStore';
  import { dateRange } from '../../stores/dateStore';
  import DownloadButton from '../DownloadButton.svelte';
  import type { WaterData } from '../../lib/api/waterAPI';

  let displayState: 'initial' | 'loading' | 'error' | 'data' = 'initial';
  let errorMessage = '';
  let currentDeviceId: string | undefined;
  let waterData: WaterData[] = [];
  let tableTitle = 'Water Detection Data';

  async function fetchWaterData(startDate: string, endDate: string, deviceId?: string) {
    if (!deviceId) return null;

    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      ...(deviceId && { device_id: deviceId })
    });
    
    const response = await fetch(`/api/water/data?${params}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return (await response.json()).result;
  }

  async function fetchAndUpdateData() {
    if (!currentDeviceId) {
      displayState = 'initial';
      return;
    }

    displayState = 'loading';
    
    try {
      const data = await fetchWaterData(
        $dateRange.start,
        $dateRange.end,
        currentDeviceId
      );
      
      if (!data || data.length === 0) {
        waterData = [];
        errorMessage = 'No data available for selected date range';
        displayState = 'error';
        return;
      }
      
      waterData = [...data].sort((a, b) => 
        new Date(a.Timestamp).getTime() - new Date(b.Timestamp).getTime()
      );
      
      displayState = 'data';
      
    } catch (e) {
      console.error('Error fetching water detection data:', e);
      waterData = [];
      errorMessage = e instanceof Error ? e.message : 'Failed to load water detection data';
      displayState = 'error';
    }
  }

  // Handle device changes
  $: {
    if ($deviceTypes) {
      const waterDevice = Object.entries($deviceTypes).find(([key]) =>
        key.toLowerCase().includes('water')
      );
      
      if (waterDevice) {
        const [_, config] = waterDevice;
        tableTitle = config.selected
          ? `${config.selected}`
          : 'Water Detection Data';
          
        currentDeviceId = config.selected ? config.deviceMap[config.selected] : undefined;
        
        if (currentDeviceId) {
          fetchAndUpdateData();
        }
      }
    }
  }

  // Handle date range changes
  $: if ($dateRange && currentDeviceId) {
    fetchAndUpdateData();
  }

  onMount(() => {
    if (currentDeviceId) {
      fetchAndUpdateData();
    }
  });
</script>

<div class="water-table-wrapper">
  <div class="table-header">
    <h2>{tableTitle}</h2>
    <DownloadButton 
      data={waterData}
      disabled={displayState !== 'data'}
      dataType="water"
      fileName="water-detection-data"
    />
  </div>
  
  <div class="table-container">
    {#if displayState === 'data' && waterData.length > 0}
      <div class="grid-table-container">
        <div class="grid-table-header">
          <div class="header-cell">Date</div>
          <div class="header-cell">Time</div>
          <div class="header-cell">Water Detected</div>
          <div class="header-cell">Device ID</div>
        </div>
        <div class="grid-table-body">
          {#each waterData as reading}
            <div class="grid-table-row">
              <div class="grid-cell">{reading.Date}</div>
              <div class="grid-cell">{reading.Time}</div>
              <div class="grid-cell">
                <span class="{reading.WaterDetected ? 'text-red-500' : 'text-green-500'}">
                  {reading.WaterDetected.toString()}
                </span>
              </div>
              <div class="grid-cell font-mono">{reading.DeviceID}</div>
            </div>
          {/each}
        </div>
      </div>
    {:else}
      <div class="overlay" class:error={displayState === 'error'}>
        {#if displayState === 'loading'}
          Loading data...
        {:else if displayState === 'error'}
          {errorMessage}
        {:else}
          Select a device to view water detection data
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .water-table-wrapper {
    background: #1f1f23;
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 2px 4px 0 rgb(0 0 0 / 0.4);
  }
  
  .table-header {
    padding: 1.5rem 1.5rem 0 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  h2 {
    font-size: 1.125rem;
    font-weight: 500;
    color: #e2e8f0;
    font-family: "Inter", system-ui, sans-serif;
    margin: 0;
  }
  
  .table-container {
    padding: 1.5rem;
    position: relative;
    min-height: 350px;
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(31, 31, 35, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2;
    color: #94a3b8;
    font-family: "Inter", system-ui, sans-serif;
    text-align: center;
    padding: 1rem;
  }
  
  .error {
    color: #ef4444;
  }

  .grid-table-container {
    width: 100%;
    border: 1px solid #2d2d32;
    border-radius: 4px;
    overflow-x: auto;
  }

  .grid-table-header {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background-color: #2d2d32;
    border-bottom: 1px solid #2d2d32;
  }

  .header-cell {
    padding: 12px 16px;
    color: #e2e8f0;
    font-weight: 500;
    text-align: left;
    font-size: 14px;
  }

  .grid-table-body {
    max-height: 400px;
    overflow-y: auto;
  }

  .grid-table-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border-bottom: 1px solid #2d2d32;
    transition: background-color 0.2s;
  }

  .grid-table-row:hover {
    background-color: #2d2d32;
  }

  .grid-cell {
    padding: 12px 16px;
    color: #e2e8f0;
    font-size: 14px;
    text-align: left;
    display: flex;
    align-items: center;
  }
</style>