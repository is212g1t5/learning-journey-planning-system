const display_journey = Vue.createApp({
    data(){
        return{
            learning_journeys: [],
            emptyText: "",
            searchQuery: null,
            fields: [
                { key: 'learning_journey_name', label: 'Learning Journey Name', sortable: true, sortDirection: 'desc' },
                { key: 'actions', label: 'Actions' }
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
                pageOptions: [5, 10, 15, 100],
                startRow: 0,
                endRow: 10,
                pageSize: null,
                sortBy: '',
                sortDesc: false,
                sortDirection: 'asc',
                currentSort:'learning_journey_name',
                currentSortDir:'asc',
                sortIcon: {'learning_journey_name': 'mx-2 fa fa-xs fa-sort'},
                pageItemIcon: {
                'false': 'page-item',
                'true': 'page-item active'
                },
        }
    },
    computed: {
        sortedResultQuery() {
            return this.resultQuery.sort((a,b) => {
                let modifier = 1;
                if(this.currentSortDir === 'desc') modifier = -1;
                if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
                if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
                return 0;
            });
        },
        resultQuery() {
            if (this.searchQuery) {
                return this.learning_journeys.filter(item => {
                return this.searchQuery
                    .toLowerCase()
                    .split(" ")
                    .every(v => item.learning_journey_name.toLowerCase().includes(v));
                });
            } else {
                return this.learning_journeys;
            }
        },
        paginatedQuery(){
          return this.sortedResultQuery.slice(this.startRow, this.endRow)
        },
    },
    watch: {
        perPage() {
            this.pageSize = Math.ceil(this.totalRows/this.perPage);
            this.startRow = 0;
            this.endRow = this.perPage;
        }
    },
    methods: {
        createJourney(){
            window.location.href = 'create_journey.html';
        },
        viewJourneyDetails(learning_journey_id, staff_id){
            window.location.href = 'learning_journey_details.html?id=' + learning_journey_id + '&staff_id=' + staff_id ;
        },
        updateJourney(id){
            window.location.href = 'update_journey.html?id=' + learning_journey_id;
        },
        deleteJourney(id){
            window.location.href = 'delete_journey.html?id=' + learning_journey_id;
        },
        sort(s) {
            //if s == current sort, reverse
            if(s === this.currentSort) {
                this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
                this.sortIconFn(s)
            }
            this.currentSort = s;
            this.sortIconFn(s)
          },
        sortIconFn(s){   
            Object.keys(this.sortIcon).forEach(key => {
                this.sortIcon[key] = 'mx-2 fa fa-xs fa-sort'
            });          
            if (this.currentSortDir=='asc'){ 
                this.sortIcon[s]='mx-2 fa fa-xs fa-sort-asc'
            } else if (this.currentSortDir=='desc'){
                this.sortIcon[s]='mx-2 fa fa-xs fa-sort-desc'
            } else {
                this.sortIcon[s]='mx-2 fa fa-xs fa-sort'
            }
        },
        nextPage() {
            if(this.currentPage != this.pageSize){
                this.startRow= parseInt(this.endRow);
                this.endRow= parseInt(this.endRow)+ parseInt(this.perPage);
                this.currentPage++;
            }
        },
        prevPage() {
            if(this.currentPage > 1){
              this.endRow= parseInt(this.startRow);
              this.startRow= parseInt(this.endRow)- parseInt(this.perPage);
              this.currentPage--;
            }
        },
        currentPageFn(page){
            this.currentPage= page;
            this.endRow = parseInt(this.currentPage) * parseInt(this.perPage);
            this.startRow = parseInt(this.endRow) - parseInt(this.perPage); 
        },
    },
    mounted(){
        axios
        .get("http://localhost:5004/learning_journeys/140078")
        .then((response) => {
            if(error.response.data.code == 404){
                this.emptyText= "No learning journey recorded. Please create new learning journey.";
            } else {
                console.log(response.data);
                var learning_journeys = response.data.data.learning_journeys;
                this.learning_journeys= learning_journeys;
                console.log(learning_journeys);

                // this.totalRows = this.learning_journeys.length;
                // this.pageSize = Math.ceil(this.totalRows/this.perPage);
            }
        })
        .catch((error) => {
            console.log(error);
        })
    },
})

display_journey.mount("#display_journey");