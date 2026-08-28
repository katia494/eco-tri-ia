/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                ecoGreen: '#16a34a',
                ecoBrown: '#854d0e',
                ecoLight: '#f5f5f4',
            }
        },
    },
    plugins: [],
}