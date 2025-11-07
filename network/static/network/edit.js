document.querySelectorAll('.edit').forEach(editbtn => {
    let postid = Number.parseInt(editbtn.id.slice(5));

    let normalDiv = document.getElementById(`normal-${postid}`);
    let editingDiv = document.getElementById(`editing-${postid}`);

    let postText = document.getElementById(`post-${postid}`);
    let submitbtn = document.getElementById(`submit-${postid}`);
    let textarea = document.getElementById(`postText-${postid}`);

    let cancelbtn = document.getElementById(`cancel-${postid}`);

    editbtn.addEventListener('click', () => {
        normalDiv.style.display = 'none';
        editingDiv.style.display = 'block';
        textarea.innerText = postText.innerText;
        textarea.focus();
        textarea.selectionStart = textarea.selectionEnd = textarea.value.length;
    });

    document.getElementById(`postText-${postid}`).addEventListener('keyup', (event) => {
        if (event.target.value === postText.innerText || event.target.value === '' || event.target.value.length > 280) submitbtn.disabled = true;
        else submitbtn.disabled = false;
    })

    cancelbtn.addEventListener('click', () => {
        normalDiv.style.display = 'block';
        editingDiv.style.display = 'none';
    })

    document.getElementById(`save-${postid}`).addEventListener('submit', (event) => {
        event.preventDefault();
        cancelbtn.style.display = 'none';
        submitbtn.disabled = true;
        submitbtn.innerHTML = 'Saving...';
        event.target.postText.disabled = true;

        let text = event.target.postText.value;
    
        fetch(event.target.action, {
            method: 'PUT',
            body: JSON.stringify({
                text: text
            }),
            headers: {
                "X-CSRFToken":  event.target.csrfmiddlewaretoken.value
            }
        })
        .then(() => {
            submitbtn.innerHTML = 'Save';
            event.target.postText.disabled = false;
            postText.innerHTML = text;
            normalDiv.style.display = 'block';
            editingDiv.style.display = 'none';
            cancelbtn.style.display = 'block';
        })
    })
})