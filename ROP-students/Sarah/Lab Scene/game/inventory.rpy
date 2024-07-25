"""
Inventory Function File ------------------------------------------------

This file contains all of the functions required for the inventory system (including the evidence box and toolbar menus), as well as 
the screens that are required for the game. All of the functions and screens were given descriptions and detailed comments describing
their functionalities. 

For explanations on how to modify/configure this file for your own level, please reference the inventory guide I sent on Teams!

For more detailed explanations about the code, feel free to check out this tutorial series:
https://www.youtube.com/watch?v=YHbTHSYvQYk&list=PL7wM8yQ325u-l6A-i3TAcbb8V_PYnYB18 which is where I got most of my code from.

GENERAL NOTES:
    - The term, "inventory" is used to represent the evidence box. So functions prefixed with "inventory" refer to the evidence hotbar.
    This name will be changed in the final product.
    - Some functions will be labelled as unfinished if they aren't complete. You may ignore those until further notice/updates.
    - Only change the parts of the code as indicated on the inventory guide.
    - If you find any bugs in this code, please let me (Vivian) know!
"""

init python:
    # INVENTORY FUNCTIONS -----------------------------------------------
    """
    When the user clicks the "hand" icon, this function updates the item's position in the evidence box to match the cursor so it moves
    wherever the cursor moves (evidence box).

    Takes in "shown time" parameter (don't worry about this)
    """
    def inventoryUpdate(st):
        if inventory_drag == True:
            for item in inventory_sprites:
                if item.type == item_dragged:
                    item.x = mousepos[0] - item.width / 2
                    item.y = mousepos[1] - item.height / 2
                    item.zorder = 99
            return 0
        return None

    """
    When the user clicks the "hand" icon, this function updates the item's position to match the cursor so it moves
    wherever the cursor moves (toolbox).

    Takes in "shown time" parameter (don't worry about this)
    """
    def toolboxUpdate(st):
        if toolbox_drag == True:
            for item in toolbox_sprites:
                if item.type == item_dragged:
                    item.x = mousepos[0] - item.width / 2
                    item.y = mousepos[1] - item.height / 2
                    item.zorder = 99
            return 0
        return None

    """
    When the user clicks the "hand" icon, this function updates the item's position to match the cursor so it moves
    wherever the cursor moves (pop-up bar).

    Takes in "shown time" parameter (don't worry about this)
    """
    def toolboxPopUpdate(st):
        if toolboxpop_drag == True:
            for item in toolboxpop_sprites:
                if item.type == item_dragged:
                    item.x = mousepos[0] - item.width / 2
                    item.y = mousepos[1] - item.height / 2
                    item.zorder = 99
            return 0
        return None

    """
    This function handles all of the events for the evidence box's items including wthe following:
    
    1. When 2 evidence items are combined
    2. When an evidence item is combined with an environment item
    3. What happens when you mouse over an evidence item in its slot - showing the hand and inspect icons

    This function takes in 4 parameters, the event currently occurring, the x and y positions of the mouse cursor as the event is occurring, 
    and the time since the sprite is shown on screen (at) (don't worry about these)
    """
    # inventory events
    def inventoryEvents(event, x, y, at):
        global mousepos
        global dialogue
        global inventory_drag
        global i_overlap
        global ie_overlap
        global holding_towel
        global holding_knife
        global holding_knife_lifted_print
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in inventory_sprites:
                    if item1.visible == True:
                        if item1.x <= x <= item1.x + item1.width and item1.y <= y <= item1.y + item1.height:
                            inventory_drag = False
                            i_combine = False
                            ie_combine = False
                            # ------------------ INVENTORY ITEM INTERACTIONS (BETWEEN EACH OTHER) ------------------
                            for item2 in inventory_sprites:
                                items_overlap = checkItemsOverlap(item1, item2) 
                                if items_overlap == True:
                                    i_overlap = True
                                    #------------------ ADD CUSTOM INTERACTIONS HERE ------------------
                                    # More details about this part on the guide!
                                    # NOTE: item1 = object being dragged, item2 = object being interacted with
                                    # NOTE: replace the below parameters with your own custom items
                                    if (item1.type == "[insert first inventory item]" or item1.type == "[insert second inventory item]") and (item2.type == "[insert first inventory item]" or item2.type == "[insert second inventory item]"):   
                                        i_combine = True
                                        # ---- INSERT INTERACTIONS HERE ----
                                        if item1.type == "[insert first inventory item]":
                                            removeInventoryItem(item1)
                                        else:
                                            removeInventoryItem(item2)
                                        lantern_image = Image("Inventory Items/inventory-lantern-lit.png")
                                        t = Transform(child = lantern_image, zoom = 0.5)
                                        inventory_sprites[inventory_items.index("lantern")].set_child(t)
                                        inventory_sprites[inventory_items.index("lantern")].item_image = lantern_image
                                        inventory_sprites[inventory_items.index("lantern")].state = "lit"
                                        renpy.show_screen("inspectItem", ["lantern"])
                                        characterSay(who = "", what = ["The lantern is now lit!"], inspectItem = True)
                                        inventory_SM.redraw(0)
                                        renpy.restart_interaction()
                                        break
                                    else:
                                        #------------------ DEFAULT INTERACTION ------------------
                                        # What happens when a player interacts with the wrong item
                                        item1.x = item1.original_x
                                        item1.y = item1.original_y
                                        item1.zorder = 0
                                        characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue"])
                                        break
                            # ------------------ INVENTORY + ENVIRONMENT ITEM INTERACTIONS ------------------
                            if i_combine == False:
                                    #------------------ ADD CUSTOM INTERACTIONS HERE ------------------
                                    # More details about this part on the guide!
                                    # NOTE: item1 = object being dragged, item2 = object being interacted with
                                    # NOTE: replace the below parameters with your own custom items
                                    for item3 in environment_sprites:
                                        items_overlap = checkItemsOverlap(item1, item3)
                                        if items_overlap == True:
                                            ie_overlap = True
                                            
                                            if item1.type == "evidence_bag" and item3.type == "lid":
                                                ie_combine = True
                                                removeEnvironmentItem(item3)
                                                addToInventory(["jar_in_bag"])
                                                renpy.show_screen("inspectItem", ["jar_in_bag"])
                                                characterSay(who = "", what = ["Great job! Let's head back and see if we can find anything else. \n\n\n>> press space to continue"])
                                                inventory_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            elif item1.type == "evidence_bag" and item3.type == "duct_tape":
                                                ie_combine = True
                                                removeEnvironmentItem(item3)
                                                addToInventory(["tape_in_bag"])
                                                renpy.show_screen("inspectItem", ["tape_in_bag"])
                                                characterSay(who = "", what = ["Great job! Let's head back and see if we can find anything else. \n\n\n>> press space to continue"])
                                                inventory_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            else:
                                                item1.x = item1.original_x
                                                item1.y = item1.original_y
                                                item1.zorder = 0
                                                characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue."])
                                                break
                            if i_combine == False and ie_combine == False:
                                item1.x = item1.original_x
                                item1.y = item1.original_y
                                item1.zorder = 0
                                # ----------- ADDED CODE ------------
                                # Code for when the player clicks on the screen to put the item away 
                                # Check for what item is currently being held
                                if item1.type == "dish_towel":
                                    # Change appropriate variables and hide appropriate screens (will also need to add 
                                    # global insertvariablename at the beginning of the funciton)
                                    holding_towel = False
                                    renpy.hide_screen("place_towel_on_lab_bench")
                                elif item1.type == "knife":
                                    holding_knife = False
                                    renpy.hide_screen("place_knife_in_cyanosafe")
                                    renpy.hide_screen("place_knife_on_lab_bench")
                                elif item1.type == "knife_with_lifted_fingerprint":
                                    holding_knife_lifted_print = False
                                    renpy.hide_screen("put_knife_in_fumehood")
                                # ----------- END OF ADDED CODE -------------

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

    """
    This function handles all of the events for the toolbox's items including wthe following:
    
    1. When 2 toolbox items are combined
    2. When an toolbox item is combined with an environment item
    3. What happens when you mouse over a toolbox item in its slot - showing the hand and inspect icons

    This function takes in 4 parameters, the event currently occurring, the x and y positions of the mouse cursor as the event is occurring, 
    and the time since the sprite is shown on screen (at) (don't worry about these)
    """
    # toolbox events
    def toolboxEvents(event, x, y, at):
        global mousepos
        global dialogue
        global toolbox_drag
        global i_overlap
        global ie_overlap
        global holding_superglue
        global holding_disitlled_water
        global holding_basic_yellow
        global holding_scalebar
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in toolbox_sprites:
                    if item1.visible == True:
                        if item1.x <= x <= item1.x + item1.width and item1.y <= y <= item1.y + item1.height:
                            toolbox_drag = False
                            i_combine = False
                            ie_combine = False
                            for item2 in toolbox_sprites:
                                items_overlap = checkItemsOverlap(item1, item2)
                                if items_overlap == True:
                                    i_overlap = True
                                    # if I need to use items on stuff, add those interactions here
                                    # item1 = object being dragged, item2 = object being interacted with from 
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
                                        characterSay(who = "", what = ["The lantern is now lit!"], inspectItem = True)
                                        inventory_SM.redraw(0)
                                        renpy.restart_interaction()
                                        break
                                    else:
                                        item1.x = item1.original_x
                                        item1.y = item1.original_y
                                        item1.zorder = 0
                                        characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue"])
                                        break
                            if i_combine == False:
                                for item3 in environment_sprites:
                                    items_overlap = checkItemsOverlap(item1, item3)
                                    if items_overlap == True:
                                        ie_overlap = True
                                        if item1.type == "tape" and item3.type == "box":
                                            ie_combine = True
                                            removeToolboxItem(item1)
                                            removeEnvironmentItem(item3)
                                            addToToolbox(["secateur", "matches"])
                                            renpy.show_screen("inspectItem", ["secateur", "matches"])
                                            characterSay(who = "", what = ["This tool might come in handy. \n\n\n>> press space to continue", "But for what? \n\n\n>> press space to continue"], inspectItem = True)
                                            toolbox_SM.redraw(0)
                                            environment_SM.redraw(0)
                                            renpy.restart_interaction()
                                            break
                                        elif item1.type == "tape" and item3.type == "door-vines":
                                            ie_combine = True
                                            removeToolboxItem(item1)
                                            removeToolboxItem(item3)
                                            characterSay(who = "", what = ["Great job!"], jump_to = "setupScene2") # jump to setupScene2 with dialogue first.
                                            addToToolbox(["tape"])
                                            toolbox_SM.redraw(0)
                                            environment_SM.redraw(0)
                                            renpy.restart_interaction()
                                            break
                                        else:
                                            item1.x = item1.original_x
                                            item1.y = item1.original_y
                                            item1.zorder = 0
                                            characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue"])
                                            break
                            if i_combine == False and ie_combine == False:
                                item1.x = item1.original_x
                                item1.y = item1.original_y
                                item1.zorder = 0
                                # -------------- ADDED CODE -----------------
                                if item1.type == "superglue":
                                    holding_superglue = False
                                    renpy.hide_screen("add_superglue_to_cyanosafe")
                                    renpy.hide_screen("add_superglue_before_knife")
                                elif item1.type == "distilled_water":
                                    holding_distilled_water = False
                                    renpy.hide_screen("add_water_to_cyanosafe")
                                    renpy.hide_screen("add_water_before_knife")
                                elif item1.type == "basic_yellow":
                                    holding_basic_yellow = False
                                    renpy.hide_screen("spray_knife")
                                elif item1.type == "scalebar":
                                    holding_scalebar = False
                                    renpy.hide("place_scalebar")
                                # ---------- END OF ADDED CODE ------------

        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            if toolbox_drag == False:
                for item in toolbox_sprites:
                    if item.visible == True:
                        if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                            renpy.show_screen("toolboxItemMenu", item = item)
                            renpy.restart_interaction()
                            break
                        else:
                            renpy.hide_screen("toolboxItemMenu")
                            renpy.restart_interaction()

    """
    This function handles all of the events for the toolbox pop-up's items including wthe following:
    
    1. When 2 toolbox pop-up items are combined
    2. When an toolbox pop-up item is combined with an environment item
    3. What happens when you mouse over a toolbox pop-up item in its slot - showing the hand and inspect icons

    This function takes in 4 parameters, the event currently occurring, the x and y positions of the mouse cursor as the event is occurring, 
    and the time since the sprite is shown on screen (at) (don't worry about these)
    """
    # toolbox popup events
    def toolboxPopupEvents(event, x, y, at):
        global mousepos
        global dialogue
        global toolboxpop_drag
        global i_overlap
        global ie_overlap
        if event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                for item1 in toolboxpop_sprites:
                    if item1.visible == True:
                        if item1.x <= x <= item1.x + item1.width and item1.y <= y <= item1.y + item1.height:
                            toolboxpop_drag = False
                            i_combine = False
                            ie_combine = False
                            for item2 in toolboxpop_sprites:
                                items_overlap = checkItemsOverlap(item1, item2)
                                if items_overlap == True:
                                    i_overlap = True
                                    # if I need to use items on stuff, add those interactions here
                                    # item1 = object being dragged, item2 = object being interacted with from 
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
                                        characterSay(who = "", what = ["The lantern is now lit!"], inspectItem = True)
                                        inventory_SM.redraw(0)
                                        renpy.restart_interaction()
                                        break
                                    else:
                                        item1.x = item1.original_x
                                        item1.y = item1.original_y
                                        item1.zorder = 0
                                        characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue"])
                                        break
                            if i_combine == False:
                                    for item3 in environment_sprites:
                                        items_overlap = checkItemsOverlap(item1, item3)
                                        if items_overlap == True:
                                            ie_overlap = True
                                            if item1.type == "tape" and item3.type == "box":
                                                ie_combine = True
                                                removeToolboxPopItem(item1)
                                                removeEnvironmentItem(item3)
                                                addToToolbox(["secateur", "matches"])
                                                renpy.show_screen("inspectItem", ["secateur", "matches"])
                                                characterSay(who = "", what = ["This tool might come in handy.", "But for what?"], inspectItem = True)
                                                toolboxpop_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            elif item1.type == "empty_gun" and item3.type == "box":
                                                ie_combine = True
                                                removeToolboxPopItem(item1)
                                                characterSay(who = "", what = ["Hmm, this gun looks like it's missing something. \n\n\n>> press space to continue"], jump_to = "gun_front")
                                                toolboxpop_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            elif (item1.type == "cartridges" and item3.type == "gun_front") or (item1.type == "cartridges" and item3.type == "box"):
                                                ie_combine = True
                                                removeToolboxPopItem(item1)
                                                addToToolboxPop(["gun_with_cartridges"])
                                                renpy.show_screen("inspectItem", ["gun_with_cartridges"])
                                                toolboxpop_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            elif item1.type == "gun_with_cartridges" and item3.type == "box":
                                                ie_combine = True
                                                removeToolboxPopItem(item1)
                                                characterSay(who = "", what = ["Great, we have the cartridges! We might need something else though... \n\n\n>> press space to continue"], jump_to = "gun_side")
                                                toolboxpop_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            elif (item1.type == "tip" and item3.type == "gun_with_cartridges") or (item1.type == "tip" and item3.type == "box"):
                                                ie_combine = True
                                                removeToolboxPopItem(item1)
                                                removeEnvironmentItem(item3)
                                                addToToolboxPop(["gun_all"])
                                                renpy.show_screen("inspectItem", ["gun_all"])
                                                characterSay(who = "", what = ["Great, the gun is locked and loaded! Now, what should we do with it? \n\n\n>> press space to continue"], jump_to = "impression")
                                                toolboxpop_SM.redraw(0)
                                                environment_SM.redraw(0)
                                                renpy.restart_interaction()
                                                break
                                            else:
                                                item1.x = item1.original_x
                                                item1.y = item1.original_y
                                                item1.zorder = 0
                                                characterSay(who = "", what = ["Hmm, that doesn't seem to work. Let's try something else. \n\n\n>> press space to continue"])
                                                break
                            if i_combine == False and ie_combine == False:
                                item1.x = item1.original_x
                                item1.y = item1.original_y
                                item1.zorder = 0

        if event.type == renpy.pygame_sdl2.MOUSEMOTION:
            mousepos = (x, y)
            if toolboxpop_drag == False:
                for item in toolboxpop_sprites:
                    if item.visible == True:
                        if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                            renpy.show_screen("toolboxPopItemMenu", item = item)
                            renpy.restart_interaction()
                            break
                        else:
                            renpy.hide_screen("toolboxPopItemMenu")
                            renpy.restart_interaction()

    """
    This function handles are the environment item events (what happens when you interact with an item in the
    environment).
    
    1. When 2 toolbox pop-up items are combined
    2. When an toolbox pop-up item is combined with an environment item
    3. What happens when you mouse over a toolbox pop-up item in its slot - showing the hand and inspect icons

    This function takes in 4 parameters, the event currently occurring, the x and y positions of the mouse cursor as the event is occurring, 
    and the time since the sprite is shown on screen (at) (don't worry about these)
    """
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
                            characterSay(who = "", what = ["Interesting... looks like a mason jar lid. I might want to store this somewhere. \n\n\n>> press space to continue"])
                        elif item.type == "duct_tape":
                            characterSay(who = "", what = ["Interesting... looks like a piece of duct tape. I might want to store this somewhere. \n\n\n>> press space to continue"])
                        elif item.type == "gun_front":
                            removeEnvironmentItem(item)
                        elif item.type == "gun_with_cartridges":
                            removeEnvironmentItem(item)
                        elif item.type == "door-vines":
                            pass

    """
    Controls dragging mechanism for evidence box items.

    Takes in the current item being dragged.
    """
    def startDrag(item):
        global inventory_drag
        global item_dragged
        # ------------------- ADDED CODE ---------------------
        # add variables that you want to change the value of here:
        global holding_towel
        global holding_knife
        global holding_knife_with_lifted_print
        global swab_sample_being_looked_at
        # set the original x and y values to be the current x and y values before the item is dragged
        item.original_x = item.x
        item.original_y = item.y
        # check what item you have using item.type
        if item.type == "dish_towel":
            # Have code for what to do when that item is selected
            # Can use variables defined in the script file, only need to have the global statement with the variable name above 
            # if you plan on changing the value of the variable.
            # If you show a screen you will need to go to the corresponding event function (in this case inventoryEvents) 
            # and hide the screen for the case that the player puts the tool away.
            # If jumping to a different section of code, the item will not be dragged, I usually use this for messages to pop up 
            # for the player.
            holding_towel = True
            if at_lab_bench and not knife_on_lab_bench:
                renpy.show_screen("place_towel_on_lab_bench")
            elif knife_on_lab_bench:
                renpy.jump("something_on_bench")
        elif item.type == "knife":
            holding_knife = True
            if at_cyanosafe_machine and close_to_cyanosafe and not ran_cyanosafe and not warned_player_about_fingerprint_before_swabbing:
                renpy.jump("warn_player_about_lifting_print")
            if at_cyanosafe_machine and close_to_cyanosafe and not ran_cyanosafe:
                renpy.show_screen("place_knife_in_cyanosafe")
            if at_lab_bench and not towel_on_lab_bench:
                renpy.show_screen("place_knife_on_lab_bench")
            elif towel_on_lab_bench:
                renpy.jump("something_on_bench")
        elif item.type == "knife_with_lifted_fingerprint":
            holding_knife_lifted_print = True
            if at_fumehood:
                renpy.show_screen("put_knife_in_fumehood")
        elif item.type == "sample_from_floor":
            swab_sample_being_looked_at = "floor"
            renpy.jump("ask_to_send_for_extraction")
        elif item.type == "sample_from_towel":
            swab_sample_being_looked_at = "towel"
            renpy.jump("ask_to_send_for_extraction")
        elif item.type == "sample_from_knife":
            swab_sample_being_looked_at = "knife"
            renpy.jump("ask_to_send_for_extraction")
        # ------------------ END OF ADDED CODE ---------------------
        inventory_drag = True
        item_dragged = item.type
        inventory_SM.redraw(0)

    """
    Controls dragging mechanism for toolbox items.

    Takes in the current item being dragged.
    """
    def startDrag2(item):
        global toolbox_drag
        global item_dragged
        # ---------- ADDED CODE ------------
        global holding_superglue
        global holding_distilled_water
        global holding_basic_yellow
        global holding_scalebar
        item.original_x = item.x
        item.original_y = item.y
        if item.type == "superglue":
            holding_superglue = True
            if at_cyanosafe_machine and not added_superglue and close_to_cyanosafe and not ran_cyanosafe:
                if knife_in_cyanosafe:
                    renpy.show_screen("add_superglue_to_cyanosafe")
                else:
                    renpy.show_screen("add_superglue_before_knife")
        elif item.type == "distilled_water":
            if at_lab_bench:
                renpy.jump("selected_water")
            holding_distilled_water = True
            if at_cyanosafe_machine and not added_water and close_to_cyanosafe and not ran_cyanosafe:
                if knife_in_cyanosafe:
                    renpy.show_screen("add_water_to_cyanosafe")
                else:
                    renpy.show_screen("add_water_before_knife")
        elif item.type == "basic_yellow":
            holding_basic_yellow = True
            if knife_in_fumehood:
                renpy.show_screen("spray_knife")
        elif item.type == "scalebar":
            holding_scalebar = True
            if not scaled_knife and not at_lab_bench:
                renpy.show_screen("place_scalebar")
        elif item.type == "hemastix":
            if at_lab_bench:
                if currently_swabbing:
                    renpy.jump("busy_swabbing")
                elif (current_evidence.name == "dish towel" and determined_blood_on_towel) or (current_evidence.name == "knife" and determined_blood_on_knife):
                    renpy.jump("already_used_hemastix")
                elif towel_on_lab_bench or knife_on_lab_bench:
                    renpy.jump("using_hemastix")
        elif item.type == "cotton_swab":
            if at_lab_bench:
                if currently_using_hemastix:
                    renpy.jump("busy_using_hemastix")
                elif (current_evidence.name == "dish towel" and not determined_blood_on_towel) or (current_evidence.name == "knife" and not determined_blood_on_knife):
                    renpy.jump("use_hemastix_first")
                elif (current_evidence.name == "dish towel" and sample_collected_from_towel) or (current_evidence.name == "knife" and sample_collected_from_knife):
                    renpy.jump("already_swabbed")
                elif towel_on_lab_bench or knife_on_lab_bench:
                    renpy.jump("using_swab")
        # --------------- END OF ADDED CODE ------------------
        toolbox_drag = True
        item_dragged = item.type
        toolbox_SM.redraw(0)

    """
    Controls dragging mechanism for toolbox pop-up items.

    Takes in the current item being dragged.
    """
    def startDrag3(item):
        global toolboxpop_drag
        global item_dragged
        # ---------- ADDED CODE ------------
        global holding_450nm_flashlight
        global holding_incorrect_flashlight
        item.original_x = item.x
        item.original_y = item.y
        if item.type == "450nm_flashlight":
            if photographing_knife:
                holding_450nm_flashlight = True
                renpy.jump("correct_als_flashlight")
            else:
                renpy.jump("dont_need_flashlight")
        else:
            if photographing_knife:
                holding_incorrect_flashlight = True
                renpy.jump("incorrect_als_flashlight")
            else:
                renpy.jump("dont_need_flashlight")
        # ----------- END OF ADDED CODE -------------
        toolboxpop_drag = True
        item_dragged = item.type
        toolboxpop_SM.redraw(0)

    """
    Checks if items overlap each other (items are combined together)

    Takes in 2 items being checked.
    """
    def checkItemsOverlap(item1, item2):
        if abs((item1.x + item1.width / 2) - (item2.x + item2.width / 2)) * 2 < item1.width + item2.width and abs((item1.y + item1.height / 2) - (item2.y + item2.height / 2)) * 2 < item1.height + item2.height and item1.type != item2.type:
            return True
        else:
            return False

    """
    Controls dialogue in between interactions. You may use this for dialogue pop-ups when interacting with objects in a particular scene.

    Parameters:
    1. who = name of person saying dialogue
    2. what = dialogue
    3. jump_to = label to jump to
    """
    def characterSay(who, what, inspectItem = False, jump_to = None):
        if isinstance(what, str):
            renpy.call_screen("characterSay", who = who, what = what, jump_to = jump_to) # pass on the jump_to parameter in case one chooses to jump to another scene after dialogue.
        elif isinstance(what, list):
            global dialogue
            dialogue = {"who" : who, "what" : what}
            if inspectItem == False:
                renpy.show_screen("characterSay", jump_to = jump_to) # pass on the jump_to parameter in case one chooses to jump to another scene after dialogue.
                renpy.restart_interaction()

    """
    Repositions evidence box items after clicking arrow keys.
    """
    def repositionInventoryItems():
        global inventory_ub_enabled
        global inventory_db_enabled

        for i, item in enumerate(inventory_sprites):
            if i == 0:
                item.x = inventory_first_slot_x
                item.y = inventory_first_slot_y
                item.original_x = item.x
                item.original_y = item.y
            else:
                item.x = inventory_first_slot_x
                item.original_x = item.x
                item.y = (inventory_first_slot_y + inventory_slot_size[0] * i) + (inventory_slot_padding * i)
                item.original_y = item.y
            if item.y < inventory_first_slot_y or item.y > (inventory_first_slot_y + (item.height * 4)) + (inventory_slot_padding * 3):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(inventory_sprites) > 0:
            if inventory_sprites[-1].visible == True:
                inventory_db_enabled = False
            else:
                inventory_db_enabled = True
            if inventory_sprites[0].visible == True:
                inventory_ub_enabled = False
            else:
                inventory_ub_enabled = True

    """
    Repositions toolbox items after clicking arrow keys.
    """
    def repositionToolboxItems():
        global toolbox_ub_enabled
        global toolbox_db_enabled
        for i, item in enumerate(toolbox_sprites):
            if i == 0:
                item.x = toolbox_first_slot_x
                item.y = toolbox_first_slot_y
                item.original_x = item.x
                item.original_y = item.y
            else:
                item.x = toolbox_first_slot_x
                item.original_x = item.x
                item.y = (toolbox_first_slot_y + toolbox_slot_size[0] * i) + (toolbox_slot_padding * i)
                item.original_y = item.y
            if item.y < toolbox_first_slot_y or item.y > (toolbox_first_slot_y + (item.height * 4)) + (toolbox_slot_padding * 3):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(toolbox_sprites) > 0:
            if toolbox_sprites[-1].visible == True:
                toolbox_db_enabled = False
            else:
                toolbox_db_enabled = True
            if toolbox_sprites[0].visible == True:
                toolbox_ub_enabled = False
            else:
                toolbox_ub_enabled = True

    """
    Repositions toolbox pop-up items after clicking arrow keys.
    """
    def repositionToolboxPopItems():
        global toolboxpop_ub_enabled
        global toolboxpop_db_enabled
        for i, item in enumerate(toolboxpop_sprites):
            if i == 0:
                item.x = toolboxpop_first_slot_x
                item.y = toolboxpop_first_slot_y
                item.original_x = item.x
                item.original_y = item.y
            else:
                item.x = toolboxpop_first_slot_x
                item.original_x = item.x
                item.y = (toolboxpop_first_slot_y + toolboxpop_slot_size[0] * i) + (toolboxpop_slot_padding * i)
                item.original_y = item.y
            if item.y < toolboxpop_first_slot_y or item.y > (toolboxpop_first_slot_y + (item.height * 2)) + (toolboxpop_slot_padding * 1):
                setItemVisibility(item = item, visible = False)
            elif item != "": # prevent errors
                setItemVisibility(item = item, visible = True)

        if len(toolboxpop_sprites) > 0:
            if toolboxpop_sprites[-1].visible == True:
                toolboxpop_db_enabled = False
            else:
                toolboxpop_db_enabled = True
            if toolboxpop_sprites[0].visible == True:
                toolboxpop_ub_enabled = False
            else:
                toolboxpop_ub_enabled = True

    """
    Primary function for adding items to the evidence box.
    
    Takes in a list of items to add to the evidence box as a single parameter.
    """
    def addToInventory(items):
        for item in items:
            inventory_items.append(item)
            item_image = Image("Inventory Items/Inventory-{}.png".format(item))

            t = Transform(child = item_image, zoom = 0.5)
            inventory_sprites.append(inventory_SM.create(t))
            # sprite we just created
            inventory_sprites[-1].width = inventory_slot_size[0]
            inventory_sprites[-1].height = inventory_slot_size[1]
            inventory_sprites[-1].type = item
            inventory_sprites[-1].item_image = item_image
            inventory_sprites[-1].y = 500
            inventory_sprites[-1].original_y = 500
            inventory_sprites[-1].original_x = 1000
            inventory_sprites[-1].visible = True

            # removes item from scene once you pick it up
            for envitem in environment_sprites:
                if envitem.type == item:
                    removeEnvironmentItem(item= envitem)
                    break

            repositionInventoryItems()

            inventory_SM.redraw(0)
            environment_SM.redraw(0)
            renpy.restart_interaction()
    
    """
    Primary function for adding items to the toolbox.

    Takes in a list of items to add to the toolbox as a single parameter.
    """
    def addToToolbox(items):
        for item in items:
            toolbox_items.append(item)
            item_image = Image("Toolbox Items/Toolbox-{}.png".format(item))

            t = Transform(child = item_image, zoom = 0.5)
            toolbox_sprites.append(toolbox_SM.create(t))
            # sprite we just created
            toolbox_sprites[-1].width = toolbox_slot_size[0]
            toolbox_sprites[-1].height = toolbox_slot_size[1]
            toolbox_sprites[-1].type = item
            toolbox_sprites[-1].item_image = item_image
            toolbox_sprites[-1].y = 500
            toolbox_sprites[-1].original_y = 500
            toolbox_sprites[-1].original_x = 1000
            toolbox_sprites[-1].visible = True

            # removes item from scene once you pick it up
            for envitem in environment_sprites:
                if envitem.type == item:
                    removeEnvironmentItem(item= envitem)
                    break

            repositionToolboxItems()

            toolbox_SM.redraw(0)
            environment_SM.redraw(0)
            renpy.restart_interaction()

    """
    Primary function for adding items to the toolbox pop-up slot.

    Takes in a list of items to add to the toolbox pop-up slot as a single parameter.
    """
    def addToToolboxPop(items):
        for item in items:
            toolboxpop_items.append(item)
            item_image = Image("Toolbox Items/Toolbox-{}.png".format(item))
                
            t = Transform(child = item_image, zoom = 0.5)
            toolboxpop_sprites.append(toolboxpop_SM.create(t))
            # sprite we just created
            toolboxpop_sprites[-1].width = toolboxpop_slot_size[0]
            toolboxpop_sprites[-1].height = toolboxpop_slot_size[1]
            toolboxpop_sprites[-1].type = item
            toolboxpop_sprites[-1].item_image = item_image
            toolboxpop_sprites[-1].y = 500
            toolboxpop_sprites[-1].original_y = 500
            toolboxpop_sprites[-1].original_x = 1000
            toolboxpop_sprites[-1].visible = True

            # removes item from scene once you pick it up
            for envitem in environment_sprites:
                if envitem.type == item:
                    removeEnvironmentItem(item= envitem)
                    break
            
            repositionToolboxPopItems()

            toolboxpop_SM.redraw(0)
            environment_SM.redraw(0)
            renpy.restart_interaction()

    """
    Removes environment item from the environment (makes environment item disappear)

    Takes in the item to be removed as a parameter.
    """
    def removeEnvironmentItem(item):
        item.destroy()
        # environment_items_deleted.append(item.type)
        environment_sprites.pop(environment_sprites.index(item))
        environment_items.pop(environment_items.index(item.type))

    """
    Removes evidence box item from the evidence bar.

    Takes in the item to be removed as a parameter.
    """
    def removeInventoryItem(item):
        item.destroy()
        inventory_sprites.pop(inventory_sprites.index(item))
        inventory_items.pop(inventory_items.index(item.type))
        repositionInventoryItems()

    """
    Removes toolbox item from the toolbox bar.

    Takes in the item to be removed as a parameter.
    """
    def removeToolboxItem(item):
        item.destroy()
        toolbox_sprites.pop(toolbox_sprites.index(item))
        toolbox_items.pop(toolbox_items.index(item.type))
        repositionToolboxItems()

    """
    Removes evidence box item from the toolbox pop-up bar.

    Takes in the item to be removed as a parameter.
    """
    def removeToolboxPopItem(item):
        item.destroy()
        toolboxpop_sprites.pop(toolboxpop_sprites.index(item))
        toolboxpop_items.pop(toolboxpop_items.index(item.type))
        repositionToolboxPopItems()

    """
    Controls arrow functionality for the evidence box bar.
    """
    def inventoryArrows(button):
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global inventory_ub_enabled
        global inventory_db_enabled

        # check if we have more than 5 items in inventory (5 is max)
        if len(inventory_sprites) >= 5:
            citem = "" # current item

            # iterate through inventory items
            for i, item in enumerate(inventory_sprites):
                # up button 
                if button == "down" and inventory_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if inventory_sprites[-1].visible == False:
                        # shift inventory items up
                        item.y -= toolbox_slot_size[0] + inventory_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = item
                elif button == "up" and inventory_ub_enabled == True:
                    if inventory_sprites[0].visible == False:
                        reversed_index = (len(inventory_sprites) - 1) - i
                        inventory_sprites[reversed_index].y += toolbox_slot_size[0] + inventory_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = inventory_sprites[reversed_index]
                # checks if item was moved beyond first or beyond last item in inventory slots
                if citem != "" and (citem.y < inventory_first_slot_y or citem.y > (inventory_first_slot_y + (citem.height * 4)) + (inventory_slot_padding * 4)):
                    setItemVisibility(item = citem, visible = False)

                elif citem != "": # prevent errors
                    setItemVisibility(item = citem, visible = True)

            if inventory_sprites[-1].visible == True:
                inventory_db_enabled = False
            else:
                inventory_db_enabled = True
            if inventory_sprites[0].visible == True:
                inventory_ub_enabled = False
            else:
                inventory_ub_enabled = True
                
            if citem != "":
                inventory_SM.redraw(0)
                renpy.restart_interaction
    
    """
    Controls arrow functionality for the toolbox bar.
    """
    def toolboxArrows(button):
        
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global toolbox_ub_enabled
        global toolbox_db_enabled

        # check if we have more than 5 items in toolbox (5 is max)
        if len(toolbox_sprites) > 4:
            citem = "" # current item

            # iterate through toolbox items
            for i, item in enumerate(toolbox_sprites):
                # up button 
                if button == "down" and toolbox_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if toolbox_sprites[-1].visible == False:
                        # shift toolbox items up
                        item.y -= toolbox_slot_size[0] + toolbox_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = item
                elif button == "up" and toolbox_ub_enabled == True:
                    if toolbox_sprites[0].visible == False:
                        reversed_index = (len(toolbox_sprites) - 1) - i
                        toolbox_sprites[reversed_index].y += toolbox_slot_size[0] + toolbox_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = toolbox_sprites[reversed_index]
                # checks if item was moved beyond first or beyond last item in toolbox slots
                if citem != "" and (citem.y < toolbox_first_slot_y or citem.y > (toolbox_first_slot_y + (citem.height * 4)) + (toolbox_slot_padding * 4)):
                    setItemVisibility(item = citem, visible = False)

                elif citem != "": # prevent errors
                    setItemVisibility(item = citem, visible = True)

            if toolbox_sprites[-1].visible == True:
                toolbox_db_enabled = False
            else:
                toolbox_db_enabled = True
            if toolbox_sprites[0].visible == True:
                toolbox_ub_enabled = False
            else:
                toolbox_ub_enabled = True
                
            if citem != "":
                toolbox_SM.redraw(0)
                renpy.restart_interaction

    """
    Controls arrow functionality for the toolbox pop-up bar.
    """
    def toolboxPopArrows(button):
        # determines if arrow buttons should be enabled or disabled - might change to up and down
        global toolboxpop_ub_enabled
        global toolboxpop_db_enabled

        # check if we have more than 5 items in toolbox (5 is max)
        if len(toolboxpop_sprites) > 2:
            citem = "" # current item

            # iterate through toolbox items
            for i, item in enumerate(toolboxpop_sprites):
                # up button 
                if button == "down" and toolboxpop_db_enabled == True:
                    # if last item not visible meaning we have at least 1 extra item
                    if toolboxpop_sprites[-1].visible == False:
                        # shift toolbox items up
                        item.y -= toolbox_slot_size[0] + toolboxpop_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = item
                elif button == "up" and toolboxpop_ub_enabled == True:
                    if toolboxpop_sprites[0].visible == False:
                        reversed_index = (len(toolboxpop_sprites) - 1) - i
                        toolboxpop_sprites[reversed_index].y += toolbox_slot_size[0] + toolboxpop_slot_padding # MODIFIED TO BE BASED OFF TOOL SLOT SIZE INSTEAD OF SIZE OF IMAGE
                        item.origial_y = item.y # ADDED CODE
                        citem = toolboxpop_sprites[reversed_index]
                # checks if item was moved beyond first or beyond last item in toolbox slots
                if citem != "" and (citem.y < toolboxpop_first_slot_y or citem.y > (toolboxpop_first_slot_y + (citem.height * 2)) + (toolboxpop_slot_padding * 1)):
                    setItemVisibility(item = citem, visible = False)

                elif citem != "": # prevent errors
                    setItemVisibility(item = citem, visible = True)

            if toolboxpop_sprites[-1].visible == True:
                toolboxpop_db_enabled = False
            else:
                toolboxpop_db_enabled = True
            if toolboxpop_sprites[0].visible == True:
                toolboxpop_ub_enabled = False
            else:
                toolboxpop_ub_enabled = True
                
            if citem != "":
                toolboxpop_SM.redraw(0)
                renpy.restart_interaction

    """
    Controls item visibility in the toolbar.

    Takes in an item and boolean controlling item's visibility (visible).
    """
    def setItemVisibility(item, visible):
        if visible == False:
            item.visible = False
            t = Transform(child = item.item_image, zoom = 0.5, alpha = 0)
            item.set_child(t)
        else:
            item.visible = True
            t = Transform(child = item.item_image, zoom = 0.5, alpha = 100)
            item.set_child(t)
        inventory_SM.redraw(0)
        toolbox_SM.redraw(0)
        toolboxpop_SM.redraw(0)

