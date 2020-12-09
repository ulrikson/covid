<template>
    <div>
        {{newsposts}}
    </div>
</template>

<script>
import axios from 'axios';

export default {

    data() {
        return {
            newsposts: {}
        }
    },
    
    mounted() {
        this.getNews()
    },

    methods: {
        getNews() {
            axios.get('/news')
            .then((res) => {
                this.newsposts = res.data.posts;
            })
        }
    }
}
</script>