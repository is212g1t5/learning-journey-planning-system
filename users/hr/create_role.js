const createRole = Vue.createApp({
   data() {
      return {
         roleForm: {
            name: "",
            description: "",
            status: true
         },
         confirmationMsg: "",
         errorMsgs: {
            name: "",
            category: "",
            description: "",
         },
         role_api: {
            create: "http://127.0.0.1:5002/roles/create",
            getAll: "http://127.0.0.1:5002/roles",
         },
         existingRoles: [],
      };
   },
   created() {
      this.getAllRoleNames();
      console.log(this.existingRoles);
      // this.getAllSkillCategories();
   },
   computed: {
      isFormValid() {
         return (
            !this.roleForm.name.trim() ||
            !this.roleForm.category.trim() ||
            !this.roleForm.description.trim() ||
            Object.values(this.errorMsgs).some((error) => {
               return error !== "";
            })
         );
      },
   },
   watch: {
      "roleForm.name"(newValue) {
         if (newValue && newValue.trim().length > 0) {
         //check if skill name already exists
         if (this.existingRoles.includes(newValue.toLowerCase())) {
            this.errorMsgs.name = "Skill already exists";
         } else {
            this.errorMsgs.name = "";
         }
         } else {
            this.errorMsgs.name = "Skill name cannot be empty";
         }
      },
      //validate whether description is empty
      "roleForm.description"(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.description = "";
         } else {
            this.errorMsgs.description = "Description cannot be empty";
         }
      },
   },
   methods: {
      //api call to retrieve all existing skill names
      async getAllRoleNames() {

         //call api to get all skill names
         try {
            const res = await axios({
               url: this.role_api.getAll,
            });

            data = res.data.data;
            console.log(data);
            this.existingRoles = data;

         } catch (err) {
            // Handle Error Here
            console.error(err);
         }
      },
      //trigger confirmation popup before creating skill
      confirmNewRole() {
         this.confirmationMsg =
         "Are you sure you want to create this role, " +
         this.roleForm.name +
         "?";
      },
      //call role api to create new skill
      async createNewRole() {
         //call api to create new skill
         try {
            const res = await axios({
               method: "post",
               url: this.role_api.create,
               data: {
                  skill_name: this.roleForm.name,
                  skill_category: this.roleForm.category,
                  skill_desc: this.roleForm.description,
                  skill_status: this.roleForm.status,
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

createRole.mount("#create-role");
