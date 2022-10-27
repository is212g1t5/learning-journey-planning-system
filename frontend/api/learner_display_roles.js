const learner_display_roles = Vue.createApp({
  data() {
    return {
      role_list: [],
      emptyText: "",
      searchQuery: null,
      fields: [
        {
          key: "role_name",
          label: "Role",
          sortable: true,
          sortDirection: "desc",
        },
        { key: "role_sector", label: "Role Sector", sortable: true },
        { key: "role_track", label: "Role Track", sortable: true },
      ],
      totalRows: 1,
      currentPage: 1,
      perPage: 10,
      pageOptions: [5, 10, 15, 100],
      startRow: 0,
      endRow: 10,
      pageSize: null,
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      currentSort: "role_name",
      currentSortDir: "asc",
      sortIcon: {
        role_name: "mx-2 fa fa-xs fa-sort",
        role_sector: "mx-2 fa fa-xs fa-sort",
        role_track: "mx-2 fa fa-xs fa-sort",
        role_status: "mx-2 fa fa-xs fa-sort",
      },
      pageItemIcon: {
        false: "page-item",
        true: "page-item active",
      },
    };
  },
  computed: {
    sortedResultQuery() {
      return this.resultQuery.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === "desc") modifier = -1;
        if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },
    resultQuery() {
      if (this.searchQuery) {
        return this.role_list.filter((item) => {
          return this.searchQuery
            .toLowerCase()
            .split(" ")
            .every((v) => item.role_name.toLowerCase().includes(v));
        });
      } else {
        return this.role_list;
      }
    },
    paginatedQuery() {
      return this.sortedResultQuery.slice(this.startRow, this.endRow);
    },
  },
  watch: {
    perPage() {
      this.pageSize = Math.ceil(this.totalRows / this.perPage);
      this.startRow = 0;
      this.endRow = this.perPage;
    },
  },
  methods: {
    sort(s) {
      //if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === "asc" ? "desc" : "asc";
        this.sortIconFn(s);
      }
      this.currentSort = s;
      this.sortIconFn(s);
    },
    sortIconFn(s) {
      Object.keys(this.sortIcon).forEach((key) => {
        this.sortIcon[key] = "mx-2 fa fa-xs fa-sort";
      });
      if (this.currentSortDir == "asc") {
        this.sortIcon[s] = "mx-2 fa fa-xs fa-sort-asc";
      } else if (this.currentSortDir == "desc") {
        this.sortIcon[s] = "mx-2 fa fa-xs fa-sort-desc";
      } else {
        this.sortIcon[s] = "mx-2 fa fa-xs fa-sort";
      }
    },
    nextPage() {
      if (this.currentPage != this.pageSize) {
        this.startRow = parseInt(this.endRow);
        this.endRow = parseInt(this.endRow) + parseInt(this.perPage);
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.endRow = parseInt(this.startRow);
        this.startRow = parseInt(this.endRow) - parseInt(this.perPage);
        this.currentPage--;
      }
    },
    currentPageFn(page) {
      this.currentPage = page;
      this.endRow = parseInt(this.currentPage) * parseInt(this.perPage);
      this.startRow = parseInt(this.endRow) - parseInt(this.perPage);
    },
    createJourney(role_id) {
      window.location.href = "create_journey.html?id=" + role_id;
    },
  },
  async mounted() {
    await axios
      .get("http://localhost:5002/roles")
      .then((response) => {
        var role_list = response.data.data.roles;
        var filteredList = [];
        for (role of role_list) {
          console.log(role.role_status);
          if (role.role_status) {
            role.role_status = "Active";
            filteredList.push(role);
          }
        }
        this.role_list = filteredList;
        // Set the initial number of items
        this.totalRows = filteredList.length;
        this.pageSize = Math.ceil(this.totalRows / this.perPage);
        console.log(filteredList);
      })
      .catch((error) => {
        if (error.response.data.code == 404) {
          this.emptyText = "There are no roles available.";
        }
        console.log(error);
      });
  },
});

learner_display_roles.mount("#learner_display_roles");
