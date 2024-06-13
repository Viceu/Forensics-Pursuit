﻿### The script of the game goes in this file.

# variable that describes whether current user is in the center (of all five possible positions)
default middle = True
# which direction currently looking at 
default front_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default curr_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default hallway_directions = {'up': False, 'down': False, 'left': False, 'right': False}
default stove_directions = {'up': False, 'down': False, 'left': False, 'right': False}
# whether toolbox is currently displayed
default toolbox_show = False
# first time exploring toolbox?
default first_time_toolbox = True
# which tool is currently enabled (shown on screen)
default tools = { "tape" : False, "bag": False, "powder": False, "marker": False, "scalebar": False, "light": True, "lifting_tape": False}
# finished evidence collection?
default finish_collection = False
# finish tutorial
default finish_tutorial = False

init python:
    config.keymap['dismiss'].append('K_UP')
    config.keymap['dismiss'].append('K_DOWN')
    config.keymap['dismiss'].append('K_LEFT')
    config.keymap['dismiss'].append('K_RIGHT')

    # inventory -------------------------

    def inventoryUpdate(st):
        if inventory_drag == True:
            for item in inventory_sprites:
                if item.type == item_dragged:
                    item.x = mousepos[0] - item.width / 2
                    item.y = mousepos[1] - item.height / 2
                    item.zorder = 99
            return 0
        return None
    
    def inventoryEvents(event, x, y, at):
        global mousepos
        global dialogue
        global inventory_drag
        global i_overlap
        global ie_overlap
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in inventory_sprites:
                    if item1.x <= x <= item1.x + item1.width and item1.y <= y <= item1.y + item1.height:
                        inventory_drag = False
                        i_combine = False
                        ie_combine = False
                        for item2 in inventory_sprites:
                            items_overlap = checkItemsOverlap(item1, item2)
                            if items_overlap == True:
                                i_overlap = True

                                # if I need to use items on stuff, add those interactions here
                                # item1 = object being dragged, item2 = object being itneracted with from 
                                # feel free to combine with nina's drag and drop code
                                if (item1.type == "matches" or item1.type == "lantern") and (item2.type == "matches" or item2.type == "lantern"):
                                    i_combine = True
                                    if item1.type == "matches":
                                        removeInventoryItem(item1)
                                    else:
                                        removeInventoryItem(item2)
                                    lantern_image = Image("Inventory Items/inventory-lantern-lit.png")
                                    t = Transform(child = lantern_image, zoom = 0.5)
                                    inventory_sprites[inventory_items.index("lantern")].set_child(t)
                                    inventory_sprites[inventory_items.index("lantern")].item_image = lantern_image
                                    inventory_sprites[inventory_items.index("lantern")].state = "lit"
                                    renpy.show_screen("inspectItem", ["lantern"])
                                    characterSay(who = "Claire", what = ["The lantern is now lit!"], inspectItem = True)
                                    inventory_SM.redraw(0)
                                    renpy.restart_interaction()
                                    break
                                else:
                                    item1.x = item1.original_x
                                    item1.y = item1.original_y
                                    item1.zorder = 0
                                    characterSay(who = "Claire", what = ["Hmm, that doesn't seem to work.", "Try something else."])
                                    break
                        if i_combine == False:
                                for item3 in environment_sprites:
                                    items_overlap = checkItemsOverlap(item1, item3)
                                    if items_overlap == True:
                                        ie_overlap = True
                                        if item1.type == "tape" and item3.type == "box":
                                            ie_combine = True
                                            removeInventoryItem(item1)
                                            removeEnvironmentItem(item3)
                                            addToInventory(["secateur", "matches"])
                                            renpy.show_screen("inspectItem", ["secateur", "matches"])
                                            characterSay(who = "Claire", what = ["This tool might come in handy.", "But for what?"], inspectItem = True)
                                            inventory_SM.redraw(0)
                                            environment_SM.redraw(0)
                                            renpy.restart_interaction()
                                            break
                                        elif item1.type == "tape" and item3.type == "door-vines":
                                            ie_combine = True
                                            removeInventoryItem(item1)
                                            removeEnvironmentItem(item3)

                                            characterSay(who = "", what = ["Great job!"], jump_to = "setupScene2") # jump to setupScene2 with dialogue first.
                                            addToInventory(["tape"])
                                            inventory_SM.redraw(0)
                                            environment_SM.redraw(0)
                                            renpy.restart_interaction()
                                            break
                                        else:
                                            item1.x = item1.original_x
                                            item1.y = item1.original_y
                                            item1.zorder = 0
                                            characterSay(who = "Claire", what = ["Hmm, that doesn't seem to work.", "Try something else."])
                                            break
                        if i_combine == False and ie_combine == False:
                            item1.x = item1.original_x
                            item1.y = item1.original_y
                            item1.zorder = 0

        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            if inventory_drag == False:
                for item in inventory_sprites:
                    if item.visible == True:
                        if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                            renpy.show_screen("inventoryItemMenu", item = item)
                            renpy.restart_interaction()
                            break
                        else:
                            renpy.hide_screen("inventoryItemMenu")
                            renpy.restart_interaction()

    def environmentEvents(event, x, y, at):
        # what happens when cursor hovers over object
        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            for item in environment_sprites:
                if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                    t = Transform(child= item.hover_image, zoom= 0.5)
                    item.set_child(t)
                    environment_SM.redraw(0)
                else:
                    t = Transform(child= item.idle_image, zoom= 0.5)
                    item.set_child(t)
                    environment_SM.redraw(0)
        # action on click
        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
             if event.button == 1:
                for item in environment_sprites:
                    if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                        if item.type == "tape":
                            # action for what happens when key is clicked
                            # the following action is for adding to inventory
                            addToInventory(["tape"])
                        elif item.type == "lantern":
                            addToInventory(["lantern"])
                        elif item.type == "box":
                            # dialogue box pop-up
                            characterSay(who = "Vivian", what = ["Hmm, this box is locked. I think it needs a key."])
                        elif item.type == "door-vines":
                            pass
    
    def startDrag(item):
        global inventory_drag
        global item_dragged
        inventory_drag = True
        item_dragged = item.type
        inventory_SM.redraw(0)

    def checkItemsOverlap(item1, item2):
        if abs((item1.x + item1.width / 2) - (item2.x + item2.width / 2)) * 2 < item1.width + item2.width and abs((item1.y + item1.height / 2) - (item2.y + item2.height / 2)) * 2 < item1.height + item2.height and item1.type != item2.type:
            return True
        else:
            return False

    def characterSay(who, what, inspectItem = False, jump_to = None):
        if isinstance(what, str):
            renpy.call_screen("characterSay", who = who, what = what, jump_to = jump_to) # pass on the jump_to parameter in case one chooses to jump to another scene after dialogue.
        elif isinstance(what, list):
            global dialogue
            dialogue = {"who" : who, "what" : what}
            if inspectItem == False:
                renpy.show_screen("characterSay", jump_to = jump_to) # pass on the jump_to parameter in case one chooses to jump to another scene after dialogue.
                renpy.restart_interaction()

    def repositionInventoryItems():
        global inventory_lb_enabled
        global inventory_rb_enabled

        for i, item in enumerate(inventory_sprites):
            if i == 0:
                item.x = inventory_first_slot_x
                item.original_x = item.x
            else:
                item.x = (inventory_first_slot_x + inventory_slot_size[0] * i) + (inventory_slot_padding * i)
                item.original_x = item.x
            # if item.x < inventory_first_slot_x or item.x > (inventory_first_slot_x + (item.width * 7)) + (inventory_slot_padding * 5):
            #     setItemVisibility(item = item, visible = False)
            # elif item != "":
            #     setItemVisibility(item = item, visible = True)

        # if len(inventory_sprites) > 0:
        #     if inventory_sprites[-1].visible == True:
        #         inventory_rb_enabled = False
        #     else:
        #         inventory_rb_enabled = True
        #     if inventory_sprites[0].visible == True:
        #         inventory_lb_enabled = False
        #     else:
        #         inventory_lb_enabled = True

        # renpy.retain_after_load()


    def addToInventory(items):
        for item in items:
            inventory_items.append(item)
            # checks if lantern is lit - ignore this
            if item == "lantern":
                item_image = Image("Inventory Items/Inventory-lantern-unlit.png")
            else:
                item_image = Image("Inventory Items/Inventory-{}.png".format(item))

            t = Transform(child = item_image, zoom = 0.5)
            inventory_sprites.append(inventory_SM.create(t))
            # sprite we just created
            inventory_sprites[-1].width = inventory_slot_size[0]
            inventory_sprites[-1].height = inventory_slot_size[1]
            inventory_sprites[-1].type = item
            inventory_sprites[-1].item_image = item_image
            inventory_sprites[-1].y = 940
            inventory_sprites[-1].original_y = 940
            inventory_sprites[-1].original_x = 0
            inventory_sprites[-1].visible = True

            if item == "lantern":
                inventory_sprites[-1].state = "unlit"
            else:
                inventory_sprites[-1].state = "default"

            # removes item from scene once you pick it up
            for envitem in environment_sprites:
                if envitem.type == item:
                    removeEnvironmentItem(item= envitem)
                    break

            repositionInventoryItems()

            inventory_SM.redraw(0)
            environment_SM.redraw(0)
            renpy.restart_interaction()

    def removeEnvironmentItem(item):
        item.destroy()
        # environment_items_deleted.append(item.type)
        environment_sprites.pop(environment_sprites.index(item))
        environment_items.pop(environment_items.index(item.type))

    def removeInventoryItem(item):
        item.destroy()
        inventory_sprites.pop(inventory_sprites.index(item))
        inventory_items.pop(inventory_items.index(item.type))
        repositionInventoryItems()


    def inventoryArrows(button):
        pass

     # inventory -------------------------

