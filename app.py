from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from models import db, Employee, Supplier, Ingredient, MenuItem, Recipe, Order, OrderItem, OrderStatus, func
from datetime import datetime
import locale

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://100neroot:Lone23wow13vip@localhost/coffee_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


@app.template_filter('currency')
def currency_filter(value):
    return f"{value:.2f} ₽"


@app.route('/')
def dashboard():
    today = datetime.today()

    # Статистика
    today_orders = Order.query.filter(
        db.func.date(Order.order_date) == today.date()
    ).count()

    today_revenue = db.session.query(
        db.func.sum(Order.total_amount)
    ).filter(
        db.func.date(Order.order_date) == today.date()
    ).scalar() or 0

    total_items = MenuItem.query.count()

    # Последние заказы
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()

    # Популярные товары (исправленный запрос)
    popular_items = db.session.query(
        MenuItem.name.label('name'),
        db.func.sum(OrderItem.quantity).label('count')
    ).join(
        OrderItem, MenuItem.item_id == OrderItem.item_id
    ).group_by(
        MenuItem.name
    ).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).limit(5).all()

    return render_template('dashboard.html',
                           today_orders=today_orders,
                           today_revenue=today_revenue,
                           total_items=total_items,
                           recent_orders=recent_orders,
                           popular_items=popular_items)
@app.route('/menu')
def menu():
    items = MenuItem.query.all()
    return render_template('menu.html', items=items)


@app.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        item = MenuItem(
            name=request.form['name'],
            category=request.form['category'],
            price=float(request.form['price']),
            description=request.form['description'],
            is_available='is_available' in request.form
        )
        db.session.add(item)
        db.session.commit()
        flash('Товар добавлен в меню!', 'success')
        return redirect(url_for('menu'))
    return render_template('add_menu_item.html')


@app.route('/menu/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.category = request.form['category']
        item.price = float(request.form['price'])
        item.description = request.form['description']
        item.is_available = 'is_available' in request.form
        db.session.commit()
        flash('Товар успешно обновлен!', 'success')
        return redirect(url_for('menu'))
    return render_template('edit_menu_item.html', item=item)


@app.route('/menu/<int:item_id>/delete', methods=['POST'])
def delete_menu_item(item_id):
    try:
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Товар удален'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/orders')
def orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('orders.html', orders=orders)


@app.route('/order/<int:order_id>')
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('view_order.html', order=order)


@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        try:
            employee_id = request.form['employee_id']
            payment_method = request.form['payment_method']
            item_ids = request.form.getlist('item_id')
            quantities = request.form.getlist('quantity')

            total = 0
            order_items = []

            for item_id, quantity in zip(item_ids, quantities):
                menu_item = MenuItem.query.get(item_id)
                if menu_item and int(quantity) > 0:
                    total += menu_item.price * int(quantity)
                    order_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'unit_price': menu_item.price
                    })

            order = Order(
                employee_id=employee_id,
                total_amount=total,
                payment_method=payment_method,
                status=OrderStatus.COMPLETED
            )
            db.session.add(order)
            db.session.flush()

            for item in order_items:
                db.session.add(OrderItem(
                    order_id=order.order_id,
                    item_id=item['item_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                ))

            db.session.commit()
            flash('Заказ успешно создан!', 'success')
            return redirect(url_for('orders'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')
            return redirect(url_for('create_order'))

    employees = Employee.query.all()
    menu_items = MenuItem.query.filter_by(is_available=True).all()
    return render_template('create_order.html',
                           employees=employees,
                           menu_items=menu_items)


@app.route('/order/<int:order_id>/update_status', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    try:
        new_status = request.form['status'].upper()  # Приводим к верхнему регистру
        order.status = OrderStatus[new_status]  # Преобразуем строку в enum
        db.session.commit()
        flash('Статус заказа обновлён!', 'success')
    except (KeyError, ValueError) as e:
        db.session.rollback()
        flash(f'Ошибка: неверный статус "{new_status}"', 'danger')
    return redirect(url_for('view_order', order_id=order_id))

@app.route('/inventory')
def inventory():
    ingredients = db.session.query(Ingredient, Supplier.company_name) \
        .join(Supplier).all()
    return render_template('inventory.html', ingredients=ingredients)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)