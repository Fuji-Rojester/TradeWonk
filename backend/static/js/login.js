// static/js/login.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    // Use the ID from login.html
    const emailOrUsernameInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const generalError = document.getElementById('general-error');
    const rememberCheckbox = document.getElementById('remember-me'); // Get remember checkbox
    const loginButton = form.querySelector('button[type="submit"]');

    if (!form) {
        console.error("Login form not found");
        return;
    }

    const showError = (inputEl, errorEl, message) => {
        if (inputEl) inputEl.classList.add('input-error'); // Use CSS class
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block'; // Make error visible
        }
    };

    const clearError = (inputEl, errorEl) => {
        if (inputEl) inputEl.classList.remove('input-error');
        if (errorEl) {
            errorEl.textContent = '';
            errorEl.style.display = 'none'; // Hide error space
        }
    };

    const clearAllErrors = () => {
        clearError(emailOrUsernameInput, emailError);
        clearError(passwordInput, passwordError);
        if (generalError) {
            generalError.textContent = '';
            generalError.style.display = 'none';
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearAllErrors();

        let isValid = true;
        const emailOrUsername = emailOrUsernameInput.value.trim();
        const password = passwordInput.value; // Don't trim password
        const remember = rememberCheckbox ? rememberCheckbox.checked : false; // Get remember value

        // Basic Validation
        if (!emailOrUsername) {
            showError(emailOrUsernameInput, emailError, 'Email or Username is required.');
            isValid = false;
        } else if (emailOrUsername.includes('@') && !/\S+@\S+\.\S+/.test(emailOrUsername)) {
            showError(emailOrUsernameInput, emailError, 'Please enter a valid email format.');
            isValid = false;
        }

        if (!password) {
            showError(passwordInput, passwordError, 'Password is required.');
            isValid = false;
        }

        if (!isValid) return;

        // Prepare payload matching backend expectations
        const payload = {
            [emailOrUsername.includes('@') ? 'email' : 'username']: emailOrUsername,
            password: password,
            remember: remember // Send remember status
        };

        if (loginButton) {
            loginButton.disabled = true;
            loginButton.textContent = 'Logging in...';
        }

        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include', // Important for cookies/sessions
                body: JSON.stringify(payload)
            });

            // Try parsing JSON even if response is not ok, backend might send error details
            const data = await res.json();

            if (res.ok) { // Status 200-299
                // SUCCESS: Redirect to dashboard (or other target)
                window.location.href = '/dashboard'; // Ensure this route exists
            } else {
                // FAILURE: Display error from backend response
                if (generalError) {
                    generalError.textContent = data.error || `Login failed (Status: ${res.status})`;
                    generalError.style.display = 'block';
                } else {
                    alert(data.error || `Login failed (Status: ${res.status})`); // Fallback
                }
            }
        } catch (err) {
            console.error("Login fetch error:", err);
            if (generalError) {
                generalError.textContent = 'Network error or server unavailable. Please try again.';
                generalError.style.display = 'block';
            } else {
                alert('Network error or server unavailable. Please try again.'); // Fallback
            }
        } finally {
            if (loginButton) {
                loginButton.disabled = false;
                loginButton.textContent = 'Login';
            }
        }
    });
});