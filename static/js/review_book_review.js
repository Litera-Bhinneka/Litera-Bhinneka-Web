async function getReviews() {
    return fetch("/review/get-review-json/" + window.book_id + "/").then((res) => res.json())
}
async function getBook(){
    return fetch("/review/get-book-json/" + window.book_id + "/").then((res) => res.json())
}
async function getWishlist(){
    return fetch("/review/get-wishlist-json/" + window.book_id + "/").then((res) => res.json())
}
async function showBook() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const container = document.getElementById("book_container");
    container.innerHTML = "";  // Clear the current content.
    
    const book = await getBook();
    const reviews = await getReviews();
    const wishlist = await getWishlist();
    let messageRating = "rating"
    let avgRating = 0;

    reviews.forEach((review) => {
        avgRating += review.fields.review_score;
    });

    if (reviews.length > 0) {
        avgRating = avgRating / reviews.length;
        if (reviews.length > 1) {
            messageRating = "ratings";
        }
    }

    let showText;
    let hiddenText;
    let exceed;
    console.log(book[0].fields.description.length)
    if (book[0].fields.description.length > 250) {
        exceed = true;
        let reversedSubstring = book[0].fields.description.substring(250).split('').reverse().join(''); 
        let spaceIndex = reversedSubstring.indexOf(" "); 

        let sepIdx = spaceIndex !== -1 ? 250 - spaceIndex : 0; 
        showText = book[0].fields.description.substring(0, sepIdx);
        hiddenText = book[0].fields.description.substring(sepIdx, book[0].fields.description.length);
    } else {
        exceed = false;
    }
    
    let htmlString = '';
    let truncatedDesc = book[0].fields.description.split(' ').slice(0, 50).join(' ');

    htmlString += `
    <div id="book_image" class="m-4 w-1/3 flex justify-center items-center rounded-lg overflow-hidden shadow-xl">
        <img class="w-full h-auto object-cover" style="max-height: 600px; max-width: 550px;" src="${book[0].fields.image_link}" alt="book cover">
    </div>
        <div class="m-4 w-2/3 p-4">
            <h1 class="text-2xl font-bold mb-4">${book[0].fields.title}</h1>
            <div class="mb-4">
                <p class="text-gray-700">by <b>${book[0].fields.author}</b></p>
            </div>
            <div class="my-4 border-t border-solid border-gray-600 border-t-4 border-opacity-75 mx-0 w-full"></div>
            <div class="mb-4">
                <p class="text-gray-700 text-base">${exceed ? showText + `<span class="text-gray-700 text-base" id="dots-1">` + `<span id="realDots-1">...</span>`+ `<button onclick="readMore(-1)" id="readMoreBtn-1" class="text-blue-500 hover:text-blue-700 text-sm font-medium">Read More</button>` +`<span class="text-gray-700 text-base" id="more-1" style="display: none;">${hiddenText}</span>` + `</span>` : book[0].fields.description}</p>
                ${exceed ? `<button onclick="readMore(-1)" id="readLessBtn-1" class="text-blue-500 hover:text-blue-700 text-sm font-medium" style="display: none;">Read less</button>` : ''}
            </div>
            <div class="mb-4 flex items-center">
                <span class="mr-2">${avgRating.toFixed(1)}</span>
                <div class="star-rating" title="${avgRating*20}%">
                    <div class="back-stars">
                        <i class="fas fa-star" aria-hidden="true"></i>
                        <i class="fas fa-star" aria-hidden="true"></i>
                        <i class="fas fa-star" aria-hidden="true"></i>
                        <i class="fas fa-star" aria-hidden="true"></i>
                        <i class="fas fa-star" aria-hidden="true"></i>
                        
                        <div class="front-stars" style="width: ${avgRating*20}%">
                            <i class="fas fa-star" aria-hidden="true"></i>
                            <i class="fas fa-star" aria-hidden="true"></i>
                            <i class="fas fa-star" aria-hidden="true"></i>
                            <i class="fas fa-star" aria-hidden="true"></i>
                            <i class="fas fa-star" aria-hidden="true"></i>
                        </div>
                    </div>
                </div>
                <span class="ml-2">(${reviews.length} ${messageRating})</span>
            </div>
            <div class="mb-4">
                <button data-modal-target="add-review-modal" data-modal-toggle="add-review-modal" data-bs-target="#add-review-modal" class="custom-button" type="button" onclick="toggleModal()">
                    Add Review
                </button>
                <div class="love-widget">
                    <input type="checkbox" name="wishlist" value="yes" class="hidden" id="wishlist">
                    <label for="wishlist" class="fa fa-heart cursor-pointer" onclick="initializeLoveButton(${book[0].pk})"></label>
                </div>
            </div>
        </div>`;       

    
    const starRatingWrapper = document.querySelector('.star-rating');
    const frontStars =  document.querySelector('.front-stars');

    const rate = e => {
        const percentage = e.target.value + '%';
        starRatingWrapper.title = percentage;
        frontStars.style.width = percentage;
    };
    container.innerHTML = htmlString;

    if (wishlist.length >= 1) {
        // Auto check the wishlist checkbox
        document.getElementById('wishlist').checked = true;
    } else {
        // Wishlist is empty, checkbox remains unchecked (default state)
        document.getElementById('wishlist').checked = false;
    }
}

