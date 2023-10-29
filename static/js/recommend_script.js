

var isUserAuthenticated = document.getElementById('auth-status').dataset.isAuthenticated === 'true';

if (isUserAuthenticated) {
    
async function getRecommendations() {
    return fetch(window.recommendationUrl).then((res) => res.json())
}

async function getIdBooks(){
    const response = await fetch(window.bookIdsUrl);
    const data = await response.json();
    const bookIds = data.book_ids;
    return bookIds;
}

async function getUserBooks(){
    const response = await fetch(window.userInventoryUrl);
    const data = await response.json();
    const bookTitles = data.book_titles;
    return bookTitles;
}

async function getBookImages(){
    const response = await fetch(window.bookImageUrl);
    const data = await response.json();
    const bookImages = data.book_images;
    return bookImages;
}

async function refreshRecommendations() {
    document.getElementById("card-container").innerHTML = ""
    const recommendations = await getRecommendations()
    if (recommendations.length === 0){
        let htmlString = ''
        htmlString += `
        <div class="w-full p-4 mb-4">
            <div class="card text-center">
                <div class="card-text flex items-center justify-center mb-1">
                    There are no recommendations yet, Start recommending now!
                </div>
            </div>
        </div>`
        document.getElementById("card-container").innerHTML = htmlString;
    }else{
        let htmlString = ''
        recommendations.forEach((rec) => {
            let datetime = rec.fields.recommendation_date;
            let formattedDate = (new Date(datetime)).toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: true,
            });
            htmlString += `
            <div class="w-full p-4 mb-4">
                <div class="card">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="card-content">
                            <div class="card-title">If you like to read this book </div>
                            <a href="/review/book-review/${rec.fields.book_id}" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                                <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-l-lg" src="${rec.fields.book_image}" id="book-image2" alt="book image">
                                <div class="flex flex-col justify-between p-4 leading-normal">
                                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.fields.book_title}</h5>
                                </div>
                            </a>
                        </div>
                        <div class="card-content">
                            <div class="card-title">You may like to read this book </div>
                            <a href="/review/book-review/${rec.fields.another_book_id}" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                                <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-l-lg" src="${rec.fields.another_book_image}" id="book-image2" alt="book image">
                                <div class="flex flex-col justify-between p-4 leading-normal">
                                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.fields.another_book_title}</h5>
                                </div>
                            </a>
                        </div>
                    </div>
                        <div class="card-desc">
                            ${rec.fields.description}
                        </div>
                        <div class="card-footer">
                            <span class="card-date">recommended by ${rec.fields.recommender_name} - ${formattedDate}</span>
                        </div>
                </div>
            </div>`;
            document.getElementById("card-container").innerHTML = htmlString;
        })
    }
}
let selectedBookTitleGlobal;
let selectedBookTitleGlobal2;
let selectedBookIdGlobal;
let selectedBookIdGlobal2;
async function refreshInventory(){
    const books_title = await getUserBooks()
    const book_image = await getBookImages()
    const selectedElement = document.getElementById("owned_book");
    const selectedElement2 = document.getElementById("owned_book2");
    let firstItem;
    if (Array.isArray(books_title) && books_title.length > 1) {
        books_title.forEach((title, idx) => {
        const option = document.createElement("option");
        option.value = title;
        option.text = title;
        selectedElement.appendChild(option);
        if (idx === 0) {
            document.getElementById("book-image").setAttribute("src", book_image[0]);
            document.getElementById("label_owned_book2").textContent = "Choose a book similar to " + title;
            firstItem = title;
            selectedBookTitleGlobal = title;
            selectedBookIdGlobal = 0;

        } else if (idx == 1){
            books_title.forEach((title2) => {
                if(title2 != firstItem){
                    const option2 = document.createElement("option");
                    option2.value = title2;
                    option2.text = title2;
                    selectedElement2.appendChild(option2);
                }
            });
            selectedBookTitleGlobal2 = books_title[1];
            selectedBookIdGlobal2 = 1;
            document.getElementById("book-image2").setAttribute("src", book_image[1]);
        }
    });
    } else {
        const option = document.createElement("option");
        const option2 = document.createElement("option");
        option.text = "You must atleast has 2 books to recommend";
        option2.text = "You must atleast has 2 books to recommend";
        selectedElement.appendChild(option);
        selectedElement2.appendChild(option2);
        selectedElement.disabled = true;
        selectedElement2.disabled = true;
        document.getElementById("book-image").style.display = "none";
        document.getElementById("book-image2").style.display = "none";
        document.getElementById("label_owned_book2").textContent = "Choose a book similar to your book";
    }
}
$(document).ready(function() {
$("select.owned_book").change(async function() {
    const bookTitles = await getUserBooks();
    const bookImages = await getBookImages();
    
    let selectedIndex = $(this).prop("selectedIndex");
    let newImageSource = bookImages[selectedIndex];
    const selectedBookTitle = $(this).val();
    selectedBookTitleGlobal = selectedBookTitle;
    selectedBookIdGlobal = bookTitles.indexOf(selectedBookTitle);

    $("#book-image").attr("src", newImageSource);
    $("#label_owned_book2").text("Choose a book similar to " + selectedBookTitle);
    $("#owned_book2").empty();
    bookTitles.forEach(function(book) {
        if (book != selectedBookTitleGlobal) {
            const option = document.createElement("option");
            option.value = book;
            option.text = book;
            document.getElementById("owned_book2").appendChild(option);
        }
    });
    if(selectedIndex == 0){
        document.getElementById("book-image2").setAttribute("src", bookImages[1]);
        selectedBookTitleGlobal2 = bookTitles[1];
        selectedBookIdGlobal2 = 1;
    }else{
        document.getElementById("book-image2").setAttribute("src", bookImages[0]);
        selectedBookTitleGlobal2 = bookTitles[0];
        selectedBookIdGlobal2 = 0;
    }
    });
});
$(document).ready(function() {
$("select.owned_book2").change(async function() {
    const bookTitles = await getUserBooks();
    const bookImages = await getBookImages();

    bookImages.splice(bookTitles.indexOf(selectedBookTitleGlobal), 1);
    
    let selectedIndex = $(this).prop("selectedIndex");
    let newImageSource = bookImages[selectedIndex];
    const selectedBookTitle = $(this).val();
    selectedBookTitleGlobal2 = selectedBookTitle;
    selectedBookIdGlobal2 = bookTitles.indexOf(selectedBookTitle);
    
    $("#book-image2").attr("src", newImageSource);
    });
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("submit-button").onclick = addRecommendationAjax;
});

