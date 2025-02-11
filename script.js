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