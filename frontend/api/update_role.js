const update = Vue.createApp({
  data() {
    return {
      id: "",
      roleForm: {
        id: "",
        name: "",
        description: "",
        status: true, //0 - retired; 1 - active
        sector: "",
        track: "",
      },
      errorMsgs: {
        name: "",
        description: "",
        sector: "",
        track: "",
      },
      alerts: {
        showAlert: false,
        alertMsg: "",
        showSuccess: false,
        successMsg: "",
      },
    };
  },
  methods: {
    updateRole() {
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;
      axios
        .put(
          "http://localhost:5002/roles/update/" + this.id,
          {
            role_name: this.roleForm.name,
            role_desc: this.roleForm.description,
            role_status: this.roleForm.status,
            role_sector: this.roleForm.sector,
            role_track: this.roleForm.track,
          },
          {}
        )
        .then((response) => {
          this.alerts.showSuccess = true;
          this.alerts.successMsg = response.data.message;
        })
        .catch((error) => {
          if (error) {
            this.alerts.showAlert = true;
            this.alerts.alertMsg = error.response.data.message;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
      this.id = urlParams.get("id");
    }
  },
  mounted() {
    axios
      .get("http://localhost:5002/roles/" + this.id)
      .then((response) => {
        role = response.data;
        this.roleForm.id = role.role_id;
        this.roleForm.name = role.role_name;
        this.roleForm.description = role.role_desc;
        this.roleForm.status = role.role_status;
        this.roleForm.sector = role.role_sector;
        this.roleForm.track = role.role_track;
      })
      .catch((error) => {
        console.log(error);
        this.error = true;
      })
      .finally(() => {
        this.loading = false;
      });
  },
  watch: {
    "roleForm.name"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.name = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.name = "Role name cannot be more than 64 characters";
        } else {
          this.errorMsgs.name = "";
        }
      } else {
        this.errorMsgs.name = "Role name cannot be empty";
      }
    },
    "roleForm.description"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.description = "";
        if (newValue && newValue.trim().length > 512) {
          this.errorMsgs.description =
            "Description cannot be more than 512 characters";
        } else {
          this.errorMsgs.description = "";
        }
      } else {
        this.errorMsgs.description = "Description cannot be empty";
      }
    },
    "roleForm.sector"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.sector = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.sector =
            "Role sector cannot be more than 64 characters";
        } else {
          this.errorMsgs.sector = "";
        }
      } else {
        this.errorMsgs.sector = "Role sector cannot be empty";
      }
    },
    "roleForm.track"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.track = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.track = "Role track cannot be more than 64 characters";
        } else {
          this.errorMsgs.track = "";
        }
      } else {
        this.errorMsgs.track = "Role track cannot be empty";
      }
    },
  },
  computed: {
    isFormValid() {
      return (
        !this.roleForm.name.trim() ||
        !this.roleForm.description.trim() ||
        !this.roleForm.sector.trim() ||
        !this.roleForm.track.trim() ||
        Object.values(this.errorMsgs).some((error) => {
          return error !== "";
        })
      );
    },
  },
});

update.mount("#update");
