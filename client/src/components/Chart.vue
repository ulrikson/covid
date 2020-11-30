<template>
    <div class="w-90/100">
        <line-chart :chart-data="datacollection" :options="options"></line-chart>
    </div>
</template>

<script>

import axios from 'axios';
import LineChart from './LineChart.js'

export default {

    components: {
        LineChart
    },
    
    data() {
		return {
            settings: {
                statistica: 'deaths_diff',
                period: 'week'
            },

            timeline: '',

            datacollection: {},

            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    easing: 'easeOutQuart'
                },
                scales: {
                    xAxes: [{
                        display: false
                    }],
                    yAxes: [{
                        display: false
                    }]
                },
                elements: {
                    point:{
                        radius: 0
                    },
                    line: {
                        borderWidth: 5 
                    }
                },
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: false
                }
            }
		}
	},

	mounted() {
		this.getTimeline(this.settings);
	},

	methods: {
		getTimeline(settings) {
			axios.post('/timeline', {
                statistica: settings.statistica,
                period: settings.period
            })
            .then((res) => {
                this.timeline = res.data;
                this.fillData();
            });
        },

        getMoving(settings) {
			axios.post('/moving', {
                statistica: settings.statistica,
                period: 'doy', // always per day
                window: settings.window
            })
            .then((res) => {
                this.timeline = res.data;
                this.fillData();
            });
        },

        getLinear(settings) {
            axios.post('/linear', {
                statistica: settings.statistica,
                period: 'doy', // always per day
            })
            .then((res) => {
                this.timeline = res.data;
                this.$emit('extra-info', res.data.r_square);
                this.fillData();
            });
        },
        
        fillData() {
            const ctx = document.getElementById('line-chart').getContext("2d");

            const primaryBorder = ctx.createLinearGradient(100, 0, 1000, 0);
            const primaryFill = ctx.createLinearGradient(100, 0, 1000, 0);
            primaryBorder.addColorStop(0, "rgba(37, 99, 235, 1)"); // blue-600
            primaryBorder.addColorStop(1, "rgba(167, 243, 208, 1)"); // green-200
            primaryFill.addColorStop(0, "rgba(37, 99, 235, 0.6)"); // blue-600
            primaryFill.addColorStop(1, "rgba(167, 243, 208, 0.6)"); // green-200

            this.datacollection = {
                labels: this.timeline.labels,
                datasets: [
                    {
                        backgroundColor: primaryFill,
                        borderColor: primaryBorder,
                        data: this.timeline.covid_data
                    },
                    {
                        backgroundColor: 'transparent',
                        borderColor: 'rgba(219, 39, 119, 1)', //pink-600
                        data: this.timeline.predict
                    }
                ]
            }
        }
	}
    
}
</script>