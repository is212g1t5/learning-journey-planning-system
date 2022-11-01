const create_journey = Vue.createApp({
  data() {
    return {
      name: "",
      role: "",
      role_id: "",
      learning_id: "",
      skill_list: [],
      course_list: {},
      skills_roles_list: [],
      existing_names: [],
      course_dict: {},
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
        this.name != this.name ||
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
        if (newValue && this.existing_names.includes(newValue)) {
          this.errorMsgs.name = "Learning journey name already exists.";
        } else {
          this.errorMsgs.name = "";
        }
      } else {
        this.errorMsgs.name = "Learning journey name cannot be empty";
      }
    },
  },
  methods: {
    change(event) {
      if (!this.errorMsgs.role) {
        this.skills_roles_list = [];//list of skill_role objects based on role of learning journey
        this.skill_list = [];       //list of skill objects associated with role of leearning journey
        this.course_list = {};      //list of ids of courses mapped to learning journey
        this.course_dict = {};      //list of course objects mapped to learning journey
        this.selectCourses = [];
        this.loadData();
      }
    },
    async loadData() {
      await axios
        .get("http://127.0.0.1:5004/learning_journeys/" + this.staff_id)
        .then((response) => {
          for (lj_names of response.data.data.learning_journeys) {
            this.existing_names.push(lj_names.learning_journey_name);
          }
        });
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
            this.skill_list.push(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
      }

      for (skill of this.skill_list) {
        await axios
          .get("http://127.0.0.1:5005/skills_courses/skill/" + skill.skill_id)
          .then((response) => {
            this.course_list[skill.skill_id] = response.data.data.skills_courses.map(obj => {return obj.course_id});
          })
          .catch((error) => {
            console.log(error);
          });
      }

      for (courses of Object.values(this.course_list)) {
        for (course_id of courses) {
          await axios
          .get("http://127.0.0.1:5003/courses/" + course_id)
          .then((response) => {
            this.course_dict[course_id] = response.data.data;
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error);
          });
        }
      }

      console.log(this.course_dict);

      await new Promise((resolve, reject) => setTimeout(resolve, 3000));
      return;
    },
    updateJourney() {
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;

      axios
        .put(
          "http://127.0.0.1:5004/learning_journeys/update/" + this.learning_id,
          { learning_journey_name: this.name },
          {}
        )
        .then((response) => {
          this.alerts.showSuccess = true;
          this.alerts.successMsg = "Learning journey updated successfully.";
        })
        .catch((error) => {
          this.alerts.showAlert = true;
          this.alerts.alertMsg = "Error updating learning journey.";
        });
    },
  },
  mounted() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
      this.learning_id = urlParams.get("id");
    }
    axios
      .get(
        "http://127.0.0.1:5004/learning_journeys/single_journey/" +
          this.learning_id
      )
      .then((response) => {
        this.name = response.data.data.learning_journey_name;
        this.role_id = response.data.data.role_id;
        this.role = response.data.data.role_name;
        this.staff_id = response.data.data.staff_id;
        this.loadData();
      })
      .catch((error) => {
        console.log(error);
      });
  },
});

create_journey.mount("#update_journey");
