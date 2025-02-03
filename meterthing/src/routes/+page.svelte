<!-- src/routes/+page.svelte -->
<script>
  import Header from "../components/Header.svelte";
  import Sidebar from "../components/Sidebar.svelte";
  import MainContent from "../components/MainContent.svelte";
  import "../app.css";
</script>

<div class="app-container">
  <Header />
  <div class="content-wrapper">
    <Sidebar />
    <MainContent />
  </div>
</div>

<style>
  .app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .content-wrapper {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  @media (max-width: 768px) {
    .content-wrapper {
      flex-direction: column;
    }
  }
</style>