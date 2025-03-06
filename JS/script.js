// Wait for the DOM to be fully loaded before running any code
document.addEventListener('DOMContentLoaded', function() {
    
    // =============== CART FUNCTIONALITY ===============
    // Initialize cart array to store items
    let cart = [];

    // Get all "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    // Add click event listener to each "Add to Cart" button
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Get the parent menu item container
            const menuItem = e.target.closest('.menu-item');
            
            // Extract item details
            const itemDetails = {
                name: menuItem.querySelector('h3').textContent,
                price: menuItem.querySelector('.price').textContent,
                image: menuItem.querySelector('img').src,
                quantity: 1
            };

            // Add item to cart
            addToCart(itemDetails);
            
            // Show confirmation message
            showNotification('Item added to cart!');
        });
    });

    // Function to add items to cart
    function addToCart(item) {
        // Check if item already exists in cart
        const existingItem = cart.find(cartItem => cartItem.name === item.name);
        
        if (existingItem) {
            // If item exists, increase quantity
            existingItem.quantity += 1;
        } else {
            // If item is new, add to cart
            cart.push(item);
        }

        // Save cart to localStorage
        saveCart();
        
        // Update cart count display
        updateCartCount();
    }

    // Function to save cart to localStorage
    function saveCart() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Function to update cart item count in the UI
    function updateCartCount() {
        const cartButton = document.querySelector('.cart-btn');
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartButton.textContent = `Cart (${totalItems})`;
    }

    // =============== NOTIFICATION SYSTEM ===============
    // Function to show notification messages
    function showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;

        // Add notification to page
        document.body.appendChild(notification);

        // Remove notification after 2 seconds
        setTimeout(() => {
            notification.remove();
        }, 2000);
    }

    // =============== MENU NAVIGATION ===============
    // Get all menu section links
    const menuLinks = document.querySelectorAll('.menu-category');
    
    // Add click event listener to each menu link
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            menuLinks.forEach(link => link.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Scroll to corresponding section
            const targetId = this.getAttribute('href').slice(1);
            const targetSection = document.getElementById(targetId);
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // =============== SCROLL TO TOP ===============
    // Create scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-top';
    scrollButton.innerHTML = '↑';
    document.body.appendChild(scrollButton);

    // Show/hide scroll button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });

    // Scroll to top when button is clicked
    scrollButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // =============== INITIALIZE PAGE ===============
    // Load cart from localStorage when page loads
    function initializePage() {
        const savedCart = localStorage.getItem('cart');
        if (savedCart) {
            cart = JSON.parse(savedCart);
            updateCartCount();
        }
    }

    // Call initialization function
    initializePage();
});

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // =============== HERO SECTION SLIDER ===============
    const heroSlider = {
        currentSlide: 0,
        slides: document.querySelectorAll('.hero-slide'),
        dots: document.querySelectorAll('.slider-dot'),
        autoPlayInterval: null,

        init() {
            // Show first slide
            this.showSlide(0);
            
            // Set up auto-play
            this.startAutoPlay();

            // Add click events to dots
            this.dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    this.showSlide(index);
                    this.resetAutoPlay();
                });
            });

            // Add touch events for mobile
            let touchStartX = 0;
            document.querySelector('.hero-slider').addEventListener('touchstart', (e) => {
                touchStartX = e.touches[0].clientX;
            });

            document.querySelector('.hero-slider').addEventListener('touchend', (e) => {
                const touchEndX = e.changedTouches[0].clientX;
                const difference = touchStartX - touchEndX;

                if (difference > 50) { // Swipe left
                    this.nextSlide();
                } else if (difference < -50) { // Swipe right
                    this.previousSlide();
                }
            });
        },

        showSlide(index) {
            // Hide all slides
            this.slides.forEach(slide => {
                slide.style.display = 'none';
            });

            // Remove active class from all dots
            this.dots.forEach(dot => {
                dot.classList.remove('active');
            });

            // Show current slide and activate corresponding dot
            this.slides[index].style.display = 'block';
            this.dots[index].classList.add('active');
            this.currentSlide = index;
        },

        nextSlide() {
            const next = (this.currentSlide + 1) % this.slides.length;
            this.showSlide(next);
        },

        previousSlide() {
            const prev = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
            this.showSlide(prev);
        },

        startAutoPlay() {
            this.autoPlayInterval = setInterval(() => {
                this.nextSlide();
            }, 5000); // Change slide every 5 seconds
        },

        resetAutoPlay() {
            clearInterval(this.autoPlayInterval);
            this.startAutoPlay();
        }
    };

    // Initialize hero slider
    heroSlider.init();

    // =============== POPULAR ITEMS CAROUSEL ===============
    const popularItemsCarousel = {
        container: document.querySelector('.popular-items'),
        items: document.querySelectorAll('.popular-item'),
        prevBtn: document.querySelector('.carousel-prev'),
        nextBtn: document.querySelector('.carousel-next'),
        currentPosition: 0,

        init() {
            if (!this.container) return;

            // Add click events to navigation buttons
            this.prevBtn?.addEventListener('click', () => this.slide('prev'));
            this.nextBtn?.addEventListener('click', () => this.slide('next'));

            // Update carousel on window resize
            window.addEventListener('resize', () => this.updateCarousel());
            
            // Initial setup
            this.updateCarousel();
        },

        slide(direction) {
            const itemWidth = this.items[0].offsetWidth + 20; // Width + margin
            const visibleItems = Math.floor(this.container.offsetWidth / itemWidth);
            const maxPosition = this.items.length - visibleItems;

            if (direction === 'next' && this.currentPosition < maxPosition) {
                this.currentPosition++;
            } else if (direction === 'prev' && this.currentPosition > 0) {
                this.currentPosition--;
            }

            this.updateCarousel();
        },

        updateCarousel() {
            const translation = this.currentPosition * -(this.items[0].offsetWidth + 20);
            this.container.style.transform = `translateX(${translation}px)`;

            // Update button states
            if (this.prevBtn) this.prevBtn.disabled = this.currentPosition === 0;
            if (this.nextBtn) this.nextBtn.disabled = 
                this.currentPosition >= this.items.length - Math.floor(this.container.offsetWidth / (this.items[0].offsetWidth + 20));
        }
    };

    // Initialize popular items carousel
    popularItemsCarousel.init();

    // =============== SEARCH FUNCTIONALITY ===============
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = this.querySelector('input').value.trim();
            if (searchTerm) {
                // Redirect to search results page
                window.location.href = `search.html?q=${encodeURIComponent(searchTerm)}`;
            }
        });
    }

    // =============== LOCATION SELECTOR ===============
    const locationSelector = document.querySelector('.location-selector');
    if (locationSelector) {
        locationSelector.addEventListener('change', function() {
            const selectedLocation = this.value;
            // Save selected location to localStorage
            localStorage.setItem('userLocation', selectedLocation);
            // Optionally refresh content based on location
            updateContentForLocation(selectedLocation);
        });
    }

    function updateContentForLocation(location) {
        // Update relevant content based on selected location
        // This function would be implemented based on your specific needs
        console.log(`Updating content for location: ${location}`);
    }

    // =============== SPECIAL OFFERS COUNTDOWN ===============
    function updateCountdown() {
        const countdowns = document.querySelectorAll('.offer-countdown');
        
        countdowns.forEach(countdown => {
            const endTime = new Date(countdown.dataset.endTime).getTime();
            const now = new Date().getTime();
            const distance = endTime - now;

            if (distance < 0) {
                countdown.innerHTML = 'Offer expired';
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            countdown.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        });
    }

    // Update countdown every second
    setInterval(updateCountdown, 1000);

    // =============== LOAD CART COUNT ===============
    function updateCartCount() {
        const cartBtn = document.querySelector('.cart-btn');
        if (cartBtn) {
            const cart = JSON.parse(localStorage.getItem('cart')) || [];
            const itemCount = cart.reduce((total, item) => total + item.quantity, 0);
            cartBtn.innerHTML = `<i class="fas fa-shopping-cart"></i> Cart (${itemCount})`;
        }
    }

    // Initialize cart count
    updateCartCount();

    // =============== NEWSLETTER SUBSCRIPTION ===============
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            // Simulate newsletter subscription
            setTimeout(() => {
                alert(`Thank you for subscribing with ${email}!`);
                this.reset();
            }, 500);
        });
    }

    // =============== SCROLL TO TOP ===============
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-top';
    scrollBtn.innerHTML = '↑';
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});