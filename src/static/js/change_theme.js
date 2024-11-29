// Получаем элементы
const toggleButton = document.getElementById("toggleThemeButton");
const backgroundSky = document.getElementById("backgroundSky");
const backgroundGrayCity = document.getElementById("backgroundGrayCity");
const orbImage = document.querySelector(".orb img");

// Функция для получения значения cookie по имени
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Проверяем, есть ли информация о выбранной теме в cookie
let isDay = getCookie("theme") === "day";

// Применяем сохраненную тему при загрузке страницы
if (isDay) {
    orbImage.src = "static/images/sun.png";
    backgroundSky.src = "static/images/sky.png";
    backgroundGrayCity.src = "static/images/gray_city.png";
} else {
    orbImage.src = "static/images/moon.png";
    backgroundSky.src = "static/images/night_sky.png";
    backgroundGrayCity.src = "static/images/gray_city_night.png"
}

// Функция для установки cookie
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000)); // Срок действия cookie
    const expires = "expires=" + d.toUTCString();
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

// Функция переключения темы
toggleButton.addEventListener("click", () => {
    if (isDay) {
        // Переключение на ночную тему
        orbImage.src = "static/images/moon.png";
        backgroundSky.src = "static/images/night_sky.png";
        backgroundGrayCity.src = "static/images/gray_city_night.png"
        setCookie("theme", "night", 365); // Сохраняем выбранную тему на 365 дней
    } else {
        // Переключение на дневную тему
        orbImage.src = "static/images/sun.png";
        backgroundSky.src = "static/images/sky.png";
        backgroundGrayCity.src = "static/images/gray_city.png"
        setCookie("theme", "day", 365); // Сохраняем выбранную тему на 365 дней
    }
    isDay = !isDay; // Переключаем состояние
});
