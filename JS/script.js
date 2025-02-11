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