image string_tape_left = "string_tape_left.png"
define s = Character("Supervisor")

### The game starts here.
label start:
    # $ = global variable
    $config.rollback_enabled = False
    $quick_menu = False
    $environment_SM = SpriteManager(event = environmentEvents)
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents)
    $environment_sprites = []
    $inventory_sprites = []
    $environment_items = []
    $inventory_items = []
    $environment_item_names = []
    # objects
    $inventory_item_names = ["Tape", "Lantern", "Matches", "Secateur"] 
    $current_scene = "scene1"
    $inventory_rb_enabled = False
    $inventory_lb_enabled = False
    $inventory_slot_size = (int(215 / 2), int(196 / 2))
    $inventory_slot_padding = 120 / 2
    # 22
    $inventory_first_slot_x = 550
    # 350
    $dialogue = {}
    $inventory_drag = False
    $item_dragged = ""
    $mousepos = (0.0, 0.0)
    $i_overlap = False
    $ie_overlap = False
    call screen opening_screen
    


label enter_splash_screen:
    scene entering_splash_screen
    with Dissolve(.8)
    call screen splash_screen

# label instructions_text:
#     scene instructions_bg
#     with Dissolve(.8)
#     call screen instructions_text_screen

# label exposition:
#     play music "ambient.mp3" volume 0.5
#     hide screen instructions_text_screen
#     jump robarts_exterior

