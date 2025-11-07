let followers = document.getElementById("followers");
let button = document.getElementById("rel");


document.getElementById("form").addEventListener('submit', (event) => {
    event.preventDefault();

    let followers_count = Number.parseInt(followers.innerText);

    if (button.innerText === 'Follow') {
        button.className = "btn btn-dark py-1 px-3";
        button.innerText = "Unfollow";
        followers.innerText = followers_count + 1;
    } else {
        button.className = "btn btn-primary py-1 px-3";
        button.innerText = "Follow";
        followers.innerText = followers_count - 1;
    }

    fetch(event.target.action, {
        method: "PUT",
        headers: {
            "X-CSRFToken":  event.target.csrfmiddlewaretoken.value
        }
    })
})