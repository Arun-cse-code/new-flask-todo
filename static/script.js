document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("theme-toggle");
    const body = document.body;

    // Check local storage for theme preference
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
    }

    // Toggle Theme on Button Click
    toggleBtn.addEventListener("click", () => {
        body.classList.toggle("dark-mode");

        // Store theme preference in local storage
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
});
