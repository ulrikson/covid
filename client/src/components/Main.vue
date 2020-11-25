<template>
	<div class="bg-dark h-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><RefreshIcon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
			</div>
			<div class="py-8">
				<div class="w-full h-12 bg-semiDark rounded-3xl"></div>
			</div>
			<div class="w-full bg-semiDark flex justify-center rounded-3xl pb-10">
				<Chart ref="lineChart" />
			</div>
		</div>
	</div>
</template>

<script>

import axios from 'axios';

import Chart from './Chart';
import RefreshIcon from './RefreshIcon'

export default {
	name: 'Main',

	components: {
		Chart,
		RefreshIcon
	},

	data() {
		return {
			loading: false,
			chartData: ''
		}
	},

	methods: {
		refreshData() {
			this.loading = true;
			axios.get('http://localhost:5000/refresh')
            .then(() => {
				this.$refs.lineChart.getTimeline();
				this.loading = false;
            });
		}
	}
}

</script>