# label coffee:
#     call screen coffee_bitter

# label newspaper:
#     call screen newspaper_close_up

# label phone:
#     scene instructions_bg_idle
#     play sound "phone.mp3"
#     pause
#     call screen phone_ring()


# label supervisor_call:
#     "Supervisor: Apologies for calling you in on a weekend but we need you on site ASAP! \n\n\n>>hit space to continue"
#     "Supervisor: Come to Robarts Library. There's been a robbery! \n\n\n>>hit space to continue"
#     "You quickly get up and head to Robarts. \n\n\n>>hit space to continue"
#     scene black
#     play sound "driving.mp3"
#     "10 minutes later... \n\n\n>>hit space to continue"
#     jump robarts_exterior

label robarts_exterior:
    stop music fadeout 1.0
    scene robarts_exterior

    "You finally arrive at Robarts and spot your supervisor. \n\n\n>>hit space to continue"
    
    show supervisor
    s "You're late."
    s "You're lucky I haven't fired you."
    s "Anyways, a female student went missing a couple days ago and was last seen at Robarts Library, specifically in the Robarts Commons."
    s "Witnesses close to the student were asked to come in for questioning and sources close to the student claim the student was staying late studying for a chemistry exam and never returned home nor showed up for their exam."
    s "Our forensics team also retrieved some critical information about the student that you might want to look at."
    s "Here, take a look."
    scene folder
    call screen file_folder()

