const update = Vue.createApp({
  data() {
    return {
      id: "",
      skillForm: {
        id: "",
        name: "",
        category: "",
        description: "",
        status: true, //0 - retired; 1 - active
      },
      errorMsgs: {
        name: "",
        category: "",
        description: "",
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
    updateSkill() {
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;
      axios
        .put(
          "http://localhost:5001/skills/update/" + this.id,
          {
            skill_name: this.skillForm.name,
            skill_category: this.skillForm.category,
            skill_desc: this.skillForm.description,
            skill_status: this.skillForm.status,
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
      .get("http://localhost:5001/skills/" + this.id)
      .then((response) => {
        skill = response.data;
        this.skillForm.id = skill.skill_id;
        this.skillForm.name = skill.skill_name;
        this.skillForm.category = skill.skill_category;
        this.skillForm.description = skill.skill_desc;
        this.skillForm.status = skill.skill_status;
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
    "skillForm.name"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        //check if skill name already exists
        this.errorMsgs.name = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.name = "Skill name cannot be more than 64 characters";
        } else {
          this.errorMsgs.description = "";
        }
      } else {
        this.errorMsgs.name = "Skill name cannot be empty";
      }
    },
    //validate whether category is empty
    "skillForm.category"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.category = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.category =
            "Category cannot be more than 64 characters";
        } else {
          this.errorMsgs.description = "";
        }
      } else {
        this.errorMsgs.category = "Category cannot be empty";
      }
    },
    //validate whether description is empty
    "skillForm.description"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.description = "";
        if (newValue && newValue.trim().length > 512) {
          this.errorMsgs.description =
            "Description cannot be more than 250 characters";
        } else {
          this.errorMsgs.description = "";
        }
      } else {
        this.errorMsgs.description = "Description cannot be empty";
      }
    },
  },
  computed: {
    isFormValid() {
      return (
        !this.skillForm.name.trim() ||
        !this.skillForm.category.trim() ||
        !this.skillForm.description.trim() ||
        Object.values(this.errorMsgs).some((error) => {
          return error !== "";
        })
      );
    },
  },
});

update.mount("#update");
