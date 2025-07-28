// Логика для страницы заказов
document.addEventListener('DOMContentLoaded', function() {
    const orderItems = [];
    let currentOrderTotal = 0;

    // Добавление товара в заказ
    document.querySelectorAll('.add-to-order').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const itemName = this.dataset.name;
            const itemPrice = parseFloat(this.dataset.price);

            // Проверяем, есть ли уже такой товар в заказе
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
        const totalElement = document.getElementById('order-total');

        // Очищаем контейнер
        itemsContainer.innerHTML = '';

        // Пересчитываем общую сумму
        currentOrderTotal = 0;

        // Добавляем каждый товар
        orderItems.forEach((item, index) => {
            currentOrderTotal += item.price * item.quantity;

            const itemElement = document.createElement('div');
            itemElement.className = 'order-item mb-2 p-2 border rounded';
            itemElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${item.name} ($${item.price.toFixed(2)})</span>
                    <div class="input-group" style="width: 120px">
                        <button class="btn btn-sm btn-outline-secondary decrease-quantity" data-index="${index}">-</button>
                        <input type="number" class="form-control text-center quantity-input"
                               value="${item.quantity}" min="1" data-index="${index}">
                        <button class="btn btn-sm btn-outline-secondary increase-quantity" data-index="${index}">+</button>
                    </div>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                    <button class="btn btn-sm btn-outline-danger remove-item" data-index="${index}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `;

            itemsContainer.appendChild(itemElement);
        });

        // Обновляем общую сумму
        totalElement.textContent = `$${currentOrderTotal.toFixed(2)}`;

        // Добавляем обработчики событий для новых элементов
        addEventListenersToOrderItems();
    }

    // Дополнительные функции для управления количеством
    function addEventListenersToOrderItems() {
        // Увеличение количества
        document.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                orderItems[index].quantity += 1;
                updateOrderDisplay();
            });
        });

        // Уменьшение количества
        document.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                if (orderItems[index].quantity > 1) {
                    orderItems[index].quantity -= 1;
                    updateOrderDisplay();
                }
            });
        });

        // Ручное изменение количества
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

        // Удаление товара
        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                orderItems.splice(index, 1);
                updateOrderDisplay();
            });
        });
    }
});