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
        }
      };
    },
    methods: {
        deleteSkill() {      
            axios.delete("http://localhost:5001/skills/delete/" + 2)
            .then((response) => {
                console.log(response.data)
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
            this.skillInfo.status = false;
        },
        restoreSkill() {      
            axios.delete("http://localhost:5001/skills/restore/" + 2)
            .then((response) => {
                console.log(response.data)
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
            this.skillInfo.status = true;
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
        .get("http://localhost:5001/skills/" + 2)
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