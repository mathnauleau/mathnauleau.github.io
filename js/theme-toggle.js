const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;

themeToggle.addEventListener('click', () => {
    htmlElement.classList.toggle('dark');
});

// Check if there's a theme preference in localStorage
const currentTheme = localStorage.getItem('theme');

// If there's a theme preference, apply it
if (currentTheme) {
    htmlElement.classList.add(currentTheme);
} else {
    // If there's no theme preference, set the default theme
    htmlElement.classList.add('light'); // Or whichever theme you want as default
}

// Function to toggle between light and dark themes
function toggleTheme() {
    if (htmlElement.classList.contains('light')) {
        htmlElement.classList.remove('light');
        htmlElement.classList.add('dark');
        localStorage.setItem('theme', 'dark'); // Store theme preference
    } else {
        htmlElement.classList.remove('dark');
        htmlElement.classList.add('light');
        localStorage.setItem('theme', 'light'); // Store theme preference
    }
}

// Event listener for theme toggle button
themeToggle.addEventListener('click', toggleTheme);
