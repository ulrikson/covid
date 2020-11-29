<template>
	<div class="bg-dark h-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><refresh-icon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
			</div>
			<div class="py-8">
				<div class="w-full h-12 px-2 bg-semiDark rounded-3xl flex items-center">
					<a v-for="(btn, i) in stats" :key="i" href="javascript:void(0);" @click.prevent="changeStatistica(btn.statistica)">
						<stat-button :text="btn.text" :bgColor="'bg-blue-600'" :chosen="choices.statistica == btn.statistica"/>
					</a>
					<a v-for="(btn, i) in periods" :key="i" href="javascript:void(0);" @click.prevent="changePeriod(btn.period)">
						<stat-button :text="btn.text" :bgColor="'bg-green-200'" :chosen="choices.period == btn.period"/>
					</a>
					<a href="javascript:void(0);" @click.prevent="getMoving()">
						<stat-button :text="'5dag MA'" :bgColor="'bg-pink-200'" :chosen="choices.period == 'moving_average'" />
					</a>
					<a href="javascript:void(0);" @click.prevent="getMoving()">
						<stat-button :text="'SLR'" :bgColor="'bg-pink-200'" :chosen="choices.period == 'linear'" />
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
import StatButton from './StatButton.vue';

export default {
	name: 'Main',

	components: {
		Chart,
		RefreshIcon,
		StatButton
	},

	data() {
		return {
			loading: false,

			choices: {
				statistica: 'deaths_diff',
				period: 'week',
				window: 5 // always 5, atleast right now
			},

			stats: {
				deaths: {
					statistica: 'deaths_diff',
					text: 'Döda'
				},
				last30: {
					statistica: 'confirmed_diff',
					text: 'Bekräftade'
				},
			},

			periods: {
				daily: {
					period: 'doy',
					text: 'Dag'
				},
				weekly: {
					period: 'week',
					text: 'Vecka'
				},
				monthly: {
					period: 'month',
					text: 'Månad'
				},
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

		changeStatistica (setting) {
			this.choices.statistica = setting;

			if (this.choices.period == 'moving_average') {
				this.getMoving()
			} else if (this.choices.period == 'linear'){
				this.getLinear()
			} else {
				this.$refs.lineChart.getTimeline(this.choices);
			}
		},

		changePeriod (setting) {
			this.choices.period = setting;
			this.$refs.lineChart.getTimeline(this.choices);
		},

		getMoving() {
			this.$refs.lineChart.getMoving(this.choices);
			this.choices.period = 'moving_average';
		}
	}
}

</script>