<script>
  import { writable } from "svelte/store";

  // Store for the date range
  export const dateRange = writable({
    start: new Date().toISOString().split("T")[0], // Today as default
    end: new Date().toISOString().split("T")[0],
  });
</script>

<div class="date-range-picker">
  <h2>Date Range</h2>

  <div class="form-group">
    <label for="start-date">Start Date</label>
    <input
      type="date"
      id="start-date"
      bind:value={$dateRange.start}
      max={$dateRange.end}
    />
  </div>

  <div class="form-group">
    <label for="end-date">End Date</label>
    <input
      type="date"
      id="end-date"
      bind:value={$dateRange.end}
      min={$dateRange.start}
    />
  </div>
</div>

<style>
  .date-range-picker {
    padding: 1rem;
    font-family: "Inter", sans-serif;
  }

  h2 {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 1.5rem;
    font-weight: 600;
  }

  .form-group {
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #e2e8f0;
    font-size: 0.875rem;
    font-weight: 500;
  }

  input[type="date"] {
    width: 100%;
    padding: 0.5rem;
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 0.375rem;
    color: #e2e8f0;
    font-size: 0.875rem;
    font-family: "Inter", sans-serif;
    transition: all 0.15s ease;
  }

  input[type="date"]:hover {
    border-color: #475569;
  }

  input[type="date"]:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
  }

  input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1);
    opacity: 0.6;
    cursor: pointer;
  }

  input[type="date"]::-webkit-calendar-picker-indicator:hover {
    opacity: 0.8;
  }
</style>