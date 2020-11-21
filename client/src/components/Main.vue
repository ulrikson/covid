<template>
	<div>
		<h1 class="text-6xl text-gray-400">HEJ</h1>
		<div>{{timeline}}</div>
	</div>
</template>

<script>

import axios from 'axios';

export default {
	name: 'Main',

	data() {
		return {
			timeline: ''
		}
	},

	mounted() {
		this.getTimeline();
	},

	methods: {
		getTimeline() {
			axios.get('http://localhost:5000/timeline')
            .then((res) => {
                this.timeline = res.data;
            });
		}
	}
}

</script>
