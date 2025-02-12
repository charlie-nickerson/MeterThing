<!-- src/components/DownloadButton.svelte -->
<script lang="ts">
    import { DownloadCloud } from 'lucide-svelte';
    
    interface BaseData {
      Timestamp: string;
      DeviceID: string;
    }
  
    interface TemperatureData extends BaseData {
      Temperature: number;
    }
  
    interface TurbidityData extends BaseData {
      Turbidity: number;
    }
  
    interface WaterDetectionData extends BaseData {
      WaterDetected: boolean;
    }
  
    type SensorData = TemperatureData | TurbidityData | WaterDetectionData;
  
    export let data: SensorData[] = [];
    export let disabled: boolean = false;
    export let dataType: 'temperature' | 'turbidity' | 'waterDetection' = 'temperature';
    export let fileName: string = 'sensor-data';
  
    function getHeaders(type: typeof dataType): string[] {
      const baseHeaders = ['Timestamp', 'DeviceID'];
      switch (type) {
        case 'temperature':
          return [...baseHeaders, 'Temperature'];
        case 'turbidity':
          return [...baseHeaders, 'Turbidity'];
        case 'waterDetection':
          return [...baseHeaders, 'WaterDetected'];
        default:
          return baseHeaders;
      }
    }
  
    function formatRowData(row: SensorData, type: typeof dataType): string[] {
      const baseData = [row.Timestamp, row.DeviceID];
      
      switch (type) {
        case 'temperature':
          return [...baseData, (row as TemperatureData).Temperature.toString()];
        case 'turbidity':
          return [...baseData, (row as TurbidityData).Turbidity.toString()];
        case 'waterDetection':
          return [...baseData, (row as WaterDetectionData).WaterDetected.toString()];
        default:
          return baseData;
      }
    }
  
    function escapeCSV(value: string): string {
      if (value.includes(',') || value.includes('"') || value.includes('\n')) {
        return `"${value.replace(/"/g, '""')}"`;
      }
      return value;
    }
  
    function downloadCSV() {
      if (!data || data.length === 0) return;
      
      const headers = getHeaders(dataType);
      
      const csvRows = [
        headers.join(','),
        ...data.map(row => 
          formatRowData(row, dataType)
            .map(escapeCSV)
            .join(',')
        )
      ];
      
      const csvContent = csvRows.join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      
      const timestamp = new Date().toISOString().split('T')[0];
      const downloadFileName = `${fileName}-${timestamp}.csv`;
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', downloadFileName);
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  </script>
  
  <button
    on:click={downloadCSV}
    class="download-button"
    disabled={disabled || !data.length}
    title={!data.length ? 'No data available to download' : `Download ${dataType} data as CSV`}
    aria-label="Download data"
  >
    <DownloadCloud
      size={20}
      class="icon"
      color={disabled || !data.length ? '#64748b' : '#e2e8f0'}
    />
  </button>
  
  <style>
    .download-button {
      background: transparent;
      border: none;
      border-radius: 0.375rem;
      padding: 0.5rem;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  
    .download-button:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.1);
    }
  
    .download-button:disabled {
      cursor: not-allowed;
      opacity: 0.5;
    }
  
    .icon {
      display: block;
    }
  </style>