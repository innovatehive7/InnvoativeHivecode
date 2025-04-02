    document.addEventListener("DOMContentLoaded", function () {
        // Handle form submission
        const form = document.getElementById("quickContactForm");
        const messageBox = document.getElementById("messageBox");

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            // Simulate form submission (replace with actual fetch/AJAX in Flask)
            const formData = new FormData(form);
            const data = {
                name: formData.get("name"),
                phone: formData.get("phone"),
                email: formData.get("email"),
                message: formData.get("message")
            };

            // Simulate success/error (in Flask, this would be server-side)
            try {
                // Simulate successful email send
                console.log("Form Data:", data); // Debug output
                messageBox.textContent = "Your message has been sent successfully!";
                messageBox.className = "message-box success";
                form.reset(); // Clear form
            } catch (error) {
                messageBox.textContent = "Error sending message. Please try again.";
                messageBox.className = "message-box error";
                console.error("Error:", error);
            }
        });

        // Scroll animation for sections
        const sections = document.querySelectorAll(".contact-section, .footer");

        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8
            );
        }

        function handleScroll() {
            sections.forEach((section) => {
                if (isInViewport(section) && !section.classList.contains("visible")) {
                    section.classList.add("visible");
                }
            });
        }

        // Initial check on page load
        handleScroll();

        // Add scroll event listener
        window.addEventListener("scroll", handleScroll);

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
            anchor.addEventListener("click", function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute("href")).scrollIntoView({
                    behavior: "smooth"
                });
            });
        });
    }); 
