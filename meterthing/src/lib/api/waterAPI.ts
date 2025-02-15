export interface WaterData {
    Timestamp: string;
    DeviceID: string;
    Date: string;
    Time: string;
    WaterDetected: boolean;
  }
  
  export async function fetchWaterData(startDate: string, endDate: string, deviceId?: string) {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      ...(deviceId && { device_id: deviceId })
    });
  
    const response = await fetch(`/api/water/data?${params}`);
    const data = await response.json();
    return data.result as WaterData[];
  }