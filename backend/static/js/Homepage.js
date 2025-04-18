document.addEventListener('DOMContentLoaded', () => {

    // --- Initialize AOS ---
    // AOS is initialized via <script> tag in HTML after including the library
    // AOS.init({ duration: 800, once: true }); // Moved to HTML for clarity

    // --- Smooth Scrolling for Anchor Links ---
    const headerHeight = document.querySelector('.header')?.offsetHeight || 70; // Dynamically get header height or fallback
    const scrollLinks = document.querySelectorAll('a[href^="#"]'); // Select all anchor links

    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            // Ensure it's a valid internal link and not just "#"
            if (targetId && targetId.startsWith('#') && targetId.length > 1) {
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    e.preventDefault(); // Prevent default jump only if target exists

                    const offsetTop = targetElement.offsetTop - headerHeight - 10; // Adjusted offset (header + extra space)

                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });

                    // Close mobile nav if open after clicking a link
                    if (mobileNavToggle && navLinksContainer.classList.contains('active')) {
                       closeMobileMenu();
                    }
                }
            }
            // Allow default behavior for links like href="#" (e.g., buttons not for scrolling)
        });
    });


    // --- Mobile Navigation Toggle ---
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinksContainer = document.querySelector('.nav-links');
    const body = document.body; // Get body element

    function openMobileMenu() {
        navLinksContainer.classList.add('active');
        mobileNavToggle.innerHTML = '<i class="fas fa-times"></i>'; // Change to X icon
        mobileNavToggle.setAttribute('aria-expanded', 'true');
        body.style.overflow = 'hidden'; // Prevent background scroll when menu is open
    }

     function closeMobileMenu() {
        navLinksContainer.classList.remove('active');
        mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>'; // Change back to Bars
        mobileNavToggle.setAttribute('aria-expanded', 'false');
        body.style.overflow = ''; // Restore scrolling
    }

    if (mobileNavToggle && navLinksContainer) {
        mobileNavToggle.addEventListener('click', () => {
            const isExpanded = navLinksContainer.classList.contains('active');
            if (isExpanded) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
    }

    // --- Dark Mode Toggle ---
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const moonIcon = '<i class="fas fa-moon"></i>';
    const sunIcon = '<i class="fas fa-sun"></i>';

    // Function to apply theme based on preference
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            darkModeToggle.innerHTML = sunIcon; // Show sun icon in dark mode
             darkModeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            body.classList.remove('dark-mode');
            darkModeToggle.innerHTML = moonIcon; // Show moon icon in light mode
             darkModeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    };

    // Check localStorage for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    // Check system preference if no saved theme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Initialize theme: use saved theme, or system preference, or default to light
    const initialTheme = savedTheme ? savedTheme : (prefersDark ? 'dark' : 'light');
    applyTheme(initialTheme);


    // Event listener for the toggle button
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const currentTheme = body.classList.contains('dark-mode') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme); // Save the new preference
        });
    }

     // Listen for changes in system preference
     window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        // Only change if no theme is explicitly saved by the user
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });


    // --- Update Footer Year Dynamically ---
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // Accessibility: Ensure focus is managed appropriately if dynamic content loading occurs (not applicable here)
    // Accessibility: Ensure interactive elements are keyboard accessible (buttons, links, details/summary already are).

}); // End DOMContentLoaded