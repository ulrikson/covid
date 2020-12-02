<template>
	<div class="h-screen md:w-screen">
		<div class="w-full p-8">
			<div class="flex justify-start items-center">
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
				<a href="javascript:void(0);" @click.prevent="refreshData"><refresh-icon :class="['ml-2 h-5 w-5 text-white', {'animate-spin': loading}]"/></a>
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

			<div class="mt-2">
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
						<stat-button :text="'5dag MA'" :bgColor="'bg-yellow-200'" :chosen="choices.period == 'moving_average'" />
					</a>
					<a v-if="experimental" href="javascript:void(0);" @click.prevent="getLinear()">
						<stat-button :text="'MLR'" :bgColor="'bg-yellow-200'" :chosen="choices.period == 'linear'" />
					</a>
				</div>
			</div>

			<div class="flex w-full justify-end items-center min-h-8">
				<p v-if="choices.period == 'linear'" class="text-gray-400">{{r2Percentage}}</p>
			</div>

			<div class="w-full bg-semiDark flex justify-center rounded-3xl py-10">
				<chart ref="lineChart" @extra-info="handleExtraInfo"/>
			</div>

			<div class="flex items-center bg-semiDark rounded-3xl mt-8 text-gray-400 px-4 py-2">
				© Erik Billebjer Ulrikson 
				<a href="https://github.com/ulrikson" target="blank_"><i class="fa fa-github-square text-xl text-white ml-4"></i></a>
				<a href="https://linkedin.com/in/erik-billebjer-ulrikson/" target="blank_"><i class="fa fa-linkedin-square text-xl text-blue-600 ml-2"></i></a>
				<a href="https://twitter.com/ulrikson2" target="blank_"><i class="fa fa-twitter-square text-xl text-blue-200 ml-2"></i></a>
			</div>
		</div>
	</div>
</template>

<script>

import axios from 'axios';

import RefreshIcon from './icons/Refresh.vue';
import ConfirmedIcon from './icons/Confirmed.vue';
import DeadIcon from './icons/Dead.vue';

import Chart from './Chart.vue';
import StatButton from './StatButton.vue';

export default {
	name: 'Main',

	components: {
		Chart,
		RefreshIcon,
		ConfirmedIcon,
		DeadIcon,
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
		refreshData() {
			this.loading = true;
			axios.get('/refresh')
            .then(() => {
				this.$refs.lineChart.getTimeline({statistica: 'deaths_diff', period: 'doy'});
				this.loading = false;
            });
		},

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

		formatNumber(number) {
			return number.toFixed(0);
		}
	}
}

</script>