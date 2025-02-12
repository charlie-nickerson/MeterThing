<!-- src/components/Charts/TemperatureChart.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';
  import { deviceTypes } from '../../stores/deviceStore';
  import { dateRange } from '../../stores/dateStore';
  import type { ChartConfiguration } from 'chart.js';
  import DownloadButton from '../DownloadButton.svelte';

  let chart: Chart;
  let canvas: HTMLCanvasElement;
  let chartTitle = 'Temperature Chart';
  let displayState: 'initial' | 'loading' | 'error' | 'data' = 'initial';
  let errorMessage = '';
  let currentDeviceId: string | undefined;
  let chartData: any[] = []; // Store the data for the download button

  async function fetchTemperatureData(startDate: string, endDate: string, deviceId?: string) {
    if (!deviceId) return null;

    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      ...(deviceId && { device_id: deviceId })
    });
    
    const response = await fetch(`/api/temperature/data?${params}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return (await response.json()).result;
  }

  function clearChart() {
    if (chart) {
      chart.data.labels = [];
      chart.data.datasets[0].data = [];
      chart.update();
    }
  }

  async function fetchAndUpdateData() {
    if (!chart || !currentDeviceId) {
      displayState = 'initial';
      return;
    }

    displayState = 'loading';
    
    try {
      const data = await fetchTemperatureData(
        $dateRange.start,
        $dateRange.end,
        currentDeviceId
      );
      
      if (!data || data.length === 0) {
        clearChart();
        errorMessage = 'No data available for selected date range';
        displayState = 'error';
        chartData = []; // Clear the data
        return;
      }
      
      const sortedData = [...data].sort((a, b) => 
        new Date(a.Timestamp).getTime() - new Date(b.Timestamp).getTime()
      );
      
      chartData = sortedData; // Store the data for downloading
      
      chart.data.labels = sortedData.map(d => {
        const date = new Date(d.Timestamp);
        return date.toLocaleString();
      });
      
      chart.data.datasets[0].data = sortedData.map(d => d.Temperature);
      chart.update();
      displayState = 'data';
      
    } catch (e) {
      console.error('Error fetching temperature data:', e);
      clearChart();
      errorMessage = e.message;
      displayState = 'error';
      chartData = []; // Clear the data
    }
  }

  onMount(() => {
    initChart();
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });

  function initChart() {
    if (!canvas) return;
    
    const config: ChartConfiguration = {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'Temperature (°C)',
          data: [],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.05)',
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: '#ffffff',
          pointHoverBorderColor: '#3b82f6',
          pointHoverBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
          },
          legend: {
            position: 'top',
            align: 'end',
            labels: {
              color: '#94a3b8',
              boxWidth: 12,
              padding: 20,
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 12
              }
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: '#1e293b',
            titleColor: '#e2e8f0',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1,
            padding: 12,
            bodyFont: {
              family: 'Inter, system-ui, sans-serif'
            },
            titleFont: {
              family: 'Inter, system-ui, sans-serif'
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: '#64748b',
              maxRotation: 45,
              minRotation: 45,
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 11
              }
            }
          },
          y: {
            grid: {
              color: '#334155'
            },
            ticks: {
              color: '#64748b',
              font: {
                family: 'Inter, system-ui, sans-serif',
                size: 11
              }
            }
          }
        }
      }
    };
    
    chart = new Chart(canvas, config);
  }

  // Handle device changes
  $: {
    if ($deviceTypes) {
      const temperatureDevice = Object.entries($deviceTypes).find(([key]) =>
        key.toLowerCase().includes('temperature')
      );
      
      if (temperatureDevice) {
        const [_, config] = temperatureDevice;
        chartTitle = config.selected
          ? `Temperature Sensor: ${config.selected}`
          : 'Temperature Chart';
          
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
</script>

<div class="chart-wrapper">
  <div class="chart-header">
    <h2>{chartTitle}</h2>
    <DownloadButton 
      data={chartData}
      disabled={displayState !== 'data'}
      dataType="temperature"
      fileName="temperature-data"
    />
  </div>
  <div class="chart-container">
    <canvas bind:this={canvas} class="chart"></canvas>
    {#if displayState !== 'data'}
      <div class="overlay" class:error={displayState === 'error'}>
        {#if displayState === 'loading'}
          Loading data...
        {:else if displayState === 'error'}
          {errorMessage}
        {:else}
          Select a device to view temperature data
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .chart-wrapper {
    background: #1f1f23;
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 2px 4px 0 rgb(0 0 0 / 0.4);
  }
  
  .chart-header {
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
  
  .chart-container {
    padding: 1.5rem;
    height: 350px;
    width: 100%;
    position: relative;
  }

  .chart {
    position: relative;
    z-index: 1;
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