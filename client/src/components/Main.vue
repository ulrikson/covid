<template>
	<div class="bg-dark h-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><refresh-icon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
			</div>
			<div class="py-8">
				<div class="w-full h-12 px-2 bg-semiDark rounded-3xl flex items-center">
					<a 
						v-for="(stat, i) in choices.statisticas" :key="i" href="javascript:void(0);" 
						@click.prevent="changeTimeline(stat)" 
						:class="['bg-greenBlue text-dark mx-2 py-1 px-2 rounded-3xl hover:opacity-50', chosenStat == stat.statistica ? 'opacity-50' : 'opacity-80']"
					>
					{{stat.text}}
					</a>
				</div>
			</div>
			<div class="w-full bg-semiDark flex justify-center rounded-3xl py-10">
				<chart ref="lineChart"/>
			</div>
		</div>
	</div>
</template>

<script>

import axios from 'axios';

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
			chosenStat: 'deaths_diff',
			choices: {
				statisticas : {
					deaths: {
						statistica: 'deaths_diff',
						text: 'Döda'
					},
					last30: {
						statistica: 'confirmed_diff',
						text: 'Bekräftade'
					},
				}
			}
		}
	},

	methods: {
		refreshData() {
			this.loading = true;
			axios.get('http://localhost:5000/refresh')
            .then(() => {
				this.$refs.lineChart.getTimeline({statistica: 'deaths_diff'});
				this.loading = false;
            });
		},

		changeTimeline (settings) {
			this.chosenStat = settings.statistica;
			this.$refs.lineChart.getTimeline(settings);
		},
	}
}

</script>