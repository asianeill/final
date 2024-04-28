# The script of the game goes in this file.

#characters
define d = Character("Detective Beaver", color= "#f7e1a5")
define r = Character("Rodrick Rabbit", color= "#C40000")
define p = Character("Priscilla Pig", color= "#9100A7")
define b = Character("Blarf", color= "#036B00")
define c = Character("Clarice Cat", color= "#FF3399")
define y = Character("You", color= "#ffffff")
define k = Character("The Coca-Koala", color= "#7d94e1")

#transitions
define dissolve = Dissolve(0.01)


#for paper puzzle
default page_pieces = 12
default full_page_size = (711, 996)
default piece_coordinates = [(451, 149), (719, 139), (868, 238), (421, 399), (658, 318), (700, 488), (796, 538), (453, 718), (776, 773), (464, 925), (743, 958), (921, 888)]
default initial_piece_coordinates = []
default finished_pieces = 0
define secondTry = False

init python:
    def setup_puzzle():
        for i in range(page_pieces):
            start_x = 1200
            start_y = 200
            end_x = 1700
            end_y = 800
            rand_loc = (renpy.random.randint(start_x, end_x), renpy.random.randint(start_y, end_y))
            initial_piece_coordinates.append(rand_loc)

    def piece_drop(dropped_on, dragged_piece):
        global finished_pieces

        if dragged_piece[0].drag_name == dropped_on.drag_name:
            dragged_piece[0].snap(dropped_on.x, dropped_on.y)
            dragged_piece[0].draggable = False
            finished_pieces += 1

            if finished_pieces == page_pieces:
                renpy.jump("reassemble_complete")

screen reassemble_puzzle:
    image "background.png"
    frame:
        background "puzzle-frame.png"
        xysize full_page_size
        anchor(0.5, 0.5)
        pos(650, 535)
    
    draggroup:
        for i in range(page_pieces):
            drag:
                drag_name i
                pos initial_piece_coordinates[i]
                anchor(0.5, 0.5)
                focus_mask True
                drag_raise True
                image "Pieces/piece-%s.png" % (i + 1)

        for i in range(page_pieces):
            drag:
                drag_name i
                draggable False
                droppable True
                dropped piece_drop
                pos piece_coordinates[i]
                anchor(0.5, 0.5)
                focus_mask True
                image "Pieces/piece-%s.png" % (i + 1) alpha 0.0

#for safe puzzle
init python:
    import math
    def dial_events(event, x, y, st):
        global dial_rotate
        global old_mousepos
        global old_degrees
        global degrees
        global dial_start_rotate
        global dial_text
        global dial_number
        global previous_dial_text
        global dial_changed
        global combination_check
        global combination_length
        global completed_combination_numbers
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONDOWN:
            if event.button == 1:
                if dial_start_rotate:
                    if dial_sprite.x <= x <= dial_sprite.x + dial_size[0] + dial_offset and dial_sprite.y <= y <= dial_sprite.y + dial_size[1] + dial_offset:
                        dial_rotate = True
                        old_mousepos = (x, y)
                        angle_radians = math.atan2((dial_sprite.y + dial_size[1] - dial_offset / 2) - y, (dial_sprite.x + dial_size[0] - dial_offset / 2) - x)
                        old_degrees = math.degrees(angle_radians) % 360
                else:
                    if dial_sprite.x <= x <= dial_sprite.x + dial_size[0] and dial_sprite.y <= y <= dial_sprite.y + dial_size[1]:
                        dial_rotate = True
                        old_mousepos = (x, y)
                        angle_radians = math.atan2((dial_sprite.y + dial_size[1] / 2) - y, (dial_sprite.x + dial_size[0] / 2) - x)
                        old_degrees = math.degrees(angle_radians) % 360
            
        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                dial_rotate = False
                safe = "safe_{}".format(current_safe)
                if dial_changed:
                    if combination_length < 4:
                        dial_changed = False
                        combination_check = None
                        if len(completed_combination_numbers) == 0:
                            completed_combination_numbers[safe] = []
                            completed_combination_numbers[safe].append(dial_text)
                        else:
                            completed_combination_numbers[safe].append(dial_text)
                        combination_length += 1
                    if combination_length == 4:
                        if completed_combination_numbers[safe] == combinations[safe]:
                            dial_changed = False
                            combination_length = 0
                            completed_combination_numbers = {}
                            combination_check = "correct"
                            renpy.play("audio/success.ogg", "sound")
                        else:
                            dial_changed = False
                            combination_length = 0
                            completed_combination_numbers = {}
                            combination_check = "wrong"
                            renpy.play("audio/error.ogg", "sound")
                            renpy.jump("tryagain")
                renpy.restart_interaction()
        elif event.type == renpy.pygame_sdl2.MOUSEMOTION:
            if dial_rotate:
                angle_radians = math.atan2((dial_sprite.y + dial_size[1] / 2) - y, (dial_sprite.x + dial_size[0] / 2) - x)
                degrees = math.degrees(angle_radians) % 360
                rotate_amount = math.hypot(x - old_mousepos[0], y - old_mousepos[1]) / 5
                if degrees > old_degrees:
                    dial_sprite.rotate_amount += rotate_amount
                elif degrees < old_degrees:
                    dial_sprite.rotate_amount -= rotate_amount

                t = Transform(child = dial_image, zoom = 0.5)
                t.rotate = 3.6 * round(dial_sprite.rotate_amount / 3.6)
                if int(t.rotate / 3.6) % 100 == 0 and int(t.rotate / 3.6) != 0:
                    dial_number = 0
                    dial_sprite.rotate_amount = 0.0
                else:
                    dial_number = int(t.rotate / 3.6)

                if dial_number > 0:
                    dial_text = 100 - dial_number
                elif dial_number < 0:
                    dial_text = abs(dial_number)
                else:
                    dial_text = dial_number

                if dial_text != previous_dial_text:
                    dial_changed = True
                    renpy.music.play("audio/dial.ogg", "sound", relative_volume = 0.3)
                
                previous_dial_text = dial_text
                
                t.subpixel = True
                dial_start_rotate = True
                dial_sprite.set_child(t)
                dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2 - dial_offset
                dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2 - dial_offset
                old_degrees = math.degrees(angle_radians) % 360
                old_mousepos = (x, y)
                dial_sprite_manager.redraw(0)
                renpy.restart_interaction()

    def reset_safe():
        global dial_number
        global dial_text
        global completed_combination_numbers
        global combination_length
        global combination_check
        global dial_start_rotate

        dial_number = 0
        dial_text = 0
        dial_sprite.rotate_amount = 0
        completed_combination_numbers = {}
        combination_length = 0
        combination_check = None
        dial_start_rotate = False


        t = Transform(child = dial_image, zoom = 0.5)
        dial_sprite.set_child(t)
        dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
        dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
        dial_sprite_manager.redraw(0)

screen scene_1:
    image "images/scene-1-background1.png"
    imagebutton auto "images/scene-1-safe-door-%s.png" focus_mask True action [Show("safe_puzzle", Fade(1, 1, 1)), Hide("scene_1")] at half_size

