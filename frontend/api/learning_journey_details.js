const display_learning_journey_details = Vue.createApp({
    data() {
        return {
            learning_journey_details: [],
            lj_id: '',
            lj_name: '',
            staff_id: '',
            emptyText: '',
        }
    },
    methods: {
        getLearningJourneyDetails() {
            axios.get('http://localhost:5004/learning_journeys/id/'+this.lj_id)
                .then(response => {
                    
                    information = response.data.data.learning_journey
                        console.log('awaiting response...')
                        console.log(information)
                        var courses = information.courses
                        this.lj_name = information['learning_journey_name']
                        var course_list = Object.keys(courses)

                        var skills = information.skills
                        var skill_list = Object.keys(skills)
                        results = []
                        for (course of course_list) {
                            var course_items = {}
                            course_items['course_code'] = course
                            course_items['status'] = courses[course]['status']
                            console.log(courses)
                            course_items['skills'] = ''
                            for (skill of skill_list) {
                                var skill_info = skills[skill]

                                var course_codes = skill_info['mapping']
                                if (course_codes.includes(course)) {
                                    console.log(course)
                                    console.log(skill_info['skill_status'])
                                    course_items['skills'] += skill_info['skill_name'] + ', '
                                }
                            }
                            results.push(course_items)
                        this.learning_journey_details = results
                    }

                    
                            })
                .catch(error => {
                    console.log(error)
                    this.emptyText = 'No Learning Journey Details Found'
                })
        },
        deleteCourse(course_id) {
            window.location.href = 'delete_course.html?id=' + course_id;
        }
    },
    async mounted() {
        let urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has("id")) {
            this.lj_id = urlParams.get("id");
        }
        if (urlParams.has("staff_id")) {
            this.staff_id = urlParams.get("staff_id");
        }
        await this.getLearningJourneyDetails(this.lj_id, this.staff_id);
    },
    async created() {
        
        
    }
})

display_learning_journey_details.mount("#display_learning_journey_details");

