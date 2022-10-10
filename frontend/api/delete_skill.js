const delete_skill = Vue.createApp({
    data() {
      return {
        id: "",
        skillInfo: {
            id: "",
            name: "",
            category: "",
            desc: "",
            status: true,
        },
        msges: {
            successMsg: "",
            successAlert: false,
            errorMsg: "",
            errorAlert: false,
        }
      };
    },
    methods: {
        deleteSkill() {      
            this.msges.errorAlert = false;
            this.msges.successAlert = false;       
            axios.delete("http://localhost:5001/skills/delete/" + this.id)
            .then((response) => {
                console.log(response.data)
            })
            .catch((error) => {
                if (error) {
                    this.msges.errorAlert = true;
                    this.msges.errorMsg = "❌ Delete Unsuccessful";
                    console.log(error);
                    this.error = true;
                }
            })
            .finally(() => {
                this.loading = false;
            });
            this.skillInfo.status = false;
            this.msges.successAlert = true;
            this.msges.successMsg = "✔️ Delete Successful!"
        },
        restoreSkill() {      
            this.msges.errorAlert = false;
            this.msges.successAlert = false;   
            axios.put("http://localhost:5001/skills/restore/" + this.id)
            .then((response) => {
                console.log(response.data)
            })
            .catch((error) => {
                if (error) {
                    this.msges.errorAlert = true;
                    this.msges.errorMsg = "❌ Delete Unsuccessful";
                    console.log(error);
                    this.error = true;
                }
            })
            .finally(() => {
                this.loading = false;
            });
            this.skillInfo.status = true;
            this.msges.successAlert = true;
            this.msges.successMsg = "✔️ Restore Successful!"
        },
        
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has("id")) {
            this.id = urlParams.get("id");
        }
    },
    mounted() {
        axios
        .get("http://localhost:5001/skills/" + this.id)
        .then((response) => {
            skill = response.data;
            this.skillInfo.id = skill.skill_id;
            this.skillInfo.name = skill.skill_name;
            this.skillInfo.category = skill.skill_category;
            this.skillInfo.desc = skill.skill_desc;
            this.skillInfo.status = skill.skill_status;
        })
        .catch((error) => {
            if (error) {
                console.log(error);
                this.error = true;
            }
        })
        .finally(() => {
            this.loading = false;
        });
    },
    });
  
delete_skill.mount("#delete_skill");