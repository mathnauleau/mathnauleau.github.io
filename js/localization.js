// Function to update content based on selected language
function updateContent(langData) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = langData[key];
    });
}

// Function to set the language preference
function setLanguagePreference(lang) {
    localStorage.setItem('language', lang);
}

// Function to fetch language data
async function fetchLanguageData(lang) {
    const response = await fetch(`languages/${lang}.json`);
    return response.json();
}

// Function to change language
async function changeLanguage(lang) {
    setLanguagePreference(lang);
    const langData = await fetchLanguageData(lang);
    updateContent(langData);

    // Check the associated radio button
    document.getElementById('option1').checked = (lang === 'fr');
    document.getElementById('option2').checked = (lang === 'en');
}

// Call changeLanguage() based on radio button selection
document.getElementById('option1').addEventListener('click', function() {
    changeLanguage('fr');
});

document.getElementById('option2').addEventListener('click', function() {
    changeLanguage('en');
});

// Call updateContent() on page load
window.addEventListener('DOMContentLoaded', async () => {
    const userPreferredLanguage = localStorage.getItem('language') || 'en';
    await changeLanguage(userPreferredLanguage);
});
