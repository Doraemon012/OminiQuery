isSQLConfigured = false;

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("mysqlConfigForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the form from submitting via the browser
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());
        console.log(data)
        // Replace '/submit-form' with your Flask route
        fetch('/submit-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                isSQLConfigured = true;
                // send user to /chat
                window.location.href = "/chat";
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});