label inside_library:
    scene robarts_exterior
    show supervisor
    s "Let's have a look and secure the area."
    scene task1
    pause
    hide string_tape_left
    scene main_lib_interior
    call screen task_1()

label tape:
    call screen tape()

label footprints:
    call screen footprints()

label taped:
    if front_directions['left']:
        play sound "tape.mp3"
        scene left_taped
    elif front_directions['right']:
        play sound "tape.mp3"
        scene right_taped

label instructions_key_arrows:
    #show screen move_on
    hide screen instructions_text_screen
    "Great job! Now let's head back!"
    #hide screen move_on
    call screen instructions_key_screen()

label choose_location:
    menu:
        "Explore outside": 
            call screen robarts_exterior_3()
        "Explore inside":
            scene interior
            call screen robarts_interior()

label look_around:
    

label jump_directions:
    hide screen opening
    if middle:
        if front_directions['up']:
            $ curr_directions['up'] = True
            scene front_up
            show screen opening('looking up')
        elif front_directions['down']:
            $ curr_directions['down'] = True
            scene front_down
            show screen opening('looking down')
            show screen toolbox
        elif front_directions['right']:
            $ curr_directions['right'] = True
            scene right
            show screen opening('looking to the right')
        elif front_directions['left']:
            $ curr_directions['left'] = True
            scene left
            show screen opening('looking to the left')
        $ middle = False
        call screen instructions_key_screen()

    else:
        scene robarts_outside_2
        show screen opening('back in center')
        python:
            middle = True
            for c_d in front_directions:
                front_directions[c_d] = False
            for c_d in curr_directions:
                curr_directions[c_d] = False
        call screen instructions_move_on_screen
        call screen instructions_key_screen()

label keep_exploring:
    call screen instructions_key_screen()

# ---------------------
label interior_scene2:
    scene interior_2
    show screen taped_left
    jump setupScene1

label interior_scene3:
    scene right_1
    call screen interior_scene3a

label r2:
    scene right_2
    call screen interior_scene3b

label r3:
    scene right_3
    call screen interior_scene3c

label r4:
    scene right_4
    pause

label setupScene2:
    # show screen tape_left
    show string_tape_left:
        xalign 0.3
        yalign 0.5
    #xpos 200 ypos 550 at half_size

screen taped_left:
    zorder 1
    # image "taped_left.png" xpos 0 ypos 0.8 at half_size
    imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= Show("inventory"), false= Hide("inventory")) xpos 0.03 ypos 0.825 at half_size

# ---------------------

### entering scene 
label enter_scene:
    hide screen opening
    #show screen move_on
    "Great job! Let's continue securing the area! \n\n\n>>hit space to continue"
    pause
    #hide screen move_on
    scene main_lib_interior
    call screen task_1()
    
# label hallway:
#     hide screen entering_screen
#     scene hallway
#     with Dissolve(.8)
#     #show screen move_on
#     "You are looking at the hallway.\n\n\n>>hit space to continue"
#     "You may click the arrow keys to explore the hallway. Once you are ready to move on, hit space.\n\n>>hit space to continue"
#     call screen hallway_screen

# label hallway_directions:
#     if middle:
#         if hallway_directions['up']:
#             $ curr_directions['up'] = True
#             scene hallway_up
#         elif hallway_directions['down']:
#             $ curr_directions['down'] = True
#             scene hallway_down
#         elif hallway_directions['right']:
#             $ curr_directions['right'] = True
#             scene hallway_right
#         elif hallway_directions['left']:
#             $ curr_directions['left'] = True
#             scene hallway_left
#         $ middle = False
#         call screen hallway_screen
#     else:
#         scene hallway
#         python:
#             middle = True
#             for c_d in hallway_directions:
#                 hallway_directions[c_d] = False
#             for c_d in curr_directions:
#                 curr_directions[c_d] = False
#         call screen hallway_screen

