<!-- src/routes/+layout.svelte -->
<script>
    import "../app.css";
    import { page } from "$app/stores";
  </script>
  
  <div class="app-container">
    <header class="app-header">
      <h1>Meter<span class="accent">Things</span></h1>
      <nav>
        <a 
          href="/dashboard" 
          class="nav-link" 
          class:active={$page.url.pathname.startsWith('/dashboard')}
        >
          Dashboard
        </a>
        <a 
          href="/devices" 
          class="nav-link" 
          class:active={$page.url.pathname.startsWith('/devices')}
        >
          Device Config
        </a>
      </nav>
    </header>
    
    <slot />
  </div>
  
  <style>
    .app-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
    }
  
    .app-header {
      background: #1a1a1a;
      padding: 1.2rem 2.5rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      position: relative;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    .app-header::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(
        90deg,
        rgba(51, 153, 255, 0) 0%,
        rgba(51, 153, 255, 0.5) 50%,
        rgba(51, 153, 255, 0) 100%
      );
    }
  
    h1 {
      font-family: "Inter", sans-serif;
      color: #ffffff;
      margin: 0;
      font-size: 1.8rem;
      font-weight: 600;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
  
    .accent {
      background: linear-gradient(135deg, #3399ff, #00ccff);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      font-weight: 700;
    }
  
    nav {
      display: flex;
      gap: 1.5rem;
    }
  
    .nav-link {
      color: #94a3b8;
      text-decoration: none;
      font-family: "Inter", sans-serif;
      font-size: 0.95rem;
      padding: 0.5rem 0.75rem;
      border-radius: 0.375rem;
      transition: all 0.2s;
    }
  
    .nav-link:hover {
      color: #e2e8f0;
      background: rgba(255, 255, 255, 0.1);
    }
  
    .nav-link.active {
      color: #3399ff;
      background: rgba(51, 153, 255, 0.1);
    }
  
    @media (max-width: 768px) {
      .app-header {
        padding: 1rem 1.5rem;
        flex-direction: column;
        gap: 1rem;
      }
  
      h1 {
        font-size: 1.5rem;
      }
  
      nav {
        width: 100%;
        justify-content: center;
      }
    }
  </style>