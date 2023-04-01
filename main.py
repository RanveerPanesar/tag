@namespace
class SpriteKind:
    Text = SpriteKind.create()
    Ball = SpriteKind.create()
    Booth = SpriteKind.create()
    Mouse = SpriteKind.create()
    Crosshair = SpriteKind.create()
    Moon = SpriteKind.create()
    StatusBar = SpriteKind.create()
def checkIfWon():
    if len(sprites2) == 1:
        if sprites2[0] == mp.get_player_sprite(mp.PlayerNumber.ONE):
            game.splash("Player 1 Wins!")
        elif sprites2[0] == mp.get_player_sprite(mp.PlayerNumber.TWO):
            game.splash("Player 2 Wins!")
        elif sprites2[0] == mp.get_player_sprite(mp.PlayerNumber.THREE):
            game.splash("Player 3 Wins!")
        else:
            game.splash("Player 4 Wins!")
        game.reset()

def on_life_zero(player2):
    global it
    mp.get_player_sprite(player2).destroy(effects.fire, 500)
    sprites2.remove_at(sprites2.index(mp.get_player_sprite(player2)))
    if it == mp.get_player_sprite(player2):
        it.say_text("", 2000, False)
        it = sprites2._pick_random()
        youreIt()
    checkIfWon()
mp.on_life_zero(on_life_zero)

def youreIt():
    it.say_text("It", 2000, False)
    it.set_position(randint(5, 155), randint(15, 115))
    it.set_kind(SpriteKind.enemy)
    info.start_countdown(10)

def on_countdown_end():
    global it
    it.set_kind(SpriteKind.player)
    reduceLife(it)
    it = sprites2._pick_random()
    youreIt()
info.on_countdown_end(on_countdown_end)

def reduceLife(sprite: Sprite):
    if sprite == mp.get_player_sprite(mp.PlayerNumber.ONE):
        mp.change_player_state_by(mp.PlayerNumber.ONE, MultiplayerState.lives, -1)
    elif sprite == mp.get_player_sprite(mp.PlayerNumber.TWO):
        mp.change_player_state_by(mp.PlayerNumber.TWO, MultiplayerState.lives, -1)
    elif sprite == mp.get_player_sprite(mp.PlayerNumber.THREE):
        mp.change_player_state_by(mp.PlayerNumber.THREE, MultiplayerState.lives, -1)
    else:
        mp.change_player_state_by(mp.PlayerNumber.FOUR, MultiplayerState.lives, -1)

def on_on_overlap(sprite2, otherSprite):
    global it
    info.stop_countdown()
    it.say_text("", 2000, False)
    reduceLife(sprite2)
    it = sprite2
    otherSprite.set_kind(SpriteKind.player)
    youreIt()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

it: Sprite = None
sprites2: List[Sprite] = []
game.show_long_text("Once all your friends have joined, press \"A\" to continue.",
    DialogLayout.CENTER)
game.show_long_text("When you're it, tag a friend and they will lose a life. Be careful, if time runs out you'll lose a life instead!",
    DialogLayout.CENTER)
game.show_long_text("If you lose all of your lives, it is game over for you and and the other people in game continue.",
    DialogLayout.CENTER)
game.show_long_text("The Last man standing wins", DialogLayout.CENTER)
game.show_long_text("That is all I have to say so Good luck and Survive!",
    DialogLayout.CENTER)
sprites2 = [sprites.create(img("""
            2 2 2 2 2 2 2 2 
                2 2 2 1 1 2 2 2 
                2 2 2 2 1 2 2 2 
                2 2 2 2 1 2 2 2 
                2 2 2 2 1 2 2 2 
                2 2 2 2 1 2 2 2 
                2 2 1 1 1 1 1 2 
                2 2 2 2 2 2 2 2
        """),
        SpriteKind.player),
    sprites.create(img("""
            8 8 8 8 8 8 8 8 
                8 8 1 1 1 1 8 8 
                8 8 1 8 8 1 8 8 
                8 8 8 8 8 1 8 8 
                8 8 8 8 1 8 8 8 
                8 8 8 1 8 8 8 8 
                8 8 1 1 1 1 1 8 
                8 8 8 8 8 8 8 8
        """),
        SpriteKind.player),
    sprites.create(img("""
            4 4 4 4 4 4 4 4 
                4 4 1 1 1 1 4 4 
                4 4 1 4 4 1 4 4 
                4 4 4 4 4 1 4 4 
                4 4 4 4 1 4 4 4 
                4 4 1 4 4 1 4 4 
                4 4 1 1 1 1 4 4 
                4 4 4 4 4 4 4 4
        """),
        SpriteKind.player),
    sprites.create(img("""
            7 7 7 7 7 7 7 7 
                7 1 7 7 7 1 7 7 
                7 1 7 7 7 1 7 7 
                7 1 7 7 7 1 7 7 
                7 1 1 1 1 1 7 7 
                7 7 7 7 7 1 7 7 
                7 7 7 7 7 1 7 7 
                7 7 7 7 7 7 7 7
        """),
        SpriteKind.player)]
for value in mp.all_players():
    mp.set_player_sprite(value, sprites2[mp.player_to_index(value)])
    mp.move_with_buttons(value, mp.get_player_sprite(value))
    mp.get_player_sprite(value).set_stay_in_screen(True)
    mp.set_player_state(value, MultiplayerState.lives, 5)
mp.get_player_sprite(mp.PlayerNumber.ONE).set_position(5, 15)
mp.get_player_sprite(mp.PlayerNumber.TWO).set_position(155, 15)
mp.get_player_sprite(mp.PlayerNumber.THREE).set_position(5, 105)
mp.get_player_sprite(mp.PlayerNumber.FOUR).set_position(155, 105)
it = sprites2._pick_random()
youreIt()