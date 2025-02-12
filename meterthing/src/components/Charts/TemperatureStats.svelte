<!-- src/components/Stats/TemperatureStats.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { deviceTypes } from '../../stores/deviceStore';
    import type { TemperatureData } from '../../lib/api/temperatureAPI';
  
    interface SensorStat {
      name: string;
      deviceId: string;
      averageMax: number | null;
      isLoading: boolean;
      error: string | null;
    }
  
    let sensorStats: SensorStat[] = [];
  
    async function fetchTemperatureData(deviceId: string) {
      // Calculate date range for last 7 days
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(endDate.getDate() - 7);
  
      const params = new URLSearchParams({
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        device_id: deviceId
      });
      
      const response = await fetch(`/api/temperature/data?${params}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return (await response.json()).result;
    }
  
    async function calculateStats(deviceName: string, deviceId: string) {
      const statIndex = sensorStats.findIndex(stat => stat.deviceId === deviceId);
      if (statIndex === -1) return;
  
      sensorStats[statIndex].isLoading = true;
      sensorStats[statIndex].error = null;
      sensorStats = [...sensorStats]; // Trigger Svelte reactivity
  
      try {
        const data: TemperatureData[] = await fetchTemperatureData(deviceId);
        
        if (!data || data.length === 0) {
          sensorStats[statIndex].error = "Not enough data";
          sensorStats = [...sensorStats];
          return;
        }
  
        // Group temperatures by date
        const dailyTemps = data.reduce((acc, reading) => {
          const date = reading.Timestamp.split('T')[0];
          if (!acc[date]) {
            acc[date] = [];
          }
          acc[date].push(reading.Temperature);
          return acc;
        }, {} as { [key: string]: number[] });
  
        // Calculate max temperature for each day
        const dailyMaxes = Object.values(dailyTemps).map(temps => Math.max(...temps));
  
        // Need at least 3 days of data to show a meaningful average
        if (dailyMaxes.length < 3) {
          sensorStats[statIndex].error = "Not enough data";
          sensorStats = [...sensorStats];
          return;
        }
  
        // Calculate average of daily maximums
        sensorStats[statIndex].averageMax = Number(
          (dailyMaxes.reduce((sum, max) => sum + max, 0) / dailyMaxes.length).toFixed(1)
        );
        sensorStats = [...sensorStats];
  
      } catch (e) {
        console.error('Error fetching temperature data:', e);
        sensorStats[statIndex].error = "Error fetching data";
        sensorStats = [...sensorStats];
      } finally {
        sensorStats[statIndex].isLoading = false;
        sensorStats = [...sensorStats];
      }
    }
  
    // Initialize stats for all temperature sensors
    $: {
      if ($deviceTypes) {
        const temperatureDevices = Object.entries($deviceTypes).filter(([key]) =>
          key.toLowerCase().includes('temperature')
        );
        
        // Get all temperature devices and their IDs
        const allSensors: SensorStat[] = [];
        
        temperatureDevices.forEach(([_, config]) => {
          // Add all devices from this temperature sensor type
          config.devices.forEach(deviceName => {
            const deviceId = config.deviceMap[deviceName];
            allSensors.push({
              name: deviceName,
              deviceId: deviceId,
              averageMax: null,
              isLoading: false,
              error: null
            });
          });
        });
  
        // Update sensorStats with new list
        sensorStats = allSensors;
  
        // Calculate stats for all sensors
        allSensors.forEach(sensor => {
          calculateStats(sensor.name, sensor.deviceId);
        });
      }
    }
  </script>
  
  <div class="stats-grid">
    {#each sensorStats as stat}
      <div class="stat-card">
        <div class="stat-header">
          <h3>{stat.name}</h3>
          <p class="subtitle">7-Day Avg Max Temp</p>
        </div>
        
        <div class="stat-value">
          {#if stat.isLoading}
            <span class="loading">Loading...</span>
          {:else if stat.error}
            <span class="error">{stat.error}</span>
          {:else if stat.averageMax !== null}
            <span class="temp">{stat.averageMax}°C</span>
          {/if}
        </div>
      </div>
    {/each}
  </div>
  
  <style>
    .stats-grid {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }
  
    .stat-card {
      background: #1f1f23;
      border-radius: 0.75rem;
      padding: 1.25rem;
      box-shadow: 0 2px 4px 0 rgb(0 0 0 / 0.4);
    }
  
    .stat-header {
      margin-bottom: 1rem;
    }
  
    h3 {
      font-size: 1rem;
      font-weight: 500;
      color: #e2e8f0;
      margin: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  
    .subtitle {
      color: #94a3b8;
      font-size: 0.75rem;
      margin: 0.25rem 0 0 0;
    }
  
    .stat-value {
      text-align: center;
      font-size: 1.5rem;
      font-weight: 600;
      min-height: 2.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  
    .temp {
      color: #3b82f6;
    }
  
    .loading {
      color: #94a3b8;
      font-size: 1rem;
      font-weight: normal;
    }
  
    .error {
      color: #94a3b8;
      font-size: 0.875rem;
      font-weight: normal;
    }
  </style>