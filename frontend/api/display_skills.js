const display_skills = Vue.createApp({
    data() {
        return {
            skill_list: [],
            noSkillsMsg: "",
        }
    },
    methods:{
        sendMessage(){
            skillBus.$emit('send-message', skill_list)
          }
      },
    mounted() {
        axios
            .get("http://localhost:5001/skills")
            .then((response) => {
                var skill_list = response.data.data;
                this.skill_list= skill_list
                console.log(skill_list)
                if (skill_list.length==0){
                    this.noSkillsMsg= "No skills recorded. Please create a skill."
                }
                this.sendMessage()
            })
            .catch((error) => {
                console.log(error);
            })
    },
})

display_skills.mount("#display_skills");