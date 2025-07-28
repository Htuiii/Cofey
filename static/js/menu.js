// Логика для страницы меню
document.addEventListener('DOMContentLoaded', function() {
    // Фильтрация меню по категориям
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const menuItems = document.querySelectorAll('.menu-item');

            menuItems.forEach(item => {
                if (selectedCategory === 'all' || item.dataset.category === selectedCategory) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
// Удаление товара
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', async function() {
            const itemId = this.dataset.id;

            if (confirm('Вы точно хотите удалить этот товар?')) {
                try {
                    const response = await fetch(`/menu/${itemId}/delete`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    const data = await response.json();

                    if (data.success) {
                        // Удаляем строку таблицы
                        this.closest('tr').remove();
                        alert('Товар успешно удалён');
                    } else {
                        alert('Ошибка: ' + data.error);
                    }
                } catch (error) {
                    console.error('Ошибка:', error);
                    alert('Ошибка сети');
                }
            }
        });
    });
    // Переключение доступности товара
    const availabilityToggles = document.querySelectorAll('.availability-toggle');
    availabilityToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const itemId = this.dataset.id;
            const isAvailable = this.checked;

            // Здесь должна быть AJAX-запрос к серверу
            fetch(`/menu/${itemId}/availability`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({
                    available: isAvailable
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(`Товар ${isAvailable ? 'доступен' : 'недоступен'}`, 'success');
                } else {
                    this.checked = !isAvailable;
                    showAlert('Ошибка при обновлении', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isAvailable;
                showAlert('Ошибка сети', 'danger');
            });
        });
    });
});