const form = document.getElementById('p-form');

const title = document.getElementById('out_book_title');
const another_title = document.getElementById('another_out_book_title');
const description = document.getElementById('out_description');
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = "";

form.addEventListener('submit', e=>{
    e.preventDefault();
    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('out_book_title', title.value);
    fd.append('another_out_book_title', another_title.value);
    fd.append('out_description', description.value);
    console.log(fd.get('out_book_title'));
    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(response){
            const bookTitle = response.name;
            const anotherBookTitle = response.another_name;

            // Console log the specific fields
            console.log('Book Title:', bookTitle);
            console.log('Another Book Title:', anotherBookTitle);
        },
        error: function(error){
            console.log(error)
        },
        cache: false,
        contentType: false,
        processData: false,
        
    })
    
})