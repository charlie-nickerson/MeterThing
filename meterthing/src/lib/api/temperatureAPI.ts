// src/lib/api/temperatureAPI.ts
export interface TemperatureData {
  Timestamp: string;  // Format: 'YYYY-MM-DD HH:MM:SS'
  Temperature: number;
  DeviceID: string;
}

export async function fetchTemperatureData(startDate: string, endDate: string, deviceId?: string) {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
    ...(deviceId && { device_id: deviceId })
  });

  const response = await fetch(`/api/temperature/data?${params}`);
  const data = await response.json();
  return data.result as TemperatureData[];
}