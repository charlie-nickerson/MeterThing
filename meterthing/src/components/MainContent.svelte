<!-- src/components/MainContent.svelte -->
<script>
  import TemperatureChart from './Charts/TemperatureChart.svelte';
  import TemperatureStats from './Charts/TemperatureStats.svelte';
  import WaterDetectionTable from './Charts/WaterDetectionTable.svelte';
</script>

<main class="main-content">
  <div class="content-wrapper">
    <TemperatureStats />
    <TemperatureChart />
    <WaterDetectionTable />
  </div>
</main>

<style>
  .main-content {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
    background: #121214;
  }

  .content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  @media (max-width: 768px) {
    .main-content {
      padding: 1rem;
    }
  }
</style>