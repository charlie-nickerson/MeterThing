<!-- src/routes/dashboard/+page.svelte -->
<script>
    import Sidebar from "../../components/Sidebar.svelte";
    import MainContent from "../../components/MainContent.svelte";
  </script>
  
  <div class="content-wrapper">
    <Sidebar />
    <MainContent />
  </div>
  
  <style>
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