<!-- src/components/Charts/TemperatureChart.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';
  import { deviceTypes } from '../../stores/deviceStore';
  import { dateRange } from '../../stores/dateStore';
  import type { ChartConfiguration } from 'chart.js';

  let chart: Chart;
  let canvas: HTMLCanvasElement;
  let chartTitle = 'Temperature Chart';

  // Debug store changes
  $: console.log('deviceTypes store changed:', $deviceTypes);

  // Mock data - will replace with real data later
  const mockData = Array.from({ length: 24 }, (_, i) => ({
    time: `${i}:00`,
    temperature: 20 + Math.random() * 10
  }));

  onMount(() => {
    initChart();
  });

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });

  function updateChartTitle(newTitle: string) {
    if (chart?.options?.plugins?.title) {
      chart.options.plugins.title.text = newTitle;
      chart.update();
      console.log('Chart title updated to:', newTitle);
    } else {
      console.log('Failed to update chart title - chart not properly initialized');
    }
  }

  function initChart() {
    if (!canvas) return;

    const config: ChartConfiguration = {
      type: 'line',
      data: {
        labels: mockData.map(d => d.time),
        datasets: [{
          label: 'Temperature (°C)',
          data: mockData.map(d => d.temperature),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,  // Remove the Chart.js title
          },
          legend: {
            position: 'top',
            align: 'end',
            labels: {
              color: '#e2e8f0',
              boxWidth: 12,
              padding: 20
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: '#1e293b',
            titleColor: '#e2e8f0',
            bodyColor: '#e2e8f0',
            borderColor: '#334155',
            borderWidth: 1
          }
        },
        scales: {
          x: {
            grid: {
              color: '#334155'
            },
            ticks: {
              color: '#94a3b8'
            }
          },
          y: {
            grid: {
              color: '#334155'
            },
            ticks: {
              color: '#94a3b8'
            }
          }
        }
      }
    };

    chart = new Chart(canvas, config);
  }

  // Subscribe to date range changes
  $: if (chart && $dateRange) {
    console.log('Date range changed:', $dateRange);
  }

  // Subscribe to device selection changes and update title
  $: {
    if ($deviceTypes) {
      const temperatureDevice = Object.entries($deviceTypes).find(([key]) => 
        key.toLowerCase().includes('temperature')
      );
      
      if (temperatureDevice) {
        const [_, config] = temperatureDevice;
        chartTitle = config.selected 
          ? `Temperature Sensor : ${config.selected}`
          : 'Temperature Chart';
      }
    }
  }
</script>

<div class="chart-wrapper">
<div class="chart-header">
  <h2>{chartTitle}</h2>
</div>
<div class="chart-container">
  <canvas bind:this={canvas}></canvas>
</div>
</div>

<style>
.chart-wrapper {
  background: #1f1f23;
  border: 1px solid #334155;
  border-radius: 0.5rem;
  overflow: hidden;
}

.chart-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #334155;
}

h2 {
  font-size: 1.125rem;
  font-weight: 500;
  color: #e2e8f0;
  font-family: "Inter", sans-serif;
  margin: 0;
}

.chart-container {
  padding: 1rem;
  height: 350px;
  width: 100%;
}
</style>