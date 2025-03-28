export const generateChart = (chartData) => {
    const chartOptions = {
        type: 'bar', // Example type
        data: chartData,
        options: { responsive: true }
    };

    return chartOptions; // To be used with a charting library (e.g., Chart.js)
};
