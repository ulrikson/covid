<template>
    <div class="w-full bg-semiDark rounded-3xl p-10 mt-8 text-gray-200">
        <h2 class="text-xl font-bold mb-4">Senaste nytt</h2>
        <p v-for="(post,i) in newsposts" :key="i" class="mb-4 hover:underline">
            <a :href="post.url" target="blank_">{{post.title}}</a>
        </p>
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
                this.newsposts = res.data.posts.slice(0,5);
            })
        }
    }
}
</script>