const display_skills = Vue.createApp({
    data() {
        return {
            skill_list: [],
            emptyText: "",
            searchQuery: null,
            categoryQuery:null,
            fields: [
                { key: 'skill_name', label: 'Skill Name', sortable: true, sortDirection: 'desc' },
                { key: 'skill_category', label: 'Skill Category', sortable: true },
                {
                  key: 'skill_status',
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
              currentSort:'skill_name',
              currentSortDir:'asc',
              sortIcon: {
                'skill_name': 'mx-2 fa fa-xs fa-sort',
                'skill_category': 'mx-2 fa fa-xs fa-sort',
                'skill_status': 'mx-2 fa fa-xs fa-sort',
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
            return this.skill_list.filter(item => {
              return this.searchQuery
                .toLowerCase()
                .split(" ")
                .every(v => item.skill_name.toLowerCase().includes(v));
              });
          }
        else if(this.categoryQuery) {
            return this.skill_list.filter(item => {
                return this.categoryQuery
                    .toLowerCase()
                    .split(" ")
                    .every(v => item.skill_category.toLowerCase().includes(v));
            });
        } else{
            return this.skill_list;
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
    methods:{
          updateSkill(id) {
            window.location.href = 'update_skill.html?id=' + id;
          },
          deleteSkill(id) {
            window.location.href = 'delete_skill.html?id=' + id;
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
            if(this.currentSortDir=='asc'){ 
              this.sortIcon[s]='mx-2 fa fa-xs fa-sort-asc'
            }else if (this.currentSortDir=='desc'){
              this.sortIcon[s]='mx-2 fa fa-xs fa-sort-desc'
            }else{
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
    mounted() {
        axios
            .get("http://localhost:5001/skills")
            .then((response) => {
                var skill_list = response.data.data.skills;
                this.skill_list= skill_list
                
                // Set the initial number of items
                this.totalRows = this.skill_list.length;
                this.pageSize = Math.ceil(this.totalRows/this.perPage);
                console.log(skill_list)
            })
            .catch((error) => {
                if(error.response.data.code==404){
                  this.emptyText= "There are no skills recorded. Please create new skill."
                }
                console.log(error);
            })
    },
})

display_skills.mount("#display_skills");