# INVENTORY SCREENS ------------------------- (might move to custom_screens)

"""
Sets up inventory screen when player enters.
"""
screen full_inventory:
    zorder 1
    image "UI/inv-icon-bg.png" xpos 0.014 ypos -0.03 at half_size
    imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= [Show("inventory"), Hide("toolbox"), Hide("toolboxpop")], false= [Hide("inventory"), Hide("toolboxpop")]) xpos 0.087 ypos 0.02 at half_size
    imagebutton auto "UI/tool-inventory-icon-%s.png" action If(renpy.get_screen("toolbox") == None, true= [Show("toolbox"), Hide("inventory")], false= [Hide("toolbox"), Hide("toolboxpop")]) xpos 0.037 ypos 0.02 at half_size

# evidence:
screen inventory:
    zorder 3
    image "UI/inventory-bg.png" xpos 0.02 ypos 0.09 at half_size
    image "UI/inventory-slots.png" xpos 0.047 ypos 0.25 at half_size
    imagebutton idle If(inventory_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(inventory_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(inventoryArrows, button = "down") xpos 0.063 ypos 0.89 at half_size
    imagebutton idle If(inventory_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(inventory_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(inventoryArrows, button = "up") xpos 0.063 ypos 0.15 at half_size
    add inventory_SM

# toolbox:
screen toolbox:
    zorder 3
    image "UI/tools-bg.png" xpos 0.02 ypos 0.09 at half_size
    image "UI/inventory-slots.png" xpos 0.047 ypos 0.25 at half_size
    imagebutton idle If(toolbox_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(toolbox_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(toolboxArrows, button = "down") xpos 0.063 ypos 0.89 at half_size
    imagebutton idle If(toolbox_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(toolbox_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(toolboxArrows, button = "up") xpos 0.063 ypos 0.15 at half_size
    add toolbox_SM

# toolbox pop-up:
screen toolboxpop:
    zorder 3
    image "UI/toolboxpop-bg.png" xpos 0.13 ypos 0.28 at half_size
    image "UI/toolboxpop-slots.png" xpos 0.1415 ypos 0.41 at half_size
    imagebutton idle If(toolboxpop_db_enabled == True, true= "UI/inventory-arrow-down-enabled-idle.png", false= "UI/inventory-arrow-down-disabled.png") hover If(toolboxpop_db_enabled == True, true= "UI/inventory-arrow-down-enabled-hover.png", false= "UI/inventory-arrow-down-disabled.png") action Function(toolboxPopArrows, button = "down") xpos 0.157 ypos 0.73 at half_size
    imagebutton idle If(toolboxpop_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-idle.png", false= "UI/inventory-arrow-up-disabled.png") hover If(toolboxpop_ub_enabled == True, true= "UI/inventory-arrow-up-enabled-hover.png", false= "UI/inventory-arrow-up-disabled.png") action Function(toolboxPopArrows, button = "up") xpos 0.157 ypos 0.32 at half_size
    add toolboxpop_SM

# evidence box item menu
screen inventoryItemMenu(item):
    zorder 7
    frame:
        xysize (inventory_slot_size[0], inventory_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("inventoryItemMenu")]
        imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(startDrag, item = item), Hide("inventoryItemMenu")]
        # imagebutton auto "UI/expand-inventory-item-%s.png" align (2.0, 0.5) at half_size action If(renpy.get_screen("toolboxpop") == None, true= Show("toolboxpop"), false= Hide("toolboxpop")) 

# toolbox item menu
screen toolboxItemMenu(item):
    zorder 7
    frame:
        xysize (toolbox_slot_size[0], toolbox_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("toolboxItemMenu")]
        # MODIFIED SO ONLY ALS LIGHTS HAVE THE EXPAND OPTION
        if item.type == "als_flashlights":
            imagebutton auto "UI/expand-inventory-item-%s.png" align (1.0, 0.5) at half_size action If(renpy.get_screen("toolboxpop") == None, true= Show("toolboxpop"), false= Hide("toolboxpop")) 
        else:
            imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(startDrag2, item = item), Hide("toolboxItemMenu")]

# toolbox pop-up item menu
screen toolboxPopItemMenu(item):
    zorder 7
    frame:
        xysize (toolboxpop_slot_size[0], toolboxpop_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("toolboxPopItemMenu")]
        imagebutton auto "UI/use-inventory-item-%s.png" align (1.0, 0.5) at half_size action [Function(startDrag3, item = item), Hide("toolboxPopItemMenu")]

"""
Controls item inspection (when player clicks info button on an item for closer inspection).

Takes in a list of items.
"""
screen inspectItem(items):
    modal True
    zorder 54
    button:
        xfill True
        yfill True
        action If(len(items) > 1, true = RemoveFromSet(items, items[0]), false= [Hide("inspectItem"), If(len(dialogue) > 0, true= Show("characterSay"), false= NullAction())])
        image "Items Pop Up/items-pop-up-bg.png" align (0.5, 0.55) at half_size

        python:
            item_name = ""
            item_desc = ""
            for name in inventory_item_names:
                temp_name = name.replace(" ", "-")
                temp_name = name.replace(" ", "_")
                if temp_name.lower() == items[0]:
                    item_name = name

        text "{}".format(item_name) size 30 align (0.5, 0.65) color "#000000"
        if items[0] == "lantern":
            $lantern_state = inventory_sprites[inventory_items.index("lantern")].state
            image "Items Pop Up/{}-{}-pop-up.png".format("lantern", lantern_state) align (0.5, 0.5) at half_size
        else:
            image "Items Pop Up/{}-pop-up.png".format(items[0]) align (0.5, 0.5) at half_size

"""
Displays dialogue box.
"""
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
    if what is None:
        key "K_SPACE" action If(len(dialogue["what"]) > 1, true= RemoveFromSet(dialogue["what"], dialogue["what"][0]), false= [Hide("characterSay"), SetVariable("dialogue", {}), If(jump_to is not None, true = Jump("{}".format(jump_to)), false = NullAction())])
    else:
        key "K_SPACE"action [Return(True), If(jump_to is not None, true = Jump("{}".format(jump_to)), false = NullAction())]


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

screen scene1:
    add environment_SM