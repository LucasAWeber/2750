import phylib;
import sqlite3;
import os;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE      = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON;
DRAG          = phylib.PHYLIB_DRAG;
MAX_TIME      = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS;

FRAME_RATE    = 0.01;

HEADER        = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />\n""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_STILL_BALL, number, pos, None, None, 0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
    
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall Class
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position, velocity, and acceleration as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;
    
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]);

class Hole( phylib.phylib_object ):
    """
    Python Hole Class
    """

    def __init__( self, pos):
        """
        Constructor function. Requires position as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;
    
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);

class HCushion( phylib.phylib_object ):
    """
    Python HCushion Class
    """

    def __init__( self, y):
        """
        Constructor function. Requires y as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;
    
    def svg( self ):
        if (self.obj.hcushion.y == 0):
            y = -25
        else:
            y = 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % y;

class VCushion( phylib.phylib_object ):
    """
    Python VCushion Class
    """

    def __init__( self, x):
        """
        Constructor function. Requires y as arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;
    
    def svg( self ):
        if (self.obj.vcushion.x == 0):
            x = -25
        else:
            x = 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % x;


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number, Coordinate(0,0), Coordinate(0,0), Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            
            if isinstance( ball, StillBall ):
                #create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number, Coordinate( ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y ) );
                
                # ass ball to table
                new += new_ball;

        # return table
        return new;
    
    def cueBall( self ):
        cueBall = None;
        for object in self:
            if (object == None):
                continue;
            if (object.type == 0 and object.obj.still_ball.number == 0):
                cueBall = object;
        return cueBall;

    def svg( self ):
        string = HEADER;
        for object in self:
            if (object == None):
                continue;
            string += object.svg();
        string += FOOTER;
        return string;

    def setupTable( self ):
        Y_OFFSET = math.sqrt(BALL_DIAMETER**2 - BALL_RADIUS**2) + 4;
        X_OFFSET = BALL_RADIUS + 4;

        # Setting up table
        pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - (TABLE_WIDTH / 2.0));
        ball = StillBall(0, pos);
        self += ball;
        pos.y = TABLE_WIDTH / 2.0 + Y_OFFSET * 2;
        ball = StillBall(1, pos);
        self += ball;
        pos = Coordinate(TABLE_WIDTH / 2.0 - X_OFFSET, TABLE_WIDTH / 2.0 + Y_OFFSET)
        ball = StillBall(10, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(3, pos);
        self += ball;
        pos = Coordinate(TABLE_WIDTH / 2.0 - X_OFFSET * 2, TABLE_WIDTH / 2.0);
        ball = StillBall(6, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(8, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(13, pos);
        self += ball;
        pos = Coordinate(TABLE_WIDTH / 2.0 - X_OFFSET * 3, TABLE_WIDTH / 2.0 - Y_OFFSET);
        ball = StillBall(9, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(4, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(15, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(2, pos);
        self += ball;
        pos = Coordinate(TABLE_WIDTH / 2.0 - X_OFFSET * 4, TABLE_WIDTH / 2.0 - Y_OFFSET * 2);
        ball = StillBall(14, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(11, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(5, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(12, pos);
        self += ball;
        pos.x += X_OFFSET * 2;
        ball = StillBall(7, pos);
        self += ball;

class Database():
    def __init__( self, reset=False ):
        if (reset and os.path.exists('phylib.db')):
            os.remove('phylib.db');
        self.conn = sqlite3.connect('phylib.db');

    def createDB( self ):
        cursor = self.conn.cursor();
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ball (
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
        )""");

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TTable (
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
        )""");

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BallTable (
            BALLID INTEGER NOT NULL,
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
        )""");
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Shot (
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
        )""");

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TableShot (
            TABLEID INTEGER NOT NULL,
            SHOTID INTEGER NOT NULL,
            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
            FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
        )""");

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game (
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL
        )""");

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Player (
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
        )""");

        cursor.close();
        self.conn.commit();

    def readTable( self, tableID ):
        cursor = self.conn.cursor();
        tableID += 1;
        cursor.execute(f"SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball INNER JOIN BallTable ON Ball.BALLID=BallTable.BALLID WHERE TABLEID={tableID}");

        balls = cursor.fetchall();
        if (len(balls) == 0):
            return None;
        
        table = Table();
        cursor.execute(f"SELECT TIME FROM TTable WHERE TABLEID={tableID}");
        table.time = cursor.fetchone()[0];
        for ball in balls:
            pos = Coordinate(ball[1], ball[2]);
            if (ball[3] == None and ball[4] == None):
                table+=StillBall(ball[0], pos);
            else:
                vel = Coordinate(ball[3], ball[4]);
                acc = Coordinate(0, 0);
                speed = phylib.phylib_length(vel);
                if (speed > VEL_EPSILON):
                    acc = Coordinate(-1.0 * vel.x / speed * DRAG, -1.0 * vel.y / speed * DRAG);
                table+=RollingBall(ball[0], pos, vel, acc);

        cursor.close();
        return table;
    
    def writeTable( self, table ):
        cursor = self.conn.cursor();
        cursor.execute(f"INSERT INTO TTable (TIME) VALUES ({table.time})");
        tableID = cursor.lastrowid;
        for obj in table:
            if (obj == None):
                continue;
            elif (obj.type == 0):
                cursor.execute(f"INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES ({obj.obj.still_ball.number}, {obj.obj.still_ball.pos.x}, {obj.obj.still_ball.pos.y})");
                ballID = cursor.lastrowid;
                cursor.execute(f"INSERT INTO BallTable (BALLID, TABLEID) VALUES ({ballID}, {tableID})");
            elif (obj.type == 1):
                cursor.execute(f"INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES ({obj.obj.rolling_ball.number}, {obj.obj.rolling_ball.pos.x}, {obj.obj.rolling_ball.pos.y}, {obj.obj.rolling_ball.vel.x}, {obj.obj.rolling_ball.vel.y})");
                ballID = cursor.lastrowid;
                cursor.execute(f"INSERT INTO BallTable (BALLID, TABLEID) VALUES ({ballID}, {tableID})");

        cursor.close();
        return tableID-1;

    def getGame( self, gameID ):
        cursor = self.conn.cursor();
        cursor.execute(f"SELECT Game.GAMENAME, Player.PLAYERNAME FROM Game INNER JOIN Player ON Game.GAMEID = Player.GAMEID WHERE Game.GAMEID={gameID+1}");
        temp = cursor.fetchall();
        gameName = temp[0][0];
        player1Name = temp[0][1];
        player2Name = temp[1][1];
        cursor.close();
        return gameName, player1Name, player2Name;
    
    def setGame( self, gameName, player1Name, player2Name ):
        cursor = self.conn.cursor();
        cursor.execute(f"INSERT INTO Game (GAMENAME) VALUES ('{gameName}')");
        gameID = cursor.lastrowid;
        cursor.execute(f"INSERT INTO Player (GAMEID, PLAYERNAME) VALUES ({gameID}, '{player1Name}')");
        cursor.execute(f"INSERT INTO Player (GAMEID, PLAYERNAME) VALUES ({gameID}, '{player2Name}')");
        cursor.close();
        return gameID;
    
    def newShot( self, gameName, playerName ):
        cursor = self.conn.cursor();
        cursor.execute(f"SELECT Game.GAMEID, Player.PLAYERID FROM Game INNER JOIN Player ON Game.GAMEID = Player.GAMEID WHERE Game.GAMENAME='{gameName}' AND Player.PLAYERNAME='{playerName}'");
        temp = cursor.fetchone();
        cursor.execute(f"INSERT INTO Shot (PLAYERID, GAMEID) VALUES ({temp[1]}, {temp[0]})");
        shotID = cursor.lastrowid;
        cursor.close();
        return shotID;

    def setTableShot( self, tableID, shotID ):
        cursor = self.conn.cursor();
        cursor.execute(f"INSERT INTO TableShot (TABLEID, SHOTID) VALUES ({tableID}, {shotID})");
        cursor.close();
    
    def commit( self ):
        self.conn.commit();

    def close( self ):
        self.conn.commit();
        self.conn.close();

