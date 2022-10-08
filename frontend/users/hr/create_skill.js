const create = Vue.createApp({
   data() {
      return {
         skillForm: {
            name: "",
            category: "",
            description: "",
            level: 1,
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
         },
         existingSkills: [],
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
         //tbc
         this.existingSkills = ["skill1", "skill2", "skill3"];

         //call api to get all skill names
         // try {
         //    const res = await axios({
         //       url: this.skill_api.getAll,
         //    });

         //    data = res.data.data;
         //    console.log(data);
         //    this.existingSkills = data;

         // } catch (err) {
         //    // Handle Error Here
         //    console.error(err);
         // }
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
      //cancel skill creation
      cancelNewSkill() {
         this.confirmationMsg = "";
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
            this.confirmationMsg = "";

         //to be continued...
         //redirect to created skill details page
         } catch (err) {
            // Handle Error Here
            console.error(err);
         }
      },
   },
});

create.mount("#create-skill");
