let submitButton = document.getElementById('submit');
let info = document.getElementById('info');

document.getElementById('newPost').addEventListener('submit', (event) => {
    event.preventDefault();
    submitButton.disabled = true;
    submitButton.innerHTML = 'Posting...';
    event.target.postText.disabled = true;

    fetch(event.target.action, {
        method: 'POST',
        body: JSON.stringify({
            text: event.target.postText.value
        }),
        headers: {
            "X-CSRFToken":  event.target.csrfmiddlewaretoken.value
        }
    })
    .then(() => {
        submitButton.innerHTML = 'Post';
        event.target.postText.value = '';
        event.target.postText.disabled = false;
        info.style.display = 'flex';
        setTimeout(() => {
            info.style.display = 'none';
        }, 5000);
    })
})

document.getElementById('postText').addEventListener('keyup', (event) => {
    if (event.target.value === '' || event.target.value.length > 280) submitButton.disabled = true;
    else submitButton.disabled = false;
})