const namebar = document.querySelector('.namebar');
const contentbar = document.querySelector('.contentbar');
if (window.innerWidth < 1080) {
    namebar.style.display = 'none';
    contentbar.style.top = '10px'
    contentbar.style.left = '10px'
} else {
    namebar.style.display = 'block';
    contentbar.style.top = '70px'
    contentbar.style.left = '10px'
}


if (window.innerWidth < 900) {
    contentbar.style.display = 'none';
} else {
    contentbar.style.display = 'block';
}
// Ширина
window.addEventListener("resize", function() {
    const namebar = document.querySelector('.namebar');
    const contentbar = document.querySelector('.contentbar');
    if (window.innerWidth < 1080) {
        namebar.style.display = 'none';
        contentbar.style.top = '10px'
        contentbar.style.left = '10px'
    } else {
        namebar.style.display = 'block';
        contentbar.style.top = '70px'
        contentbar.style.left = '10px'
    }

    
    if (window.innerWidth < 900) {
        contentbar.style.display = 'none';
    } else {
        contentbar.style.display = 'block';
    }
});