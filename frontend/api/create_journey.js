const create_journey = Vue.createApp({
    data() {
      return {
        name: "",
        role: "",
        role_id: "",
        skill_list: [],
        course_list: [],
        course_dict: {},
        role_list: [],
        skills_roles_list: [],
        course_details_list: [],
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
      role(newValue) {
        this.skills_roles_list= [];
        this.skill_list = [];
        this.course_list=[];
        this.course_details_list=[];
        this.course_dict= {};
        axios
          .get("http://127.0.0.1:5006/skills_roles/" + this.role_id)
          .then((response) => {
            for (skill_roles of response.data.data.skills_roles) {
              axios
                .get("http://127.0.0.1:5001/skills/" + skill_roles.skills_id)
                .then((response) => {
                  this.skill_list.push(response.data);
                  for(skill of this.skill_list){
                    axios
                    .get("http://127.0.0.1:5005/skills_courses/skill/" + skill.skill_id)
                    .then((response) => {
                      // this.course_list.push(response.data.data.skills_courses);
                        console.log('skill_rokes')
                        console.log(skill_roles)
                        console.log('skill')
                        console.log(skill.skill_id)
                        if(skill.skill_id in this.course_dict){
                          this.course_dict[skill.skill_id].push(...response.data.data.skills_courses);
                        }
                        else{
                          this.course_dict[skill.skill_id]= response.data.data.skills_courses;
                        }
                      
                      
                    })
                    .catch((error) => {
                      console.log(error);
                    })
                  }
                })
                .catch((error) => {
                  console.log(error);
                })
            }
          })
          console.log(this.course_dict)
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
          this.skill_list = [];
          this.role = event.target.value;
          for (role of this.role_list) {
            if (role.role_name == this.role) {
              this.role_id = role.role_id;
              // console.log(this.role_id);
            }
          }
        }
      },
      selectCourses() {
        window.location.href =
          "select_courses.html?role_id=" + this.role_id + "&name=" + this.name;
      },
      getSkillRoleList(){
        axios
          .get("http://127.0.0.1:5006/skills_roles/" + this.role_id)
          .then((response) => {
            this.skills_roles_list= response.data.data.skills_roles
          })
          .catch((error) => {
            console.log(error);
          })
        },
      getSkillList(){
        for (skill_roles of this.skills_roles_list) {
          axios
            .get("http://127.0.0.1:5001/skills/" + skill_roles.skills_id)
            .then((response) => {
              this.skill_list.push(response.data)
              })
            .catch((error) => {
              console.log(error);
            })
        }
      },
      getCourseList(){
        for(skill of this.skill_list){
          axios
          .get("http://127.0.0.1:5005/skills_courses/skill/" + skill.skill_id)
          .then((response) => {
            this.course_list.push(response.data.data.skills_courses);
          })
          .catch((error) => {
            console.log(error);
          })
        }
    },
    getAll(){
      axios.all([
        axios.get("http://127.0.0.1:5006/skills_roles/" + this.role_id),
        axios.get("http://127.0.0.1:5001/skills/" + skill_roles.skills_id),
        axios.get("http://127.0.0.1:5005/skills_courses/skill/" + skill.skill_id)
    ])

    .then(axios.spread(function (response1, response2, response3) {
        //response1 is the result of first call
        //response2 is the result of second call
        this.skills_roles_list= response1.data.data.skills_roles
        this.skill_list.push(response2.data)
        this.course_list.push(response3.data.data.skills_courses);
    }))
    .catch(function (error) {
      console.log(error);
    });
    }
    // async createLists(){
    //   await this.getRoleList();
    //   await this.getSkillList();
    //   await this.getCourseList();
    // }
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
    // async created(){
  //     await this.getRoleList();
  //     await this.getSkillList();
  //     await this.getCourseList();
  // }
  });
  
  create_journey.mount("#create_journey");
  