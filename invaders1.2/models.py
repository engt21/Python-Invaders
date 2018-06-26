"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Name: Timothy Eng (te76)
Date Completed: December 08, 2017
"""
from consts import *
from game2d import *
from cornell import Point2

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _shipShoot: Boolean that is used in determining if the ship can shoot a bolt.
    If a bolt is currently being fired, then the attribute is False. It is only True
    if the ship can fire another bolt, which means none are on the screen. [True or False]
    """
    #pass
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def shipShoot(self):
        """
        Getter for the _shipShoot attribute.
        """
        return self._shipShoot
    
    def setShipShoot(self, ship_shoot):
        """
        Setter for the _shipShoot attribute.
        
        Pararmeter ship_shoot: the new boolean value for _shipShoot.
        Invariant: _shipShoot is a boolean.
        """
        assert isinstance(ship_shoot, bool)
        
        self._shipShoot = ship_shoot
        
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, width, height, source):
        """
        Constructs a new Alien object positioned at x, y with width and height,
        image is given by paramter source. According to its parent, GImage, if
        the attributes width and height do not agree with the actual size of the
        image, the image is scaled to fit. 
        
        Parameter x: The horizontal coordinate of the object center.
        Invariant: Value must be an int or float

        Parameter y: The vertical coordinate of the object center.
        Invariant: Value must be an int or float
        
        Parameter width: The width of the image.
        Invariant: Value must be an int or float. If it does not agree with the
        actual size of the image, the image is scaled to fit.
        
        Paramter height: The height of the image.
        Invariant: Value must be an int or float. If it does not agree with the
        actual size of the image, the image is scaled to fit
        
        Paramter source: The source file for this image.
        Invariant. Value be a string refering to a valid file.
        """
        super().__init__(x = x, y = y, width = SHIP_WIDTH, height = SHIP_HEIGHT, source = source)
        self._shipShoot = True
        
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collision(self, bolt):
        """
        Returns: True if the bolt was fired by the an Alien and collides with the player
            
        Suggestion to make all points Point2 objects by Caleb Berman (ckb65).
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        
        if not bolt.isPlayerBolt():
            if self.contains(Point2(bolt.x - BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x - BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x + BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x + BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2)):
                    return True
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    scoreValue: the alien's point value [int]
    """
    #pass
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # GETTER FOR scoreValue
    def getScoreValue(self):
        """
        Getter for scoreValue attribute of Alien.
        """
        return self.scoreValue
    
    # SETTER FOR scoreValue
    def setScoreValue(self, value):
        """
        Setter for scoreValue attribute.
        
        Parameter value: the new scoreValue.
        Invariant: value is an int.
        """
        assert isinstance(value, int)
        
        self.scoreValue = value

    # GETTER FOR TIELevel
    def getTIELevel(self):
        """
        Getter for TIELevel attribute.
        """
        return self._TIELevel
        
    # SETTER FOR TIELevel
    def setTIELevel(self, level):
        """
        Setter for TIE level (health).
        
        Parameter level: the level of the TIE.
        Precondtion: level is an int.
        """
        assert isinstance(level, int)
        self._TIELevel = level
        
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, width, height, source):
        """
        Constructs a new Alien object positioned at x, y with width and height,
        image is given by paramter source. According to its parent, GImage, if
        the attributes width and height do not agree with the actual size of the
        image, the image is scaled to fit. 
        
        Parameter x: The horizontal coordinate of the object center.
        Invariant: Value must be an int or float

        Parameter y: The vertical coordinate of the object center.
        Invariant: Value must be an int or float
        
        Parameter width: The width of the image.
        Invariant: Value must be an int or float. If it does not agree with the
        actual size of the image, the image is scaled to fit.
        
        Parameter height: The height of the image.
        Invariant: Value must be an int or float. If it does not agree with the
        actual size of the image, the image is scaled to fit.
        
        Parameter source: The source file for this image.
        Invariant. Value be a string refering to a valid file.
        
        """
        
        super().__init__(x = x, y = y, width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = source)
        self.scoreValue = 0
        self._TIELevel = 0
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collision(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
        
        Suggestion to make all points Point2 objects by Caleb Berman (ckb65).
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        
        if bolt.isPlayerBolt():
            if self.contains(Point2(bolt.x - BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x - BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x + BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2)) or \
                self.contains(Point2(bolt.x + BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2)):
                    return True
            
        #pass
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY            
    

class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _isPlayerBolt: Boolean that states whether or not a bolt came from the player
        [True or False], default set to False.
        _playerBoltFired: Boolean that determines if a bolt was fired from the player.
    """
    #pass
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def velocity(self):
        """
        Getter for velocity attribute.
        """
        return self._velocity
    
    def set_velocity(self, velocity):
        """
        Setter for velocity attribute of bolt.
        
        THIS METHOD IS NEVER USED.
        
        Parameter velocity: the new velocity of of the bolt. (int)
        Invariante: _velocity is an int.
        """
        assert isinstance(velocity, int)
        
        self._velocity = velocity
        
    def isPlayerBolt(self):
        """
        Getter for isPlayerBolt attribute.
        """
        return self._isPlayerBolt
    
    def setPlayerBolt(self, player_bolt):
        """
        Setter for _isPlayerBolt attribute.
        
        Parameter player_bolt: new boolean for isPlayerBolt.
        Invariant: _isPlayerBolt attribute is a boolean.
        """
        assert isinstance(player_bolt, bool)
        
        self._isPlayerBolt = player_bolt
        
    def playerBoltFired(self):
        """
        Getter for _playerBoltFired attribute.
        """
        return self._playerBoltFired
    
    def setPlayerBoltFired(self, pboltfired):
        """
        Setter for _playerBoltFired attribute.
        
        Parameter pboltfired: the new boolean value for _playerBoltFired.
        Invariant: _playerBoltFired attribute is a boolean.
        """
        assert isinstance(pboltfired, bool)
        
        self._playerBoltFired = pboltfired
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, width, height, fillcolor, linewidth):
        """
        Constructs a new Bolt object positioned at x, y with width and height,
        fillcolor and linecolor default to black.
        
        Bolt is a sub class of GRectangle, whose standard constructor is
        GRectangle(x = 0, y = 0, width = 10, height = 10, fillcolor = 'red').
        This class supports the all same keywords as GObject plus the additional keyword linewidth.
        
        Also creates attributes _velocity, _isPlayerBolt, and _playerBoltFired.
        
        Parameter x: The horizontal coordinate of the object center.
        Invariant: Value must be an int or float

        Parameter y: The vertical coordinate of the object center.
        Invariant: Value must be an int or float.
        
        Parameter width: The width of the bolt.
        Invariant: Value must be an int or float. 
        
        Parameter height: The height of the bolt.
        Invariant: Value must be an int or float.
        
        Parameter fillcolor: the fillcolor of the bolt.
        
        Parameter linewidth: The width of the exterior line of this shape.
        Setting this to 0 means that the rectangle has no border. [int or float >= 0]
        """
        super().__init__(x = x, y = y, width = BOLT_WIDTH, height = BOLT_HEIGHT, fillcolor = fillcolor, linewidth = linewidth)
        
        self._velocity = BOLT_SPEED
        self._isPlayerBolt = False
        self._playerBoltFired = False
            
    #    ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    #def _isPlayerBolt(self):   
    #    return False
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE