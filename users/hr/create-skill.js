const app = Vue.createApp({
   data() {
         return {
            skillForm: {
               name: '',
               category: 'example',
               description: 'testing only',
               level: 1,
               status: true, //0 - retired; 1 - active
            },
            confirmationMsg: '',
            errorMsgs: {
               name: '',
               category: '',
               description: '',
            },
            skill_api: {
               create: ""
            }
         }
   },
   created() {
      // this.getAllSkillNames();
      // this.getAllSkillCategories();
   },
   computed: {
      isFormValid() {
         return !this.skillForm.name.trim() 
         || !this.skillForm.category.trim() 
         || !this.skillForm.description.trim()
         || !Object.values(this.errorMsgs).some(
            value => value !== ''
         );
      },//trying to make it check that if there are error msgs, dont allow submit
   },
   watch: {
      'skillForm.name'(newValue) {
         if (newValue && newValue.trim().length >= 3) {
            this.errorMsgs.name = '';

         } else {
            this.errorMsgs.name = 'Not long enough';
         }
      },
      //validate whether category is empty
      'skillForm.category'(newValue) {
         if (newValue && newValue.trim().length > 0) {
            this.errorMsgs.category = '';

         } else {
            this.errorMsgs.category = 'Category cannot be left empty';
         }
      }
   },
   methods: {
      //api call to retrieve all existing skill names
      getAllSkilNames() {
         //tbc
         
      },
      //api call to retrieve all existing skill categories
      getAllSkillCategories(){
         //tbc
      },
      //trigger confirmation popup before creating skill
      confirmNewSkill() {
         this.confirmationMsg = 'Are you sure you want to create this skill, '
         + this.skillForm.name
         + '?';

         this.createNewSkill();
         
      },
      //call role api to create new skill
      createNewSkill() {
         console.log("API Call to create new skill");
         console.log(this.skillForm);

         //call api to create new skill
      },
   }
});

// component templates
app.component('sound-icon', {
   data() {
         return {
            soundEmojis: ['🔇', '🔈', '🔉', '🔊']
         }
   },
   props: ['level'],
   template: `<span> {{soundEmojis[level]}} </span>` // TODO: add your template code here
})

app.mount("#create-skill");