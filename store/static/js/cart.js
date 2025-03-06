var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        if (user === 'AnonymousUser'){
            alert('Please login to add items to cart')
            window.location.href = '/login/'
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('Data:', data)
        
        // Always update cart total in navbar
        let cartTotal = document.getElementById('cart-total')
        if(cartTotal) {
            cartTotal.textContent = data.cartItems
        }
        
        // If we're on the cart page, update quantities and totals
        if(window.location.pathname.includes('cart')) {
            let quantityElement = document.querySelector(`.cart-row[data-product="${productId}"] .quantity`)
            if(quantityElement) {
                if(data.itemQuantity > 0) {
                    quantityElement.textContent = data.itemQuantity
                    document.querySelector(`.cart-row[data-product="${productId}"] .item-total`).textContent = '₹' + data.itemTotal.toFixed(2)
                } else {
                    let row = document.querySelector(`.cart-row[data-product="${productId}"]`)
                    if(row) row.remove()
                }
            }
            
            let cartTotalElement = document.getElementById('cart-total-price')
            if(cartTotalElement) {
                cartTotalElement.textContent = '₹' + data.cartTotal.toFixed(2)
            }
            
            if(data.itemQuantity === 0) {
                location.reload()
            }
        }
    })
} 