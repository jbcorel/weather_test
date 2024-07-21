function updateUIWithWeatherData(data) {
    const weatherResultDiv = document.getElementById('forecast');
    const nameDiv = document.getElementById('name');
    const currentDiv = document.getElementById('current');

    nameDiv.innerHTML = '';
    currentDiv.innerHTML = '';
    weatherResultDiv.innerHTML = '';


    nameDiv.innerHTML += `
    <p>City: ${data.name}</p>
    `;
    currentDiv.innerHTML += `
    <p>Current temperature: ${data.current} °C</p>
    `
    const forecastArr = Object.entries(data.forecast);
    for (let i=0; i<forecastArr.length; i++) {
        let date = forecastArr[i][0];
        let temps = forecastArr[i][1]
        weatherResultDiv.innerHTML += `
        <p>Date: ${date}
        <p>Max Temperature: ${temps[0]}°C</p>
        <p>Min Temperature: ${temps[1]}°C</p>
    `;
    }
}

function clearOutUI(){
    const weatherResultDiv = document.getElementById('forecast');
    const nameDiv = document.getElementById('name');
    const currentDiv = document.getElementById('current');

    nameDiv.innerHTML = '';
    currentDiv.innerHTML = '';
    weatherResultDiv.innerHTML = '';
}

async function fetchWeatherData (city) {
    try {
        const response = await fetch(`/get-weather?city=${encodeURIComponent(city)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });
        weatherData = await response.json();
        console.log('Weather data fetched:', weatherData);
        if (weatherData.status_code==200){
            updateUIWithWeatherData(weatherData); // Use the fetched data
        } else {
            alert(weatherData.detail);
        }
    } catch (error) {   
        console.error('Error fetching weather data:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('weatherForm');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        clearOutUI();
        const city = document.getElementById('searchbar').value;
        document.getElementById('searchbar').value = '';
        // Await the async function to ensure the data is fetched before continuing
        await fetchWeatherData(city);
    });
});