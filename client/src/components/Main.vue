<template>
	<div class="bg-dark h-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><refresh-icon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
			</div>
			<div class="py-8">
				<div class="w-full h-12 px-2 bg-semiDark rounded-3xl flex items-center">
					<a v-for="(choice, i) in choices" :key="i" href="javascript:void(0);" @click.prevent="changeScope(choice.daysDiff)" class="bg-greenBlue text-dark mx-2 py-1 px-2 rounded-3xl opacity-80">{{choice.text}}</a>
				</div>
			</div>
			<div class="w-full bg-semiDark flex justify-center rounded-3xl pb-10">
				<chart ref="lineChart"/>
			</div>
		</div>
	</div>
</template>

<script>

import axios from 'axios';
import moment from 'moment';

import RefreshIcon from './RefreshIcon.vue';
import Chart from './Chart.vue';

export default {
	name: 'Main',

	components: {
		Chart,
		RefreshIcon,
	},

	data() {
		return {
			loading: false,
			chartData: '',
			currentScope: '2020-02-25',
			choices: {
				last7: {
					daysDiff: 7,
					text: 'Senaste 7'
				},
				last30: {
					daysDiff: 30,
					text: 'Senaste 30'
				},
				allTime: {
					daysDiff: 1000,
					text: 'Från början'
				}
			}
		}
	},

	methods: {
		refreshData() {
			this.loading = true;
			axios.get('http://localhost:5000/refresh')
            .then(() => {
				this.$refs.lineChart.getTimeline(this.currentScope);
				this.loading = false;
            });
		},

		changeScope (daysDiff) {
			this.currentScope = moment().subtract(daysDiff, 'days').format('YYYY-M-D')
			this.$refs.lineChart.getTimeline(this.currentScope);
		}
	}
}

</script>