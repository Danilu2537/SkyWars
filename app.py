from flask import Flask, redirect, render_template, request, url_for

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, EnemyUnit, PlayerUnit

app = Flask(__name__)

heroes = {'player': BaseUnit, 'enemy': BaseUnit}

arena = Arena()


@app.route('/')
def menu_page():
    return render_template('index.html')


@app.route('/fight/')
def start_fight():
    arena.start_game()
    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit')
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        return render_template('fight.html', heroes=heroes)


@app.route('/fight/use-skill')
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        return render_template('fight.html', heroes=heroes)


@app.route('/fight/pass-turn')
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        return render_template('fight.html', heroes=heroes)


@app.route('/fight/end-fight')
def end_fight():
    arena.end_game()
    return render_template('index.html', heroes=heroes)


@app.route('/choose-hero/', methods=['post', 'get'])
def choose_hero():
    equipment = Equipment()
    if request.method == 'GET':
        result = {
            'header': 'Выберите героя',
            'classes': unit_classes,
            'weapons': equipment.get_weapons_names(),
            'armors': equipment.get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        arena.player = PlayerUnit(
            request.form['name'], unit_classes[request.form['unit_class']]
        )
        arena.player.equip_weapon(equipment.get_weapon(request.form['weapon']))
        arena.player.equip_armor(equipment.get_armor(request.form['armor']))
        heroes['player'] = arena.player
        return redirect(url_for('choose_enemy'))


@app.route('/choose-enemy/', methods=['post', 'get'])
def choose_enemy():
    equipment = Equipment()
    if request.method == 'GET':
        result = {
            'header': 'Выберите противника',
            'classes': unit_classes,
            'weapons': equipment.get_weapons_names(),
            'armors': equipment.get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        arena.enemy = EnemyUnit(
            request.form['name'], unit_classes[request.form['unit_class']]
        )
        arena.enemy.equip_weapon(equipment.get_weapon(request.form['weapon']))
        arena.enemy.equip_armor(equipment.get_armor(request.form['armor']))
        heroes['enemy'] = arena.enemy
        return redirect(url_for('start_fight'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
