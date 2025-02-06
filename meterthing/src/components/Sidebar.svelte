<!-- Sidebar.svelte -->
<script>
    import DeviceSelection from "./Sidebar/DeviceSelection.svelte";
    import DateRange from "./Sidebar/DateRange.svelte";
  </script>
  
  <aside class="sidebar">
    <div class="sidebar-content">
      <DateRange />
      <DeviceSelection />
    </div>
  </aside>
  
  <style>
    .sidebar {
      width: 300px;
      background: #1f1f23;
      border-right: 1px solid rgba(255, 255, 255, 0.08);
      overflow-y: auto;
      flex-shrink: 0;
      position: relative;
    }
  </style>