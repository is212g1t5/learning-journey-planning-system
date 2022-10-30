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
            axios.get('http://localhost:5009/lj_courses/details/' + this.staff_id+'/'+this.lj_id)
                .then(response => {
                    console.log(response.data.data)
                    information = response.data.data
                    for (res of information){
                        this.learning_journey_details.push(res)
                        console.log(res)
                        this.lj_name = res.learning_journey_name
                    }
                    if (this.learning_journey_details.length == 0) {
                        this.emptyText = "No learning journey details found"
                    }
                })
                .catch(error => {
                    console.log(error)
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

