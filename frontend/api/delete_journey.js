const delete_journey = Vue.createApp({
    data() {
        return {
            id: "",
            lj: {},
            msges: {
                successMsg: "",
                successAlert: false,
                errorMsg: "",
                errorAlert: false,
            }
        };
    },
    methods: {
        deleteJourney() {      
            this.msges.errorAlert = false;
            this.msges.successAlert = false;       
            axios.delete("http://localhost:5004/learning_journeys/delete/" + this.id)
            .then((response) => {
                console.log(response.data);
                this.msges.successAlert = true;
                this.msges.successMsg = "✔️ Delete Successful!";
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
        },        
    },
    created() {
        let urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has("id")) {
            this.id = urlParams.get("id");
        }
        if (urlParams.has("staff_id")) {
            this.staff_id = urlParams.get("staff_id");
        }
    },
    mounted() {
        axios
        .get("http://localhost:5004/learning_journeys/id/" + this.id)
        .then((response) => {
            lj = response.data;
            this.lj = lj.data.learning_journey
            console.log(lj.data.learning_journey)
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

delete_journey.mount("#delete_journey");