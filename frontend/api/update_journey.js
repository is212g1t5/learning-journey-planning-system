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
      mapped_skills: [],
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
    isFormInvalid() {
      return (
        !this.name.trim() ||
        !this.role.trim() ||
        this.hasNoCourses ||
        !this.hasChanges ||
        Object.values(this.errorMsgs).some((error) => {
          return error !== "";
        })
      );
    },
    hasNoCourses() {
      //return true if no new courses getting added and all existing courses being removed
      console.log(this.lj_courses);
      return this.checked_courses.length === 0 && this.lj_courses.length === this.removed_courses.length;
    },
    hasChanges() {
      return (
        this.current_name.trim().toLowerCase() !== this.name.trim().toLowerCase() ||
        this.removed_courses.length > 0 ||
        this.checked_courses.length > 0
      );
    }
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
        this.mapped_skills = [];//list of skill_role objects based on role of learning journey
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
      if (this.course_list[sid]) {
        let counter = 0;

        for (let cid of this.course_list[sid]) {
          //count course as assigned if course mapped to lj and not in removed array
          if (this.isLjCourse(cid) && !this.isRemovedCourse(cid)) {
            counter++;
          }
        }
        return counter;
      }

      return 0;
    },
    async loadData() {
      await axios
        .get("http://127.0.0.1:5004/learning_journeys/" + this.staff_id)
        .then((response) => {
          for (lj_names of response.data.data.learning_journeys) {
            this.existing_names.push(lj_names.learning_journey_name.toLowerCase());
          }
        });
      
      //retrieve skill ids of skills mapped to learning journey
      await axios
        .get("http://127.0.0.1:5007/lj_skills/" + this.learning_id)
        .then((response) => {
          this.mapped_skills = response.data.data.lj_skills.map(obj => {return obj.skill_id});
        })
        .catch((error) => {
          console.log(error);
        });

      for (sid of this.mapped_skills) {
        await axios
          .get("http://127.0.0.1:5001/skills/" + sid)
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

      console.log(this.course_list);

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
      this.mapped_skills = [];
      this.skill_list = [];
      this.course_list = {};
      this.course_dict = {};
      this.existing_names = [];

      this.loadData();
    },
    //update courses tied to learning journey
    async updateCourses() {
      //add new courses
      for (cid of this.checked_courses) {
        await axios
          .post("http://127.0.0.1:5009/lj_courses/create",
          {
            learning_journey_id: this.learning_id,
            course_id: cid,
          })
          .then((response) => {
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      }

      //remove courses
      for (cid of this.removed_courses) {
        await axios
          .delete("http://127.0.0.1:5009/lj_courses/delete/"
          + this.learning_id + "/"
          + cid
          )
          .then((response) => {
            console.log(response);
          })
          .catch((error) => {
            console.log(error);
          });
      }

      this.removed_courses = [];
      this.checked_courses = [];
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
      
      //update courses if any changes to assigned courses
      if (this.checked_courses.length > 0 || this.removed_courses.length > 0) {
        this.updateCourses();
      }
    },    
  },
  mounted() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
      this.learning_id = urlParams.get("id");
    }
    if (urlParams.has("staff_id")) {
      this.staff_id = urlParams.get("staff_id");
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