screen safe_opened:
    on "show" action Hide("safe_puzzle")
    image "safe-opened-background.png" at half_size
    imagebutton auto "images/back-button-%s.png" action [Show("scene_1", Fade(1, 1, 1)), Hide("safe_opened")] align(0.98, 0.95) at half_size
    if current_safe == 1:
        imagebutton auto "gun-%s.png" focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Jump("getgun"),] at half_size
        

screen safe_puzzle:
    on "show" action Function(reset_safe)
    image "images/safe-closeup-background.png" at half_size
    if combination_check == "wrong":
        imagebutton auto "images/safe-handle-ind-red-%s.png" focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Play(file = "audio/locked-door.ogg", channel = "sound"), Jump("nogun"),] at half_size
    elif combination_check == "correct":
        imagebutton auto "images/safe-handle-ind-green-%s.png" focus_mask True action [Play(file = "audio/open-door.ogg", channel = "sound"), Show("safe_opened", Fade(1, 1, 1))] at half_size
    elif combination_check == None:
        imagebutton auto "images/safe-handle-ind-normal-%s.png" focus_mask True action Play(file = "audio/locked-door.ogg", channel = "sound") at half_size
   
    image "images/dial-shadow.png" align(0.48, 0.5) alpha 0.3 at half_size
    image "images/dial-backing.png" align(0.5, 0.5) at half_size
    add dial_sprite_manager
    imagebutton auto "images/dial-reset-button-%s.png" align(0.5, 0.5) focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Jump("reset")] at half_size    
    image "images/dial-text-background.png" align(0.5, 0.17) at half_size
    imagebutton auto "images/back-button-%s.png" align(0.95, 0.95) action [Show("scene_1"), Hide("safe_puzzle")] at half_size
    text "[dial_text]" color "#000000" align(0.505, 0.18) text_align 0.5

transform half_size:
    zoom 0.5


#game starts here
label start:
    #images that needed adjustmends
    image beaver right:
        "beaver right.png"
        zoom 1
    image beaver left large:
        "beaver left large.png"
        zoom 2
    image beaver angry left:
        "beaver angry left.png"
        zoom 1
    image beaver squint left:
        "beaver squint left.png"
        zoom 1
    image duck happy right:
        "duck happy right.png"
        zoom 0.50
    image duck dead side:
        "duck dead side.png"
        zoom 0.50
    image frog side eye left:
        "frog side eye left.png"
        zoom 0.70
    image frog left:
        "frog left.png"
        zoom 0.70
    image frog right:
        "frog right.png"
        zoom 0.70
    image frog side eye right:
        "frog side eye right.png"
        zoom 0.70
    image frog crack left:
        "frog crack left.png"
        zoom 0.70
    image frog crack right:
        "frog crack right.png"
        zoom 0.70
    image frog squint left:
        "frog squint left.png"
        zoom 0.70
    image frog squint right:
        "frog crack left.png"
        zoom 0.70
    image frogdark:
        "frogdark.png"
        zoom 0.70
    image coke:
        "coke.png"
        zoom 1.5
    image koala right:
        "koala right.png"
        zoom 0.80
    image koala left:
        "koala left.png"
        zoom 0.80
    image koala angry left:
        "koala angry left.png"
        zoom 0.80
    image koala angry right:
        "koala angry right.png"
        zoom 0.80
    image koala happy left:
        "koala happy left.png"
        zoom 0.80
    image koala happy right:
        "koala happy right.png"
        zoom 0.80
    image koala gun left:
        "koala gun left.png"
        zoom 0.80
    image koala gun right:
        "koala gun right.png"
        zoom 0.80
    image koala shot:
        "koala shot.png"
        zoom 0.80
    image koala shot2:
        "koala shot2.png"
        zoom 0.80
    image koala shot3:
        "koala shot3.png"
        zoom 0.80
    image koala shot4:
        "koala shot4.png"
        zoom 0.80
    image koala shot5:
        "koala shot5.png"
        zoom 0.80
    image koala shot6:
        "koala shot6.png"
        zoom 0.80
    image koala shot7:
        "koala shot7.png"
        zoom 0.80
    image koala2 right:
        "koala2 right.png"
        zoom 0.90
    
    
    play music "openingmusic.mp3"
    scene village
    with fade
    show beaver right at right
    d "The streets of Pigglydelphia are full of crime."
    show beaver left at right
    d "Luckily, I eat crime for breakfast."
    d "So it's your first case, eh?"
    show beaver angry left at right
    d "I didn't realize the agency was sending me a rookie."
    show beaver angry left at right
    d "You can call me Detective Beaver." 
    show beaver squint left at right
    d "Don't tell me your name.\nMost of my partners don't last more than a day."

    scene house
    with fade

    
    show beaver left at offscreenright
    show beaver left at right with move

    d "This is the scene of the crime.\nThe headquarters of Coca-Koala."

    show duck happy right at offscreenright
    show frog left at offscreenleft
    show pig left at offscreenleft
    show rabbit right at offscreenright

    d "There were five people in the building on Saturday."

    scene messyoffice with dissolve

    show cat right at center with move
    d "Clarice Cat"
    define slightright = Position(xpos=0.55)
    define slightlyright = Position(xpos=0.65)
    show duck happy right at slightlyright with move
    d "Dillworth Duck."
    define slightleft = Position(xpos=0.45)
    define slightlyleft = Position(xpos=0.30)
    show pig left at slightleftnew with move
    d "Priscilla Pig."
    define moreright = Position(xpos=0.75)
    define veryright = Position(xpos=0.85)
    show rabbit right at veryright with move
    d "Rodrick Rabbit."
    define moreleft = Position(xpos=0.25)
    show frog left at moreleftnew with move
    d "and Blarf."
    d "They claim to have had an office dinner party."
    d "But that evening..."
    
    pause (2.0)
    hide cat right
    hide pig left
    hide duck happy right
    hide frog left
    hide rabbit right
    show cat mad right at center
    define slightleftnew = Position(xpos=0.30)
    show pig mad left at slightleftnew
    define moreleftnew = Position(xpos=0.15)
    show frog side eye left at moreleftnew
    show rabbit mad right at veryright
    define deadduck = Position(xpos=0.85)
    show duck dead side at deadduck
    with hpunch

    d "Dillworth Duck was murdered."
    
    scene house
    with fade

    show beaver angry right at right
    d "One of those four killed that Duck."
    hide beaver angry right
    show beaver right at right
    d "I've gathered them all for questioning."
    d "Think you can crack the case?"
menu:
    "Yes":
        jump yes
    "No":
        jump no

label yes:
    hide beaver right
    show beaver squint right at right
    d "Good. Let's begin questioning."
    jump part2

label no:
    hide beaver right
    show beaver angry right at right
    d "That's the spirit..."
    jump part2

label part2:
    show beaver left at right
    d "We'll question Clarice first."

    scene boardroom
    with fade

    show cat happy right at right
    show beaver right at left with moveinleft
    d "Clarice, take us through what happened on Saturday."
    c "Well, my dearest coworkers met for dinner."
    c "As we do some Saturdays..."
    show cat left at right
    c "We dined. We drank. Didn't do much."
    show beaver squint right at left
    c "Then, we go to get our coats from the closet..."
    show cat mad left at right
    c "And return to find the dang duck dead!"
    show beaver right at left
    d "Do you remember any details?"
    show cat happy right at right
    c "As I said, we dined. We drank. Didn't do much."
    show beaver left at left
    d "Huh. Wanna ask a question, rookie?"

