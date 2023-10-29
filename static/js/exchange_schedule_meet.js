document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("scheduleMeetForm");
    const modal = document.getElementById("Modal");
    const modalMessage = document.querySelector("#Modal .text-center");
    const modalOKButton = document.getElementById("successModalOK");
    const modalCloseButton = document.getElementById("ModalClose");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        fetch("/exchange/schedule-meet/" + window.id + "/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken, // Include the CSRF token
            },
            body: new FormData(form), // Use FormData to send form data
        })
        .then(response => {
            if (response.ok) {
                form.reset();
            }
            return response.json();
        }) // Handle the response as needed
        .then(data => {
            if (data.message) {
                // Display the modal with the response message
                modalMessage.textContent = data.message;
                modal.classList.remove("hidden");
            } else {
                modalMessage.textContent = "Oops, something went wrong!";
                modal.classList.remove("hidden");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
    // Add an event listener to the modal's OK button to hide the modal
    modalOKButton.addEventListener("click", function () {
        modal.classList.add("hidden");
        window.location.href = window.ShowOffer;
    });

    modalCloseButton.addEventListener("click", function () {
        modal.classList.add("hidden");
        window.location.href = window.ShowOffer;
    });
});