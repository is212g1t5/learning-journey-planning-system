const create_journey = Vue.createApp({
    data() {
      return {
        name: "",
        role: "",
        role_id: "",
        current_ljs: [],
        skill_list: [],
        skill_dict: {},
        course_list: [],
        course_skills: {},
        selected_role: "",
        selected_courses: [],
        role_list: [],
        skills_roles_list: [],
        course_dict: {},
        alerts: {
          showAlert: false,
          alertMsg: "",
          showSuccess: false,
          successMsg: "",
        },
        errorMsgs: {
          name: "Learning Journey cannot be empty",
          role: "Role cannot be empty",
          selected_courses: "Please select at least one course",
        },
      };
    },
    computed: {
      isFormValid() {
        return (
          !this.name.trim() ||
          !this.role.trim() ||
          !this.selected_courses.length ||
          Object.values(this.errorMsgs).some((error) => {
            return error !== "";
          })
        );
      },
      selected_skills() {
        var all_skills= []
        for(course of this.selected_courses){
          all_skills.push(this.course_skills[course])
        }
        let selected_skills = [...new Set(all_skills.flat(1))];
        return selected_skills
      }
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
      selected_courses(newValue){
        console.log(newValue.length)
        if(!newValue.length){
          this.errorMsgs.selected_courses =
              "Please select at least one course";
        }else{
          this.errorMsgs.selected_courses = "";
        }
      }
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
          this.skills_roles_list= [];
          this.skill_list = [];
          this.course_list=[];  
          this.course_dict= {};
          this.selected_courses= [];
          this.selectCourses= [];
          this.role = event.target.value;
          for (role of this.role_list) {
            if (role.role_name == this.role) {
              this.role_id = role.role_id;
            }
          }
          this.loadData()
        }
      },
      selectCourses() {
        window.location.href =
          "select_courses.html?role_id=" + this.role_id + "&name=" + this.name;
      },
      async loadData(){
        await axios
          .get("http://127.0.0.1:5006/skills_roles/" + this.role_id)
          .then((response) => {
            this.skills_roles_list= response.data.data.skills_roles
          })
          .catch((error) => {
            console.log(error);
          })
          
        for (skill_roles of this.skills_roles_list) {
          await axios
            .get("http://127.0.0.1:5001/skills/" + skill_roles.skills_id)
            .then((response) => {
              this.skill_list.push(response.data)
              this.skill_dict[skill_roles.skills_id]= response.data;
              })
            .catch((error) => {
              console.log(error);
            })
        }

        for(skill of this.skill_list){
          await axios
          .get("http://127.0.0.1:5005/skills_courses/skill/" + skill.skill_id)
          .then((response) => {
            this.course_list.push(response.data.data.skills_courses);
          })
          .catch((error) => {
            console.log(error);
          })
        }
 
        var course_flat_list= this.course_list.flat()
        console.log('course_flat_list')
        console.log(course_flat_list)
        for(course of course_flat_list){
          if(course.course_id in this.course_skills && !(course.skill_id in this.course_skills[course.course_id])){
            this.course_skills[course.course_id].push(course.skill_id)
          }else{
            this.course_skills[course.course_id]=[course.skill_id]
          }
          await axios
          .get("http://127.0.0.1:5003/courses/" + course.course_id)
          .then((response) => {
              this.course_dict[course.course_id]= response.data.data;
          })
          .catch((error) => {
            console.log(error);
          })
        }
        await new Promise((resolve, reject) => setTimeout(resolve, 3000));
        return ;
      },
  },
    mounted() {
      axios
        .get("http://127.0.0.1:5002/roles")
        .then((response) => {
          console.log(response.data.data.roles);
          this.role_list = response.data.data.roles;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  });
  
  create_journey.mount("#create_journey");
  