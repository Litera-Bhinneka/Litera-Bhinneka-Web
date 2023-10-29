var isUserAuthenticated = document.getElementById('auth-status').dataset.isAuthenticated === 'true';

if (isUserAuthenticated) {
    document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("add-button").addEventListener("click", function() {
            window.location.href = `../outside-recommendation-add/`;
        });
    });
    
    async function getRecommendations() {
        return fetch(window.recommendationUrl).then((res) => res.json())
    }

    async function getUserBooks(){
        const response = await fetch(window.userInventoryUrl);
        const data = await response.json();
        const bookTitles = data.book_titles;
        return bookTitles;
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
                let datetime = rec.fields.out_recommendation_date;
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
                                <a href="#" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700" style="pointer-events: none;">
                                    <div class="flex flex-col justify-between p-4 leading-normal">
                                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.fields.out_book_title}</h5>
                                    </div>
                                </a>
                            </div>
                            <div class="card-content">
                                <div class="card-title">You may like to read this book </div>
                                <a href="#" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700" style="pointer-events: none;">
                                    <div class="flex flex-col justify-between p-4 leading-normal">
                                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.fields.another_out_book_title}</h5>
                                    </div>
                                </a>
                            </div>
                        </div>
                            <div class="card-desc">
                                ${rec.fields.out_description}
                            </div>
                            <div class="card-footer">
                                <span class="card-date">recommended by ${rec.fields.out_recommender_name} - ${formattedDate}</span>
                            </div>
                    </div>
                </div>`;
                document.getElementById("card-container").innerHTML = htmlString;
            })
        }
    }
    // search
    document.getElementById("searchForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        // Get the search query from the input field
        const searchQuery = document.getElementById("default-search").value;
        const searchResultsElement = document.getElementById("searchResults");
        searchResultsElement.innerHTML = "";
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
                                <a href="#" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700" style="pointer-events: none;">
                                    <div class="flex flex-col justify-between p-4 leading-normal">
                                        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${rec.book_title}</h5>
                                    </div>
                                </a>
                            </div>
                            <div class="card-content">
                                <div class="card-title">You may like to read this book </div>
                                <a href="#" class="flex flex-col items-center rounded-lg md:flex-row md:max-w-xl dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700" style="pointer-events: none;">
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
