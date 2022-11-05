const display_learning_journey_details = Vue.createApp({
    data() {
        return {
            learning_journey_details: [],
            lj_id: '',
            lj_name: '',
            staff_id: '',
            emptyText: '',
            role_name:'',
        }
    },
    methods: {
        getLearningJourneyDetails() {
            axios.get('http://localhost:5004/learning_journeys/id/'+this.lj_id)
                .then(response => {
                    
                    information = response.data.data.learning_journey
                        console.log('awaiting response...')
                        console.log(information)
                        var skillsInfoList =[]
                        var skills_info = information.skills
                        var courses = information.courses
                        for(skill in skills_info){
                            skillsInfoList.push(skills_info[skill])
                        }
                        console.log(skillsInfoList)
                        final_results = []
                        for(sk of skillsInfoList){
                            var skill_info = {
                                'learning_journey_id': this.lj_id,
                                'skill_name': sk.skill_name
                            }
                            for(course of sk.mapping){
                                skill_info['course_code'] =course
                                skill_info['course_status']= courses[course]['status']
                                final_results.push(skill_info)
                            }
                        }
                        
                        this.lj_name = information['learning_journey_name']

                        this.role_name = information['role']['role_name']

                        // var course_list = Object.keys(courses)

                        // var skills = information.skills
                        // var skill_list = Object.keys(skills)
                        // results = []
                        // for (course of course_list) {
                        //     var course_items = {}
                        //     course_items['course_code'] = course
                        //     course_items['status'] = courses[course]['status']
                        //     course_items['skills'] = ''
                        //     for (skill of skill_list) {
                        //         var skill_info = skills[skill]

                        //         var course_codes = skill_info['mapping']
                        //         if (course_codes.includes(course)) {
                        //             course_items['skills'] += skill_info['skill_name'] + ', '
                        //         }
                        //     }
                        //     results.push(course_items)
                        this.learning_journey_details = final_results
                    // }

                    
                            })
                .catch(error => {
                    console.log(error)
                    this.emptyText = 'No Learning Journey Details Found'
                })
        },
        updateJourney() {

            window.location.href = 'update_journey.html?id=' + this.lj_id;
        }
    },
    async mounted() {
        let urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has("id")) {
            this.lj_id = urlParams.get("id");
        }
        await this.getLearningJourneyDetails(this.lj_id);
    },
    async created() {
        
        
    }
})

display_learning_journey_details.mount("#display_learning_journey_details");

