const display_courses = Vue.createApp({
    data() {
        return {
            course_list: [],
            skill_list: [],
            skills_courses_list: [],
            emptyText: "",
            searchQuery: null,
            fields: [
                { key: 'course_name', label: 'Course Name', sortable: true, sortDirection: 'desc' },
                { key: 'course_category', label: 'Course Category', sortable: true },
                { key: 'skill_name', label: 'Skill Name', sortable: true },
                {
                    key: 'course_status',
                    label: 'Is Active',
                    formatter: (value, key, item) => {
                        return value ? 'Yes' : 'No'
                    },
                    sortable: true,
                    sortByFormatted: true,
                    filterByFormatted: true
                },
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
            currentSort: 'course_name',
            currentSortDir: 'asc',
            sortIcon: {
                'course_name': 'mx-2 fa fa-xs fa-sort',
                'course_category': 'mx-2 fa fa-xs fa-sort',
                'course_status': 'mx-2 fa fa-xs fa-sort',
                'skill_name': 'mx-2 fa fa-xs fa-sort',
            },
            pageItemIcon: {
                'false': 'page-item',
                'true': 'page-item active'
            },
        }
    },
    computed: {
        finalCourseList(){
            for(course of this.course_list){
                var course_id = course.course_id;
                var skill_name = "";
                var skill_id = "";
                for(skills_courses of this.skills_courses_list){
                    if(course_id == skills_courses.course_id){
                        skill_id = skills_courses.skill_id;
                        }
                    }
                for(skill of this.skill_list){
                    if(skill_id == skill.skill_id){
                        skill_name = skill.skill_name;
                        course.skill_name = skill_name;
                        
                    }
                    
                }
            }
        },
        sortedResultQuery() {
            return this.resultQuery.sort((a, b) => {
                let modifier = 1;
                if (this.currentSortDir === 'desc') modifier = -1;
                if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
                if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
                return 0;
            });
        },
        resultQuery() {
            
            if (this.searchQuery) {
                return this.course_list.filter(item => {
                    return this.searchQuery
                        .toLowerCase()
                        .split(" ")
                        .every(v => item.course_name.toLowerCase().includes(v));
                });
            } else {
                return this.course_list;
            }
        },
        paginatedQuery() {
            return this.sortedResultQuery.slice(this.startRow, this.endRow)
        },
    },
    watch: {
        perPage() {
            this.pageSize = Math.ceil(this.totalRows / this.perPage);
            this.startRow = 0;
            this.endRow = this.perPage;
        }
    },
    methods: {
        async getAllCourses(){
            axios
                .get("http://localhost:5003/courses")
                .then((response) => {
                    if (response.data.code == 404) {
                        this.emptyText += "There are no courses recorded. Please fetch data from LMS."
                        return
                    } else {
                        var course_list = response.data.data.courses;
                        this.course_list = course_list

                        // Set the initial number of items
                        this.totalRows = this.course_list.length;
                        this.pageSize = Math.ceil(this.totalRows / this.perPage);
                    }
                })
                .catch((error) => {
                    console.log(error);
                })
        },
        async getAllSkills(){
           await axios
                .get("http://localhost:5001/skills")
                .then((response) => {
                    if (response.data.code == 404) {
                        this.emptyText += "\nThere are no skills record, please create skill."
                        return []
                    } else {
                
                        var skill_list = response.data.data.skills;
                        this.skill_list = skill_list
                    }
                })
                .catch((error) => {
                    console.log(error);
                })
        },
        async getAllSkillsCourses(){
           await axios
                .get("http://localhost:5004/skills_courses/all")
                .then((response) => {
                    if (response.data.code == 404) {
                        return
                    } else {
                        
                        var skills_courses_list = response.data.data.skills_courses;
                        this.skills_courses_list = skills_courses_list;
                    }
                })
                .catch((error) => {
                    console.log(error);
                })
        },
        mapSkill(id) {
            window.location.href = 'map_skill.html?id=' + id;
        },
        sort(s) {
            //if s == current sort, reverse
            if (s === this.currentSort) {
                this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
                this.sortIconFn(s)
            }
            this.currentSort = s;
            this.sortIconFn(s)

        },
        sortIconFn(s) {
            Object.keys(this.sortIcon).forEach(key => {
                this.sortIcon[key] = 'mx-2 fa fa-xs fa-sort'
            });
            if (this.currentSortDir == 'asc') {
                this.sortIcon[s] = 'mx-2 fa fa-xs fa-sort-asc'
            } else if (this.currentSortDir == 'desc') {
                this.sortIcon[s] = 'mx-2 fa fa-xs fa-sort-desc'
            } else {
                this.sortIcon[s] = 'mx-2 fa fa-xs fa-sort'
            }
        },
        nextPage() {
            if (this.currentPage != this.pageSize) {
                this.startRow = parseInt(this.endRow);
                this.endRow = parseInt(this.endRow) + parseInt(this.perPage);
                this.currentPage++;
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.endRow = parseInt(this.startRow);
                this.startRow = parseInt(this.endRow) - parseInt(this.perPage);
                this.currentPage--;
            }
        },
        currentPageFn(page) {
            this.currentPage = page;
            this.endRow = parseInt(this.currentPage) * parseInt(this.perPage);
            this.startRow = parseInt(this.endRow) - parseInt(this.perPage);
        },
    },
   mounted() {
        
    },
    async created(){
        await this.getAllCourses();
        await this.getAllSkills();
        await this.getAllSkillsCourses();
    }
})

display_courses.mount("#display_courses");

