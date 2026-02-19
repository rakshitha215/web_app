async function getWeather() {
    const city = document.getElementById("cityInput").value.trim();
    const apiKey = "8cd76edcbed86dc5221cc5ba5769ca5f";   // ← put your API key

    if (!city) {
        alert("Please enter a city name");
        return;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {

            const temperature = data.main.temp;
            const weatherMain = data.weather[0].main.toLowerCase();

            const imageElement = document.getElementById("weatherImage");

            // 🌧 Rain Images
            const rainImages = [
                "https://images.unsplash.com/photo-1501696461441-7c6b37b2aebf",
                "https://images.unsplash.com/photo-1499346030926-9a72daac6c63"
            ];

            // ❄ Cold Images
            const coldImages = [
                "https://images.unsplash.com/photo-1483664852095-d6cc6870702d",
                "https://images.unsplash.com/photo-1608889175112-4a1d8a9f8c36"
            ];

            // ☁ Cloudy Images
            const cloudyImages = [
                "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
                "https://images.unsplash.com/photo-1499346030926-9a72daac6c63"
            ];

            // ☀ Clear / Hot Images
            const clearImages = [
                "https://images.unsplash.com/photo-1502082553048-f009c37129b9",
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
            ];

            function getRandomImage(arr) {
                return arr[Math.floor(Math.random() * arr.length)];
            }

            // 🌧 Priority 1 → Rain
            if (weatherMain.includes("rain")) {
                imageElement.src = getRandomImage(rainImages);
            }
            // ❄ Cold (Temperature below 15°C)
            else if (temperature <= 15) {
                imageElement.src = getRandomImage(coldImages);
            }
            // ☁ Cloudy
            else if (weatherMain.includes("cloud")) {
                imageElement.src = getRandomImage(cloudyImages);
            }
            // ☀ Hot / Clear (Temperature > 29°C)
            else if (temperature > 29) {
                imageElement.src = getRandomImage(clearImages);
            }
            // 🌤 Default
            else {
                imageElement.src = getRandomImage(clearImages);
            }

            imageElement.style.display = "block";

            document.getElementById("weatherResult").innerHTML = `
                <h3>${data.name}</h3>
                <p>🌡 Temperature: ${temperature} °C</p>
                <p>🌥 Weather: ${data.weather[0].description}</p>
                <p>💧 Humidity: ${data.main.humidity}%</p>
                <p>💨 Wind Speed: ${data.wind.speed} m/s</p>
            `;
        }
        else {
            document.getElementById("weatherResult").innerHTML =
                `<p style="color:red;">${data.message}</p>`;
        }

    } catch (error) {
        document.getElementById("weatherResult").innerHTML =
            `<p style="color:red;">Error fetching data</p>`;
    }
}
