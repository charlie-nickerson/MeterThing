<!-- src/components/DownloadButton.svelte -->
<script lang="ts">
    // Define interfaces for different data types
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
      WaterLevel: number;
    }
  
    type SensorData = TemperatureData | TurbidityData | WaterDetectionData;
  
    // Props
    export let data: SensorData[] = [];
    export let disabled: boolean = false;
    export let dataType: 'temperature' | 'turbidity' | 'waterDetection' = 'temperature';
    export let fileName: string = 'sensor-data';
  
    // Function to get CSV headers based on data type
    function getHeaders(type: typeof dataType): string[] {
      const baseHeaders = ['Timestamp', 'DeviceID'];
      switch (type) {
        case 'temperature':
          return [...baseHeaders, 'Temperature'];
        case 'turbidity':
          return [...baseHeaders, 'Turbidity'];
        case 'waterDetection':
          return [...baseHeaders, 'WaterDetected', 'WaterLevel'];
        default:
          return baseHeaders;
      }
    }
  
    // Function to format row data based on data type
    function formatRowData(row: SensorData, type: typeof dataType): string[] {
      const baseData = [row.Timestamp, row.DeviceID];
      
      switch (type) {
        case 'temperature':
          return [...baseData, (row as TemperatureData).Temperature.toString()];
        case 'turbidity':
          return [...baseData, (row as TurbidityData).Turbidity.toString()];
        case 'waterDetection':
          const waterData = row as WaterDetectionData;
          return [...baseData, waterData.WaterDetected.toString(), waterData.WaterLevel.toString()];
        default:
          return baseData;
      }
    }
  
    // Function to escape CSV values properly
    function escapeCSV(value: string): string {
      if (value.includes(',') || value.includes('"') || value.includes('\n')) {
        return `"${value.replace(/"/g, '""')}"`;
      }
      return value;
    }
  
    function downloadCSV() {
      if (!data || data.length === 0) return;
      
      // Get headers for the current data type
      const headers = getHeaders(dataType);
      
      // Convert data to CSV format
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
      
      // Create download link with formatted filename
      const timestamp = new Date().toISOString().split('T')[0];
      const downloadFileName = `${fileName}-${timestamp}.csv`;
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', downloadFileName);
      
      // Trigger download
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
  >
    Download CSV
  </button>
  
  <style>
    .download-button {
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 0.375rem;
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
      font-family: "Inter", system-ui, sans-serif;
    }
  
    .download-button:hover:not(:disabled) {
      background: #2563eb;
    }
  
    .download-button:disabled {
      background: #64748b;
      cursor: not-allowed;
      opacity: 0.7;
    }
  </style>