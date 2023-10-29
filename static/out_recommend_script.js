document.getElementById("add-button").addEventListener("click", function() {
    // Redirect to "show_out_recommendations.html"
    window.location.href = "outside-recommendation-add";
});

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
refreshRecommendations();