menu:
    "Who do you think killed Dillworth?":
        jump whoismurderercat
    "What did you all eat?":
        jump whatdidyoueatcat
    "No further questions.":
        jump nofurtherquestionscat

label whatdidyoueatcat:
    d "Really? What kind of question is that?"
    show cat left at right
    c "...Fish."
    
menu:
    "Who do you think is the murderer?":
        jump whoismurderercat
    "No further questions.":
        jump nofurtherquestionscat

label whoismurderercat:
    c "Blarf."

menu:
    "Why Blarf?":
        jump whyblarf
    "What did you eat?":
        jump whatdidyoueatcat
    "No further questions.":
        jump nofurtherquestionscat

label whyblarf:
    c "Bit of a Blarf thing to do."

menu:
    "What did you eat?":
        jump whatdidyoueatcat
    "No further questions.":
        jump nofurtherquestionscat
    
label nofurtherquestionscat:
    show cat mad left at right
    c "Well, this has been a waste."
    c "We're Dillworth's dearest friends, detectives.\nNo one wanted that duck dead."
    jump part3

label part3:
    scene house
    with fade
    show beaver squint left at right with moveinright
    d "That was strange."
    d "I think before we question anyone else,\nwe should view the security footage."

    scene messyoffice
    with dissolve
    show beaver angry right at center with moveinbottom
    d "This is where Dillworth was shot."
    show beaver right at center
    d "The security cameras are old.\nSo the footage cuts out for large spans of the day."
    d "It cut out from 5-7, but luckily\nit looks like it started up right before everyone left."
    jump securityfootage
label securityfootage:
    $ renpy.movie_cutscene("images/security.webm")
    scene messyoffice
    show beaver angry right at center
    d "Rats. That's not helpful."
    d "The technology in this building is so old.\nI can't even get a signal."
    show rabbit left at right with moveinright
    d "Rodrick Rabbit, is it?"
    show rabbit happy left at right
    r "My friends call me Rod."
    show rabbit left at right
    show beaver angry right at center
    d "Let's cut to the chase. We know it was you."
    show rabbit mad left at right
    r "W-what? I'm an honorable business man!"
    show beaver squint right at center
    d "I'll be honest, rookie, I don't know where I'm going with this."

menu:
    "Are you a real detective?":
        jump areyouareal
    "Who do you think the murderer is?":
        jump whoismurdererrabbit
    "Did you hear the gunshot?":
        jump heardshotrabbit
    "How long had you known Dillworth?":
        jump knowdillworthrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label areyouareal:
    show beaver angry right at center
    d "How DARE you?!?"
    show beaver angry left at center
    d "I graduated my online program six months ago!"
    show beaver angry right at center
    d "Sure, they don't trust me with a gun..."
    d "but I studied under the Wonder Pets!"

menu:
    "Who do you think the murderer is?":
        jump whoismurdererrabbit
    "Did you hear the gunshot?":
        jump heardshotrabbit
    "How long had you known Dillworth?":
        jump knowdillworthrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label whoismurdererrabbit:
    show beaver right at center
    show rabbit happy left at right
    r "Probably Blarf."
    show rabbit left at right
    d "Huh. Why do you think that?"
    r "Blarf has a temper.\nHe and Dillworth also argue a lot."

menu:
    "Are you a real detective?":
        jump areyouareal
    "Did you hear the gunshot?":
        jump heardshotrabbit
    "How long had you known Dillworth?":
        jump knowdillworthrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label knowdillworthrabbit:
    show rabbit left at right
    r "We've worked together at Coca-Koala since 1999."
    show rabbit happy left at right
    r "It's the best drink money can buy! You want some?"
    show beaver squint right at center
    d "Ooo yes! I love Coca-Koala!"
    show beaver coke right at center
    define drinkcoke = Position(xpos=0.15, ypos=0.63)
    show coke at drinkcoke
    show rabbit left at right
    d "Man... this tastes...\nnot as good as it used to."
    d "Anyways, what was his job?"
    r "He was Director of Transportation\n I'm the Chief Marketing Officer. We were good, good pals."
    hide coke
    show beaver right at center

menu:
    "Are you a real detective?":
        jump areyouareal
    "Who do you think the murderer is?":
        jump whoismurdererrabbit
    "Did you hear the gunshot?":
        jump heardshotrabbit
    "What did you eat for dinner that night?":
        jump whatdidyoueatrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label whatdidyoueatrabbit:
    show rabbit happy left at right
    r "Carrots."
    show rabbit left at right
menu:
    "Are you a real detective?":
        jump areyouareal
    "Who do you think the murderer is?":
        jump whoismurdererrabbit
    "Did you hear the gunshot?":
        jump heardshotrabbit
    "How long had you known Dillworth?":
        jump knowdillworthrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label heardshotrabbit:
    r "I heard it, yes."
    r "We have a loud factory downstairs.\nI assumed it was a machine."
menu:
    "Are you a real detective?":
        jump areyouareal
    "Who do you think the murderer is?":
        jump whoismurdererrabbit
    "How long had you known Dillworth?":
        jump knowdillworthrabbit
    "No further questions.":
        jump nofurtherquestionsrabbit

label nofurtherquestionsrabbit:
    r "I don't think you'll find anything here.\nNot worth spending any more of your time! Heh."
    jump part4

label part4:
    scene house
    with fade
    show noteonground
    show beaver sick left at right with moveinright
    d "Seriously, Coca-Koala has changed.\nThat was NASTY!"
    d "Anyways, who should we question next?"

menu:
    "You don't look so good...":
        jump sickbeaver
    "What's that on the ground?":
        jump whatsthat

label sickbeaver:
    show beaver sick left at right
    d "Yeah, I don't feel too good. I shouldn't have ate\nChick-fil-a before work. I swear they put crack in their sauce."
    d "Wow, I feel light-headed.\nGimme a minute; I'll be back."
    show beaver sick right at right
    hide beaver sick right with moveoutright 

menu:
    "What's that on the ground?":
        jump whatsthat2
    "Ignore the thing that is obviously evidence":
        jump beaverback1


label whatsthat:
    y "Looks like a note."
    hide noteonground
    show note
    pause (3.0)
    hide note
    y "He knows...Dillworth must've known something about Blarf."
    d "I'll be back rookie, I think I'm gonna blarf."
    show beaver sick right at right
    hide beaver sick right with moveoutright 
    pause (2.0)
    jump beaverback2

label whatsthat2:
    y "Looks like a note."
    hide noteonground
    show note
    pause (3.0)
    hide note
    y "He knows...Dillworth must've known something about Blarf."
    y "Or what if this is recent.\nMaybe Blarf is going to take out Detective Beaver!"
    y "I better go check on him..."
    jump beaverback1


label beaverback1:
    show beaver left at right with moveinright
    d "Geez, I just shit bricks!"
    show beaver squint left at right
    d "I felt like I was on death's door for a bit there."
    show beaver left at right
    d "Let's go question that pig."
    jump beforepig

