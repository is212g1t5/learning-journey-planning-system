const update = Vue.createApp({
  data() {
    return {
      id: "",
      skillMapped: [],
      allSkills: {},
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
    mapSkills() {
      console.log("Mapping");
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;
      axios
        .post(
          "http://localhost:5005/skills_courses/map",
          {
            skill_ids: this.skillMapped,
            course_id: this.id,
          }
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
    }
  },
  created() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("course_id")) {
      this.id = urlParams.get("course_id");
    }
  },
  mounted() {
    axios
      .get("http://localhost:5001/skills")
      .then((response) => {
        skills = response.data.data;
        skills.skills.forEach( element => {
          this.allSkills[element.skill_id] = {
            skillName: element.skill_name,
            skillCategory: element.skill_category,
            skillDesc: element.skill_desc,
            skillStatus: element.skill_status
          }
        });
        // console.log(skills.skills)
      })
      .catch((error) => {
        console.log(error);
        this.error = true;
      })
      .finally(() => {
        this.loading = false;
      });

    axios
      .get("http://localhost:5005/skills_courses/course/" + this.id)
      .then((response) => {
        skills_courses = response.data.data;
        skills_courses.skills_courses.forEach(element => {
          this.skillMapped.push(element.skills_id)
        });
        
        // console.log(skills_courses.skills_courses)
        // console.log(response)
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
    
  },
  computed: {

  },
});

update.mount("#mapping");