# ### kitchen scene
# label stove_directions:
#     if middle:
#         if stove_directions['up']:
#             scene stove_up
#         elif stove_directions['down']:
#             scene stove_down
#         elif stove_directions['right']:
#             scene stove_right
#         elif stove_directions['left']:
#             scene stove_left
#         $ middle = False
#         call screen stove_screen
#     else:
#         scene footprints_closeup
#         python:
#             middle = True
#             for c_d in stove_directions:
#                 stove_directions[c_d] = False
#         call screen stove_screen

# label examination_kitchen:
#     hide screen hallway_screen
#     #show screen move_on
#     scene kitchen_idle
#     "This is the kitchen of the crime scene.\n\n\n>>hit space to continue"
#     "Move your cursor around to find a surface to explore in greater detail.\n\n\n>>hit space to continue"
#     #hide screen move_on
#     call screen kitchen_screen

# label examination_stove:
#     hide screen kitchen_screen
#     scene footprints_closeup
#     show screen toolbox
#     with Dissolve(.8)
#     #show screen move_on
#     "You are looking at the stove.\n\n\n>>hit space to continue"
#     "Again, you may use the arrow keys to look around the stove.\n\n\n>>hit space to continue"
#     "Once you are done exploring, try clicking on the toolbox.\n\n\n>>hit space to continue"
#     #hide screen move_on
#     call screen stove_screen
    
# label tool_expand:
#     $ default_mouse = ''

#     scene footprints_closeup
#     hide screen uv_light_stove
#     show screen toolbox
#     if toolbox_show:
#         hide screen expand_tools
#         show screen toolbox
#         $ toolbox_show = False
#     else:
#         scene footprints_closeup
#         show screen expand_tools
#         $ toolbox_show = True
#         if first_time_toolbox:
#             $ first_time_toolbox = False
#             #show screen move_on
#             show screen arrow
#             "You found some muddy footprints. Great job!"
#             "The toolbox holds the various tools you may need to collect evidence in this stage.\n\n>>hit space to continue"
#             show screen arrow
#     if finish_collection:
#         #hide screen move_on
#         show screen move_on_lab
#     call screen stove_screen
#     show screen toolbox

# label evidence_markers:
#     $ default_mouse = 'evidence_markers'
#     "These are evidence markers.\n\n\n>>hit space to continue"
#     "These are used to mark and illustrate items of evidence at a crime scene.\n\n>>hit space to continue"
#     show screen toolbox
#     call screen stove_screen

# label evident_tape:
#     $ default_mouse = 'tape'
#     "This is an evidence tape.\n\n>>hit space to continue"
#     show screen toolbox
#     call screen stove_screen
    
# label uv_light:
#     hide screen arrow
#     $ default_mouse = 'uv_light'
#     $ toolbox_show = False
#     $ tools['powder'] = True
#     hide screen toolbox
#     hide screen expand_tools
#     scene stove_fingerprint
#     #show screen move_on
#     "This is the flashlight.\n\n\n>>hit space to continue"
#     "The flashlight enables you to perform a visual search and identify evidence that may not have been previously detected.\n\n>>hit space to continue"
#     "Shine the light around the stove top to see what you can find. Remember to use the flashlight on an oblique angle!\n\n>>hit space to continue"
#     "Once you find the evidence, click on it so that you remember its location.\n\n\n>>hit space to continue"
#     call screen uv_light_stove
    
# label finished_uv_light:
#     $ default_mouse = ''
#     $ tools['light'] = False
#     scene stove_fingerprint_persist
#     hide screen uv_light_stove
#     show screen toolbox
#     show screen expand_tools
#     "After the visual search, you now know where the fingerprint is. To help you remember, a marker will be placed beside the evidence.\n\n>>hit space to continue"
#     show screen evidence_marker_stove
#     "Let's perform dusting to collect the print by clicking on the granular powder.\n\n>>hit space to continue"
#     show screen arrow
#     #hide screen move_on
#     call screen expand_tools

