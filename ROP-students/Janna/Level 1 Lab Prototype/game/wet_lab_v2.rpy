init python:
    tool = ""

    class Bowl:
        """A custom data type that represents the bowl in the DFO mixture process.
        Can only be in one of four states: 0, 1/4, 1/2, 3/4, 1."""
        state: float
        added_methanol: bool
        added_dfo: bool
        added_acetic_acid: bool
        added_hfe: bool
        image: str

        def __init__(self) -> None:
            self.state = 0
            self.added_methanol = False
            self.added_dfo = False
            self.added_acetic_acid = False
            self.added_hfe = False
            self.image = "mixing bowl"
        
        def completed(self) -> bool:
            return self.added_methanol and self.added_dfo and self.added_acetic_acid and self.added_hfe
        
        def update_image(self) -> None:
            if self.image == "mixing bowl":
                self.image = "mixing bowl one third"
            elif self.image == "mixing bowl one third":
                self.image = "mixing bowl one half"
            elif self.image == "mixing bowl one half":
                self.image = "mixing bowl full"
        
        def update_state(self) -> None:
            self.state += 0.25
            if tool != "dfo":
                self.update_image()
    
    bowl = Bowl()

screen toolbox_dfo_v2():
    zorder 1
    hbox:
        xpos 0.86 ypos 0
        imagebutton:
            # sensitive methanol.available
            idle "methanol" at Transform(zoom=0.5)
            action [SetVariable("tool", "methanol"), Jump("pour_methanol")]
            
    hbox:
        xpos 0.89 ypos 0.27
        imagebutton:
            # sensitive dfo.available
            idle "dfo" at Transform(zoom=0.6)
            action [SetVariable("tool", "dfo"), Jump("pour_dfo")]
            
    hbox:
        xpos 0.86 ypos 0.45
        imagebutton:
            # sensitive acetic_acid.available
            idle "acetic acid" at Transform(zoom=0.6)
            action [SetVariable("tool", "acetic acid"), Jump("pour_acetic_acid")]

    hbox:
        xpos 0.88 ypos 0.72
        imagebutton:
            # sensitive hfe.available
            idle "hfe" at Transform(zoom=0.5)
            action [SetVariable("tool", "hfe"), Jump("pour_hfe")]

screen graduated_cyllinder:
    imagebutton auto "graduated cyllinder %s" at cyllinder action Jump("cyllinder_animation")

transform cyllinder:
    zoom 2.3
    rotate 0
    xpos 0.55
    ypos 0.58
    xanchor 0.5
    yanchor 0.5

transform cyllinder_rotated:
    zoom 2.3
    rotate 250
    xpos 0.45
    ypos 0.45
    xanchor 0.5
    yanchor 0.5

transform methanol:
    zoom 1.5
    rotate 0
    xpos 0.7
    ypos 0.58
    xanchor 0.5
    yanchor 0.5

transform methanol_rotated:
    zoom 1.5
    rotate 300
    xpos 0.69
    ypos 0.36
    xanchor 0.5
    yanchor 0.5

transform dfo:
    rotate 0
    xpos 0.69
    ypos 0.65
    xanchor 0.5
    yanchor 0.5

transform dfo_rotated:
    rotate 250
    xpos 0.5
    ypos 0.36
    xanchor 0.5
    yanchor 0.5

transform acetic_acid:
    zoom 1.2
    rotate 0
    xpos 0.73
    ypos 0.68
    xanchor 0.5
    yanchor 0.5

transform acetic_acid_rotated:
    zoom 1.2
    rotate 300
    xpos 0.68
    ypos 0.34
    xanchor 0.5
    yanchor 0.5

transform hfe:
    zoom 1.3
    rotate 0
    xpos 0.75
    ypos 0.62
    xanchor 0.5
    yanchor 0.5

transform hfe_rotated:
    zoom 1.3
    rotate 300
    xpos 0.73
    ypos 0.36
    xanchor 0.5
    yanchor 0.5

label fumehood_label_v2:
    hide screen casefile_physical
    hide screen ui

    if bowl.completed():
        "We've already done everything we can."
        jump materials_lab
    else:
        if oven.state == "off":
            "Let's preheat the oven first before we do anything."
            hide dfo_bottle_opened
            hide dfo bottle
            jump materials_lab

        "Let's begin mixing the DFO!"
        hide screen back_button_screen
        show mixing bowl at Transform(zoom=1.3, xpos=0.34, ypos=0.4)
        call screen toolbox_dfo_v2

label check_for_completion:
    python:
        if bowl.completed():
            renpy.say(None, "We've finished creating the DFO mixture.")
            renpy.say(None, "Let's dip our label inside.")
            renpy.movie_cutscene("images/materials_lab/wet_lab/label_dipping.webm")
            label.dipped = True
            renpy.say(None, "This label is ready to be baked!")

            if oven.state == "preheating":
                renpy.say(None, "Looks like the oven is finished preheating.")
                oven.update_state()
                renpy.say(None, "Let's check on it.")

            renpy.jump("materials_lab")
        else:
            renpy.call_screen("toolbox_dfo_v2")

label cyllinder_animation:
    pause(0.5)
    show graduated cyllinder idle at cyllinder_rotated with ease
    pause(0.5)
    show graduated cyllinder idle at cyllinder
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.15, ypos=0.4)])
    jump check_for_completion

label pour_methanol:
    if bowl.added_methanol:
        "We already added methanol."
        call screen toolbox_dfo_v2
    hide acetic acid
    hide hfe
    hide dfo
    # show mixing bowl at Transform(zoom=1.3, xpos=0.15, ypos=0.4)
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.15, ypos=0.4)])
    show graduated cyllinder idle at cyllinder
    show methanol at methanol
    pause(0.5)
    show methanol at methanol_rotated with ease
    pause(0.5)
    show methanol at methanol with ease
    $ bowl.added_methanol = True
    $ bowl.update_state()
    jump cyllinder_animation    

label pour_dfo:
    if bowl.added_dfo:
        "We already added DFO."
        call screen toolbox_dfo_v2
    hide graduated cyllinder idle
    hide methanol
    hide acetic acid
    hide hfe
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.25, ypos=0.4)])
    show dfo at dfo with ease
    pause(1.0)
    show dfo at dfo_rotated with ease
    pause(1.0)
    show dfo at dfo with ease
    pause(1.0)
    $ bowl.added_dfo = True
    $ bowl.update_state()
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.25, ypos=0.4)])
    jump check_for_completion

label pour_acetic_acid:
    if bowl.added_acetic_acid:
        "We already added acetic acid."
        call screen toolbox_dfo_v2
    hide methanol
    hide hfe
    hide dfo
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.15, ypos=0.4)])
    show graduated cyllinder idle at cyllinder
    show acetic acid at acetic_acid
    pause(1.0)
    show acetic acid at acetic_acid_rotated with ease
    pause(1.0)
    show acetic acid at acetic_acid with ease
    $ bowl.added_acetic_acid = True
    $ bowl.update_state()
    jump cyllinder_animation   

label pour_hfe:
    if bowl.added_hfe:
        "We already added HFE."
        call screen toolbox_dfo_v2
    hide methanol
    hide acetic acid
    hide dfo
    $ renpy.show(name=bowl.image, at_list=[Transform(zoom=1.3, xpos=0.15, ypos=0.4)])
    show graduated cyllinder idle at cyllinder
    show hfe at hfe with ease
    pause(1.0)
    show hfe at hfe_rotated with ease
    pause(1.0)
    show hfe at hfe with ease
    $ bowl.added_hfe = True
    $ bowl.update_state()
    jump cyllinder_animation   
