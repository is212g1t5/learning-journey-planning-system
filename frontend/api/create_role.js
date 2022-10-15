const createRole = Vue.createApp({
   data() {
      return {
         roleForm: {
            name: "",
            sector: "",
            description: "",
            track: "",
            status: true
         },
         confirmationMsg: "",
         errorMsgs: {
            name: "",
            sector: "",
            description: "",
            track: ""
         },
         role_api: {
            create: "http://127.0.0.1:5002/roles/create",
            getAll: "http://127.0.0.1:5002/roles",
         },
         existingRoles: [],
         alerts: {
            alertMsg: "",
            successMsg: "",
            showAlert: false,
            showSuccess: false
         }
      };
   },
   created() {
      this.getAllRoleNames();
   },
   computed: {
      isFormValid() {
         return (
            !this.roleForm.name.trim() ||
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
         if (this.existingRoles.includes(newValue.trim().toLowerCase())) {
            this.errorMsgs.name = "Skill already exists";
         } else {
            this.errorMsgs.name = "";
         }
         } else {
            this.errorMsgs.name = "Skill name cannot be empty";
         }
      },
      //validate whether sector is empty
      "roleForm.sector"(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.sector = "";
         } else {
            this.errorMsgs.sector = "Sector cannot be empty";
         }
      },
      //validate whether track is empty
      "roleForm.track"(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.track = "";
         } else {
            this.errorMsgs.track = "Track cannot be empty";
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
            this.existingRoles = data.roles.map((role) => role.role_name.toLowerCase());

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
                  role_name: this.roleForm.name.trim(),
                  role_sector: this.roleForm.sector.trim(),
                  role_desc: this.roleForm.description.trim(),
                  role_track: this.roleForm.track.trim(),
                  role_status: this.roleForm.status
               },
            });

            data = res.data.data;
            console.log("New skill " + data.role_name + " created successfully");
            this.confirmationMsg = "";

            this.alerts.successMsg = "New role '" + data.role_name + "' created successfully";
            this.alerts.showSuccess = true;
            this.getAllRoleNames();

         //to be continued...
         //redirect to created skill details page
         } catch (err) {
            // Handle Error Here
            console.error(err);
            this.alerts.showAlert = true;
            this.alerts.alertMsg = err;
         }
      },
   },
});

createRole.mount("#create-role");