async function refreshReviews() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const container = document.getElementById("review_container");
    container.innerHTML = "";  // Clear the current content.
    
    const reviews = await getReviews();
    const stars = ['1', '2', '3', '4', '5'];
    
    let htmlString = '<div class="flex">';


    htmlString += `
    <div class="lg:w-1/5 pt-4 md:w1/4 pt-4">
        <div id="reviewFilter" class="sticky top-20 overflow-y-auto border-2 border-sky-500 rounded-lg p-4">
            <h2 class="text-lg font-semibold mb-4"><b>Rating</b></h2>
            <div class="mb-2">
                <label class="flex items-center">
                    <input type="checkbox" id="fiveStar" onclick="filterItems()" class="mr-2"> 5 Star
                </label>
            </div>
            <div class="mb-2">
                <label class="flex items-center">
                    <input type="checkbox" id="fourStar" onclick="filterItems()" class="mr-2"> 4 Star
                </label>
            </div>
            <div class="mb-2">
                <label class="flex items-center">
                    <input type="checkbox" id="threeStar" onclick="filterItems()" class="mr-2"> 3 Star
                </label>
            </div>
            <div class="mb-2">
                <label class="flex items-center">
                    <input type="checkbox" id="twoStar" onclick="filterItems()" class="mr-2"> 2 Star
                </label>
            </div>
            <div class="mb-2">
                <label class="flex items-center">
                    <input type="checkbox" id="oneStar" onclick="filterItems()" class="mr-2"> 1 Star
                </label>
            </div>
        </div>
    </div>
    <div class="w-4/5">
        `
    if (reviews.length !== 0) {
        reviews.forEach((review, index) => {
            let showText;
            let hiddenText;
            let exceed;
            if (review.fields.review_text.length > 250) {
                exceed = true;
                let reversedSubstring = review.fields.review_text.substring(250).split('').reverse().join(''); 
                let spaceIndex = reversedSubstring.indexOf(" "); 

                let sepIdx = spaceIndex !== -1 ? 250 - spaceIndex : 0; 
                showText = review.fields.review_text.substring(0, sepIdx);
                hiddenText = review.fields.review_text.substring(sepIdx, review.fields.review_text.length);
            } else {
                exceed = false;
            }
            let datetime = review.fields.review_date
            let formattedDate = (new Date(datetime)).toLocaleDateString('en-GB', {
                                                                            day: 'numeric',
                                                                            month: 'long',
                                                                            year: 'numeric',
                                                                            hour: 'numeric',
                                                                            minute: 'numeric',
                                                                            hour12: true,
                                                                        });
            
            htmlString += `
            <div class="card-review${review.fields.review_score} w-full p-4">
                <div id="card_review" class="bg-white border-2 border-sky-500 rounded-lg overflow-hidden">
                    <div class="px-6 pt-4">
                        <div class="font-bold text-xl mb-2">${review.fields.reviewer_name}</div>

                        <div class="flex items-center">
                        <!-- display rating in star component -->
                            <div class="flex space-x-1">
                                <div class="star-rating-review" title="${review.fields.review_score*20}%">
                                    <div class="back-stars">
                                        <i class="fas fa-star" aria-hidden="true"></i>
                                        <i class="fas fa-star" aria-hidden="true"></i>
                                        <i class="fas fa-star" aria-hidden="true"></i>
                                        <i class="fas fa-star" aria-hidden="true"></i>
                                        <i class="fas fa-star" aria-hidden="true"></i>
                                        
                                        <div class="front-stars" style="width: ${review.fields.review_score*20}%">
                                            <i class="fas fa-star" aria-hidden="true"></i>
                                            <i class="fas fa-star" aria-hidden="true"></i>
                                            <i class="fas fa-star" aria-hidden="true"></i>
                                            <i class="fas fa-star" aria-hidden="true"></i>
                                            <i class="fas fa-star" aria-hidden="true"></i>
                                        </div>
                                    </div>
                                </div>  
                            </div>
                        </div>
                        <span class="my-2"><b>${review.fields.review_summary}</b></span>
                        <div class="mb-4">
                            <p class="text-gray-700 text-base">${exceed ? showText + `<span class="text-gray-700 text-base" id="dots${index}">` + `<span id="realDots${index}">...</span>`+ `<button onclick="readMore(${index})" id="readMoreBtn${index}" class="text-blue-500 hover:text-blue-700 text-sm font-medium">Read More</button>` +`<span class="text-gray-700 text-base" id="more${index}" style="display: none;">${hiddenText}</span>` + `</span>` : review.fields.review_text}</p>
                            ${exceed ? `<button onclick="readMore(${index})" id="readLessBtn${index}" class="text-blue-500 hover:text-blue-700 text-sm font-medium" style="display: none;">Read less</button>` : ''}
                        </div>

                    </div>
                    <div class="px-6 pb-6">
                        <span class="text-gray-600 text-sm">${formattedDate}</span>
                    </div>
                </div>
            </div>`;
        });
        htmlString += "</div> </div>"
    }else{
        htmlString = `
        <div class="card-review6 w-full p-4">
            <div id="card_review" class="bg-white border-2 border-sky-500 rounded-lg overflow-hidden">
                <div class="card text-center">
                    <div class="card-text flex items-center justify-center mb-1">
                        No reviews yet, be the first to review!
                    </div>
                </div>
            </div>
        </div>`;
    }

    $(document).ready(function() {
        var star_rating_width = $('.fill-ratings span').width();
        $('.star-ratings').width(star_rating_width);
    });
    showBook()
    container.innerHTML = htmlString;
}

