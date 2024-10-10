window.onscroll = function() {myFunction()};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.scrollY >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

document.querySelector('.heart-icon').addEventListener('click', function() {
  this.classList.toggle('filled');
  this.classList.toggle('bi-heart');
  this.classList.toggle('bi-heart-fill');
});

// Function to add item to cart and update the cart count
function addToCart() {
  // Assuming 'cartCount' holds the number of items in the cart
  let cartCount = parseInt(document.getElementById('cart-count').textContent);

  // Increment the cart count
  cartCount += 1;

  // Update the cart count in the badge
  document.getElementById('cart-count').textContent = cartCount;
}

// Example: Attach the addToCart function to an "Add to Cart" button
document.getElementById('busket').addEventListener('click', addToCart);