label beaverback2:
    show beaver left at right with moveinright
    d "Wheeeeew, sorry about that."
    show beaver squint left at right
    d "I felt like I was on death's door for a bit there."
    show beaver left at right
    d "Let's go question Priscilla pig."
    jump beforepig

label beforepig:
    scene closeoffice
    with fade
    show beaver left at right with moveinright
    d "Huh. I was told Priscilla would be in here."
menu:
    "Let's go find her.":
        jump findpriscilla
    "Maybe we should look around.":
        jump lookforclues
label lookforclues:
    show beaver squint left at right
    d "I don't know...\nI feel guilty snooping."
    y "Aren't you a detective?"
    show beaver angry left at right
    d "Fine. Snoop all you want, rookie."
menu:
    "Search computer":
        jump searchcomputer
    "Search drawers":
        jump searchdrawers
    "Let's go find Priscilla.":
        jump findpriscilla

label searchcomputer:
    show email
    pause(3)
    y "It looks like Pupsi used\nto make Coca-Koala's drinks."
    show beaver squint left at right
    d "No way! I swear they taste different."
    hide email
menu:
    "Search drawers":
        jump searchdrawers
    "Let's go find Priscilla.":
        jump findpriscilla
label searchdrawers:
    y "Most of these are locked."
    show beaver left at center with move
    d "There's some trash in this drawer.\nJust crumpled up paper."
    show beaver right at center
    show duckposter
    y "Am I crazy?\nOr does this look like Dillworth."
    show beaver squint right at right with move
    d "Meh. Lots of ducks look similar."
    y "But why is this here?"
menu:
    "Search computer":
        jump searchcomputer
    "Let's go find Priscilla.":
        jump findpriscilla

label findpriscilla:
    show beaver left at right
    d "Good idea."
    jump questionpig
    
label questionpig:
    scene shipping
    with fade
    show pig happy left at moreright
    show rabbit happy right at slightright
    pause (1.0)
    show pig mad left at right
    show rabbit left at slightright
    show beaver right at left with moveinleft
    d "There you are Priscilla! Oh... and Rod."
    show pig mad left at right
    show rabbit mad right at slightright
    hide rabbit mad right with moveoutright
    d "I meant Rodrick..."
    p "Detective... you're still here?"
    show beaver squint right at left
    d "Yes, yes. Long day."
    show beaver right at left
    d "So Priscilla-"
    show pig left at right
    p "You two look parched.\nLemme get you some refreshing Coca-Koala!"
    show pig happy left at right
    d "Well, who am I to say no? Thanks!"
    y "...I'm good."
    show beaver coke right at left
    y "What's your job at Coca-Koala?"
    p "Community Affairs Manager."
    y "Does the community like having a big factory here?"
    show beaver sick right at left
    p "Of course, everyone likes Coca-Koala."
    show pig left at right
    p "You looking for a job?"
menu:
    "I have a job, thanks.":
        jump nothanks
    "I'm interested.":
        jump interested

label nothanks:
    show beaver sick left at left
    show pig mad left at right
    p "Right... How's that going? Find your culprit?"
    d "I'll be right back."
    hide beaver sick left with moveoutleft
    jump continuepig

label interested:
    show beaver sick left at left
    show pig happy left at right
    p "We're always looking for smart cookies like you to join us.\nYou can become a millionaire selling Coca-Koala."
    show pig left at right
    d "I'll be right back."
    hide beaver sick left with moveoutleft
    jump continuepig

label continuepig:
    show pig happy left at right
    p "I have business to attend to.\nCan you ask me your questions?"
menu:
    "Who do you think killed Dillworth?":
        jump pigwhokilled
    "Do you mind if I look around?":
        jump lookingaround
    "Is this where Coca-Koala is made?":
        jump madecoke
    "No further questions":
        jump noqspig
    
label madecoke:
    show pig happy left at right
    p "Yes! We make everything in house\nwith our special recipe."
    y "Your product tastes a lot like Pupsi."
    show pig mad left at right
    p "It tastes nothing like Pupsi."
menu:
    "Who do you think killed Dillworth?":
        jump pigwhokilled
    "Do you mind if I look around?":
        jump lookingaround
    "No further questions":
        jump noqspig

label lookingaround:
    show pig left at right
    p "There's a lot of dangerous machinery down here.\nYou need someone with training to show you around. Not me."
menu: 
    "Who do you think killed Dillworth?":
        jump pigwhokilled
    "Is this where Coca-Koala is made?":
        jump madecoke
    "Is this where Coca-Koala is made?":
        jump madecoke
    "What did you eat at the dinner party?":
        jump eatpig
    "No further questions":
        jump noqspig

label eatpig:
    show pig mad left at right
    p "Bacon."
    y "Oh?"
menu:
    "Who do you think killed Dillworth?":
        jump pigwhokilled
    "No further questions":
        jump noqspig

label pigwhokilled:
    show pig happy left at right
    "Oh, I know it was Blarf."
menu:
    "How do you know?":
        jump howdoyouknow
    "Everyone keeps saying that...":
        jump howdoyouknow2

label howdoyouknow:
    show pig left at right
    p "It's simple. Blarf was the last one in the room."
    show pig right at right
    p "The rest of us have alibis.\nI walked out with Clarice and Rodrick." 
menu: 
    "Do you mind if I look around?":
        jump lookingaround
    "Is this where Coca-Koala is made?":
        jump madecoke
    "No further questions":
        jump noqspig
    
label howdoyouknow2:
    show pig left at right
    p "Blarf has always been... a bit off."
    show pig mad left at right
    p "He and Dillworth would get in arguments often."
    show pig left at right
    p "Anyhow, the rest of us have alibis.\nI walked out with Clarice and Rodrick."
menu: 
    "Do you mind if I look around?":
        jump lookingaround
    "Is this where Coca-Koala is made?":
        jump madecoke
    "No further questions":
        jump noqspig

label noqspig:
    show pig happy right at right
    p "It's getting late, you really should\nstay away from the factory!"
    p "This basement is creepy. Weird noises!"
    hide pig happy right with moveoutright
    y "I wonder where Detective Beaver went."
    y "If I can't look around here,\nI should look somewhere else."

    scene puzzle desk
    with fade

    y "This room looks like it hasn't been used in years."
    y "This place is so weird,\nand everyone is acting strange."
    y "So far, I have to assume the killer is:"
menu:
    "Clarice":
        jump clar
    "Rodrick":
        jump rod
    "Priscilla":
        jump pris
    "Blarf":
        jump blar
    "Detective Beaver":
        jump beav
    
label beav:
    y "But I am a dumbass, so who knows."
    jump contoffice
label clar:
    y "She was just acting so weird."
    jump contoffice
label rod:
    y "I'm not convinced he left with Priscilla and Clarice."
    jump contoffice
label pris:
    y "I think she lied about her alibis."
    jump contoffice
label blar:
    y "Everyone said it was Blarf."
    y "Blarf and Dillworth were known to argue."
    y "Also, Priscilla said she walked out with the others."
    jump contoffice

label contoffice:
    y "I think at this point, it's\nentirely plausable that no dinner party took place."
    y "Everyone said they ate something different.\nAnd there's no security footage."
    show frog crack left at right with moveinright
    b "BLARF!"
    show frog squint left at right
    b "Sorry, I didn't realize anyone was in here."
    show frog crack left at right
