from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from Models import UsersModel, Laryok_Tadzhika, FruitModel
from forms import LoginForm, RegisterForm, SearchPriceForm, SearchLaryokForm, AddLaryokForm, AddFruitForm, \
    ZakazFruitForm, BuyFruitForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tadzhik'
db = DB()
UsersModel(db.get_connection()).init_table()
Laryok_Tadzhika(db.get_connection()).init_table()
FruitModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    # Основная страница авторизованного пользователя
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'tadzhik':
        return render_template('index_for_tadzhik.html', username=session['username'])
    fruits = FruitModel(db.get_connection()).get_all()
    return render_template('fruits_for_user.html', username=session['username'], title='Все товары', fruits=fruits)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Страница для авторизации
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    # Страница для выхода
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Страница регистрации
    form = RegisterForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    # Страница пользователя с сортировкой по цене
    form = SearchPriceForm()
    if form.validate_on_submit():
        fruits = FruitModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        return render_template('fruits_for_user.html', username=session['username'], title='Просмотр базы',
                               fruits=fruits)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_laryok', methods=['GET', 'POST'])
def search_laryok():
    # Страница пользователя с сортировкой по ларькам
    form = SearchLaryokForm()
    vse_larki = [(i[0], i[1]) for i in Laryok_Tadzhika(db.get_connection()).get_all()]
    form.laryok_id.choices = vse_larki
    if form.validate_on_submit():
        fruits = FruitModel(db.get_connection()).get_by_laryok(form.laryok_id.data)
        return render_template('fruits_for_user.html', username=session['username'], title='Просмотр базы',
                               fruits=fruits)
    return render_template("search_laryok.html", title='Подбор по ларьку', form=form)


@app.route('/fruit/<int:fruit_id>', methods=['GET'])
def fruit(fruit_id):
    # Страница для просмотра одного товара. В зависимости от вида пользователя
    # подгружается разная информация
    if 'username' not in session:
        return redirect('/login')
    fruit = FruitModel(db.get_connection()).get(fruit_id)
    laryok = Laryok_Tadzhika(db.get_connection()).get(fruit[4])
    if session['username'] != 'tadzhik':
        return render_template('fruit_info.html',
                               username=session['username'],
                               title='Просмотр продукта',
                               fruit=fruit,
                               laryok=laryok)
    else:
        return render_template('fruit_info_tadzhik.html',
                               username=session['username'],
                               title='Просмотр продукта',
                               fruit=fruit,
                               laryok=laryok)


@app.route('/laryok/<int:laryok_id>', methods=['GET'])
def laryok(laryok_id):
    # Информация о ларьке(Аналогично сортировке по ларькам)
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'tadzhik':
        return redirect(url_for('index'))
    laryok = Laryok_Tadzhika(db.get_connection()).get(laryok_id)
    fruits = FruitModel(db.get_connection()).get_all()
    return render_template('laryok_info.html',
                           username=session['username'],
                           title='Просмотр информации о ларьке',
                           laryok=laryok, fruits=fruits)


@app.route('/laryok_tadzhik', methods=['GET'])
def laryok_tadzhik():
    # Страница администратора, отображающая информацию о ларьке
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'tadzhik':
        flash('Доступ запрещен')
        redirect('index')
    larki = Laryok_Tadzhika(db.get_connection()).get_all()
    return render_template('larki_tadzhik.html',
                           username=session['username'],
                           title='Просмотр ларьков',
                           larki=larki)


@app.route('/add_laryok', methods=['GET', 'POST'])
def add_laryok():
    # Добавление ларька(Только для администратора)
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'tadzhik':
        form = AddLaryokForm()
        if form.validate_on_submit():
            larki = Laryok_Tadzhika(db.get_connection())
            try:
                larki.insert(name=form.name.data, address=form.address.data)
            except Exception:
                return render_template("Error.html", title='Ошибка')
            return redirect(url_for('index'))
        return render_template("add_laryok.html", title='Добавление ларька', form=form)


@app.route('/del_laryok/<int:laryok_id>', methods=['GET'])
def del_laryok(laryok_id):
    # Удаление ларька
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'tadzhik':
        larki = Laryok_Tadzhika(db.get_connection())
        larki.delete(laryok_id)
        fruits = FruitModel(db.get_connection())
        fruits.get_delete_by_laryok(laryok_id)
        return redirect(url_for('laryok_tadzhik'))
    else:
        return redirect(url_for('index'))


@app.route('/fruit_tadzhik', methods=['GET'])
def fruit_tadzhik():
    # Отображение продукта для администратора
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'tadzhik':
        flash('Доступ запрещен')
        redirect('index')
    fruits = FruitModel(db.get_connection()).get_all()
    return render_template('fruit_tadzhik.html',
                           username=session['username'],
                           title='Просмотр продуктов',
                           fruits=fruits)


@app.route('/add_fruit', methods=['GET', 'POST'])
def add_fruit():
    # Добавление продукта администратором
    if 'username' not in session:
        return redirect('login')
    if session['username'] != 'tadzhik':
        return redirect('index')
    form = AddFruitForm()
    vse_larki = [(i[0], i[1]) for i in Laryok_Tadzhika(db.get_connection()).get_all()]
    form.laryok_id.choices = vse_larki
    if form.validate_on_submit():
        fruits = FruitModel(db.get_connection())
        fruits.insert(sort=form.sort.data,
                      price=form.price.data,
                      number=form.number.data,
                      laryok=form.laryok_id.data)
        return redirect(url_for('fruit_tadzhik'))
    return render_template("add_fruit.html", title='Добавление продукта', form=form)


@app.route('/fruit_buy_tadzhik/<int:fruit_id>', methods=['GET', 'POST'])
def fruit_buy_tadzhik(fruit_id):
    # Заказ продуктов адмнистратором
    if 'username' not in session:
        return redirect('login')
    if session['username'] != 'tadzhik':
        return redirect('index')
    form = ZakazFruitForm()
    if form.validate_on_submit():
        fruits = FruitModel(db.get_connection())
        fruits.update_buy(num=form.num.data, fruit_id=fruit_id)
        return redirect(url_for('fruit_tadzhik'))
    return render_template("zakaz_productov.html", title='Заказ продуктов', form=form)


@app.route('/fruit_buy/<int:fruit_id>', methods=['GET', 'POST'])
def fruit_buy(fruit_id):
    # Покупка продуктов пользователем
    if 'username' not in session:
        return redirect('login')
    form = BuyFruitForm()
    if form.validate_on_submit():
        fruits = FruitModel(db.get_connection())
        f = fruits.update_sell(num=form.num.data, fruit_id=fruit_id)
        if f:
            return redirect(url_for('index'))
        else:
            return render_template("Error.html", title='Ошибка')
    return render_template("sell_productov.html", title='Покупка продуктов', form=form)


@app.route('/del_fruit/<int:fruit_id>', methods=['GET'])
def del_fruit(fruit_id):
    # Снятие продукта с продажи
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'tadzhik':
        fruits = FruitModel(db.get_connection())
        fruits.delete(fruit_id)
        return redirect(url_for('fruit_tadzhik'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
