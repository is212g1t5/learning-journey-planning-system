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
        staff_id: "",
        new_lj_id: "",
        existing_lj_names: [],
        registered_courses:[],
        completed_courses: [],
        ongoing_courses: [],
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
        lj_api: {
          getAll: "http://127.0.0.1:5004/learning_journeys/create",
          create_lj:"http://127.0.0.1:5004/learning_journeys/create" ,
          create_role_skill: "http://127.0.0.1:5007/lj_skills/create",
          create_course:  "http://127.0.0.1:5009/lj_courses/create"
        }
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
        console.log(this.existing_lj_names)
        if (newValue && newValue.trim().length > 0) {
          this.errorMsgs.name = "";
          if (newValue && newValue.trim().length > 64) {
            this.errorMsgs.name =
              "Learning Journey name cannot be more than 64 characters";
          }
          else if (Object.values(this.existing_lj_names).includes(newValue)) {
            this.errorMsgs.name = "Learning Journey name already exists. Please use a unique name.";
          }  
          else {
            this.errorMsgs.name = "";
          }
        } 
        else {
          this.errorMsgs.name = "Learning Journey cannot be empty";
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
      resetValues(){
        this.skills_roles_list= [];
        this.skill_list = [];
        this.course_list=[];  
        this.course_dict= {};
        this.selected_courses= [];
        this.selected_role= "";
        this.course_skills= {};
        this.selectCourses= [];
        this.role= "";
        this.role_id= "",
        this.getNewLJID();
        this.getCurrentLJNames();
      },
      change(event) {
        if (!this.errorMsgs.role) {
          this.resetValues()
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
      isCompleted(course){
        return Object.values(this.completed_courses).includes(course);
      },
      isOngoing(course){
        return Object.values(this.ongoing_courses).includes(course);
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
      async getNewLJID(){
       await axios
        .get("http://127.0.0.1:5004/learning_journeys")
        .then((response) => {
          lj_list = response.data.data.learning_journeys;
          this.new_lj_id= lj_list[lj_list.length -1].learning_journey_id+1;
        })
        .catch((error) => {
          if (error.response.data.code == 404){
            this.new_lj_id= 1;
          }
          console.log(error);
        });
      },
      async getCurrentLJNames(){
        await axios
        .get("http://127.0.0.1:5004/learning_journeys/" + this.staff_id)
        .then((response) => {
          lj_list = response.data.data.learning_journeys;
          for (const [key, value] of Object.entries(lj_list)) {
            this.existing_lj_names.push(value["learning_journey_name"])
          }
          console.log(this.existing_lj_names)
          
        })
        .catch((error) => {
          if (error.response.data.code == 404){
            this.existing_lj_names= [];
          }
          console.log(error);
        });
      },
      async getAllRegisteredCourses(){
        await axios
        .get("http://127.0.0.1:5012/registration/" + this.staff_id)
        .then((response) => {
          this.registered_courses = response.data.data.registration;
          for (const [key, value] of Object.entries(this.registered_courses)) {
            console.log("value")
            if(value["completion_status"] == "Completed"){
              this.completed_courses.push(value["course_id"])
            }
            else if (value["completion_status"] == "Ongoing"){
              this.ongoing_courses.push(value["course_id"])
            }
          }
          console.log("registered courses")
          console.log(this.registered_courses)
          console.log(this.completed_courses)
          console.log(this.ongoing_courses)
        })
        .catch((error) => {
          if (error.response.data.code == 404){
            this.registered_courses= [];
          }
          console.log(error);
        });
      },
      async createNewLJ() {
        try{
            await axios 
            .post(this.lj_api.create_lj, {
              learning_journey_id: this.new_lj_id,
              learning_journey_name: this.name,
              staff_id: this.staff_id,
              role_id: this.role_id,
            })
            .then((response) => {
              console.log(response);
            });

          for (sid of this.selected_skills){
            await axios 
            .post(this.lj_api.create_role_skill, {
              learning_journey_id: this.new_lj_id,
              role_id: this.role_id,
              skill_id: sid
            })
            .then((response) => {
              console.log(response);
            });
          }

          for (cid of this.selected_courses){
            await axios 
            .post(this.lj_api.create_course, 
              {
              learning_journey_id: this.new_lj_id,
              course_id: cid
            })
            .then((response) => {
              console.log(response);
            });
            
          }
          //reset values
          this.alerts.successMsg= "Learning Journey " + this.name + " has been created successfully."
          this.alerts.showSuccess = true;
          this.name="";
          this.resetValues();

        }
        catch(err){
          console.error(err);
          this.alerts.alertMsg = "Please try again later."
          this.alerts.showAlert = true;
          this.name="";
          this.resetValues();
        }
     
     
      }
      
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

        this.getAllRegisteredCourses();
     
    },
    created() {
      let urlParams = new URLSearchParams(window.location.search);
      if (urlParams.has("staff_id")) {
        this.staff_id = urlParams.get("staff_id");
      }
      this.getNewLJID();
      this.getCurrentLJNames();
    
    },
  });
  
  create_journey.mount("#create_journey");
  