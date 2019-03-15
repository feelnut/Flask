from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Форма авторизации"""
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Форма регистрации"""
    user_name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Email адрес', validators=[DataRequired(), Email()])
    password_hash = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired()])
    accept = BooleanField('Да здравствует торговля!', validators=[DataRequired()])
    submit = SubmitField('Создать аккаунт')

class SearchPriceForm(FlaskForm):
    """Форма поиска по цене"""
    start_price = IntegerField('Минимальная цена', validators=[DataRequired()], default=75)
    end_price = IntegerField('Максимальная цена', validators=[DataRequired()], default=150)
    submit = SubmitField('Поиск')

class SearchLaryokForm(FlaskForm):
    laryok_id = SelectField('Номер ларька', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Поиск')

class AddLaryokForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Добавить ларёк')

class AddFruitForm(FlaskForm):
    sort = StringField('Сорт', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    number = IntegerField('Количество', validators=[DataRequired()])
    laryok_id = SelectField('Название ларька', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить продукт')

class ZakazFruitForm(FlaskForm):
    num = IntegerField('Количество', validators=[DataRequired()], default=1)
    submit = SubmitField('Заказать')

class BuyFruitForm(FlaskForm):
    num = IntegerField('Количество', validators=[DataRequired()], default=1)
    submit = SubmitField('Купить')