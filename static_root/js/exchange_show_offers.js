$(document).ready(function() {

    function closeModalPrompt() {
        $("#modalPrompt").addClass("hidden");
        location.reload();
    }

    // Close the modal prompt when the close button is clicked
    $("#modalPromptClose").click(function() {
        closeModalPrompt();
    });
});

function openModalPrompt(message) {
    $("#modalPromptMessage").text(message);
    $("#modalPrompt").removeClass("hidden");
}

function sendRequest(offerId, accept) {
    let url;
    console.log("sendRequest called");
    if (accept) {
        url = `/exchange/accept-offer/${offerId}/`;
    } else {
        url = `/exchange/delete-offer/${offerId}/`;
    }
    const headers = {
        "X-CSRFToken": csrfToken,
    };
    fetch(url, {
            method: "POST",
            headers: headers,
        })
        .then((response) => response.json())
        .then(function (response) {
            if (response.message) {
                openModalPrompt(response.message);
            } else {
                openModalPrompt("An error has occurred while exchanging. Please make a new Offer");
            }
        })
        .catch(function () {
            openModalPrompt("An error has occurred while exchanging. Please make a new Offer");
        });
}