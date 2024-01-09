const postSelector = document.getElementById('postSelector');
const postContent = document.getElementById('postContent');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');

const posts = [
    { title: 'Man takes Mug into Car.', file: 'drinking-out-of-a-coffe-mug-while-driving' },
    { title: 'Covid Pepsi', file: 'covid-pepsi' },
    // Add more posts as needed
];
let currentIndex = -1;

function loadPost(index) {
    if (index >= 0 && index < posts.length) {
        const selectedPost = posts[index];
        currentIndex = index;
        const selectedFile = selectedPost.file;
        window.history.replaceState({}, '', `?post=${selectedFile}`);
        fetch(`static/blog/${selectedFile}.html`)
            .then(response => response.text())
            .then(html => {
                // Update HTML content
                postContent.innerHTML = html;
                
                // Replace "####" in image and link sources
                updateAttributeSources(postContent);

                // Replace "####" in audio sources
                updateAudioSources(postContent);

                // Replace "####" in style content
                updateStyleContent(postContent);

                postSelector.value = selectedFile;
                updateButtons();
            })
            .catch(error => console.error('Error loading post:', error));
    }
}

function updateAttributeSources(element) {
    // Get all image and link elements in the loaded content
    var elements = element.querySelectorAll('img, a');

    // Iterate through each element and update the src or href attribute
    elements.forEach(function (element) {
        if (element.tagName.toLowerCase() === 'img') {
            // For images
            updateAttribute(element, 'src');
        } else if (element.tagName.toLowerCase() === 'a') {
            // For links
            updateAttribute(element, 'href');
        }
    });
}

function updateAudioSources(element) {
    // Get all audio elements in the loaded content
    var audioElements = element.querySelectorAll('audio');

    // Iterate through each audio element and update the source
    audioElements.forEach(function (audioElement) {
        // Get the original source value
        var originalSource = audioElement.querySelector('source');

        if (originalSource) {
            // Get the original source value
            var originalSrc = originalSource.getAttribute('src');

            // Check if the source value starts with "####" (indicating a relative path)
            if (originalSrc && originalSrc.startsWith('####')) {
                // Update the source value with the static URL
                originalSource.setAttribute('src', STATIC_URL + originalSrc.substring(5)); // Remove the "####" from the original path
            }
        }
    });
}

function updateStyleContent(element) {
    // Get all style elements in the loaded content
    var styleElements = element.querySelectorAll('style');

    // Iterate through each style element and update the content
    styleElements.forEach(function (styleElement) {
        // Replace "####" in style content
        styleElement.innerHTML = styleElement.innerHTML.replace(/####/g, STATIC_URL);
    });
}

function updateAttribute(element, attribute) {
    // Get the original attribute value
    var originalValue = element.getAttribute(attribute);

    // Check if the attribute value starts with "####" (indicating a relative path)
    if (originalValue && originalValue.startsWith('####')) {
        // Update the attribute value with the static URL
        element.setAttribute(attribute, STATIC_URL + originalValue.substring(5)); // Remove the "####" from the original path
    }
}

function updateButtons() {
    prevButton.disabled = currentIndex <= 0;
    nextButton.disabled = currentIndex >= posts.length - 1;
}

postSelector.addEventListener('change', () => {
    const selectedFile = postSelector.value;
    const index = posts.findIndex(post => post.file === selectedFile);
    if (index !== -1) {
        loadPost(index);
    }
});

prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        loadPost(currentIndex);
    }
});

nextButton.addEventListener('click', () => {
    if (currentIndex < posts.length - 1) {
        currentIndex++;
        loadPost(currentIndex);
    }
});

const initialFile = new URLSearchParams(window.location.search).get('post');
const initialIndex = posts.findIndex(post => post.file === initialFile);
currentIndex = initialIndex !== -1 ? initialIndex : 0;

for (const post of posts) {
    const option = document.createElement('option');
    option.value = post.file;
    option.textContent = post.title;
    postSelector.appendChild(option);
}

loadPost(currentIndex);
