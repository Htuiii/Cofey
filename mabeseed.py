from app import app, db
from app import Supplier, Ingredient, MenuItem, Recipe, Employee, Order, OrderItem
from sqlalchemy import text  # Добавляем импорт text


def reset_database():
    with app.app_context():
        try:
            # Отключаем проверку foreign keys (правильный синтаксис для SQLAlchemy)
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))
            db.session.commit()

            # Очищаем таблицы в правильном порядке
            tables = [
                OrderItem.__table__,
                Order.__table__,
                Recipe.__table__,
                Ingredient.__table__,
                MenuItem.__table__,
                Supplier.__table__,
                Employee.__table__
            ]

            for table in tables:
                db.session.execute(text(f'TRUNCATE TABLE {table.name}'))
                print(f"Таблица {table.name} очищена")

            # Включаем проверку foreign keys обратно
            db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
            db.session.commit()

            # Создаем таблицы заново
            db.create_all()
            print("\nБаза данных полностью очищена и таблицы пересозданы")

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при очистке базы данных: {str(e)}")
            raise


def seed_test_data():
    with app.app_context():
        try:
            # 1. Добавляем поставщиков
            suppliers = [
                {'company_name': 'Coffee Beans Co.', 'contact_person': 'Иван Петров',
                 'phone': '+79161112233', 'email': 'beans@coffee.com'},
                {'company_name': 'Fresh Milk Ltd.', 'contact_person': 'Мария Сидорова',
                 'phone': '+79162223344', 'email': 'milk@fresh.com'},
                {'company_name': 'Sweet Ingredients', 'contact_person': 'Алексей Козлов',
                 'phone': '+79163334455', 'email': 'sweet@ingred.com'}
            ]

            for data in suppliers:
                supplier = Supplier(**data)
                db.session.add(supplier)
            db.session.commit()
            print("Добавлены поставщики")

            # 2. Добавляем ингредиенты
            ingredients = [
                {'name': 'Арабика', 'quantity': 10.5, 'unit': 'кг', 'supplier_id': 1},
                {'name': 'Молоко', 'quantity': 25.0, 'unit': 'л', 'supplier_id': 2},
                {'name': 'Сахар', 'quantity': 15.0, 'unit': 'кг', 'supplier_id': 3},
                {'name': 'Шоколад', 'quantity': 5.0, 'unit': 'кг', 'supplier_id': 3}
            ]

            for data in ingredients:
                ingredient = Ingredient(**data)
                db.session.add(ingredient)
            db.session.commit()
            print("Добавлены ингредиенты")

            # 3. Добавляем товары меню
            menu_items = [
                {'name': 'Эспрессо', 'category': 'Кофе', 'price': 150,
                 'description': 'Крепкий черный кофе', 'is_available': True},
                {'name': 'Капучино', 'category': 'Кофе', 'price': 220,
                 'description': 'Кофе с молочной пенкой', 'is_available': True},
                {'name': 'Латте', 'category': 'Кофе', 'price': 240,
                 'description': 'Кофе с большим количеством молока', 'is_available': True},
                {'name': 'Горячий шоколад', 'category': 'Напиток', 'price': 200,
                 'description': 'Ароматный горячий шоколад', 'is_available': True}
            ]

            for data in menu_items:
                menu_item = MenuItem(**data)
                db.session.add(menu_item)
            db.session.commit()
            print("Добавлены товары меню")

            # 4. Добавляем рецепты (убедимся, что товары и ингредиенты существуют)
            espresso = MenuItem.query.filter_by(name='Эспрессо').first()
            cappuccino = MenuItem.query.filter_by(name='Капучино').first()
            latte = MenuItem.query.filter_by(name='Латте').first()
            chocolate = MenuItem.query.filter_by(name='Горячий шоколад').first()

            coffee = Ingredient.query.filter_by(name='Арабика').first()
            milk = Ingredient.query.filter_by(name='Молоко').first()
            sugar = Ingredient.query.filter_by(name='Сахар').first()
            choco = Ingredient.query.filter_by(name='Шоколад').first()

            recipes = [
                {'item_id': espresso.item_id, 'ingredient_id': coffee.ingredient_id,
                 'quantity': 0.02, 'unit': 'кг'},
                {'item_id': cappuccino.item_id, 'ingredient_id': coffee.ingredient_id,
                 'quantity': 0.02, 'unit': 'кг'},
                {'item_id': cappuccino.item_id, 'ingredient_id': milk.ingredient_id,
                 'quantity': 0.15, 'unit': 'л'},
                {'item_id': latte.item_id, 'ingredient_id': coffee.ingredient_id,
                 'quantity': 0.02, 'unit': 'кг'},
                {'item_id': latte.item_id, 'ingredient_id': milk.ingredient_id,
                 'quantity': 0.2, 'unit': 'л'},
                {'item_id': chocolate.item_id, 'ingredient_id': choco.ingredient_id,
                 'quantity': 0.1, 'unit': 'кг'}
            ]

            for data in recipes:
                recipe = Recipe(**data)
                db.session.add(recipe)
            db.session.commit()
            print("Добавлены рецепты")

            # 5. Добавляем сотрудников
            employees = [
                {'first_name': 'Анна', 'last_name': 'Иванова', 'position': 'Бариста',
                 'phone': '+79165556677', 'email': 'anna@coffee.ru', 'hire_date': '2023-01-10', 'salary': 45000},
                {'first_name': 'Дмитрий', 'last_name': 'Смирнов', 'position': 'Менеджер',
                 'phone': '+79167778899', 'email': 'dmitry@coffee.ru', 'hire_date': '2022-11-15', 'salary': 60000}
            ]

            for data in employees:
                employee = Employee(**data)
                db.session.add(employee)
            db.session.commit()
            print("Добавлены сотрудники")

            print("\nТестовые данные успешно добавлены!")

        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при добавлении тестовых данных: {str(e)}")
            raise


if __name__ == '__main__':
    reset_database()
    seed_test_data()