menu:
    "Blarf, I have some questions for you.":
        jump blarfquestion
    "Blarf, I know you did it.":
        jump blarfaccuse

label blarfaccuse:
    show frog squint left at right
    b "BLARF! I DIDN'T DO IT!\nI wouldn't hurt a fly!"
menu:
    "You just couldn't settle your arguement, huh?":
        jump blarfop1
    "You were the last one he saw!":
        jump blarfop2

label blarfop1:
    show frog crack left at right
    b "Dill was my only friend here.\nI swear it wasn't me!"
    b "We argued... but not about... BLARF!"
    show frog squint left at right
    b "I'd tell you if I could..."
    jump tellmeblarf

label blarfop2:
    show frog crack left at right
    b "Dill was my only friend here.\nWe only spoke to each other."
    show frog squint left at right
    b "That night, before he was shot...\nI was trying to...BLARF!"
    show frog squint right at right
    b "I'd tell you if I could..."
    jump tellmeblarf

label tellmeblarf:
    y "If you don't tell me, you are going to get blamed."
    show frog squint left at right
    b "He'll know..."
    y "Who??"
    jump confessblarf

label blarfquestion:
menu:
    "What did you and Dillworth argue about?":
        jump blarfop3
    "Do you have any alibis?":
        jump blarfop4
label blarfop3:
    show frog crack left at right
    b "We... had a disagreement about the future."
    y "About Coca-Koala?"
    show frog squint right at right
    b "Yeah..."
    jump accuseblarf
label blarfop4:
    show frog squint left at right
    b "No...I know this looks bad. BLARF!"
    show frog squint right at right
    b "I ran out of that building as quick as I could..."
    jump accuseblarf
label accuseblarf:
menu: 
    "Why?":
        jump contblarfop41
    "So you killed him!":
        jump contblarfop42
label contblarfop41:
    show frog squint right at right
    b "BLARF! If I tell you, he'll know!"
    y "Who will know??"
    jump confessblarf
label contblarfop42:
    show frog squint left at right
    b "BLARF! I swear I didn't!"
    show frog crack left at right
    b "It was..."
    jump confessblarf

label confessblarf:
    show frog squint left at right
    b "I CAN'T TELL YOU!"
    show frog squint right at right
    b "This is bad...this is bad..."
    show frog crack left at right
menu:
    "Why are your eyes red?":
        jump eyesred
    "Threaten Blarf":
        jump threatenblarf
    "Be nice to Blarf":
        jump nicetoblarf

label eyesred:
    show frog crack right at right
    b "They...uh...are always like this."
menu:
    "Threaten Blarf":
        jump threatenblarf
    "Be nice to Blarf":
        jump nicetoblarf
label threatenblarf:
    y "IF YOU DON'T TELL ME WHAT YOU KNOW..."
    y "I'm arresting you right now!"
    show frog squint left at right
    b "WAHHHHHHHH I DESERVE IT!!"
    show frog squint right at right
    y "Oh?"
    show frog squint left at right
    b "I've done terrible things for him!\nI deserve to rot in jail."
    y "Tell me what you know.\nI'll try to make things right!"
    show frog crack left at right
    b "I work for a criminal... I work for..."
    jump trueconfession
label nicetoblarf:
    y "Listen...\nYou're clearly dealing with a lot of stress."
    show frog squint left at right
    y "I'm just here to help..."
    show frog crack left at right
    y "If you tell me what you know,\nI can help you get out of whatever this is."
    show frog squint left at right
    b "You promise?"
    y "Sure."
    show frog crack left at right
    b "Okay..."
    b "Awhile ago... I started working for a criminal.\nThey call him..."
    jump trueconfession

label trueconfession:
    b "THE COCA-KOALA!"
    with hpunch
    y "The drink?"
    show frog crack left at right
    b "No! He's real! He runs Pigglydelphia!"
    show frog squint right at right
    y "Are you joking?"
    show frog squint left at right
    b "He has eyes all over the city.\nHe's been getting away with crime for decades!"
    show frog squint right at right
    b "He bought out the media to cover his tracks.\nNo one remembers all the terrible things he did."
    b "Coca-Koala is more than a drink brand...\nYou don't believe me?"
    show frog crack left at right
    b "Look in that box. I hid evidence in there years ago."
    b "Although, someone tore it up."
    jump paperpuzzle

label paperpuzzle:
    $setup_puzzle()
    call screen reassemble_puzzle

label reassemble_complete:
    scene finishedpuzzletable
    pause (2.0)
    y "Woah. I don't remember ever hearing about this."
    
    scene puzzle desk
    with fade
    show frog crack left at right
    b "BLARF! Dillworth didn't used to be an employee.\nHe was an undercover cop!"
    show frog squint left at right
    b "Coca-Koala is just a massive front\nfor the Coca-Koala's cocaine empire!"
    b "Dillworth infiltrated Coca-Koala,\nbut then got addicted to cocaine."
    b "He's worked here since 1999.\nHe barely remembers life before this."
    show frog squint right at right
    b "Five years later, I got sent in."
    show frog squint left at right
    y "You're an undercover cop?"
    show frog crack left at right
    b "It's hard to remember.\nI also got addicted to cocaine and started working here for real."
    y "It's that good?"
    show frog squint left at right
    b "You don't understand, man. This is Coca-Koala Cocaine." 
    show frog crack left at right
    b "The best powder money can buy. I don't even think I get paid anymore." 
    b "My last paycheck was 3 Pokemon cards,\na tootsie roll and cocaine."
    y "Wow, so the Coca-Koala killed Dillworth?"
    show frog squint right at right
    b "Dillworth and I planned to escape.\nWe were gonna bust the opperation and turn ourselves in."
    b "But then he got a visit from the Coca-Koala..." 
    b "Dillworth thought he could still carry\nthrough with the plan. I tried to warn him!"
    b "We were told to gather here on Saturday.\nThe Coca-Koala shot Dillworth in front of us."
    y "That's awful..."
    show frog crack left at right
    b "BLARF! The Coca-Koala lives in the building."
    show frog squint left at right
    b "He can probably hear us now.\nWe're fucked!"
menu:
    "I better find Detective Beaver!":
        jump findbeaverstart
    "We gotta call for backup!":
        jump phone1

label phone1:
    show frog crack right at right
    b "There's no reception for miles!"
    jump findbeaver

label findbeaverstart:
    show frog squint left at right
    b "Don't tell me he drank Coca-Koala..."
    show frog crack left at right
    y "Two cans of it."
    b "We just started making our own product."
    show frog squint left at right
    b "It has loads of chemicals in it."
    b "Six out of ten testers died."
    y "So they were trying to kill him..."
    show frog crack left at right
    b "The Coca-Koala isn't going to let you\nor the Beaver get out of here."
    jump findbeaver


