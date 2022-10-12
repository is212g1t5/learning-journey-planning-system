const delete_role = Vue.createApp({
    data() {
      return {
        id: "",
        roleInfo: {
            id: "",
            name: "",
            desc: "",
            status: true,
            sector: "",
            track: "",
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
        deleteRole() {      
            this.msges.errorAlert = false;
            this.msges.successAlert = false;       
            axios.delete("http://localhost:5002/roles/delete/" + this.id)
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
            this.roleInfo.status = false;
            this.msges.successAlert = true;
            this.msges.successMsg = "✔️ Delete Successful!"
        },
        restoreRole() {      
            this.msges.errorAlert = false;
            this.msges.successAlert = false;   
            axios.put("http://localhost:5002/roles/restore/" + this.id)
            .then((response) => {
                console.log(response.data)
            })
            .catch((error) => {
                if (error) {
                    this.msges.errorAlert = true;
                    this.msges.errorMsg = "❌ Restore Unsuccessful";
                    console.log(error);
                    this.error = true;
                }
            })
            .finally(() => {
                this.loading = false;
            });
            this.roleInfo.status = true;
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
        .get("http://localhost:5002/roles/" + this.id)
        .then((response) => {
            role = response.data;
            this.roleInfo.id = role.role_id;
            this.roleInfo.name = role.role_name;
            this.roleInfo.desc = role.role_desc;
            this.roleInfo.status = role.role_status;
            this.roleInfo.sector = role.role_sector;
            this.roleInfo.track = role.role_track;
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
  
delete_role.mount("#delete_role");