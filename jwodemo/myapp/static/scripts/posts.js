const postSelector = document.getElementById('postSelector');
const postContent = document.getElementById('postContent');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');

const posts = [
    
    { title: 'Man takes Mug into Car.', file: 'drinking-out-of-a-coffe-mug-while-driving' },
    { title: 'Covid Pepsi', file: 'covid-pepsi' },
    //{ title: 'Schmabe Nicknames', file: 'schmabe-nicknames' }
   // { title: 'Post 2', file: 'post-test-2' }
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
                postContent.innerHTML = html;
                postSelector.value = selectedFile;
                updateButtons();
            })
            .catch(error => console.error('Error loading post:', error));
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
