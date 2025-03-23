document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('waitlistForm');
    const emailInput = document.getElementById('email');
    const errorMessage = document.querySelector('.error-message');
    const optionsError = document.querySelector('.options-error');
    const formView = document.querySelector('.form-view');
    const successView = document.querySelector('.success-view');

    // Function to validate email format
    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    // Function to show email error message
    const showEmailError = () => {
        emailInput.classList.add('error');
        errorMessage.classList.add('visible');
    };

    // Function to hide email error message
    const hideEmailError = () => {
        emailInput.classList.remove('error');
        errorMessage.classList.remove('visible');
    };

    // Function to show options error message
    const showOptionsError = () => {
        optionsError.classList.add('visible');
    };

    // Function to hide options error message
    const hideOptionsError = () => {
        optionsError.classList.remove('visible');
    };

    // Function to get selected use cases
    const getSelectedUseCases = () => {
        const checkboxes = document.querySelectorAll('input[name="useCase"]:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    };

    // Function to show success state
    const showSuccessState = () => {
        // Animate transition
        formView.classList.add('fade-out');
        setTimeout(() => {
            formView.classList.add('hidden');
            successView.classList.remove('hidden');
            // Force reflow
            successView.offsetHeight;
            successView.classList.add('fade-in');
        }, 500);
    };

    // Validate on form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = emailInput.value;
        const selectedUseCases = getSelectedUseCases();
        let isValid = true;
        
        // Validate email
        if (!isValidEmail(email)) {
            showEmailError();
            emailInput.focus();
            isValid = false;
        } else {
            hideEmailError();
        }

        // Validate options selection
        if (selectedUseCases.length === 0) {
            showOptionsError();
            isValid = false;
        } else {
            hideOptionsError();
        }

        // If all validations pass
        if (isValid) {
            try {
                const response = await fetch('/api/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email,
                        useCases: selectedUseCases
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Show success state
                    showSuccessState();
                } else {
                    // Show error message
                    alert(data.error || 'Something went wrong. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to submit form. Please try again.');
            }
        }
    });

    // Hide email error when user starts typing again
    emailInput.addEventListener('input', () => {
        hideEmailError();
    });

    // Hide options error when user selects an option
    document.querySelectorAll('input[name="useCase"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (getSelectedUseCases().length > 0) {
                hideOptionsError();
            }
        });
    });
}); 