label findbeaver:
    b "We need a weapon!\nIt's the only chance we have!"
    show frog squint left at right
    b "Aren't you a detective?"
    y "In training... I don't have anything."
    show frog crack left at right
    b "There's a gun in the storage room!"
    y "Where's the storage room?"
    b "In the basement, next to\nthe room with the machines."
    show frog squint left at right
    b "You get the gun, I'll warn Detective Beaver!"
    show frog squint right at right
    b "Hurry! We don't have much time!"
    hide frog squint right with moveoutright
    y "Wait! Where are we meeting?!?"
    y "I guess I better go to the basement..."

    scene shipping
    with fade
    y "Here's all the machines."
    y "Where's the storage room?"
    show pig left at right with moveinright
    with hpunch
    show pig mad left at right
    p "I thought I told you to stay away from the factory..."
    y "Oh...I just..."
menu:
    "I was looking for the storage room.":
        jump lookingforstorage
    "I was looking for Detective Beaver.":
        jump lookingforbeaver
    "I was looking for you.":
        jump lookingforyou
label lookingforstorage:
    p "The storage room? Whatever for?"
menu:
    "I was told to question Clarice in there.":
        jump storageclarice
    "I need a mop.":
        jump mop
    "I'm looking for a gun.":
        jump blunder
label storageclarice:
    p "I thought you already questioned Clarice..."
    y "We barely questioned her."
    show pig mad right at right
    p "Funny... I just saw Clarice upstairs."
    p "She didn't mention any more questioning."
    show pig mad left at right
    y "Oh...really? Weird."
    y "Well, I better go meet her."
    p "I don't think you should."
    y "???"
    p "What are you really doing down here, detective."
    y "I...uh..."
    show pig mad right at right
    p "I think you've been snooping\naround for a little too long..."
    show pig mad left at right
    p "Maybe it's time we put an end to that."
    jump runorfight

label mop:
    p "A mop? For what?"
    y "Detective Beaver keeps throwing up."
    y "I guess his stomach and\nCoca-Koala don't get along..."
    show pig left at right
    p "Hm... Strange. I guess not."
    y "Detective Beaver said he wanted to\nask you a few more questions."
    show pig mad left at right
    y "I'll get the mop and meet you upstairs."
    show pig mad right at right
    p "Fine. Be quick. I don't have all day."
    hide pig mad right with moveoutright
    y "Phew. That was a close one."
    jump keeplooking
label blunder:
    p "A gun? Whatever for, detective."
    y "I know what you're up to here.\nYou're all criminals!"
    show pig mad right at right
    p "Well well well...\nYou caught us."
    show pig mad left at right
    p "Too bad you won't live to tell anyone."
    jump runorfight
label lookingforbeaver:
    show pig happy left at right
    p "Oh don't you worry!\nI just saw that Beaver upstairs."
    show pig mad left at right
    p "Go on, join him."
    show pig left at right
    y "Oh... I just... uh"
    show pig mad left at right
    p "What are you really doing down here, detective."
    y "I...uh..."
    show pig mad right at right
    p "I think you've been snooping\naround for a little too long..."
    show pig mad left at right
    p "Maybe it's time we put an end to that."
    jump runorfight
label runorfight:
menu:
    "Knock Priscilla out":
        jump violence
    "RUN!":
        jump runaway
label violence:
    define knockedpig = Position(ypos=0.999)
    show pig dead at knockedpig
    with hpunch
    y "Wow. Those karate lessons really paid off."
    y "She's still breathing...right?"
    y "I better find the storage room..."
    jump keeplooking
label runaway:
    p "Hey! Come back here!"
    show pig mad right at right
    p "You can run. But you\ncan't hide from the Coca-Koala."
    jump keeplooking
label lookingforyou:
    p "For me?"
    y "I wanted to ask you..."
    y "If I... could work here?"
    show pig happy left at right
    p "Don't like being a detective, eh?"
    y "I would much rather help out the community... like you."
    show pig left at right
    p "I'm sure we could find a job\nfor a smart cookie like yourself."
    show pig happy right at right
    p "Let me go ask the boss."
    hide pig happy right with moveoutright
    y "Phew. That was close."
    jump keeplooking

label keeplooking:
    scene storage
    with fade
    y "Here's the storage room!"
    y "Let me just lock the door..."
    y "There's the safe!"
    y "Shit. What's the combination?"
    jump reset
label reset:
menu:
    "I know the combination.":
        jump lookaround
    "I don't know the combination.":
        jump nogun
label tryagain:
    y "Click reset on the dial to try again. Click the red handle to give up."

label lookaround:
    # Dial variables
    $dial_image = "images/dial.png"
    $dial_size = (660 / 2, 660 / 2)
    $t = Transform(child = dial_image, zoom = 0.5)
    $dial_sprite_manager = SpriteManager(event = dial_events)
    $dial_sprite = dial_sprite_manager.create(t)
    $dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
    $dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
    $dial_rotate = False
    $dial_sprite.rotate_amount = 0
    $dial_offset = 68.2
    $dial_start_rotate = False
    $dial_number = 0
    $dial_text = 0
    $previous_dial_text = 0
    $dial_changed = False

    #Other variables
    $old_mousepos = (0.0, 0.0)
    $degrees = 0
    $old_degrees = 0
    $combinations = {"safe_1" : [8, 21, 47, 62], "safe_2" : [23, 5, 75, 44]}
    $completed_combination_numbers = {}
    $combination_check = None
    $current_safe = 1
    $combination_length = 0
    call screen scene_1

label getgun:
    scene storage
    if secondTry == True:
        jump getgun2
    else:
        y "Got it.\nTime to go find Blarf and Detective Beaver."
        jump finalewithgun
label getgun2:
    scene storage
    y "Got it.\nTime to go find Blarf and Detective Beaver."
    jump finalewithgun2

label nogun:
    y "Blarf said to hurry...\nBut I really need a weapon..."
    y "Do I have time to look for the code?"
menu:
    "Yes":
        jump lookforcode
    "No":
        jump finalenogun

label lookforcode:
    $ secondTry = True
    y "I can't show up empty-handed."
    y "Where should I look?"
menu:
    "The room where Dillworth was killed":
        jump wrong1
    "The empty office":
        jump wrong2
    "The office where I talked to Blarf":
        jump rightanswer
label wrong1:
    scene messyoffice
    with fade
    y "Could be in here...but where?"
    show rabbit mad left at right with moveinright
    with hpunch
    r "Detective! Lost your partner?"
    y "Oh...yeah I did."
    show rabbit mad right at right
    r "Pity."
    show rabbit left at right
    r "You look a bit..."
    show rabbit mad left at right
    r "Frightened."
    y "Me? N-no, I should get going though."
    show rabbit left at right
    r "Hm. You're running out of time, detective."
    show rabbit mad right at right
    y "???"
menu:
    "Go to the empty office":
        jump wrong2
    "Go to the office where I talked to Blarf":
        jump rightanswer
    "Give up":
        jump finalenogun2
label wrong2:
    scene closeoffice
    with fade
    y "Maybe it's on the computer...\nor in the drawers?"
menu:
    "Check computer":
        jump checkcomp
    "Check drawers":
        jump checkdrawers
label checkcomp:
    show loggedout
    pause(1)
    y "Hm. Someone logged out."
    c "Yes, someone did."
    hide loggedout
    show cat mad left at right with moveinright
    with hpunch
    y "Clarice!"
    c "What are you doing in my office?"
    y "Just looking for Detective Beaver!"
    y "Have you seen him?"
    show cat mad right at right
    c "Certainly not in here."
    y "Yeah...I'm just going to go..."
    show cat mad left at right
    c "Mhmm. Farewell, detective."
