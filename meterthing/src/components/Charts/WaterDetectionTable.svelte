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
      <div class="data-grid">
        <!-- Headers -->
        <div class="header-row">
          <div class="header-cell">Date</div>
          <div class="header-cell">Time</div>
          <div class="header-cell">Water Detected</div>
        </div>
        
        <!-- Data Rows -->
        {#each waterData as reading}
          <div class="data-row">
            <div class="data-cell">{reading.Date}</div>
            <div class="data-cell">{reading.Time}</div>
            <div class="data-cell">
              <span class="{reading.WaterDetected ? 'text-red-500' : 'text-green-500'}">
                {reading.WaterDetected.toString()}
              </span>
            </div>
          </div>
        {/each}
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

  .data-grid {
    border: 1px solid #2d2d32;
    border-radius: 4px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    max-height: 350px;
    overflow-y: auto;
    scrollbar-width: none;  /* For Firefox */
    -ms-overflow-style: none;  /* For Internet Explorer and Edge */
  }

  .data-grid::-webkit-scrollbar {
    display: none;  /* For Chrome, Safari and Opera */
  }

  .header-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background-color: #2d2d32;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .header-cell {
    padding: 12px 16px;
    font-weight: 500;
    color: #e2e8f0;
    text-align: center;
    font-size: 14px;
  }

  .data-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-bottom: 1px solid #2d2d32;
  }

  .data-row:hover {
    background-color: #2d2d32;
  }

  .data-cell {
    padding: 12px 16px;
    color: #e2e8f0;
    text-align: center;
    font-size: 14px;
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
</style>