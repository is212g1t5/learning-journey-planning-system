const create_journey = Vue.createApp({
  data() {
    return {
      name: "",
      current_name: "",
      role: "",
      role_id: "",
      learning_id: "",
      skill_list: [],
      course_list: {},
      skills_roles_list: [],
      existing_names: [],
      course_dict: {},
      lj_courses: [],
      checked_courses: [],
      removed_courses: [],
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
        this.current_name.trim().toLowerCase() === this.name.trim().toLowerCase() ||
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
        if (newValue && this.existing_names.includes(newValue.trim().toLowerCase())) {
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
        this.course_list = {};      //list of ids of skill(key): list of course ids(value) of learning journey
        this.course_dict = {};      //list of course objects mapped to learning journey
        this.selectCourses = [];
        this.loadData();
      }
    },
    //returns boolean whether course is already added to learning journey
    isLjCourse(id) {
      return this.lj_courses.includes(id);
    },
    //returns boolean whether course is already added to removed array
    isRemovedCourse(id) {
      return this.removed_courses.includes(id);
    },
    //remove course or undo remove depending on whether course is already in removed array
    removeCourse(id) {
      if (this.removed_courses.includes(id)) {
        this.removed_courses.splice(this.removed_courses.indexOf(id), 1);
      } else {
        this.removed_courses.push(id);
      }
    },
    //number of courses assigned in this skill
    skill_course_count(sid) {
      return this.course_list[sid] ? this.course_list[sid].length : 0;
    },
    async loadData() {
      await axios
        .get("http://127.0.0.1:5004/learning_journeys/" + this.staff_id)
        .then((response) => {
          for (lj_names of response.data.data.learning_journeys) {
            this.existing_names.push(lj_names.learning_journey_name.toLowerCase());
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
          })
          .catch((error) => {
            console.log(error);
          });
        }
      }

      //get courses mapped to learning journey
      await axios
        .get("http://127.0.0.1:5009/lj_courses/" + this.learning_id)
        .then((response) => {
          this.lj_courses = response.data.data.lj_courses.map(obj => {return obj.course_id});
        });

      await new Promise((resolve, reject) => setTimeout(resolve, 3000));
      return;
    },
    refreshData() {
      //reset updated data variables
      this.skills_roles_list = [];
      this.skill_list = [];
      this.course_list = {};
      this.course_dict = {};
      this.existing_names = [];

      this.loadData();
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

          this.current_name = this.name;

          this.refreshData();
        })
        .catch((error) => {
          this.alerts.showAlert = true;
          this.alerts.alertMsg = "Error updating learning journey.";
        });
    },
    //update courses tied to learning journey
    // updateCourses() {

    // }
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
        this.current_name = response.data.data.learning_journey_name;
        this.role_id = response.data.data.role_id;
        this.staff_id = response.data.data.staff_id;
        //get role name from role table
        axios
          .get("http://127.0.0.1:5002/roles/" + this.role_id)
          .then((response) => {
            this.role = response.data.role_name;
          })
          .catch((error) => {
            console.log(error);
          });

        this.loadData();
      })
      .catch((error) => {
        console.log(error);
      });

    
  },
});

create_journey.mount("#update_journey");