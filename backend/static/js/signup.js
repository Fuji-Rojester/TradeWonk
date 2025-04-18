document.addEventListener('DOMContentLoaded', () => {
    // --- Get references to elements (MAKE SURE IDs MATCH YOUR HTML!) ---
    const signupForm = document.getElementById('signup-form');
    const fullnameInput = document.getElementById('fullname'); // Used as Username
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const termsCheckbox = document.getElementById('terms');

    // --- Get references to error/feedback message elements ---
    const fullnameError = document.getElementById('fullname-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const confirmPasswordError = document.getElementById('confirm-password-error');
    const termsError = document.getElementById('terms-error');
    const generalError = document.getElementById('general-error'); // For general/backend errors

    // --- Password feedback elements (Add these to your HTML!) ---
    const passwordFeedback = document.getElementById('password-feedback'); // A container div
    const lengthCheck = document.getElementById('length-check');         // e.g., <li id="length-check">More than 8 characters</li>
    const upperCheck = document.getElementById('upper-check');           // e.g., <li id="upper-check">Uppercase letter</li>
    const lowerCheck = document.getElementById('lower-check');           // e.g., <li id="lower-check">Lowercase letter</li>
    const symbolCheck = document.getElementById('symbol-check');         // e.g., <li id="symbol-check">Symbol</li>

    if (!signupForm) {
        console.error("Signup form not found! Check the 'signup-form' ID in your HTML.");
        return;
    }

    // --- Debounce function ---
    let debounceTimeout;
    function debounce(func, delay) {
        return (...args) => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        };
    }

    // --- Helper Function to Show Errors ---
    function showError(inputElement, errorElement, message) {
        if (errorElement) errorElement.textContent = message;
        inputElement?.classList.add('input-error');
        if (inputElement?.type === 'checkbox') {
            inputElement?.closest('.checkbox-group')?.classList.add('input-error');
        }
        if(errorElement) errorElement.style.display = 'block'; // Make sure error message is visible
    }

    // --- Helper Function to Clear Errors ---
    function clearError(inputElement, errorElement) {
        if (errorElement) errorElement.textContent = '';
        inputElement?.classList.remove('input-error');
         if (inputElement?.type === 'checkbox') {
            inputElement?.closest('.checkbox-group')?.classList.remove('input-error');
        }
        if(errorElement) errorElement.style.display = 'none'; // Hide error message space
    }

    // --- Function to update live password feedback UI ---
    function updatePasswordFeedback(password) {
        const criteria = {
            length: password.length > 8, // Min 9 characters
            upper: /[A-Z]/.test(password),
            lower: /[a-z]/.test(password),
            symbol: /[^A-Za-z0-9]/.test(password) // Checks for non-alphanumeric
        };

        const updateCheck = (element, isValid) => {
            if (element) {
                element.classList.toggle('valid', isValid); // Add/remove 'valid' class
                element.classList.toggle('invalid', !isValid); // Add/remove 'invalid' class
                // Optional: Change text/icon based on valid/invalid
                // element.textContent = isValid ? `✓ ${element.dataset.text}` : `✗ ${element.dataset.text}`;
            }
        };

        if (passwordFeedback) passwordFeedback.style.display = 'block'; // Show feedback area
        updateCheck(lengthCheck, criteria.length);
        updateCheck(upperCheck, criteria.upper);
        updateCheck(lowerCheck, criteria.lower);
        updateCheck(symbolCheck, criteria.symbol);

        return criteria; // Return validation results
    }


    // --- Live Username Check Function ---
    async function checkUsernameAvailability(username) {
        clearError(fullnameInput, fullnameError); // Clear previous error first

        if (username.length < 3) { // Only check if reasonably long
             return;
        }

        try {
            const response = await fetch('/api/auth/check-username', { // NEW Endpoint
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username })
            });
            const result = await response.json();

            if (!response.ok) {
                console.error("Error checking username:", result);
                 // Handle server error if needed, maybe show a generic error
            } else if (result.exists) {
                showError(fullnameInput, fullnameError, 'Username already taken, please choose another.');
            } else {
               // Username is available, error is already cleared
               // Optionally show a success message/icon
            }
        } catch (error) {
            console.error('Network error checking username:', error);
            // Maybe show a temporary network error message
        }
    }
    // Debounced version of the username check
    const debouncedUsernameCheck = debounce(checkUsernameAvailability, 500); // 500ms delay


    // --- Add LIVE event listeners ---

    // Live Username Check Listener
    if (fullnameInput) {
        fullnameInput.addEventListener('input', (event) => {
            const username = event.target.value.trim();
            debouncedUsernameCheck(username);
        });
    }

    // Live Password Validation Listener
    if (passwordInput) {
        passwordInput.addEventListener('input', (event) => {
            const password = event.target.value;
            updatePasswordFeedback(password);
             // Also clear confirm password error if password changes
            clearError(confirmPasswordInput, confirmPasswordError);
        });
         // Clear feedback if field loses focus and is empty (optional)
        passwordInput.addEventListener('blur', (event) => {
            if (!event.target.value && passwordFeedback) {
                 passwordFeedback.style.display = 'none';
                 clearError(passwordInput, passwordError); // Clear submit error too
            }
        });
    }
     // Live check for confirm password matching
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', (event) => {
             const password = passwordInput ? passwordInput.value : '';
             const confirmPassword = event.target.value;
             if (password && confirmPassword && password !== confirmPassword) {
                 showError(confirmPasswordInput, confirmPasswordError, 'Passwords do not match.');
             } else {
                 clearError(confirmPasswordInput, confirmPasswordError);
             }
        });
    }


    // --- Add event listener for form SUBMISSION ---
    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default submission

        // --- Clear previous submission errors ---
        clearError(fullnameInput, fullnameError);
        clearError(emailInput, emailError);
        clearError(passwordInput, passwordError);
        clearError(confirmPasswordInput, confirmPasswordError);
        clearError(termsCheckbox, termsError);
        if (generalError) generalError.textContent = '';

        // --- Get values from form ---
        const username = fullnameInput ? fullnameInput.value.trim() : '';
        const email = emailInput ? emailInput.value.trim() : '';
        const password = passwordInput ? passwordInput.value : '';
        const confirmPassword = confirmPasswordInput ? confirmPasswordInput.value : '';
        const termsAccepted = termsCheckbox ? termsCheckbox.checked : false;

        // --- Final Client-Side Validation on Submit ---
        let isValid = true;

        // 1. Full Name / Username (Basic check, real check done live/backend)
        if (username.length < 3) {
            showError(fullnameInput, fullnameError, 'Username must be at least 3 characters.');
            isValid = false;
        }
        // Re-check username availability on submit in case it was taken between typing and submitting
        // (Optional, adds another request but safer)
        // await checkUsernameAvailability(username); // If you want to double-check
        // if (fullnameError.textContent) isValid = false;


        // 2. Email Validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
             showError(emailInput, emailError, 'Please enter a valid email address (e.g., name@domain.com).');
            isValid = false;
        }

        // 3. Password Validation (using live feedback function result)
        const passwordCriteria = updatePasswordFeedback(password); // Get latest validation state
        let passwordErrMsg = '';
        if (!passwordCriteria.length) {
            passwordErrMsg = 'Password must be more than 8 characters.';
        } else if (!passwordCriteria.upper) {
            passwordErrMsg = 'Password must contain an uppercase letter.';
        } else if (!passwordCriteria.lower) {
            passwordErrMsg = 'Password must contain a lowercase letter.';
        } else if (!passwordCriteria.symbol) { // Added Symbol Check
            passwordErrMsg = 'Password must contain a symbol (e.g., !@#$).';
        }

        if (passwordErrMsg) {
            showError(passwordInput, passwordError, passwordErrMsg);
             // Ensure feedback area is visible if hidden previously
            if(passwordFeedback) passwordFeedback.style.display = 'block';
            isValid = false;
        }

        // 4. Confirmation Password Match
        if (!passwordErrMsg && password !== confirmPassword) {
            showError(confirmPasswordInput, confirmPasswordError, 'Passwords do not match.');
            isValid = false;
        } else if (!confirmPassword && !passwordErrMsg) {
             showError(confirmPasswordInput, confirmPasswordError, 'Please confirm your password.');
            isValid = false;
        }

        // 5. Terms Checkbox
        if (!termsAccepted) {
             showError(termsCheckbox, termsError, 'You must agree to the terms.');
            isValid = false;
        }

        // --- Stop if Validation Failed ---
        if (!isValid) {
            return;
        }

        // --- Prepare data for API (Validation Passed) ---
        const dataToSend = {
            username: username,
            email: email,
            password: password
        };

        // --- Send data to backend API using fetch ---
        // Disable button during submission (optional)
        const submitButton = signupForm.querySelector('button[type="submit"]');
        if (submitButton) submitButton.disabled = true;


        try {
            const apiUrl = '/api/auth/register'; // Your existing backend route
            console.log(`Sending request to: ${apiUrl}`);
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend),
            });
            const result = await response.json();

            if (response.ok) {
                console.log('Registration successful:', result);
                // Redirect to login or maybe a "check your email" page
                window.location.href = '/login'; // Or '/signup-success' etc.
            } else {
                console.error(`Registration failed with status ${response.status}:`, result);
                 // Display backend error message (e.g., email already exists)
                if (result && result.error) {
                    if (generalError) {
                        generalError.textContent = result.error;
                        generalError.style.display = 'block';
                    } else alert(result.error);
                } else {
                    const errorText = `Registration failed. Please try again later. (Status: ${response.status})`;
                    if(generalError) {
                        generalError.textContent = errorText;
                        generalError.style.display = 'block';
                    } else alert(errorText);
                }
            }
        } catch (error) {
            console.error('Network or fetch error:', error);
            if (generalError) {
                generalError.textContent = 'Could not connect to the server. Please check your internet connection.';
                 generalError.style.display = 'block';
            } else alert('Could not connect to the server.');
        } finally {
             // Re-enable button
            if (submitButton) submitButton.disabled = false;
        }
    });
});