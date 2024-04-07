import daisyui from 'daisyui';
/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {},
		fontFamily: {
			sans: ['Roboto', 'sans-serif'],
			serif: ['Roboto Serif', 'serif'],
			mono: ['Roboto Mono', 'monospace']
		}
	},
	plugins: [daisyui]
};
