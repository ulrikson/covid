<template>
    <div class="w-90/100">
        <line-chart :chart-data="datacollection" :options="options" style="max-height: 45vh"></line-chart>
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
                        borderColor: '#285FD5',
                        borderWidth: 10 
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
            var ctx = document.getElementById('line-chart').getContext("2d");
            var gradientFill = ctx.createLinearGradient(0, 0, 0, 350); // numbers control x1,x2,y1,y2

            gradientFill.addColorStop(0, 'rgba(40, 95, 213, 0.8)') // show this color at 0%;
            gradientFill.addColorStop(0.5, 'rgba(40, 95, 213, 0.5)'); // show this color at 50%
            gradientFill.addColorStop(1, 'rgba(40, 95, 213, 0'); // show this color at 100%

            this.datacollection = {
                labels: this.timeline.labels,
                datasets: [
                    {
                        backgroundColor: gradientFill,
                        data: this.timeline.confirmed
                    }
                ]
            }
        }
	}
    
}
</script>