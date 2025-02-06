<!-- src/components/MainContent.svelte -->
<script>
    import TemperatureChart from './Charts/TemperatureChart.svelte';
  </script>
  
  <main class="main-content">
    <div class="chart-grid">
      <div class="chart-card">
        <TemperatureChart />
      </div>
    </div>
  </main>
  
  <style>
    .main-content {
      flex: 1;
      padding: 2rem;
      overflow-y: auto;
      background: #121214;
    }
  
    .chart-grid {
      display: grid;
      gap: 2rem;
      max-width: 1400px;
      margin: 0 auto;
    }
  
    .chart-card {
      background: #1f1f23;
      border-radius: 0.5rem;
      padding: 1.5rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
  
    .chart-card h2 {
      font-size: 1.25rem;
      font-weight: 600;
      color: #e2e8f0;
      margin-bottom: 1rem;
      font-family: "Inter", sans-serif;
    }
  
    @media (max-width: 768px) {
      .main-content {
        padding: 1rem;
      }
    }
  </style>