function addReview(book_id) {
    var reviewText = document.getElementById('review').value;
    var reviewSummary = document.getElementById('review_summary').value;
    var reviewScore = document.querySelector('input[name="review_score"]:checked');
    var alertRating = document.getElementById("ratingAlert");

    // Validate review_text, review_summary, and review_score
    if (!reviewText.trim() || !reviewSummary.trim()) {
        return false;
    }

    if (!reviewScore) {
        alertRating.style.color = "";
        alertRating.style.userSelect = "";
        setTimeout(function() {
            alertRating.style.color = "transparent";
            alertRating.style.userSelect = "none";
        }, 5000); // 5000 milliseconds = 5 seconds
        return false;
    }

    fetch("add-review-ajax/" + book_id + "/", {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshReviews)
    closeModal()

    // alertRating.style.display = "none";

    document.getElementById("form").reset()
    return false
}

function closeModal() {
    var modal = document.getElementById('add-review-modal');
    modal.classList.add('hidden');
}

function toggleModal() {
    var modal = document.getElementById('add-review-modal');
    modal.classList.toggle('hidden');
}
function readMore(index) {
    var dots = document.getElementById(`dots${index}`);
    var moreText = document.getElementById(`more${index}`);
    var realDots = document.getElementById(`realDots${index}`);
    var readLessBtn = document.getElementById(`readLessBtn${index}`);
    var readMoreBtn = document.getElementById(`readMoreBtn${index}`);

    if (readMoreBtn.style.display === "none") {
        // hide 
        dots.style.display = "inline";
        realDots.style.display = "inline";
        readMoreBtn.style.display = "inline";
        readLessBtn.style.display = "none";
        moreText.style.display = "none";
    } else {
        // show
        dots.style.display = "inline";
        realDots.style.display = "none";
        readMoreBtn.style.display = "none";
        readLessBtn.style.display = "inline";
        moreText.style.display = "inline";
        
    }
}
function filterItems() {
    var rating5 = document.getElementsByClassName('card-review5 w-full p-4');
    var rating4 = document.getElementsByClassName('card-review4 w-full p-4');
    var rating3 = document.getElementsByClassName('card-review3 w-full p-4');
    var rating2 = document.getElementsByClassName('card-review2 w-full p-4');
    var rating1 = document.getElementsByClassName('card-review1 w-full p-4');

    toggleDisplay(rating5, 'fiveStar');
    toggleDisplay(rating4, 'fourStar');
    toggleDisplay(rating3, 'threeStar');
    toggleDisplay(rating2, 'twoStar');
    toggleDisplay(rating1, 'oneStar');
}

function toggleDisplay(elements, checkboxId) {
    var allUnchecked = true;

    // Check if any checkbox is checked
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        if (checkbox.checked) {
            allUnchecked = false;
        }
    });

    // If all checkboxes are unchecked, show all elements
    if (allUnchecked) {
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = 'block';
        }
        return;
    }

    // If any checkbox is checked, apply individual display logic
    var shouldHide = document.getElementById(checkboxId).checked;

    for (var i = 0; i < elements.length; i++) {
        elements[i].style.display = shouldHide ? 'block' : 'none';
    }
}
function initializeLoveButton(book_id) {
    $('.love-widget input[name="wishlist"]').click(function() {
        if ($(this).is(':checked')) {
            fetch("{% url 'manage_user:add_wishlist' book_id=book.id %}", {
                method: "POST",
                headers: {
                "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                }
            })
            $(this).next('label').css('color', 'rgb(213, 52, 52)');
        } else {
            fetch("{% url 'manage_user:remove_wishlist' book_id=book.id %}", {
                method: "DELETE",
                headers: {
                "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                }
            })
            $(this).next('label').css('color', '#afafaf');
        }
    });
}

// Call the function to initialize the love button behavior
$(document).ready(function() {
    initializeLoveButton();
});


showBook()
refreshReviews()