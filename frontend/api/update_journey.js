const create_journey = Vue.createApp({
  data() {
    return {
      name: "",
      role: "",
      role_id: "",
      learning_id: "",
      skill_list: [],
      course_list: [],
      skills_roles_list: [],
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
    change(event) {
      if (!this.errorMsgs.role) {
        this.skills_roles_list = [];
        this.skill_list = [];
        this.course_list = [];
        this.course_dict = {};
        this.selectCourses = [];
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
            this.course_list.push(response.data.data.skills_courses);
          })
          .catch((error) => {
            console.log(error);
          });
      }

      var course_flat_list = this.course_list.flat();
      for (course of course_flat_list) {
        await axios
          .get("http://127.0.0.1:5003/courses/" + course.course_id)
          .then((response) => {
            this.course_dict[course.course_id] = response.data.data;
          })
          .catch((error) => {
            console.log(error);
          });
      }

      await new Promise((resolve, reject) => setTimeout(resolve, 3000));
      return;
    },
    updateJourney() {
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;
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
        this.loadData();
      })
      .catch((error) => {
        console.log(error);
      });
  },
});

create_journey.mount("#update_journey");
