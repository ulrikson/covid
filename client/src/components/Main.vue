<template>
	<div class="bg-dark h-screen flex justify-end">
		<div class="w-17/24 p-8 rounded-l-3xl bg-light">
			<div>
				<h1 class="font-bold text-xl text-superdark">COVID I SVERIGE</h1>
			</div>
			<div class="flex justify-between py-8">
				<InfoCards />
				<InfoCards />
				<InfoCards />
			</div>
			<div class="pt-0 pb-8">
				<div class="w-full h-12 bg-white rounded-3xl"></div>
			</div>
			<div class="w-full bg-white flex justify-center rounded-3xl">
				<Chart />
			</div>
		</div>
		<div class="w-3/12 bg-white">

		</div>
	</div>
</template>

<script>

import Chart from './Chart';
import InfoCards from './InfoCards';

export default {
	name: 'Main',

	components: {InfoCards, Chart},
}

</script>
