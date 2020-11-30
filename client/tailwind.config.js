module.exports = {
	purge: {
		enabled: true,
		content: [
			'.**/*.html',
		]
	},
	darkMode: false, // or 'media' or 'class'
	theme: {
		extend: {
			width: {
				'17/24': '70.833%',
				'30/100': '30%',
				'90/100': '90%' 
			},
			minHeight: {
				'8': '2rem'
			},
			colors: {
				dark: '#101821',
				semiDark: '#1a2940',
			}
		},
	},
	variants: {
		extend: {},
	},
	plugins: [],
}