class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        self.db = Database(True);
        self.db.createDB();
        if (gameID != None and gameName == None and player1Name == None and player2Name == None):
            self.gameID = gameID;
            self.gameName, self.player1Name, self.player2Name = self.db.getGame(gameID);
        elif (gameID == None and gameName != None and player1Name != None and player2Name != None):
            self.gameName = gameName;
            self.player1Name = player1Name;
            self.player2Name = player2Name;
            self.gameID = self.db.setGame(gameName, player1Name, player2Name);
        else:
            raise TypeError("Invalid Game class arguements");
        
    def shoot( self, gameName, playerName, table, xvel, yvel ):
        shotID = self.db.newShot(gameName, playerName);
        cueBall = table.cueBall();
        pos = Coordinate(cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y);
        cueBall.type = 1;
        cueBall.obj.rolling_ball.number = 0;
        cueBall.obj.rolling_ball.pos.x = pos.x;
        cueBall.obj.rolling_ball.pos.y = pos.y;
        cueBall.obj.rolling_ball.vel.x = xvel;
        cueBall.obj.rolling_ball.vel.y = yvel;
        acc = Coordinate(0, 0);
        speed = phylib.phylib_length(cueBall.obj.rolling_ball.vel);
        if (speed > VEL_EPSILON):
            acc = Coordinate(-1.0 * xvel / speed * DRAG, -1.0 * yvel / speed * DRAG);
        cueBall.obj.rolling_ball.acc.x = acc.x;
        cueBall.obj.rolling_ball.acc.y = acc.y;
        #tableIDArray = [];
        tableArray = [];
        while (table):
            #tableID = self.db.writeTable(table);
            #tableIDArray.append(tableID);
            #self.db.setTableShot(tableID, shotID);
            tableArray.append(table);
            temp = table;
            start = table.time;
            table = table.segment();
            if (table == None):
                break;
            end = table.time;
            for i in range(1,round((end - start) / FRAME_RATE)):
                temp = temp.roll(FRAME_RATE);
                temp.time = start+(i*FRAME_RATE);
                #tableID = self.db.writeTable(temp);
                #tableIDArray.append(tableID);
                #self.db.setTableShot(tableID, shotID);
                tableArray.append(temp);

        # resets cue ball position if it was sunk
        if (temp.cueBall() == None):
            pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_LENGTH - (TABLE_WIDTH / 2.0));
            cue = StillBall(0, pos);
            temp += cue;
            #tableID = self.db.writeTable(temp);
            #tableIDArray.append(tableID);
            #self.db.setTableShot(tableID, shotID);
            tableArray.append(temp);
        #self.db.commit();
        #return tableIDArray;
        return tableArray;