# label magnetic_powder:
#     hide screen arrow
#     $ default_mouse = 'magnetic_powder'
#     $ toolbox_show = False
#     $ tools['scalebar'] = True
#     scene stove_fingerprint_persist
#     hide screen toolbox
#     hide screen expand_tools
#     hide screen evidence_marker_stove
#     #show screen move_on
#     "This is the black granular powder.\n\n\n>>hit space to continue"
#     "Reveal the latent print with the powder by dusting on it.\n\n\n>>hit space to continue"
#     call screen magnetic_powder_stove

# label finished_magnetic_powder:
#     $ default_mouse = ''
#     $ tools['powder'] = False
#     hide screen magnetic_powder_stove
#     show screen toolbox
#     show screen expand_tools
#     #show screen move_on
#     show screen evidence_marker_stove
#     scene stove_fingerprint_dusted
#     "Following dusting, we have fingerprint collection.\n\n\n>>hit space to continue"
#     "The first step in fingerprint collection is to add a scalebar beside our evidence. Click on the scalebar.\n\n>>hit space to continue"
#     show screen arrow
#     #hide screen move_on
#     call screen expand_tools

# label scalebar:
#     scene stove_fingerprint_zoomed
#     hide screen arrow
#     $ default_mouse = "scalebar"
#     $ toolbox_show = False
#     $ tools['lifting_tape'] = True
#     hide screen toolbox
#     hide screen expand_tools
#     hide screen evidence_marker_stove
#     #show screen move_on
#     "This is the scalebar.\n\n\n>>hit space to continue"
#     "The scalebar helps to indicate the relative size of the evidence which will become helpful in later stages.\n\n>>hit space to continue"
#     "Click on a surface next to the fingerprint to affix the scalebar. Make sure not to obscure the evidence.\n\n>>hit space to continue"
#     call screen scalebar_stove


# label finished_scalebar:
#     $ default_mouse = ''
#     $ tools['scalebar'] = False
#     scene scalebar_taped
#     hide screen scalebar_stove
#     show screen toolbox
#     show screen expand_tools
#     #show screen move_on
#     show screen evidence_marker_stove
#     "Now we have to lift the fingerprint and document it on a backing card.\n\n\n>>hit space to continue"
#     "Let's click on the lifting tape and the backing card.\n\n\n>>hit space to continue"
#     show screen arrow
#     #hide screen move_on
#     call screen expand_tools

# label lifting_tape:
#     scene scalebar_lifting
#     hide screen arrow
#     $ default_mouse = "lifting_tape"
#     $ toolbox_show = False
#     $ tools['bag'] = True
#     hide screen toolbox
#     hide screen expand_tools
#     hide screen evidence_marker_stove
#     #show screen move_on
#     "This is the lifting tape.\n\n\n>>hit space to continue"
#     "The tape is used to lift both the fingerprint and the  scalebar at once.\n\n\n>>hit space to continue"
#     "Once lifted, we want to stick it onto a backing card for documentation purposes.\n\n>>hit space to continue"
#     "Click on the fingerprint to lift.\n\n\n>>hit space to continue"
#     call screen lifting_tape_stove

# label lifting_to_backing:
#     scene scalebar_lifting_taped
#     $ default_mouse = ''
#     "Now we have to lift and stick the tape onto a backing card.\n\n\n>>hit space to continue"
#     "Click the tape to lift it.\n\n\n>>hit space to continue"
#     call screen backing_card_stove('lift')

# label drag_tape:
#     $ default_mouse = 'tape_print_scalebar'
#     call screen backing_card_stove('drag')

# label stick_backing:
#     $ default_mouse = ''
#     show screen backing_card_stove('stick')
#     "Great! You have successfully lifted the tape onto the backing card.\n\n\n>>hit space to continue"
#     "Don't forget to fill out the information on the front and add the letter R to indicate directionality!\n\n>>hit space to continue"
#     call screen backing_card_stove('complete_front')

# label finish_lifting_tape:
#     $ default_mouse = ''
#     $ tools['lifting_tape'] = False
#     scene footprints_closeup
#     hide screen lifting_tape_stove
#     show screen toolbox
#     show screen expand_tools
#     show screen evidence_marker_stove
#     #show screen move_on
#     "With your evidence collected, now we have to package it.\n\n\n>>hit space to continue"
#     "Click on the evidence bags to package the collected fingerprint.\n\n\n>>hit space to continue"
#     show screen arrow
#     #hide screen move_on
#     call screen expand_tools

