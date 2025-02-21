var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            alert('Please log in to add items to cart')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        
        // Update the cart icon total
        document.getElementById('cart-total').textContent = data.cartItems

        // Find the cart row for this product
        const cartRow = document.querySelector(`.cart-row[data-product="${productId}"]`)
        if (cartRow) {
            // Update quantity
            const quantityElement = cartRow.querySelector('.quantity')
            if (quantityElement) {
                quantityElement.textContent = data.itemQuantity
            }

            // Update item total
            const itemTotalElement = cartRow.querySelector('.item-total')
            if (itemTotalElement) {
                itemTotalElement.textContent = '₹' + data.itemTotal.toFixed(2)
            }

            // Update cart summary
            const cartItemsElement = document.getElementById('cart-items')
            const cartTotalElement = document.getElementById('cart-total-price')
            if (cartItemsElement && cartTotalElement) {
                cartItemsElement.textContent = data.cartItems
                cartTotalElement.textContent = ' ₹' + data.cartTotal.toFixed(2)
            }

            // Remove row if quantity is 0
            if (data.itemQuantity <= 0) {
                cartRow.remove()
            }
        }

        // Show success message if needed
        if(data.message) {
            console.log(data.message)
        }
    })
    .catch((error) => {
        console.error('Error:', error)
        alert('An error occurred while updating the cart')
    })
} 