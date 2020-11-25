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
            datacollection: null,

            options: {
                maintainAspectRatio: false,
                responsive: true,
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
                        // borderColor: 'rgba(244,31,220,1)',
                        borderWidth: 5 
                    }
                },
                legend: {
                    display: false
                }
            }
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
                this.fillData()
            });
        },
        
        fillData() {
            const ctx = document.getElementById('line-chart').getContext("2d");
            const gradientBorder = ctx.createLinearGradient(100, 0, 1500, 0);
            const gradientFill = ctx.createLinearGradient(100, 0, 1500, 0);

            gradientBorder.addColorStop(0, "rgba(0, 43, 220, 1)");
            gradientBorder.addColorStop(1, "rgba(50, 222, 212, 1)");

            gradientFill.addColorStop(0, "rgba(0, 43, 220, 0.6)");
            gradientFill.addColorStop(1, "rgba(50, 222, 212, 0.6)");


            this.datacollection = {
                labels: this.timeline.labels,
                datasets: [
                    {
                        backgroundColor: gradientFill,
                        borderColor: gradientBorder,
                        data: this.timeline.confirmed
                    }
                ]
            }
        }
	}
    
}
</script>