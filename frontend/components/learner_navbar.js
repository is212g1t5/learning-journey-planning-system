const navbar = Vue.createApp({});

//navbar vue component
navbar.component("navbar", {
  data() {
    return {
      appName: "ljps",
    };
  },
  computed: {
    links() {
      if (window.location.href.includes("learners")) {
        return {
          roleLink: "./roles.html?staff_id=" + this.id,
          ljLink: "./journeys.html?staff_id=" + this.id,
          hrLink: "../hr",
          learnerLink: "./",
        };
      }
    },
  },
  created() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("staff_id")) {
        this.id = urlParams.get("staff_id");
    }
  },
  template: `<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">LJPS</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarScroll">
      <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
        <li class="nav-item">
          <a class="nav-link" aria-current="page" :href=links.roleLink>Roles</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :href=links.ljLink>Learning Journey</a>
        </li>
      </ul>
      <span>
        <ul class="d-flex navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll">
          <li class="nav-item dropdown dropstart">
            <a class="nav-link" href="#" id="navbarScrollingDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Switch User
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
              </svg> 
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarScrollingDropdown">
              <li><a class="dropdown-item" :href=links.hrLink>HR Staff</a></li>
              <li><a class="dropdown-item" :href=links.learnerLink>Learner Staff</a></li>
            </ul>
          </li>
        </ul>
      </span>
    </div>
  </div>
</nav>`,
});
navbar.mount("#navbar");
