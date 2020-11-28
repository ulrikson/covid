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

            datacollection: {},

            options: {
                responsive: true,
                maintainAspectRatio: false,
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
			axios.post('http://localhost:5000/timeline', {
                statistica: settings.statistica,
                period: settings.period
            })
            .then((res) => {
                this.timeline = res.data;
                this.fillData();
            });
        },
        
        fillData() {
            const ctx = document.getElementById('line-chart').getContext("2d");

            const gradientBorder = ctx.createLinearGradient(100, 0, 1000, 0);
            const gradientFill = ctx.createLinearGradient(100, 0, 1000, 0);

            // gradientBorder.addColorStop(0, "rgba(0, 43, 220, 1)");
            gradientBorder.addColorStop(0, "rgba(37, 99, 235, 1)"); // bg-blue-600
            gradientBorder.addColorStop(1, "rgba(167, 243, 208, 1)"); // bg-green-200

            gradientFill.addColorStop(0, "rgba(37, 99, 235, 0.6)"); // bg-blue-600
            gradientFill.addColorStop(1, "rgba(167, 243, 208, 0.6)"); // bg-green-200


            this.datacollection = {
                labels: this.timeline.labels,
                datasets: [
                    {
                        backgroundColor: gradientFill,
                        borderColor: gradientBorder,
                        data: this.timeline.covid_data
                    }
                ]
            }
        }
	}
    
}
</script>