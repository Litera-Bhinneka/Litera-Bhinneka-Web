document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form');
    const bookSearch = document.getElementById('bookSearch');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const searchQuery = bookSearch.value.trim();
        // Construct the search URL with the updated query
        const baseURL = '/exchange/'; // base URL
        const searchURL = `${baseURL}?q=${encodeURIComponent(searchQuery)}`;
        // Redirect to the new URL
        window.location.href = searchURL;
    });
});

function closeModal() {
    $("#bookModal").hide();
}

async function getOwners(book_id) {
    return fetch("/exchange/get-owners/" + book_id + "/").then((res) => res.json())
}

async function openModal(book_id) {
    const owners = await getOwners(book_id);

    $("#owners").empty();
    
    if (owners.length === 0) {
        // If there are no owners, display a message
        const noOwnersMessage = document.createElement("p");
        noOwnersMessage.textContent = "There are no users with this book";
        $("#owners").append(noOwnersMessage);
    } else {
        // If there are owners, loop through and display them
        owners.forEach(owner => {
            const ownerUsername = owner.fields.username;

            const userDiv = document.createElement("div");
            userDiv.className = "owner-info flex items-center justify-between"; // Flex layout

            // Create an image element for the user's profile picture
            const profileImage = document.createElement("img");
            profileImage.src = "https://media.discordapp.net/attachments/1054028087551078452/1167449134421254194/def.png?ex=654e2abb&is=653bb5bb&hm=627c977e5a4ddfc7fde42bede685dd1430d9f8bd22a155811a9cc2f9e1c185cc&=&width=125&height=125";
            profileImage.alt = "Profile Image";
            profileImage.className = "profile-image";

            // Create a div for the left part (profile image and username)
            const leftDiv = document.createElement("div");
            leftDiv.className = "flex items-center";

            // Create a span for the username
            const usernameSpan = document.createElement("span");
            usernameSpan.textContent = ownerUsername;
            usernameSpan.className = "ml-2"; // Add margin to separate from the profile image

            // Append the profile image and username to the left div
            leftDiv.appendChild(profileImage);
            leftDiv.appendChild(usernameSpan);

            // Create a button "Send Offer" for the user
            const sendOfferButton = document.createElement("button");
            sendOfferButton.textContent = "Send Offer";
            sendOfferButton.className = "send-offer-button";
            sendOfferButton.onclick = function () {
                window.location.href = "/exchange/offer-user/" + ownerUsername + "/";
            };

            const rightDiv = document.createElement("div");
            rightDiv.className = "flex pl-auto items-center justify-end";

            // Append the "Send Offer" button to the right div
            rightDiv.appendChild(sendOfferButton);

            // Append the left div (profile image and username) to the user div
            userDiv.appendChild(leftDiv);

            // Append the "Send Offer" button to the user div
            userDiv.appendChild(rightDiv);

            // Append the owner's div to the modal content
            $("#owners").append(userDiv);
        });
    }

    $("#bookModal").show();
}