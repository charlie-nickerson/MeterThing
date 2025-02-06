<!-- Header.svelte -->

<svelte:head>
  <!-- Option 1: Inter -->
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<header class="app-header">
  <h1>Meter<span class="accent">Things</span></h1>
</header>

<style>
  .app-header {
    background: #1a1a1a;
    padding: 1.2rem 2.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 10;
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

  .app-header h1 {
    /* Option 1: Inter - Clean, modern, professional */
    font-family: "Inter", sans-serif;

    /* Option 2: Space Grotesk - More tech/data focused */
    /* font-family: 'Space Grotesk', sans-serif; */

    /* Option 3: Outfit - Modern, friendly, approachable */
    /* font-family: 'Outfit', sans-serif; */

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

  @media (max-width: 768px) {
    .app-header {
      padding: 1rem 1.5rem;
    }

    .app-header h1 {
      font-size: 1.5rem;
    }
  }
</style>