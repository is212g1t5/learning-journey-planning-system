const create_journey = Vue.createApp({
  data() {
    return {
      name: "",
      role: "",
      role_id: "",
      skill_list: [],
      selected_role: "",
      role_list: [],
      skills_roles_list: [],
      alerts: {
        showAlert: false,
        alertMsg: "",
        showSuccess: false,
        successMsg: "",
      },
      errorMsgs: {
        name: "",
        role: "",
      },
    };
  },
  computed: {
    isFormValid() {
      return (
        !this.name.trim() ||
        !this.role.trim() ||
        Object.values(this.errorMsgs).some((error) => {
          return error !== "";
        })
      );
    },
  },
  watch: {
    name(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.name = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.name =
            "Learning journey name cannot be more than 64 characters";
        } else {
          this.errorMsgs.name = "";
        }
      } else {
        this.errorMsgs.name = "Learning journey cannot be empty";
      }
    },
  },
  methods: {
    input(event) {
      if (event.target.value.length == 0) {
        this.errorMsgs.role = "Role cannot be empty";
        this.skill_list = [];
      } else {
        this.errorMsgs.role = "";
      }
    },
    change(event) {
      if (!this.errorMsgs.role) {
        this.skills_roles_list = [];
        this.skill_list = [];
        this.role = event.target.value;
        for (role of this.role_list) {
          if (role.role_name == this.role) {
            this.role_id = role.role_id;
          }
        }
        this.loadData();
      }
    },
    async loadData() {
      await axios
        .get("http://127.0.0.1:5006/skills_roles/" + this.role_id)
        .then((response) => {
          this.skills_roles_list = response.data.data.skills_roles;
        })
        .catch((error) => {
          console.log(error);
        });

      for (skill_roles of this.skills_roles_list) {
        await axios
          .get("http://127.0.0.1:5001/skills/" + skill_roles.skills_id)
          .then((response) => {
            if (response.data.skill_status == true) {
              this.skill_list.push(response.data);
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }

      await new Promise((resolve, reject) => setTimeout(resolve, 3000));
      return;
    },
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5002/roles")
      .then((response) => {
        for (role of response.data.data.roles) {
          if (role.role_status == true) {
            this.role_list.push(role);
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
});

create_journey.mount("#create_journey");
