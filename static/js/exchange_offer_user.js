    // Get the modals and OK buttons
    var successModal = document.getElementById("successModal");
    var failedModal = document.getElementById("failedModal");
    var successModalOK = document.getElementById("successModalOK");
    var failedModalOK = document.getElementById("failedModalOK");

    // Function to open the success modal
    function openSuccessModal(id) {
        successModal.classList.remove("hidden");

        document.getElementById("scheduleMeetingButton").addEventListener("click", function () {
            // Redirect to the meeting page with the specified id
            window.location.href = `/exchange/schedule-meet/${id}/`; // Adjust the URL pattern as needed
        });
    }

    // Function to open the failed modal
    function openFailedModal() {
        failedModal.classList.remove("hidden");
    }

    // Function to close the modals
    function closeModal() {
        successModal.classList.add("hidden");
        failedModal.classList.add("hidden");
    }

    // Close the modals when the OK buttons are clicked
    successModalOK.onclick = closeModal;
    successModalClose.onclick = closeModal;
    failedModalClose.onclick = closeModal;
    failedModalOK.onclick = closeModal;


    function addOffer(username) {
        event.preventDefault();
        var form = new FormData(document.querySelector('#form'));
        form.append('target_user', username);

        // Loop through select elements and add book ID and quantity to the form data
        $("select").each(function() {
            var bookId = $(this).data("bookid");
            var bookTitle = $(this).data("booktitle");
            var quantity = $(this).val();
            form.append('book_ids', bookId);
            form.append('quantities', quantity);
            form.append('book_titles', bookTitle);
        });

        fetch(window.OfferURL, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken, // Include the CSRF token
            },
            body: form,
        }).then(response => {
            if (response.ok) {
                response.json().then(data => {
                console.log(data);
                openSuccessModal(data.id);
                });
            } else {
                openFailedModal();
            }
        });

        document.getElementById("form").reset();
        return false;
    }