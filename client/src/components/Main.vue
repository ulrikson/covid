<template>
	<div class="h-screen md:w-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-2xl text-white">COVID I SVERIGE</h1>
			</div>

			<p class="text-gray-400 text-xs mt-4">Totalt:</p>
			<div class="flex flex-wrap justify-between md:justify-start">
				<div v-for="(stat, index, i) in latestStats" :key="index" :class="['flex items-center mt-2 bg-semiDark rounded-3xl px-3 py-2 text-sm text-gray-400', {'md:ml-2': i >= 1}]">
					<span class="flex">
						<confirmed-icon v-if="index == 'confirmed'" class="mr-2 h-5 w-5 text-red-200"/>
						<dead-icon v-else class="mr-2 h-5 w-5 text-red-600"/>
						<number :to="stat" :duration="2" :format="formatNumber" class="mr-2"/> {{index == 'confirmed' ? 'bekräftade' : 'döda'}}
					</span>
				</div>
			</div>

			<div class="mt-8">
				<!-- <div class="flex justify-end items-center">
					<label class="text-gray-500 mr-2 text-sm">Experimentellt</label>
					<input type="checkbox" v-model="experimental" class="h-2.5 w-2.5"/>
				</div> -->
				<div class="w-full md:h-12 px-2 bg-semiDark rounded-3xl flex flex-wrap items-center">
					<a v-for="(btn, i) in stats" :key="i" href="javascript:void(0);" @click.prevent="changeStatistica(btn.statistica)">
						<stat-button :text="btn.text" :bgColor="'bg-blue-600'" :chosen="choices.statistica == btn.statistica"/>
					</a>
					<a v-for="(btn, i) in periods" :key="i" href="javascript:void(0);" @click.prevent="getPeriod(btn.period)">
						<stat-button :text="btn.text" :bgColor="'bg-green-200'" :chosen="choices.period == btn.period"/>
					</a>
					<a href="javascript:void(0);" @click.prevent="getMoving()">
						<stat-button :text="'5dag MA'" :bgColor="'bg-yellow-200'" :chosen="choices.period == 'moving_average'" />
					</a>
					<a href="javascript:void(0);" @click.prevent="getLinear()">
						<stat-button :text="'MLR'" :bgColor="'bg-yellow-200'" :chosen="choices.period == 'linear'" />
					</a>
					<a href="javascript:void(0);" @click.prevent="getArima()">
						<stat-button :text="'ARIMA'" :bgColor="'bg-yellow-200'" :chosen="choices.period == 'arima'" />
					</a>
				</div>
			</div>

			<div class="flex w-full justify-end items-center min-h-8">
				<p v-if="choices.period == 'linear'" class="text-gray-400">{{r2Percentage}}</p>
			</div>

			<div class="w-full bg-semiDark flex justify-center rounded-3xl py-10">
				<chart ref="lineChart" @extra-info="handleExtraInfo"/>
			</div>

			<news />

			<div class="flex items-center bg-semiDark rounded-3xl mt-8 text-gray-400 px-4 py-2">
				© Erik Billebjer Ulrikson 
				<a href="https://github.com/ulrikson" target="blank_"><i class="fa fa-github-square text-3xl text-gray-200 ml-4"></i></a>
				<a href="https://linkedin.com/in/erik-billebjer-ulrikson/" target="blank_"><i class="fa fa-linkedin-square text-3xl text-blue-600 ml-2"></i></a>
				<a href="https://twitter.com/ulrikson2" target="blank_"><i class="fa fa-twitter-square text-3xl text-blue-200 ml-2"></i></a>
				<a href="mailto:erik.ulrikson@gmail.com" target="blank_"><i class="fa fa-paper-plane text-2xl text-indigo-200 ml-2"></i></a>
			</div>
		</div>
	</div>
</template>

<script>

import axios from 'axios';

import ConfirmedIcon from './icons/Confirmed.vue';
import DeadIcon from './icons/Dead.vue';

import Chart from './Chart.vue';
import StatButton from './StatButton.vue';
import News from './News.vue';

export default {
	name: 'Main',

	components: {
		Chart,
		ConfirmedIcon,
		DeadIcon,
		StatButton,
		News
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
			latestStats: {
				confirmed: 0,
				deaths: 0
			},

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

	mounted() {
		this.getLatest()
	},

	methods: {

		getLatest() {
			axios.get('/latest-stats')
			.then((res) => {
				this.latestStats.confirmed = res.data.confirmed;
				this.latestStats.deaths = res.data.deaths;
			})
		},

		changeStatistica (setting) {
			this.choices.statistica = setting;

			if (this.choices.period == 'moving_average') {
				this.getMoving()
			} else if (this.choices.period == 'linear'){
				this.getLinear()
			} else if (this.choices.period == 'arima') {
				this.getArima()
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
		},

		getArima() {
			this.$refs.lineChart.getArima(this.choices);
			this.choices.period = 'arima';
		},

		formatNumber(number) {
			return number.toFixed(0);
		}
	}
}

</script>
