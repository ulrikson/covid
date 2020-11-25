<template>
	<div class="bg-dark h-screen">
		<div class="w-full p-8">
			<div>
				<h1 class="font-bold text-xl text-white">COVID I SVERIGE</h1>
			</div>
			<div class="py-8">
				<div class="w-full h-12 bg-semiDark rounded-3xl"></div>
			</div>
			<div class="w-full bg-semiDark flex justify-center rounded-3xl pb-10">
				<Chart />
			</div>
		</div>
	</div>
</template>

<script>

import Chart from './Chart';

export default {
	name: 'Main',

	components: {
		Chart
	},
}

</script>
