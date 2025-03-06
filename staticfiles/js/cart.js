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
        
        // Update cart item quantity
        if(data.itemQuantity){
            let quantityElement = document.querySelector(`.cart-row[data-product="${productId}"] .quantity`);
            if(quantityElement) quantityElement.textContent = data.itemQuantity;
        }
        
        // Update item total
        if(data.itemTotal){
            let totalElement = document.querySelector(`.cart-row[data-product="${productId}"] .item-total`);
            if(totalElement) totalElement.textContent = '₹' + data.itemTotal.toFixed(2);
        }
        
        // Update cart total items
        let cartItems = document.getElementById('cart-items');
        if(cartItems) cartItems.textContent = data.cartItems;
        
        // Update cart total price
        let cartTotal = document.getElementById('cart-total-price');
        if(cartTotal) cartTotal.textContent = ' ₹' + data.cartTotal.toFixed(2);
        
        // If item quantity is 0, remove the row
        if(data.itemQuantity === 0){
            let row = document.querySelector(`.cart-row[data-product="${productId}"]`);
            if(row) row.remove();
        }
        
        location.reload()
    })
} 