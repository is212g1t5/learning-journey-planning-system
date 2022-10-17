const update = Vue.createApp({
  data() {
    return {
      id: "",
      currentRoleInfo: {
        name: "",
        description: "",
        status: true, //0 - retired; 1 - active
        sector: "",
        track: "",
      },
      roleForm: {
        id: "",
        name: "",
        description: "",
        status: true,
        sector: "",
        track: "",
      },
      errorMsgs: {
        name: "",
        description: "",
        sector: "",
        track: "",
      },
      alerts: {
        showAlert: false,
        alertMsg: "",
        showSuccess: false,
        successMsg: "",
      },
      existingRoles: [],
      skillSearch: "",
      skillsList: [],
      assignedSkills: [],
      addedSkills: [],
      removedSkills: [],
    };
  },
  methods: {
    updateRole() {
      //if new skills to assign, assign added skills
      if (this.addedSkills.length > 0) {
        for (let id of this.addedSkills) {
          this.assignSkills(id);
        }
      }

      //if skills to remove, remove skills
      if (this.removedSkills.length > 0) {
        for (let id of this.removedSkills) {
          this.removeSkills(id);
        }
      }

      console.log(this.hasChangesMade);

      //update role details
      if (this.hasChangesMade) {
        this.updateRoleDetails();
      }
    },
    updateRoleDetails() {
      this.alerts.showAlert = false;
      this.alerts.showSuccess = false;
      axios
        .put(
          "http://127.0.0.1:5002/roles/update/" + this.id,
          {
            role_name: this.roleForm.name,
            role_desc: this.roleForm.description,
            role_status: this.roleForm.status,
            role_sector: this.roleForm.sector,
            role_track: this.roleForm.track,
          },
          {}
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
    },
    async getAllSkills() {
      //call api to get all skills
      try {
        const res = await axios({
          url: "http://127.0.0.1:5001/skills",
        });

        data = res.data.data;
        this.skillsList = data.skills;

      } catch (err) {
        // Handle Error Here
        console.error(err);
      }
    },
    //get skills tied to role
    async getAssignedSkills() {
      try {
        const res = await axios({
          url: "http://127.0.0.1:5005/skills_roles/" + this.id
        });

        data = res.data.data;
        this.assignedSkills = data.skills_roles.map((pair) => pair.skills_id);

      } catch (err) {
        // Handle Error Here
        console.error(err);
      }
    },
    //assign skills to role
    async assignSkills(skillId){
      try {
        const res = await axios({
          url: "http://127.0.0.1:5005/skills_roles",
          method: 'post',
          data: {
            role_id: this.id,
            skill_id: skillId
          }
        });

        data = res.data.data;
        this.addedSkills = [];
        this.getAssignedSkills();

        this.alerts.successMsg = "Skills assigned successfully.";
        this.alerts.showSuccess = true;

      } catch (err) {
        // Handle Error Here
        console.error(err);

        this.alerts.showAlert = true;
        this.alerts.alertMsg = err;
      }
    },
    //remove skills from role
    async removeSkills(skillId){
      try {
        const res = await axios({
          url: "http://127.0.0.1:5005/skills_roles/" + skillId + "/" + this.id,
          method: 'delete'
        });

        data = res.data.data;
        this.removedSkills = [];
        this.getAssignedSkills();

        this.alerts.successMsg = "Skills updated successfully.";
        this.alerts.showSuccess = true;

      } catch (err) {
        // Handle Error Here
        console.error(err);

        this.alerts.showAlert = true;
        this.alerts.alertMsg = err;
      }
    },
    //api call to retrieve all existing skill names
    async getAllRoleNames() {
      //call api to get all skill names
      try {
        const res = await axios({
          url: "http://127.0.0.1:5002/roles",
        });

        data = res.data.data;
        this.existingRoles = data.roles.map((role) => role.role_name.toLowerCase());

      } catch (err) {
        // Handle Error Here
        console.error(err);
      }
    },
  },
  created() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id")) {
      this.id = urlParams.get("id");
    }

    this.getAllRoleNames();
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5002/roles/" + this.id)
      .then((response) => {
        role = response.data;
        this.roleForm.id = role.role_id;
        this.currentRoleInfo.name = role.role_name;
        this.currentRoleInfo.description = role.role_desc;
        this.currentRoleInfo.status = role.role_status;
        this.currentRoleInfo.sector = role.role_sector;
        this.currentRoleInfo.track = role.role_track;

        this.roleForm.name = this.currentRoleInfo.name
        this.roleForm.description = this.currentRoleInfo.description
        this.roleForm.status = this.currentRoleInfo.status
        this.roleForm.sector = this.currentRoleInfo.sector
        this.roleForm.track = this.currentRoleInfo.track
      })
      .catch((error) => {
        console.log(error);
        this.error = true;
      })
      .finally(() => {
        this.loading = false;
      });

    //retrieve all skills
    this.getAllSkills();

    //retrieve list of id of assigned skills
    this.getAssignedSkills();
  },
  watch: {
    "roleForm.name"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.name = "";

        if (this.existingRoles.includes(newValue.trim().toLowerCase())) {
          this.errorMsgs.name = "Role already exists";
        } else {
          this.errorMsgs.name = "";
        }
        
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.name = "Role name cannot be more than 64 characters";
        } else {
          this.errorMsgs.name = "";
        }
      } else {
        this.errorMsgs.name = "Role name cannot be empty";
      }
    },
    "roleForm.description"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.description = "";
        if (newValue && newValue.trim().length > 512) {
          this.errorMsgs.description =
            "Description cannot be more than 512 characters";
        } else {
          this.errorMsgs.description = "";
        }
      } else {
        this.errorMsgs.description = "Description cannot be empty";
      }
    },
    "roleForm.sector"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.sector = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.sector =
            "Role sector cannot be more than 64 characters";
        } else {
          this.errorMsgs.sector = "";
        }
      } else {
        this.errorMsgs.sector = "Role sector cannot be empty";
      }
    },
    "roleForm.track"(newValue) {
      if (newValue && newValue.trim().length > 0) {
        this.errorMsgs.track = "";
        if (newValue && newValue.trim().length > 64) {
          this.errorMsgs.track = "Role track cannot be more than 64 characters";
        } else {
          this.errorMsgs.track = "";
        }
      } else {
        this.errorMsgs.track = "Role track cannot be empty";
      }
    },
  },
  computed: {
    isFormInvalid() {
      return (
        !this.roleForm.name.trim() ||
        !this.roleForm.description.trim() ||
        !this.roleForm.sector.trim() ||
        !this.roleForm.track.trim() ||
        Object.values(this.errorMsgs).some((error) => {
          return error !== ""
        }) ||
        !(this.hasChangesMade || this.addedSkills.length > 0 || this.removedSkills.length > 0) ||
        !this.hasSkills
      );
    },
    //return skills that are not assigned to role and not already added
    skillOptions() {
      let result = [];

      for (let skill of this.skillsList) {
        if (
          !this.assignedSkills.includes(skill.skill_id) &&
          !this.addedSkills.includes(skill.skill_id) &&
          !this.removedSkills.includes(skill.skill_id)
        ) {
          result.push(skill);
        }
      }

      return result;
    },
    //return if there are any skills assigend or to be assigned to the role
    hasSkills() {
      return this.addedSkills.length > 0 ||
      this.assignedSkills.length !== this.removedSkills.length;
    },
    //check if changes have been made to role details
    hasChangesMade() {
      return (
        this.roleForm.name !== this.currentRoleInfo.name ||
        this.roleForm.description !== this.currentRoleInfo.description ||
        this.roleForm.status !== this.currentRoleInfo.status ||
        this.roleForm.sector !== this.currentRoleInfo.sector ||
        this.roleForm.track !== this.currentRoleInfo.track
      );
    }
  },
});


update.mount("#update");
