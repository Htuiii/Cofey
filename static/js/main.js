document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Подтверждение для действий удаления
    document.querySelectorAll('.confirm-action').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirmMessage || 'Вы уверены?')) {
                e.preventDefault();
            }
        });
    });

    // Динамическое обновление суммы заказа
    if (document.getElementById('create-order-form')) {
        setupOrderTotalCalculator();
    }
});

function setupOrderTotalCalculator() {
    const form = document.getElementById('create-order-form');
    const totalElement = document.getElementById('order-total');
    let orderItems = [];

    // Добавление товара в заказ
    document.querySelectorAll('.add-to-order').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const itemName = this.dataset.name;
            const itemPrice = parseFloat(this.dataset.price);
            
            const existingItem = orderItems.find(item => item.id === itemId);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                orderItems.push({
                    id: itemId,
                    name: itemName,
                    price: itemPrice,
                    quantity: 1
                });
            }
            
            updateOrderDisplay();
        });
    });

    // Обновление отображения заказа
    function updateOrderDisplay() {
        const itemsContainer = document.getElementById('order-items-container');
        itemsContainer.innerHTML = '';

        let total = 0;

        orderItems.forEach((item, index) => {
            total += item.price * item.quantity;

            const itemElement = document.createElement('div');
            itemElement.className = 'order-item-card mb-3 p-3 border rounded';
            itemElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${item.name}</h6>
                        <small class="text-muted">${item.price.toFixed(2)} ₽</small>
                    </div>
                    <div class="input-group quantity-control">
                        <button class="btn btn-outline-secondary decrease-quantity" data-index="${index}">-</button>
                        <input type="number" class="form-control text-center quantity-input"
                               value="${item.quantity}" min="1" data-index="${index}">
                        <button class="btn btn-outline-secondary increase-quantity" data-index="${index}">+</button>
                    </div>
                    <div class="text-end" style="width: 100px;">
                        <strong>${(item.price * item.quantity).toFixed(2)} ₽</strong>
                    </div>
                    <button class="btn btn-outline-danger btn-sm remove-item ms-2" data-index="${index}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
                <input type="hidden" name="item_id" value="${item.id}">
                <input type="hidden" name="quantity" value="${item.quantity}">
            `;

            itemsContainer.appendChild(itemElement);
        });

        totalElement.textContent = total.toFixed(2) + ' ₽';
        document.getElementById('total-amount-hidden').value = total;

        addEventListenersToOrderItems();
    }

    // Добавление обработчиков событий для элементов заказа
    function addEventListenersToOrderItems() {
        document.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                orderItems[index].quantity += 1;
                updateOrderDisplay();
            });
        });

        document.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                if (orderItems[index].quantity > 1) {
                    orderItems[index].quantity -= 1;
                    updateOrderDisplay();
                }
            });
        });

        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const index = parseInt(this.dataset.index);
                const newQuantity = parseInt(this.value);

                if (newQuantity >= 1) {
                    orderItems[index].quantity = newQuantity;
                    updateOrderDisplay();
                } else {
                    this.value = orderItems[index].quantity;
                }
            });
        });

        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                orderItems.splice(index, 1);
                updateOrderDisplay();
            });
        });
    }
}

// Функция для показа уведомлений
function showAlert(message, type = 'success', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('.alert-container') || document.body;
    container.prepend(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, duration);
}