menu: 
    "Go to the room where Dillworth was killed":
        jump wrong1
    "Go to the office where I talked to Blarf":
        jump rightanswer
    "Give up":
        jump finalenogun2
label checkdrawers:
    y "Rats. They're all locked."
menu: 
    "Check computer":
        jump checkcomp
    "Go to the room where Dillworth was killed":
        jump wrong1
    "Go to the office where I talked to Blarf":
        jump rightanswer
    "Give up":
        jump finalenogun2
menu:
    "Go to the room where Dillworth was killed":
        jump wrong1
    "Go to the office where I talked to Blarf":
        jump rightanswer
    "Give up":
        jump finalenogun2
label rightanswer:
    scene puzzle desk
    with fade
    y "Maybe it's here."
menu:
    "Check desk":
        jump checkdesk
    "Go to the room where Dillworth was killed":
        jump wrong1
    "Go to the empty office":
        jump wrong2
    "Give up":
        jump finalenogun2
label checkdesk:
    show finishedpuzzletable
    pause(2)
    y "Hey, someone wrote numbers here."
    y "Maybe this is the combination?"
    y "8-21-47-62...\nI should write that down..."
    hide finishedpuzzletable
    scene storage
    with fade
    y "Let's try this again."
    $ secondTry = True
    jump lookaround
label finalewithgun:
    scene shipping
    with fade
    show frog squint left at right with moveinright
    b "BLARF! That was quick!"
    y "Did you find Detective Beaver?"
    show frog crack left at right
    b "He's in the cocaine room."
    y "The cocaine room?"
    show frog crack right at right
    b "BLARF! Follow me!"
    hide frog crack right with moveoutright

    scene cokeroom
    with fade
    show beaver left at beavdeath
    show frog crack right at left with moveinleft
    y "Wow, that's a lot of cocaine."
    d "Rookie! There you are!"
    show beaver squint left at beavdeath
    d "I cracked the case!"
    d "Coca-Koala's drinks taste like shit because\nthey've been too busy building with these white bricks!"
    show frog squint right at left
    b "...This is your partner?"
    show frog squint left at left
    y "Yep."
    show beaver squint right at beavdeath
    d "So... who do we think killed Dillworth?"
    show frog crack right at left
    y "Listen, we don't have much time!"
    show frog crack left at left
    y "We've got to get out of here. Now!"
    show beaver left at beavdeath
    scene cokeroomdark
    show beaver left dark at beavdeath
    show frogdark at left
    k "I'm afraid I can't let that happen." with hpunch
    pause(1)
    b "It's...it's...it's"
    show koalagundark with moveinbottom
    y "...the Coca-Koala."
    k "Well, well, well."
    k "It seems your tour of Coca-Koala is over."
    d "What is happening???"
    b "Where is he?!"
    k "Me? MWAHAHA!" with hpunch
    k "I'm right HERE!"
    hide koalagundark with moveoutbottom
    pause(0.5)
    scene cokeroom
    show frog crack right at left
    show beaver squint right at beavdeath
    pause(0.5)
    show koala happy left at right with moveinright 
    with hpunch
    pause (2)
    y "Oh."
    show frog squint right at left
    show koala angry left at right
    k "Oh?"
    y "I mean..."
    show beaver right at beavdeath
    show frog crack right at left
    d "Aw, cute little koala!"
    show koala angry right at right
    k "..."
    show koala angry left at right
    y "Sorry, it's just..."
    y "I just thought you'd be scarier."
    show frog crack left at left
    k "I'm a fucking Koala."
    y "Yeah, sorry. It's just...that this is my first case..."
    show frog crack right at left
    y "And I'm in a room full of cocaine..."
    show beaver squint left at beavdeath
    d "COCAINE?!"
    show beaver right at beavdeath
    y "And your entrance was... very dramatic."
    y "So I kinda got my expectations up."
    show koala gun left at right
    k "Is this better?"
    show frog squint left at left
    show beaver right at center with move
    d "No, no, not really."
    k "LISTEN! I AM THE COCA-KOALA." with hpunch
    show frog crack right at left
    k "I AM THE MOST POWERFUL ANIMAL IN PIGGLYDELPHIA..."
    k "AND YOU ALL ARE GOING TO DIE."
    show frog squint left at left
    show beaver squint left at center
menu:
    "Shoot him first!":
        jump sharpshooter
label sharpshooter:
    show koala shot at right with hpunch
    k "OW! WHAT THE HELL?"
    show frog crack right at left
    show beaver right at center
    show koala shot2 at right
    k "You just shot me in the paw!"
    y "Sorry, I've never uh... shot someone before."
    show beaver left at center
    show koala shot3 at right
    k "Holy shit! I'm bleeding!"
    show frog squint left at left
    show beaver right at center
    show koala shot4 at right
    k "Is it just me, or is that a lot of blood?!"
    show frog crack right at left
    show koala shot5 at right
    k "Seriously? On a scale of 1-10,\nhow much blood would you say this is?"
    show beaver squint right at center
    show frog squint right at left
    d "I don't know, seven?"
    show frog crack right at left
    show koala shot6 at right
    k "Can you like... call someone?"
    y "There's no service..."
    show koala shot7 at right
    k "Oh my god that's so annoying."
    pause(1)
    k "So like..."
    k "Ever tried cocaine?"
    show frog side eye right at left
    show beaver right at center
    scene blackscreen
    with fade
    y "And that's the story of my first case..."
    show koalaarrestedbeaver
    with fade
    y "The Coca-Koala is no longer in control of Pigglydelphia."
    y "Once we were able to gather all the evidence,\nClarice, Rodrick and Priscilla served jailtime, too."
    scene blackscreen
    with fade
    y "As for Detective Beaver..."
    y "After that case, he decided to change career paths."
    y "Best soda on the market, if you ask me."
    $ renpy.movie_cutscene("images/beaverad.webm")
    return


label finalenogun:
    y "I'm running out of time!"
    y "I'll have to think of something else."
    y "Time to go find Blarf and Detective Beaver."
    scene shipping
    with fade
    show frog squint left at right with moveinright
    b "BLARF! That was quick!"
    show frog squint right at right
    b "W-where's the gun?"
    y "I couldn't get in the safe..."
    show frog squint left at right
    jump convergenogun
label convergenogun:
    b "BLARF! We're screwed!"
    y "It's okay! I have a plan!"
    show frog crack left at right
    b "What's your plan?"
    pause(2)
    y "Okay, I have no plan."
    show frog squint left at right
    b "We're all gonna die!"
    y "Did you find Detective Beaver?"
    show frog crack right at right
    b "Yeah, I left him in the cocaine room."
    y "The cocaine room?"
    b "Follow me."
    hide frog crack right with moveoutright

    scene cokeroomdark
    with fade
    show beaver left dark at beavdeath
    show frogdark at right with moveinright
    y "Why is it so dark?"
    b "Oh no... HE'S HERE!"
    y "The Coca-Koala??"
    b "BLARF! I'm getting out of here!"
    hide frogdark with moveoutleft
    define beavdeath = Position(xpos=0.65)
    jump deathofbeaver2

