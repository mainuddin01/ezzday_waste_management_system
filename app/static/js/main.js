// Main.js

document.addEventListener("DOMContentLoaded", function() {
    // Handle delete confirmation popups
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });

    // Navbar active link highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Example: Dynamic content manipulation (hover effect)
    navLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.color = '#ff6347';  // Change color on hover
        });

        link.addEventListener('mouseout', () => {
            link.style.color = '';  // Revert back to original color
        });
    });

    // Handle form input validations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('input-error');
                } else {
                    input.classList.remove('input-error');
                }
            });
            if (!valid) {
                event.preventDefault();
                alert('Please fill out all required fields.');
            }
        });
    });

    // Accessibility: Keyboard navigation for navbar
    navLinks.forEach(link => {
        link.addEventListener('focus', () => {
            link.style.backgroundColor = '#1abc9c';
        });
        link.addEventListener('blur', () => {
            link.style.backgroundColor = '';
        });
    });
});