# label evidence_bags:
#     $ default_mouse = 'evidence_bags'
#     $ toolbox_show = False
#     hide screen arrow
#     scene footprints_closeup
#     hide screen toolbox
#     hide screen expand_tools
#     hide screen evidence_marker_stove
#     #show screen move_on
#     scene stove_evidence_bags
#     with Dissolve(.5)
#     show screen current_evidence('insensitive')
#     "Here is the evidence you have gathered so far.\n\n\n>>hit space to continue"
#     "To package a piece of evidence, drag it into the bag.\n\n\n>>hit space to continue"
#     #hide screen move_on
#     call screen current_evidence('show')

# label drag_card_into_bag:
#     $ default_mouse = 'tape_print_scalebar'
#     call screen current_evidence('drag')

# label put_card_into_bag:
#     $ default_mouse = ''
#     call screen current_evidence('put_in')

# # label evidence_bags_finished:
#     $ default_mouse = ''
#     $ tools['bag'] = False
#     $ tools['tape'] = True
#     scene footprints_closeup
#     hide screen current_evidence
#     show screen toolbox
#     show screen expand_tools
#     show screen evidence_marker_stove
#     #show screen move_on
#     #scene stove_fingerprint
#     "Lastly, let's secure the bag to prevent tampering of any kind.\n\n\n>>hit space to continue"
#     "Click on the tamper evidence tape.\n\n\n>>hit space to continue"
#     show screen arrow
#     #hide screen move_on
#     #"Congratulations! You have now finished evidence collection for this stage."
#     #$ finish_collection = True
#     call screen expand_tools

# label tamper_tape:
#     hide screen arrow
#     $ default_mouse = 'tape'
#     $ toolbox_show = False
#     $ tools['tape'] = False
#     scene seal_evidence_bags
#     hide screen toolbox
#     hide screen expand_tools
#     hide screen evidence_marker_stove
#     #show screen move_on
#     show screen tamper_evident_tape_stove(False)
#     "Click on the evidence bag to seal it.\n\n\n>>hit space to continue"
#     #hide screen move_on
#     call screen tamper_evident_tape_stove(True)


# label  tutorial_finished:
#     $ default_mouse = ''
#     $ tools['bag'] = False
#     scene footprints_closeup
#     hide screen current_evidence
#     show screen toolbox
#     show screen expand_tools
#     #show screen move_on
#     if not finish_tutorial:
#         show screen evidence_marker_stove
#         "With the evidence collected, we can now remove our evidence marker.\n\n\n>>hit space to continue"
#         $ finish_tutorial = True
#     hide screen evidence_marker_stove
#     "Congratulations! You have now finished evidence collection for this stage.\n\n\n>>hit space to continue"
#     $ finish_collection = True
#     call screen evidence_to_lab

# label enter_lab:
#     hide screen stove_center
#     hide screen move_on_lab
#     hide screen toolbox
#     hide screen expand_tools
#     #hide screen move_on
#     scene entering_lab_screen
#     with Dissolve(.8)
#     call screen temporary_pause


#     return


# ------------ inventory

screen UI:
    zorder 1
    image "UI/inventory-icon-bg.png" xpos 0 ypos 0.8 at half_size
    imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= Show("inventory"), false= Hide("inventory")) xpos 0.03 ypos 0.825 at half_size

screen inventory:
    zorder 3
    image "UI/inventory-bg.png" xpos 0.17 ypos 0.8 at half_size
    image "UI/inventory-slots.png" xpos 0.274 ypos 0.845 at half_size
    imagebutton idle If(inventory_rb_enabled == True, true= "UI/inventory-arrow-right-enabled-idle.png", false= "UI/inventory-arrow-right-disabled.png") hover If(inventory_rb_enabled == True, true= "UI/inventory-arrow-right-enabled-hover.png", false= "UI/inventory-arrow-right-disabled.png") action Function(inventoryArrows, button = "right") xpos 0.89 ypos 0.88 at half_size
    imagebutton idle If(inventory_lb_enabled == True, true= "UI/inventory-arrow-left-enabled-idle.png", false= "UI/inventory-arrow-left-disabled.png") hover If(inventory_lb_enabled == True, true= "UI/inventory-arrow-left-enabled-hover.png", false= "UI/inventory-arrow-left-disabled.png") action Function(inventoryArrows, button = "left") xpos 0.21 ypos 0.88 at half_size

    add inventory_SM

