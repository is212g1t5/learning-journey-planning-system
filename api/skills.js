const del = Vue.createApp({
    data() {
      return {
        skillInfo: {
            id: "",
            name: "",
            modalTitle:"",
            status: true,
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
        refreshData(){
            axios.get("http://localhost:5001/skills/" + this.id)
            .then((response)=>{
                this.skills=response.data;
                console.log(response.data)
            })
        },
        deleteSkill(id) {      
            this.modalTitle = "Confirm Delete Skill"      
            this.alerts.showAlert = false;
            this.alerts.showSuccess = false;
            axios.delete("http://localhost:5001/skills/delete/" + this.id,
            {skill_status: this.skillInfo.status})
            .then((response) => {
                this.alerts.showSuccess = true;
                this.alerts.successMsg = response.data.message;
                this.refreshData();
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
    },
  });
  
  del.mount("#del");