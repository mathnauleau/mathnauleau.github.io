function switchLanguage(language) {
    fetch(`/${language}.json`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('main-heading').innerText = data.heading;
            document.getElementById('content').innerText = data.content;
            // Update URL
            history.pushState({}, '', `/${language}/`);
        })
        .catch(error => console.error('Error:', error));
}