async function addRecommendationAjax() {
    const bookIds = await getIdBooks()
    let idBook = 0;
    let idBook2 = 0;
    if(selectedBookIdGlobal != undefined && selectedBookIdGlobal2 != undefined){
        idBook = bookIds[selectedBookIdGlobal];
        idBook2 = bookIds[selectedBookIdGlobal2];
    }
    let url = `/recommendation/add_recommendation_ajax/0/0/`;
    url = url.replace("0", idBook).replace("0", idBook2);
    console.log(url);
    fetch(url, {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshRecommendations)

    document.getElementById("description").value = ""
    return false
}
// Search form
document.getElementById("searchForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    // Get the search query from the input field
    const searchQuery = document.getElementById("default-search").value;
    const searchResultsElement = document.getElementById("searchResults");
    searchResultsElement.innerHTML = "";
    // Perform the search logic here
    fetch(window.recommendationSearchUrl + searchQuery)
      .then((res) => res.json())
      .then((data) => {
        const cardcontainer = document.getElementById("card-container");
        cardcontainer.innerHTML = "";
        
        if (data.recommendations.length > 0) {
            let htmlString = ''
            data.recommendations.forEach((rec) => {
                let datetime = rec.recommendation_date;
                let formattedDate = (new Date(datetime)).toLocaleDateString('en-GB', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true,
                });
                if(rec.description == undefined){
                    rec.description = ""
                }
                htmlString += `
                <div class="w-full p-4 mb-4">
                    <div class="card">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="card-content">
                                <div class="card-title">If you like to read this book </div>
                                <a href="/review/book-review/${rec.book_id}" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                                    <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-l-lg" src="${rec.book_image}" id="book-image2" alt="book image">
                                    <div class="flex flex-col justify-between p-4 leading-normal">
                                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.book_title}</h5>
                                    </div>
                                </a>
                            </div>
                            <div class="card-content">
                                <div class="card-title">You may like to read this book </div>
                                <a href="/review/book-review/${rec.another_book_id}" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                                    <img class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-l-lg" src="${rec.another_book_image}" id="book-image2" alt="book image">
                                    <div class="flex flex-col justify-between p-4 leading-normal">
                                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.another_book_title}</h5>
                                    </div>
                                </a>
                            </div>
                        </div>
                            <div class="card-desc">
                                ${rec.description}
                            </div>
                            <div class="card-footer">
                                <span class="card-date">recommended by ${rec.recommender_name} - ${formattedDate}</span>
                            </div>
                    </div>
                </div>`;
                document.getElementById("card-container").innerHTML = htmlString;
            });
        } else {
          searchResultsElement.innerHTML += `<p>There are no results for your search query.</p>`;
        }
    });

    // Update the DOM with search results
    
    if(searchQuery != ""){
        searchResultsElement.innerHTML += `<p>Search results for: <strong>${searchQuery}</strong></p>`;
    }
    // You can further customize the HTML structure based on your needs
});

    refreshInventory()
    refreshRecommendations()
} else {
    document.getElementById("logged-button").addEventListener("click", function() {
        var paragraph = document.createElement("p");
        paragraph.className = "text-sm text-gray-500";
        paragraph.textContent = "You need to login first to write a recommendation";
    
        var messageDiv = document.getElementById("messageDiv");
    
        messageDiv.innerHTML = "";
    
        messageDiv.appendChild(paragraph);
    });
    document.getElementById("card-container").innerHTML = ""
    let htmlString = ''
        htmlString += `
        <div class="w-full p-4 mb-4">
            <div class="card text-center">
                <div class="card-text flex items-center justify-center mb-1">
                    You need to log in to see user recommendations
                </div>
            </div>
        </div>`
    document.getElementById("card-container").innerHTML = htmlString;
}