label finalenogun2:
    y "Well, that was a waste of time."
    y "I'll have to think of something else."
    y "Time to go find Blarf and Detective Beaver."
    scene shipping
    with fade
    show frog squint left at right with moveinright
    b "BLARF! What took you so long?"
    show frog squint right at right
    b "W-where's the gun?"
    y "I couldn't get in the safe..."
    show frog squint left at right
    jump convergenogun

label finalewithgun2:
    scene shipping
    with fade
    show frog squint left at right with moveinright
    y "Blarf! I got the gun!"
    show frog crack right at right
    b "I told you to hurry!"
    b "BLARF!...You're too late."
    y "What do you mean?"
    show frog crack left at right
    b "T-the C-coca-Koala-"
    b "HE'S HERE!"
    y "Where's Detective Beaver?"
    show frog squint right at right
    b "Forget the Beaver!\nWe need to get out of here!"
    y "I'm not leaving without him!"
    show frog crack left at right
    b "...They never listen to me."
    show frog crack right at right
    b "Alright. He's r-right over h-h-h-here."
    hide frog crack right with moveoutright

    scene cokeroomdark
    with fade
    show beaver left dark at beavdeath
    show frogdark at right with moveinright
    b "I'm getting out of here!"
    hide frogdark with moveoutleft
    define beavdeath = Position(xpos=0.65)
    y "Why is it so dark?"
    jump deathofbeaver

label deathofbeaver:
    d "Rookie? Is that you?"
    y "Detective Beaver, we\nhave to get out of here!"
    with hpunch
    pause(1)
    scene cokeroom
    hide beaver left dark
    show beaver left at beavdeath
    k "I'm afraid I can't let that happen."
    $ renpy.movie_cutscene("images/finalbeaver.webm")
    hide beaver left
    show deadbeaver at beavdeath
    with hpunch
    k "Nice to finally meet you, detective."
    y "Sh-show yourself!"
    k "Me? MWAHAHA!"
    k "I'm right HERE!"
    with hpunch
    show koala happy left at right with moveinright
    pause (2)
    y "Oh."
    show koala angry left at right
    k "Oh?"
    y "No I mean..."
    show koala angry right at right
    k "What, is the suit not working for you?"
    show koala angry left at right
    y "No! I mean, the suit's fine.\n I just..."
    y "I just thought you'd be scarier."
    k "I'm a fucking Koala."
    y "Yeah, sorry. It's just...that this is my first case..."
    y "And I'm in a room full of cocaine..."
    y "And you just killed my partner... very dramatically."
    y "So I kinda got my expectations up."
    show koala gun left at right
    k "Is this better?"
    y "Not really."
    pause(1)
    show koala angry left at right
    k "LISTEN! I AM THE COCA-KOALA." with hpunch
    k "You've made it this far, detective..."
    show koala gun left at right
    k "But now it's game over."
menu:
    "Shoot him first!":
        jump pulloutgun
label pulloutgun:
    y "Actually..."
    y "It's game over for you."
    show koala shot at right with hpunch
    k "OW! WHAT THE HELL MAN?"
    show koala shot2 at right
    k "You just shot me in the paw!"
    y "Sorry, I've never uh... shot someone before."
    show koala shot3 at right
    k "Holy shit! I'm bleeding!"
    show koala shot4 at right
    k "Is it just me, or is that a lot of blood?!"
    show koala shot5 at right
    k "Seriously? On a scale of 1-10,\nhow much blood would you say this is?"
    show koala shot6 at right
    k "Can you like... call someone?"
    y "There's no service..."
    show koala shot7 at right
    k "Oh my god that's so annoying."
    pause(1)
    k "So like..."
    k "Ever tried cocaine?"
    jump koalaarrested
    
label koalaarrested:
    scene blackscreen
    with fade
    y "And that's the story of my first case..."
    show koalaarrestedscreen
    with fade
    y "The Coca-Koala is no longer in control of Pigglydelphia."
    y "Once we were able to gather all the evidence,\nClarice, Rodrick and Priscilla served jailtime, too."
    scene blackscreen
    with fade
    y "As for Blarf..."
    y "I'm not sure what happened to him."
    y "Hope he's doing well. Wherever he is."
    $ renpy.movie_cutscene("images/blarfending.webm")
    return

label deathofbeaver2:
    d "Rookie? Is that you?"
    y "Detective Beaver, we\nhave to get out of here!"
    with hpunch
    pause(1)
    scene cokeroom
    hide beaver left dark
    show beaver left at beavdeath
    k "I'm afraid I can't let that happen."
    $ renpy.movie_cutscene("images/finalbeaver.webm")
    hide beaver left
    show deadbeaver at beavdeath
    with hpunch
    k "Nice to finally meet you, detective."
    y "Sh-show yourself!"
    k "Me? MWAHAHA!"
    k "I'm right HERE!"
    with hpunch
    show koala happy left at right with moveinright
    pause (2)
    y "Oh."
    show koala angry left at right
    k "Oh?"
    y "No I mean..."
    show koala angry right at right
    k "What, is the suit not working for you?"
    show koala angry left at right
    y "No! I mean, the suit's fine.\n I just..."
    y "I just thought you'd be scarier."
    k "I'm a fucking Koala."
    y "Yeah, I know. It's just...that this is my first case..."
    y "And I'm in a room full of cocaine..."
    y "And you just killed my partner... very dramatically."
    y "So I kinda got my expectations up."
    show koala gun left at right
    k "Is this better?"
    y "Not really."
    pause(1)
    show koala angry left at right
    k "LISTEN! I AM THE COCA-KOALA." with hpunch
    k "You've made it this far, detective..."
    show koala gun left at right
    k "But now it's game over."
    y "Wait!"
menu:
    "I want a job!":
        jump workforkoala
label workforkoala:
    k "You what?"
    show koala angry left at right
    y "I'm not here to bust your opperation."
    y "We have a lot in common, you know."
    y "Let me join you!"
    show koala left at right
    y "You're telling me... you want to sell coke?"
    pause(2.0)
    y "Sure."
    y "In fact, I want to do more than that."
    y "I want to be the next..."
    define koala2pos = Position(xpos=0.25, ypos = 1.05)
    show koala2 right at koala2pos with moveinleft

    show koala happy left at right
    y "Coca-Koala." with hpunch
    scene blackscreen
    with fade
    y "And that's the story of how I became a coke dealer..."
    scene becomekoalascene
    y "The Coca-Koala and I ran Pigglydelphia."
    scene carupclose
    y "We made millions."
    scene becomekoalascene2
    y "We were on top of the world."
    pause(2.0)
    y "What happened to Blarf, you ask?"
    y "Well...funny story..."
    $ renpy.movie_cutscene("images/blarfcop.webm")
    return


    #ENDINGS!
    #finalenogun - you waste no time, but have no gun. Detective Beaver dies. You join Coca-Koala. - creepy vid + police blarf final vid
    #finalenogun2 - you were too slow, so Detective Beaver dies. Almost identical to finalenogun. - creepy vid + police blarf final vid

    #finalewithgun - you got the safe combination the first try, wasting no time. Detective Beaver lives. - detective beaver ad
    #finalewithgun2 - you get the gun, but too late - Detective Beaver dies. - creepy vid + blarf cocaine final vid

