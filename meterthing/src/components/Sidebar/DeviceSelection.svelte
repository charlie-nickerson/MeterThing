<script>
    import { deviceTypes } from "../../stores/deviceStore.js";
  </script>
  
  <form class="config-form">
    <div class="configurations-section">
      <h2>Chart Controls</h2>
      {#each Object.entries($deviceTypes) as [type, config]}
        <div class="form-group">
          <label for={type}>{config.label}</label>
          <select id={type} bind:value={config.selected}>
            {#each config.devices as name}
              <option value={name}>{name}</option>
            {/each}
          </select>
        </div>
      {/each}
    </div>
  </form>
  
  <style>
    .config-form {
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
      font-family: "Inter", sans-serif;
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
      font-family: "Inter", sans-serif;
    }
  
    select {
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
  
    select:hover {
      border-color: #475569;
    }
  
    select:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 1px #3b82f6;
    }
  
    option {
      background-color: #1e293b;
      color: #e2e8f0;
      padding: 0.5rem;
      font-family: "Inter", sans-serif;
    }
  </style>