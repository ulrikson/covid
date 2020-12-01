<template>
	<div class="bg-dark h-screen md:w-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><refresh-icon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
			</div>
			<div class="mt-8">
				<div class="flex justify-end items-center">
					<label class="text-gray-400 mr-2 text-xs">Experimentell</label>
					<input type="checkbox" v-model="experimental" class="h-2.5 w-2.5"/>
				</div>
				<div class="w-full md:h-12 px-2 bg-semiDark rounded-3xl flex flex-wrap items-center">
					<a v-for="(btn, i) in stats" :key="i" href="javascript:void(0);" @click.prevent="changeStatistica(btn.statistica)">
						<stat-button :text="btn.text" :bgColor="'bg-blue-600'" :chosen="choices.statistica == btn.statistica"/>
					</a>
					<a v-for="(btn, i) in periods" :key="i" href="javascript:void(0);" @click.prevent="getPeriod(btn.period)">
						<stat-button :text="btn.text" :bgColor="'bg-green-200'" :chosen="choices.period == btn.period"/>
					</a>
					<a v-if="experimental" href="javascript:void(0);" @click.prevent="getMoving()">
						<stat-button :text="'5dag MA'" :bgColor="'bg-pink-200'" :chosen="choices.period == 'moving_average'" />
					</a>
					<a v-if="experimental" href="javascript:void(0);" @click.prevent="getLinear()">
						<stat-button :text="'MLR'" :bgColor="'bg-pink-200'" :chosen="choices.period == 'linear'" />
					</a>
				</div>
			</div>
			<div class="flex w-full justify-end items-center min-h-8">
				<p v-if="choices.period == 'linear'" class="text-gray-400">{{r2Percentage}}</p>
			</div>
			<div class="w-full bg-semiDark flex justify-center rounded-3xl py-10">
				<chart ref="lineChart" @extra-info="handleExtraInfo"/>
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

	computed: {
		r2Percentage() {
			const perc = Math.round(this.extraInfo.rSquare * 100);
			const text = 'R2: ' + perc + '%';
			return text;
		}
	},

	data() {
		return {
			loading: false,
			experimental: false,

			extraInfo: {
				rSquare: ''
			},

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
			axios.get('/refresh')
            .then(() => {
				this.$refs.lineChart.getTimeline({statistica: 'deaths_diff', period: 'doy'});
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
				this.getStatistica()
			}
		},

		handleExtraInfo(info) {
			this.extraInfo.rSquare = info;
		},

		getStatistica () {
			this.$refs.lineChart.getTimeline(this.choices);
		},

		getPeriod (setting) {
			this.choices.period = setting;
			this.$refs.lineChart.getTimeline(this.choices);
		},

		getMoving() {
			this.$refs.lineChart.getMoving(this.choices);
			this.choices.period = 'moving_average';
		},

		getLinear() {
			this.$refs.lineChart.getLinear(this.choices);
			this.choices.period = 'linear';
		}
	}
}

</script>