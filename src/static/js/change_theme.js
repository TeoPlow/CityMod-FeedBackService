// Получаем элементы
const toggleButton = document.getElementById("toggleThemeButton");
const backgroundSky = document.getElementById("backgroundSky");
const backgroundGrayCity = document.getElementById("backgroundGrayCity");
const orbImage = document.querySelector(".orb img");
const body = document.body;

// Функция для получения значения cookie по имени
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Функция для установки cookie
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000); // Срок действия cookie
    const expires = "expires=" + d.toUTCString();
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

// Проверяем, есть ли информация о выбранной теме в cookie
let isDay = true; // Значение по умолчанию
if (getCookie("theme") === "night") {
    isDay = false;
}

// Применяем сохраненную тему при загрузке страницы
function applyTheme() {
    if (isDay) {
        orbImage.src = "static/images/sun.png";
        backgroundSky.src = "static/images/sky.png";
        backgroundGrayCity.src = "static/images/gray_city.png";
        body.classList.remove("night-theme");
    } else {
        orbImage.src = "static/images/moon.png";
        backgroundSky.src = "static/images/night_sky.png";
        backgroundGrayCity.src = "static/images/gray_city_night.png";
        body.classList.add("night-theme");
    }
}

// Сначала применяем тему
applyTheme();

// Обработчик переключения темы
toggleButton.addEventListener("click", () => {
    isDay = !isDay; // Переключаем состояние
    setCookie("theme", isDay ? "day" : "night", 365); // Сохраняем выбранную тему
    applyTheme(); // Применяем изменения
});
