console.log("Sanity check!");

// new
// Get Stripe publishable key
fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        document.querySelector("#make-payment").addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/create-checkout-session/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then((result) => { return result.json(); })
            .then((data) => {
                console.log(data);
                // Redirect to Stripe Checkout
                return stripe.redirectToCheckout({ sessionId: data.sessionId })
            })
            .then((res) => {
                console.log(res);
                if (res.error) {
                    alert(res.error.message);
                }
            })
            .catch(function (error) {
                console.error("Error:", error);
            });
        });
    });