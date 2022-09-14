from flask import Flask, render_template, request, redirect, url_for

from app.functions_classes import equipment
from app.functions_classes.base import Arena
from app.functions_classes.classes import unit_classes, UnitClass
from app.functions_classes.equipment import Equipment
from app.functions_classes.unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": PlayerUnit,
    "enemy": EnemyUnit
}

arena = Arena()  # инициализация класса арены


@app.route("/")
def menu_page():
    # главное меню
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    # рендер экрана боя
    result = arena.start_game(player=heroes["player"], enemy=heroes['enemy'])
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/hit")
def hit():
    # нанесение удара
    result = arena.player_attack()
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    # использование скилла
    result = arena.player_use_skill()
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # пропуск хода
    result = arena.next_turn()
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # завершение игры
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # выбор героя
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": 'Выбор героя для игрока',
            "classes": unit_classes,
            "weapons": equipment.get_weapon_names(),
            "armors": equipment.get_armor_names()
        }

        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        equipment = Equipment()
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon = equipment.get_weapon(request.form.get('weapon'))
        armor = equipment.get_armor(request.form.get('armor'))

        # создаем героя
        player_unit = PlayerUnit(name=user_name, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes['player'] = player_unit

        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # выбор соперника
    if request.method == 'GET':
        equipment = Equipment()
        result = {
            "header": 'Выбор героя для врага',
            "classes": unit_classes,
            "weapons": equipment.get_weapon_names(),
            "armors": equipment.get_armor_names()
        }

        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        # получаем из данных
        equipment = Equipment()
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon = equipment.get_weapon(request.form.get('weapon'))
        armor = equipment.get_armor(request.form.get('armor'))

        # создание врага
        enemy_unit = EnemyUnit(name=user_name, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes['enemy'] = enemy_unit

        return redirect(url_for('start_fight', _external=True))


if __name__ == "__main__":
    app.run()
