"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Name: Timothy Eng (te76)
Date Completed: December 08, 2017
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
   
    _direction: The direction to move the Aliens after hitting the border [string, either 'left' or 'right']
    lastkeys:   the number of keys pressed last frame
                [int >= 0]
    _stepsAlienShoot: the number of steps until an Alien returns fire to the ship
                [int in range 1..BOLT_RATE]
    _alienSpeed: the alien speed, used in determining walking for aliens [int or float]
    _score: the score [int]
    _scoreLabel: the score label [GLabel]
    _TIE_Sound: the TIE fighter shooting sound file [Sound object]
    _XWing_Sound: the X-Wing shooting sound file [Sound object]
    _last: attribute T/F used in mute.
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Standard initializer, which initializes the Ship and Aliens for the game.
        Also creates the defense line near the bottom of the screen.
        Also initializes all the different attributes:
       
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
        
        _direction: The direction to move the Aliens after hitting the border [string, either 'left' or 'right']
        lastkeys:   the number of keys pressed last frame
                [int >= 0]
        _stepsAlienShoot: the number of steps until an Alien returns fire to the ship
                [int in range 1..BOLT_RATE]
        _alienSpeed: the alien speed, used in determining walking for aliens [int or float]
        _score: the score [int]
        _scoreLabel: the score label [GLabel]
        _TIE_Sound: the TIE fighter shooting sound file [Sound object]
        _XWing_Sound: the X-Wing shooting sound file [Sound object]
        """
        #print('Initializing Aliens')
        self._aliens = self._fillAlienArray()
        #print('aliens stored in init')
        
        #print('Initializing Ship')
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM, SHIP_WIDTH, SHIP_HEIGHT, 'X_Wing.png')
        
        #print('Creating defense line')
        self._dline = GPath(points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE], linewidth = 2, linecolor = 'yellow')
        
        #print('Creating time, bolts, and lives')
        self._time = 0
        
        self._bolts = []
        self._bolts.insert(0, None)
        
        self._lives = SHIP_LIVES
        self.lastkeys = 0
        
        self._steps_Alien_Fire()#self._stepsAlienShoot = 0
        self._direction = 'right'
        
        self._labelLives = GLabel(text = 'Fighters left in Red Squadron: ' + str(self._lives), \
                                  font_name = 'Arcade.ttf', font_size = 20, \
                                  x = 625, y = 625, linecolor = 'yellow')
    
        self._alienSpeed = ALIEN_SPEED
        
        self._last = False
        self._TIE_Sound = Sound('TIE_Shoot.wav')
        self._XWing_Sound = Sound('XWing_Shoot.wav')
        
        self._score = START_SCORE
        self._scoreLabel = GLabel(text = 'Kill count: ' + str(self._score), \
                                  font_name = 'Arcade.ttf', font_size = 30,\
                                  x = 100, y = 625, linecolor = 'yellow')
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, key_input, dt):
        """
        Animates a single frame in the wave.
        This will animate (every frame) the ship, the aliens and their laser bolts.
        
        Parameter key_input: the input from the controller class, which
        tells the ship which direction to move. Also used for firing bolts, and
        helping with EXTENSION 2.
        Precondition: key_input is a valid GInput object.
        
        Parameter dt: counts the number of seconds that have passed since the
        last animation frame (at 60 frames as second, it is somewhere around
        0.017 seconds each time). Is the value used for summing and adding to
        the attribute _time.
        Precondition: dt is an int or float
        """
        assert isinstance(key_input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)
        
        #print(str(self._bolts))
        #print(str(self._aliens))
        #print(str(self._ship))
        #print(dt)
        
        self._moveShip(key_input)
        self._move_Aliens_Main(key_input, dt)
        self._main_Ship_Bolt_Helper(key_input)
        self._move_Alien_Bolts(key_input)
        self._check_Alien_Collision()
        self._check_Ship_Collision()
        
        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondtion: view is a valid GView object.
        """
        assert isinstance(view, GView)
        
        self._draw_labelLives(view)
        self._draw_scoreLabel(view)
        self._drawAliens(view)
        self._drawShip(view)
        self._dline.draw(view)
        self._draw_Ship_Bolt(view)
        self._draw_Alien_Bolts(view)
        
            
    """ALL HELPER METHODS BELOW"""
    
    # ALL SHIP HELPERS
    
    # Helper to return self._ship (used in app.py)
    def get_Ship(self):
        """
        Helper for returning self._ship, used in app.py.
        Suggested by Caleb Berman (ckb65).
        I forgot at first that app.py could not acess self._ship because it is a
        private attribute.
        """
        return self._ship
    
    # Helper to set ship (ONLY USED IN app.py)
    def set_Ship(self):
        """
        Helper that makes a new ship, used in app.py.
        """
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM, SHIP_WIDTH, SHIP_HEIGHT, 'X_Wing.png')
        
    # Helper to return self._lives (used in app.py)
    def get_Lives(self):
        """
        Helper for returning self._lives, used in app.py.
        Suggested by Caleb Berman (ckb65).
        I forgot at first that app.py could not acess self._lives because it is a
        private attribute.
        """
        return self._lives
        
    # SHIP MOVEMENT HELPERS
    
    #Main Ship movement helper
    def _moveShip(self, ship_input):
        """
        Moves the ship based on key input.
        If ship goes beyond the boundary of the game fram then it is reset
        so that it does not go beyond and stays at the edge.
        
        This helper is called by update every animation frame.
        
        Parameter ship_input: the input from the controller class, which
        tells the ship which direction to move.
        Precondition: ship_input is a valid GInput object.
        
        EXTENSION #2: KEY MODIFIERS:
            - IF THE LEFT SHIFT KEY IS HELD DOWN, THE SHIP MOVES AT x2 SPEED.
            - IF THE LEFT CONTROL KEY IS HELD DOWN, THE ALIENS MOVE AT x2 SPEED.
            - IF THE TAB KEY IS HELD DOWN, THE BOLTS MOVE AT x2 SPEED.
            * BELOW: SHIP x2 SPEED (shift)
        """
        assert isinstance(ship_input, GInput)
        
        if self._ship is not None:
            pos = self._is_ship_moving(ship_input)
            
            if ship_input.is_key_down('shift') or ship_input.is_key_down('rshift'):
                self._ship.x += 2 * pos
            else:
                self._ship.x += pos
        
            #print('ship position is ' + str(self._ship.x))
        
            if self._ship.x > GAME_WIDTH:
                self._ship.x = 800
            if self._ship.x < 0:
                self._ship.x = 0
                        
    # Helper for Ship movement, determines direction to move towards
    # USING CODE FROM ARROWS.PY SAMPLE CODE, provided by Prof. White.
    def _is_ship_moving(self, ship_input):
        """
        Determines whether or not the appropiate keys are being pressed to tell
        the ship to move.
        
        If left is pressed the ship will move left. If right
        is pressed the ship will move right.
        
        This method will help determine how much to move the ship;
        it is called in the moveShip helper.
        
        Parameter ship_input: the input from the controller class, which
        tells the ship which direction to move.
        Precondition: ship_input is a valid GInput object.
        """
        assert isinstance(ship_input, GInput)
        
        dx = 0
        if ship_input.is_key_down('left'):
            dx -= SHIP_MOVEMENT
        if ship_input.is_key_down('right'):
            dx += SHIP_MOVEMENT
        
        return dx


    #SHIP BOLT HELPERS
    
    # Main Ship Bolt Helper
    def _main_Ship_Bolt_Helper(self, ship_input):
        """
        Main Helper function for creating and moving ship's bolt.
        Also makes sure that there is only on ship bolt onscreeen at a time.
        
        Parameter ship_input: the input from the controller class.
        Precondition: ship_input is a valid GInput object
        """
        assert isinstance(ship_input, GInput)
        
        if self._ship is not None: 
            if (self._is_Player_Bolt_Fired(ship_input) and self._ship.shipShoot()):
                #print('Making Ship Bolt')
                self._XWing_Sound.play()
                self._make_Ship_Bolt(ship_input)
                #print(str(self._bolts[0]))
                self._ship.setShipShoot(False)
            if ((self._bolts[0] is not None) and self._bolts[0].isPlayerBolt()):
                if self._bolts[0].y >= GAME_HEIGHT:
                    self._bolts.remove(self._bolts[0])
                    self._bolts.insert(0, None)
                    self._ship.setShipShoot(True)
                else:
                    self._move_Ship_Bolt(ship_input)
             
    # Helper that determines if ship fires a bolt
    def _is_Player_Bolt_Fired(self, ship_input):
        """
        Similar to determineState in app.py, this method checks to see if fire
        button (default is space), see constant BOLT_BUTTON.
        
        This method checks for a key press, and if there is one, then the fire
        button is being pressed.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the ship to continue firing as we hold down the key. The
        user must release the key and press it again to fire again.
        
        Another different method will check to prevent more than one bolt from
        being on the screen at the same time.
        
        If button is pressed, return True. Otherwise returns False. 
        
        Parameter ship_input: the input from the controller class.
        Precondtion: ship_input is a valid GInput object.
        """
        assert isinstance(ship_input, GInput)
        
        # Determine the current number of keys pressed
        curr_keys = ship_input.is_key_down(BOLT_BUTTON) #self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys and self.lastkeys == False
        
        if change:
            # Click happened. Bolt has been fired.
            return True
        
        return False
    
    # Helper that makes the bolt for the ship
    def _make_Ship_Bolt(self, ship_input):
        """
        Helper function creates a new ship Bolt.
        
        Does not check to see if ship button has been pressed because this method is
        only called if the button is pressed.
        
        Also changes the Bolt's attribute that checks if player bolt to true.
        
        Basically, self._bolts[0] is always either None or a ship bolt. This method just
        creates a bolt and reassigns self._bolts[0].
        
        Parameter ship_input: input from the keyboard, is received from call to wave's update()
        in the update() of app.py.
        Precondtion: ship_input is a valid GInput object
        """
        assert isinstance(ship_input, GInput)
    
        ship_bolt = Bolt(self._ship.x, (self._ship.y + (SHIP_HEIGHT/2)), BOLT_WIDTH, BOLT_HEIGHT, 'red', 100)
        
        #print('Ship Bolt created')
        
        ship_bolt.setPlayerBolt(True)
        ship_bolt.setPlayerBoltFired(True)
        #print('Bolt set to is Bolt True')
        
        #if len(self._bolts) == 0:
        #    self._bolts.append(ship_bolt)#; print('Ship Bolt added to _bolts')
    
        #else:
        self._bolts[0] = ship_bolt#; print('Ship Bolt added to _bolts')
        
    # Helper that moves the ship's bolt
    def _move_Ship_Bolt(self, ship_input):
        """
        Helper that moves the ship's bolt by velocity.
        Checks to see if first bolt in list is ship bolt.
        It is only called if first element in bolts list is ship bolt so don't
        have to check if ship bolt.

        EXTENSION #2: KEY MODIFIERS:
            - IF THE LEFT SHIFT KEY IS HELD DOWN, THE SHIP MOVES AT x2 SPEED.
            - IF THE LEFT CONTROL KEY IS HELD DOWN, THE ALIENS MOVE AT x2 SPEED.
            - IF THE TAB KEY IS HELD DOWN, THE BOLTS MOVE AT x2 SPEED.
            * BELOW: BOLTS x2 SPEED FOR SHIP, ALIEN BOLTS x2 ADDRESSED IN DIFFERENT METHOD. (tab)
            
        Parameter ship_input: the input from the controller class, used in EXTENSION 1 here.
        Precondition: ship_input is a valid GInput object.
        """
        assert isinstance(ship_input, GInput)
        
        ship_bolt = self._bolts[0]
        if ship_bolt.playerBoltFired() == True:
            
            #double speed and will hit top, most restrictive case
            if ship_input.is_key_down('tab') and ship_bolt.y + 2 * ship_bolt.velocity() > GAME_HEIGHT:
                ship_bolt.y = GAME_HEIGHT#; print(str(ship_bolt.x) + ', ' + str(ship_bolt.y))
                
            #double speed 
            elif ship_input.is_key_down('tab'):
                ship_bolt.y += 2 * ship_bolt.velocity()#; print(str(ship_bolt.x) + ', ' + str(ship_bolt.y))
                
            #normal but will hit top
            elif ship_bolt.y + 2 * ship_bolt.velocity() > GAME_HEIGHT:
                ship_bolt.y = GAME_HEIGHT#; print(str(ship_bolt.x) + ', ' + str(ship_bolt.y))
            
            else: #normal case
                ship_bolt.y += ship_bolt.velocity()#; print(str(ship_bolt.x) + ', ' + str(ship_bolt.y))
                        
    # Helper that checks for player bolt
    def _check_For_Player_Bolt(self):
        """
        Helper that iterates over every bolt in the list.
        If one of the bolt's attributes isPlayerBolt is True,
        no more player bolts can be made (player can't fire).
        Usually, to help with this, the player bolt is always the first bolt
        in the list. This allows the method to run faster.
        """
        for bolt in range(len(self._bolts)):
            if bolt.isPlayerBolt() == True:
                return False
        
        return True
        
        
    
    # ALL ALIEN HELPERS
    
    #HELPER FOR SETTING ALIEN LIST
    def _fillAlienArray(self):
        """
        Returns: a list of Aliens.
        
        Iterates over number of aliens and depending on row and column and
        number of row and columns specified in consts.py, will set these to a list.
        
        Iterates starting at bottommost row and works its way to the top.
        
        Also keeps track of which alien to draw depending on how many rows have
        been iterated over.
        
        For reference, I originally tried this but didn't work because I was doing too much in
        the for loop's range() so I did computations separately. (Suggested by multiple consultants).
        
        for rows in range(rowstart, ALIEN_ROWS, (ALIEN_V_SEP + ALIEN_HEIGHT)):
            print('iterating cols')
            rowlist = []
            for cols in range(ALIEN_H_SEP, ALIENS_IN_ROW * (ALIEN_WIDTH + ALIEN_H_SEP), (ALIEN_H_SEP + ALIEN_WIDTH)):
                
                #if count > numaliens:
                #    count = 0
                print('storing alien')
                rowlist = [cols] = Alien(rows, cols, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_IMAGES[count])
                print(str(row) + ' ' + str(col))
                if rows % 2 == 1:
                    count += 1
                    count = count % numaliens
                    
            aliens[row] = rowlist
            
        
        """
        
        aliens = []
        count = 0
        numaliens = len(ALIEN_IMAGES)
        rowstart = GAME_HEIGHT - (ALIEN_CEILING + ALIEN_ROWS * (ALIEN_HEIGHT + ALIEN_V_SEP) - ALIEN_V_SEP)

        for cols in range(ALIENS_IN_ROW):
            c = (ALIEN_WIDTH + ALIEN_H_SEP) * cols + 2 * ALIEN_H_SEP
        
            sublist = []
            
            for rows in range(ALIEN_ROWS):
                r = (ALIEN_HEIGHT + ALIEN_V_SEP) * rows + rowstart
                
                alien = Alien(c, r, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_IMAGES[count])
                alien.setScoreValue(count + 1)
                alien.setTIELevel(count + 1)#; print(alien.getTIELevel())
                sublist.append(alien)
                
                if rows % 2 == 1:
                    count += 1
                    count = count % numaliens
            
            count = 0
                    
            aliens.append(sublist)
            
            
        return aliens
    
    
    # ALIEN MOVEMENT HELPERS
    
    #Main Alien movement helper
    def _move_Aliens_Main(self, key_input, dt):
        """
        Main helper that moves the aliens.
        Determines when to move aliens based on the time that has passed.
        
        At the start, and each time the aliens move, _time it is reset to 0.
        The setting of _time to 0 is taken care of in update().
        
        Then, add the number of seconds that have passed to _time,
        and do not move the aliens. When _time is bigger than ALIEN_SPEED,
        move the aliens again.
        
        If the aliens move beyond the border of the game's frame, reset position
        and move them down and then to the left. 
        
        Parameter key_input: the input from the controller class.
        Precondition: key_input is a valid GInput
        
        Parameter dt: counts the number of seconds that have passed since the
        last animation frame (at 60 frames as second, it is somewhere around
        0.017 seconds each time). Is the value used for summing and adding to
        the attribute _time.
        Precondition: dt is a int or float
        
        EXTENSION #2: KEY MODIFIERS:
            - IF THE LEFT SHIFT KEY IS HELD DOWN, THE SHIP MOVES AT x2 SPEED.
            - IF THE LEFT CONTROL KEY IS HELD DOWN, THE ALIENS MOVE AT x2 SPEED.
            - IF THE TAB KEY IS HELD DOWN, THE BOLTS MOVE AT x2 SPEED.
            * IN BELOW FUNCTION: ALIEN x2 SPEED (lctrl)
        """
        assert isinstance(key_input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)
        
        self._time += dt
        
        if key_input.is_key_down('lctrl') or key_input.is_key_down('rctrl'):
            if self._time > self._alienSpeed/2 and self._direction == 'right':
                self._check_Alien_Fire()
                #self._move_Aliens_Down_Main()
                self._move_Aliens_Right()
                self._time = 0
            
            if self._time > self._alienSpeed/2 and self._direction == 'left':
                self._check_Alien_Fire()
                #self._move_Aliens_Down_Main()
                self._move_Aliens_Left()
                self._time = 0
            
        else:
            if self._time > self._alienSpeed and self._direction == 'right':
                self._check_Alien_Fire()
                #self._move_Aliens_Down_Main()
                self._move_Aliens_Right()
                self._time = 0
            
            if self._time > self._alienSpeed and self._direction == 'left':
                self._check_Alien_Fire()
                #self._move_Aliens_Down_Main()
                self._move_Aliens_Left()
                self._time = 0
            
        #print(str(self._direction))
        
        self._move_Aliens_Down_Main()
               
    #Alien directional helper: to the right
    def _move_Aliens_Right(self):
        """
        Helper that moves all the aliens to the right by ALIEN_H_WALK.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x += ALIEN_H_WALK
        
    #Alien directional helper: to the left
    def _move_Aliens_Left(self):
        """
        Helper that moves all the aliens to the left by -ALIEN_H_WALK.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x -= ALIEN_H_WALK
    
    #Alien directional helper: main helper for down
    def _move_Aliens_Down_Main(self):
        """
        Helper function that moves the Aliens down based on which border it hits.
        
        If the aliens hit the border, move all the aliens down.
        To do this it calls the _move_Aliens_down() helper.
        
        The only time the the aliens move down is if they hit the border.
        Thus it will make use of _move_Aliens_Right() or _move_Aliens_Left(),
        to reset the Aliens in order to prevent them from going over the edge.
        
        It will then set the _direction attribute to the respective direction it
        should move next.
        """
        
        if self._rightmost_Alien_pos() >= GAME_WIDTH:
            
            self._move_Aliens_Left()
            self._move_Aliens_Down_Helper()
            self._direction = 'left'
            
        if self._leftmost_Alien_pos() <= 0:
            
            self._move_Aliens_Right()
            self._move_Aliens_Down_Helper()
            self._direction = 'right'
        
        else:
            pass
            
    #Alien directional helper: helper for main move down method           
    def _move_Aliens_Down_Helper(self):
        """
        Helper that moves all the aliens down by ALIEN_V_WALK.
        Called in _move_Aliens_Down_Main().
        """
        
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.y += -ALIEN_V_WALK
    
    # Rightmost alien helper
    def _rightmost_Alien_pos(self):
        """
        Helper that determines the rightmost Alien's position.
        
        This helper is used in determining when to move the aliens down if they
        hit the righthand border of the frame.
        
        Checks to see which columns have at least 1 alien, and returns rightmost element.
        """
        
        #List of all columns indexs in self._aliens that are not empty
        non_empty_cols = self._check_Alien_cols()#; print(str(non_empty_cols))
        
        # Index of rightmost non-empty column
        rightmostAlienListPos = len(non_empty_cols)#; print('Rightmost alien col ' + str(rightmostAlienListPos))
        
        # Rightmost non-empty column
        rightmostAlienList = self._aliens[rightmostAlienListPos - 1]#; print('Rightmost alien col ' + str(rightmostAlienListPos) + ' all aliens: ' + str(rightmostAlienList))
        
        # First alien pos in rightmost non-empty column 
        rightmostAlienPos = self._lowest_Alien_Pos(rightmostAlienList)#; print('Rightmost alien pos ' + str(rightmostAlienPos))
        
        # First alien in rightmost non-empty column
        rightmostAlien = rightmostAlienList[rightmostAlienPos]#; print(str(rightmostAlien))
        
        #rightmost border of the rightmost alien in bottom row
        #print('Rightmost border ' + str(rightmostAlien.x + ALIEN_WIDTH/2))
        #return rightmostAlien.x + ALIEN_WIDTH/2 
        return rightmostAlien.right
        
    # Leftmost Alien helper
    def _leftmost_Alien_pos(self):
        """
        Helper that determines the leftmost Alien's position.
        
        This helper is used in determining when to move the aliens down if they
        hit the lefthand border of the frame.
        """
        
        #List of all columns indexes in self._aliens that are not empty
        non_empty_cols = self._check_Alien_cols()#; print(str(non_empty_cols))
        
        # Index of leftmost non-empty column
        leftmostAlienListPos = non_empty_cols[0]#; print('Leftmost alien col ' + str(leftmostAlienListPos))
        
        # Leftmost non-empty column
        leftmostAlienList = self._aliens[leftmostAlienListPos]#; print('Leftmost alien col ' + str(leftmostAlienListPos) + ' all aliens: ' + str(leftmostAlienList))
        
        # First alien pos in leftmost non-empty column 
        leftmostAlienPos = self._lowest_Alien_Pos(leftmostAlienList)#; print('Leftmost alien pos ' + str(leftmostAlienPos))
        
        # First alien in leftmost non-empty column
        leftmostAlien = leftmostAlienList[leftmostAlienPos]#; print(str(leftmostAlien))
        
        #leftmost border of the leftmost alien in bottom row
        #print('Leftmost border ' + str(leftmostAlien.x + ALIEN_WIDTH/2))
        #return leftmostAlien.x - ALIEN_WIDTH/2
        return leftmostAlien.left
        
        
    # ALIEN BOLT HELPERS
        
    # Helper that helps determine random number of steps until an Alien fires
    def _steps_Alien_Fire(self):
        """
        Helper function that calculates the random number of steps until an Alien
        will fire at the ship.
        
        Uses the random module to pick a psuedo-random number.
        """
        randint = random.randrange(1, BOLT_RATE)
        self._stepsAlienShoot = randint
    
    # Helper that determines when have Alien fire, makes bolt
    def _check_Alien_Fire(self):
        """
        Helper method called in _move_Aliens_Main() that checks each time the aliens
        move whether or not the number of steps till an Alien shoots is 0.
        
        If it is 0, this method creates a new bolt and appends it to self._bolts.
        """
        #print('Steps before: ' + str(self._stepsAlienShoot));
        self._stepsAlienShoot -= 1#; print('Steps left after: ' + str(self._stepsAlienShoot))
        if self._stepsAlienShoot == 0:
            alien = self._pick_Random_Alien_Shooter()
            self._TIE_Sound.play()
            newAlienBolt = Bolt(alien.x + ALIEN_H_WALK, (alien.y - ALIEN_HEIGHT/2 - BOLT_HEIGHT/2),
                                BOLT_WIDTH, BOLT_HEIGHT, 'green', 10)
            newAlienBolt.set_velocity(-BOLT_SPEED)
            self._steps_Alien_Fire()
            self._bolts.append(newAlienBolt)#; print('Alien bolt created')
            if len(self._bolts) == 1:
                self._bolts.insert(0, None)

    # Helper that randomly picks an Alien to shoot a Bolt  
    def _pick_Random_Alien_Shooter(self):
        """
        Helper method that determines a random Alien to shoot a bolt from.
        
        Returns an alien in the list self._aliens.
        
        Called in the _check_Alien_Fire() method, and returned Alien's position is used
        in determining where to create a new Alien Bolt.
        """
        col_nums = self._check_Alien_cols()#; print('col_nums = ' + str(col_nums))
        rand_col = col_nums[random.randrange(len(col_nums))]#; print('rand_col = ' + str(rand_col))
        alien = self._lowest_Alien(rand_col)#; print('alien = ' + str(alien))
        
        return alien
        
    # Helper that keeps track of all columns that have Aliens (columns that are not all just None)    
    def _check_Alien_cols(self):
        """
        Helper method that returns the columns in the list of Aliens that are not empty.
        
        I use the all() function here, but redefine it for the None type.
        I found it when searching for an easy method to check type of each element of list.
        https://docs.python.org/3/library/functions.html#all
        
        Original solution for reference (didn't fully work):
        col = []
        
        for rows in range(ALIEN_ROWS):
            no_none = True
            for cols in range(ALIENS_IN_ROW):
                if self._aliens[rows[cols]] is None:
                    no_none = False
                    
            if no_none = True:
                col.append(rows)
                
        return col
        
        
        """
        cols = []
        
        for rows in range(ALIENS_IN_ROW):
            all_none = self._check_None(self._aliens[rows])
            if all_none == False:
                cols.append(rows)
        
        return cols
        
    # Helper that checks an iterable's type for None (variation on built in all() function)
    def _check_None(self, iterable):
        """
        Helper that return True if all elements of the iterable are None (or if the iterable is empty).
        
        Parameter iterable: an iterable (like a list, in this case a list)
        Precondition: iterable is an iterable, and in this case, a list
        """
        
        assert isinstance(iterable, list)
        
        for element in iterable:
            if not element is None:
                return False
        return True
            
    # Helper that finds the bottomost alien in a column
    def _lowest_Alien(self, col):
        """
        Returns bottommost Alien in a column.
        
        Parameter col: the randomly selected column.
        Precondition: col is an int, 0 <= col < len(self._aliens)
        """
        assert isinstance(col, int) and col >= 0 and col < len(self._aliens)
        
        column_list = self._aliens[col]#; print('Column list :' + str(column_list))
        pos = self._lowest_Alien_Pos(column_list)#; print('Pos : ' + str(pos))
        return column_list[pos] 
    
    # Helper that finds position of the bottomost alien in a column
    def _lowest_Alien_Pos(self, col):
        """
        Returns position of bottommost alien in a randomly selected column.
        
        Parameter col: the randomly selected column (a list).
        Precondition: col is a list of Aliens (one column in self._aliens).
        """
        assert isinstance(col, list)
        
        positions = []
        for spot in range(len(col)):
            if col[spot] is not None:
                positions.append(spot)
        
        bottommost_alien_pos = min(positions)
        
        #print('Returning bottommost alien pos ' + str(bottommost_alien_pos))
        return bottommost_alien_pos
    
    #Helper that moves the alien bolts across the screen.
    def _move_Alien_Bolts(self, key_input):
        """
        Helper that moves the Alien bolts by velocity.
        
        Parameter key_input: keyboard input, instance of GInput
        Precondition: key_input is a valid GInput object
        """
        assert isinstance(key_input, GInput)
      
        for bolt in range(len(self._bolts)):
            alien_bolt = self._bolts[bolt]#; print('checking if alien bolt')
            
            if alien_bolt is not None and alien_bolt.isPlayerBolt() == False:
                if alien_bolt.y <= 0:
                    self._bolts[bolt] = None #self._bolts.remove(alien_bolt)
                    
                elif alien_bolt.isPlayerBolt() == False and key_input.is_key_down('tab'):
                    if (alien_bolt.y + 2 * alien_bolt.velocity()) >= 0:
                        alien_bolt.y += 2 * alien_bolt.velocity()#; print('moved alien bolt to ' + str(alien_bolt.y))
                    else:
                        alien_bolt.y = 0#; print('moved alien bolt to ' + str(alien_bolt.y))
                    
                elif alien_bolt.isPlayerBolt() == False:
                    if alien_bolt.y + alien_bolt.velocity() >= 0:
                        alien_bolt.y += alien_bolt.velocity()#; print('moved alien bolt to ' + str(alien_bolt.y))
                    else:
                        alien_bolt.y = 0#; print('moved alien bolt to ' + str(alien_bolt.y))
        
        if len(self._bolts) >= 1:
            for bolt in range(len(self._bolts) - 1, 0, -1):
                if self._bolts[bolt] is None:
                    self._bolts.remove(self._bolts[bolt])     
    
    # Helper that determines if the aliens cross the defense line.        
    def crossed_Line(self):
        """
        Helper to determine if the Aliens cross the defense line.
        """
        for col in range(len(self._aliens)):
            for row in range(len(self._aliens[col])):
                if self._aliens[col][row] is not None and self._aliens[col][row].y <= DEFENSE_LINE:
                    return True
        
    # Helper that determines if the aliens are all destroyed.
    def allDead(self):
        """
        Helper to determine if the Aliens have all been destroyed.
        """
        for col in range(len(self._aliens)):
            for row in range(len(self._aliens[col])):
                if self._aliens[col][row] is not None:
                    return False
                
        return True 
        
    
    # DRAWING HELPERS
    
    # Helper that draws the Aliens to the game view.
    def _drawAliens(self, view):
        """
        Draws all the alien objects to the view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondtion: view is a valid GView object. (Do not need to assert, taken care of assertion in main draw() which calls it).
        """
        for row in self._aliens:
            #print(str(row))
            for alien in row:
                if alien is not None and isinstance(alien, Alien):
                    alien.draw(view)
     
    # Helper that draws the Ship to the game view.
    def _drawShip(self, view):
        """
        Draws the ship object to the view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondtion: view is a valid GView object. (Do not need to assert, taken care of assertion in main draw() which calls it).
        """
        if self._ship is not None:
            self._ship.draw(view)
    
    # Helper that draws the defense line to the game view. 
    def _drawDline(self, view):
        """
        Draws the dline object to the view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondtion: view is a valid GView object. (Do not need to assert, taken care of assertion in main draw() which calls it).
        """
        self._dline.draw(view)
        
    # Helper that draws the ship's bolt to the game view
    def _draw_Ship_Bolt(self, view):
        """
        Draws Ship bolt to the game view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondition: view is a valid GView object.
        """
        assert isinstance(view, GView)
        
        if self._ship is not None and (len(self._bolts) > 0 and (self._bolts[0] is not None)):
            ship_bolt = self._bolts[0]
            if ship_bolt.y <= GAME_HEIGHT:
                ship_bolt.draw(view); #print('Drawing bolt'); print('Bolt Color is ' + str(ship_bolt.fillcolor))
    
    # Helper that draws the Aliens' bolt(s) to the game view
    def _draw_Alien_Bolts(self, view):
        """
        Draws Alien bolt(s) to the game view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondition: view is a valid GView object.
        """
        assert isinstance(view, GView)
        
        for bolt in self._bolts:
            if bolt is not None:
                if bolt.y >= 0:
                    bolt.draw(view)#; print("Drawing alien bolts"); print('Bolt coordinates ' + str(bolt.x) + str(bolt.y))
    
    def _draw_labelLives(self, view):
        """
        Helper that draws lives label to view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondition: view is a valid GView object.
        """
        assert isinstance(view, GView)
        
        self._labelLives.draw(view)
    
    def _draw_scoreLabel(self, view):
        """
        Helper that draws score label to view.
        
        Parameter view: the game view, used in drawing [instance of GView; it is inherited from GameApp]
        Precondition: view is a valid GView object.
        """
        assert isinstance(view, GView)
        
        self._scoreLabel.draw(view)
        
    
    # HELPER METHODS FOR COLLISION DETECTION
    
    # SHIP COLLISION WITH ALIEN BOLT METHOD
    def _check_Ship_Collision(self):
        """
        Helper to check if the ship collides with an Alien bolt.
        """
        if len(self._bolts) > 1:
            for bolt in range(1, len(self._bolts)):
                if self._bolts[bolt] is not None and \
                    self._ship is not None and \
                    self._ship.collision(self._bolts[bolt]):
                        self._ship = None
                        self._lives -= 1
                        self._labelLives.text = 'Fighters left in Red Squadron: ' +\
                                                str(self._lives)
            
            if len(self._bolts) >= 1:
                for bolt in range(len(self._bolts) - 1, 0, -1):
                    if self._bolts[bolt] is None:
                        self._bolts.remove(self._bolts[bolt])
                        self._bolts = [None]
    
    # ALIEN COLLISION WITH SHIP BOLT METHOD
    def _check_Alien_Collision(self):
        """
        Helper to check if an alien collides with a ship bolt.
        """
        if self._bolts[0] is not None:
                for col in range(ALIENS_IN_ROW):
                    for row in range(ALIEN_ROWS):
                        if self._bolts[0] is not None and \
                            self._ship is not None and \
                            self._aliens[col][row] is not None and \
                            self._aliens[col][row].collision(self._bolts[0]):
                                    #self._aliens[col][row] = GSprite(width = ALIEN_WIDTH,\
                                    #                                 height = ALIEN_HEIGHT,\
                                    #                                 source = 'Exploding_Tie-strip.png',\
                                    #                                 format = (2, 2))
                                    #self._aliens[col][row] = ((self._aliens[col][row]).frame + 1) % 2
                                    #print('before ' + str(self._aliens[col][row].getTIELevel()))
                                    self._aliens[col][row].setTIELevel(self._aliens[col][row].getTIELevel() - 1)
                                    #print('after ' + str(self._aliens[col][row].getTIELevel()))
                                    if self._aliens[col][row].getTIELevel() == 0:
                                        score = self._aliens[col][row].getScoreValue()
                                        self._aliens[col][row] = None#; print('Removing alien at ' + str(col) + ', ' + str[row])
                                        self._bolts[0] = None
                                        self._ship.setShipShoot(True)
                                        self._alienSpeed *= 0.95
                                        self._score += score
                                        self._scoreLabel.text = 'Kill count: ' + str(self._score)
                                    elif self._aliens[col][row].getTIELevel() > 0:
                                        self._bolts[0] = None
                                        self._ship.setShipShoot(True)