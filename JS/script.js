document.querySelector(".menu-toggle").addEventListener("click", function () {
    document.querySelector(".nav-links").classList.toggle("active");
});


document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        let cartCount = document.getElementById('cart-count');
        cartCount.innerText = parseInt(cartCount.innerText) + 1;
    });
});

let cartItems = JSON.parse(localStorage.getItem('cart')) || [];
const cartContainer = document.getElementById('cart-items');
const cartTotal = document.getElementById('cart-total');

function updateCart() {
    cartContainer.innerHTML = '';
    let total = 0;
    cartItems.forEach((item, index) => {
        let cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <p>${item.name}</p>
            <p>$${item.price.toFixed(2)}</p>
            <button onclick="removeItem(${index})">Remove</button>
        `;
        cartContainer.appendChild(cartItem);
        total += item.price;
    });
    cartTotal.innerText = total.toFixed(2);
}

function removeItem(index) {
    cartItems.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cartItems));
    updateCart();
}

updateCart();

function searchFood() {
    let searchValue = document.getElementById('search').value;
    if (searchValue) {
        alert('Searching for: ' + searchValue);
    } else {
        alert('Please enter a food item to search.');
    }
}

let index = 0;
function nextSlide() {
    const slider = document.getElementById('food-slider');
    index = (index + 1) % 6;
    slider.style.transform = `translateX(-${index * 16.66}%)`;
}
function prevSlide() {
    const slider = document.getElementById('food-slider');
    index = (index - 1 + 6) % 6;
    slider.style.transform = `translateX(-${index * 16.66}%)`;
}

// Add event listeners for slider buttons
document.getElementById('next-button').addEventListener('click', nextSlide);
document.getElementById('prev-button').addEventListener('click', prevSlide);

document.addEventListener('DOMContentLoaded', function() {
    // Handle the login form submission
    const loginForm = document.querySelector('.login-form form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Basic validation
            if (email === '' || password === '') {
                alert('Please fill in all fields.');
                return;
            }

            // Simulate form submission
            alert('Login successful!');
            // You can add your form submission logic here (e.g., AJAX request)
        });
    }

    // Handle the contact form submission
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            // Basic validation
            if (name === '' || email === '' || message === '') {
                alert('Please fill in all fields.');
                return;
            }

            // Simulate form submission
            alert('Message sent successfully!');
            // You can add your form submission logic here (e.g., AJAX request)
        });
    }
});