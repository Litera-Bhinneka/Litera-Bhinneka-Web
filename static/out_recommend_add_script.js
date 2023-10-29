const form = document.getElementById('p-form');

const title = document.getElementById('out_book_title');
const another_title = document.getElementById('another_out_book_title');
const description = document.getElementById('out_description');
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = "../outside-recommendation-add/";

form.addEventListener('submit', function(e) {
    e.preventDefault();
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf[0].value,
        },
        body: new FormData(form),
    })
    .then(response => {
        if (response.ok) {
            form.reset();
        }
        return response.json();
    })

    window.location.href = `../show-out-recommendation/`;
})