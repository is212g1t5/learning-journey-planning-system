const update = Vue.createApp({
  data() {
    return {
      skillForm: {
        id: "",
        name: "",
        category: "",
        description: "",
        status: true, //0 - retired; 1 - active
      },
      errorMsgs: {
        name: "",
        category: "",
        description: "",
      },
    };
  },
  methods: {
    updateSkill() {
      axios.put(
        "http://127.0.0.1:5001/skill/update/1",
        {
          skill_name: this.skillForm.name,
          skill_category: this.skillForm.category,
          skill_desc: this.skillForm.description,
          skill_status: this.skillForm.status,
        },
        {}
      );
    },
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5001/skill/1")
      .then((response) => {
        skill = response.data;
        this.skillForm.id = skill.skill_id;
        this.skillForm.name = skill.skill_name;
        this.skillForm.category = skill.skill_category;
        this.skillForm.description = skill.skill_desc;
        this.skillForm.status = skill.skill_status;
      })
      .catch((error) => {
        console.log(error);
        this.error = true;
      })
      .finally(() => {
        this.loading = false;
      });
  },
});

update.mount("#update");
