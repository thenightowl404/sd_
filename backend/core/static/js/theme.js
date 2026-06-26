function applyTheme(theme) {

    if (theme === "light") {
        document.body.classList.add("light-theme");
        document.body.classList.remove("dark-theme");
    } else {
        document.body.classList.add("dark-theme");
        document.body.classList.remove("light-theme");
    }

}

fetch("/settings/get/")
.then(response => response.json())
.then(data => {

    applyTheme(data.theme);

    document.body.style.fontSize = data.font_size;

});