# inventory item menu
screen inventoryItemMenu(item):
    zorder 7
    frame:
        xysize (inventory_slot_size[0], inventory_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("inventoryItemMenu")]
        imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(startDrag, item = item), Hide("inventoryItemMenu")]

screen inspectItem(items):
    modal True
    zorder 4
    button:
        xfill True
        yfill True
        action If(len(items) > 1, true = RemoveFromSet(items, items[0]), false= [Hide("inspectItem"), If(len(dialogue) > 0, true= Show("characterSay"), false= NullAction())])
        image "Items Pop Up/items-pop-up-bg.png" align (0.5, 0.5) at half_size

        python:
            item_name = ""
            item_desc = ""
            for name in inventory_item_names:
                temp_name = name.replace(" ", "-")
                if temp_name.lower() == items[0]:
                    item_name = name

        text "{}".format(item_name) size 50 align (0.5, 0.6) color "#000000"
        if items[0] == "lantern":
            $lantern_state = inventory_sprites[inventory_items.index("lantern")].state
            image "Items Pop Up/{}-{}-pop-up.png".format("lantern", lantern_state) align (0.5, 0.5) at half_size
        else:
            image "Items Pop Up/{}-pop-up.png".format(items[0]) align (0.5, 0.5) at half_size


screen characterSay(who = None, what = None, jump_to = None):
    modal True
    zorder 6
    style_prefix "say"

    window:
        id "window"
        window:
            padding (20, 20)
            id "namebox"
            style "namebox"
            if who is not None:
                text who id "who"
            else:
                text dialogue["who"]

        if what is not None:
            text what id "what" xpos 0.25 ypos 0.4 xanchor 0.0
        else:
            text dialogue["what"][0] xpos 0.25 ypos 0.4 xanchor 0.0

    button:
        xfill True
        yfill True
        if what is None:
            action If(len(dialogue["what"]) > 1, true= RemoveFromSet(dialogue["what"], dialogue["what"][0]), false= [Hide("characterSay"), SetVariable("dialogue", {}), If(jump_to is not None, true = Jump("{}".format(jump_to)), false = NullAction())])
        else:
            action [Return(True), If(jump_to is not None, true = Jump("{}".format(jump_to)), false = NullAction())]


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

screen scene1:
    add environment_SM

label setupScene1:
    # environment items to interact with
    $environment_items = ["box", "door-vines", "tape", "lantern"]

    python:
        for item in environment_items:
            idle_image = Image("Environment Items/{}-idle.png".format(item))
            hover_image = Image("Environment Items/{}-hover.png".format(item))
            t = Transform(child= idle_image, zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].idle_image = idle_image
            environment_sprites[-1].hover_image = hover_image

            if item == "box":
                environment_sprites[-1].width = 1293 / 2
                environment_sprites[-1].height = 360 / 2
                environment_sprites[-1].x = 598
                environment_sprites[-1].y = 3000
            elif item == "door-vines":
                environment_sprites[-1].width = 2500 / 2
                environment_sprites[-1].height = 696 / 2
                environment_sprites[-1].x = 200
                environment_sprites[-1].y = 550
            elif item == "tape":
                environment_sprites[-1].width = 101 / 2
                environment_sprites[-1].height = 55 / 2
                environment_sprites[-1].x = 1020
                environment_sprites[-1].y = 430
            elif item == "lantern":
                environment_sprites[-1].width = 123 / 2
                environment_sprites[-1].height = 181 / 2
                environment_sprites[-1].x = 1200
                environment_sprites[-1].y = 355
        addToInventory(["tape"])

    # scene scene-1-bg at half_size # change as necessary
    call screen scene1

transform half_size:
    zoom 0.5
