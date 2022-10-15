const display_courses = Vue.createApp({
    data() {
        return {
            course_list: [],
            emptyText: "",
            searchQuery: null,
            fields: [
                { key: 'course_name', label: 'Course Name', sortable: true, sortDirection: 'desc' },
                { key: 'course_category', label: 'Course Category', sortable: true },
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
            },
            pageItemIcon: {
                'false': 'page-item',
                'true': 'page-item active'
            },
            createSkillLink: "create_skill.html"
        }
    },
    computed: {
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
        updateSkill(id) {
            window.location.href = 'update_skill.html?id=' + id;
        },
        deleteSkill(id) {
            window.location.href = 'delete_skill.html?id=' + id;
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
        }
    },
    mounted() {
        axios
            .get("http://localhost:5003/courses")
            .then((response) => {
                if (response.data.code == 404) {
                    this.emptyText = "There are no courses recorded. Please fetch data from LMS."
                    return
                } else {
                    var course_list = response.data.data.courses;
                    this.course_list = course_list

                    // Set the initial number of items
                    this.totalRows = this.course_list.length;
                    this.pageSize = Math.ceil(this.totalRows / this.perPage);
                    console.log(course_list)
                }

            })
            .catch((error) => {
                console.log(error);
            })
    },
})

display_courses.mount("#display_courses");