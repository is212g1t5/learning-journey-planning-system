const create = Vue.createApp({
   //resolving
   data() {
      return {
         skillForm: {
            name: "",
            category: "",
            description: "",
            status: true
         },
         confirmationMsg: "",
         errorMsgs: {
            name: "",
            category: "",
            description: "",
         },
         skill_api: {
            create: "http://127.0.0.1:5001/skills/create",
            getAll: "http://127.0.0.1:5001/skills",
            viewSpecific: "http://127.0.0.1:5001/skills/"
         },
         existingSkills: [],
         alerts: {
            showAlert: false,
            showSuccess: false,
            alertMsg: "",
            successMsg1: "New skill ",
            successMsg2: " created successfully."
         },
         viewSkillLink: ''
      };
   },
   created() {
      this.getAllSkillNames();
      // this.getAllSkillCategories();
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
   watch: {
      "skillForm.name"(newValue) {
         if (newValue && newValue.trim().length > 0) {
         //check if skill name already exists
         if (this.existingSkills.includes(newValue.toLowerCase())) {
            this.errorMsgs.name = "Skill already exists";
         } else {
            this.errorMsgs.name = "";
         }
         } else {
            this.errorMsgs.name = "Skill name cannot be empty";
         }
      },
      //validate whether category is empty
      "skillForm.category"(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.category = "";
         } else {
            this.errorMsgs.category = "Category cannot be empty";
         }
      },
      //validate whether description is empty
      "skillForm.description"(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.description = "";
         } else {
            this.errorMsgs.description = "Description cannot be empty";
         }
      },
   },
   methods: {
      //api call to retrieve all existing skill names
      async getAllSkillNames() {
         //call api to get all skill names
         try {
            const res = await axios({
               url: this.skill_api.getAll,
            });

            data = res.data.data;
            this.existingSkills = data.skills.map((skill) => skill.skill_name.toLowerCase());
            console.log(this.existingSkills);

         } catch (err) {
            // Handle Error Here
            console.error(err);
         }
      },
      //api call to retrieve all existing skill categories
      getAllSkillCategories() {
         //tbc
      },
      //trigger confirmation popup before creating skill
      confirmNewSkill() {
         this.confirmationMsg =
         "Are you sure you want to create this skill, " +
         this.skillForm.name +
         "?";
      },
      //call role api to create new skill
      async createNewSkill() {
         //call api to create new skill
         try {
            const res = await axios({
               method: "post",
               url: this.skill_api.create,
               data: {
                  skill_name: this.skillForm.name,
                  skill_category: this.skillForm.category,
                  skill_desc: this.skillForm.description,
                  skill_status: this.skillForm.status,
               },
            });

            data = res.data.data;
            console.log("New skill " + data.skill_name + " created successfully");
            console.log(data);
            this.confirmationMsg = "";

            //LINK HERE NEEDS TO BE CHANGED TO LINK TO VIEW SPECIFIC SKILL PAGE
            this.viewSkillLink = `<a href="${this.skill_api.viewSpecific}${data.skill_id}">${data.skill_name}</a>`;

            this.alerts.showSuccess = true;
            //reset form
            this.skillForm = {
               name: "",
               category: "",
               description: "",
               status: true
            };

         //to be continued...
         //redirect to created skill details page
         } catch (err) {
            // Handle Error Here
            console.error(err);
            this.alerts.showAlert = true;
         }
      },
   },
});

create.mount("#create-skill");
