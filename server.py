import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
import os;
import math;
import Physics;
import json;
import random;

from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

def openFile(string, num):
    file = open("table-%d.svg" % num, "w");
    file.write(string);
    file.close();
    return num+1;

def newTurn(turn):
    if (turn == 0):
        turn = 1;
    else:
        turn = 0;
    return turn;

def determinePlayerTeam(table):
    last = -1;
    sunkBall = -1;
    for obj in table:
        if (obj == None):
            last += 1;
            if (last != 0 and last != 8):
                sunkBall = last;
        elif (obj.type == 0):
            last = obj.obj.still_ball.number;
        elif (obj.type == 1):
            last = obj.obj.rolling_ball.number;
    if (sunkBall == -1):
        return 0;
    elif (sunkBall < 8):
        return -1;
    else:
        return 1;

def eightBallWin(table, playerTeams):
    balls = [];
    for obj in table:
        if (obj != None):
            if (obj.type == 0):
                balls.append(obj.obj.still_ball.number);
            elif (obj.type == 1):
                balls.append(obj.obj.rolling_ball.number);
    if (any(ball != 0 and ball < 8 for ball in balls)):
        return playerTeams.index(-1);
    elif (any(ball > 8 for ball in balls)):
        return playerTeams.index(1);
    return -1;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        print(self.path);
        # check if the web-pages matches the list
        if parsed.path in [ '/game.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            #table = Physics.Table();
            #table.setupTable();
            #content = fp.read() % table.svg();
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        
        elif parsed.path in [ '/start.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path.replace('?','') );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        
        elif parsed.path in [ '/win.html' ]:
            global game;
            global table;
            global gameStatus;

            fp = open( '.'+self.path );
            if (gameStatus == 1):
                winnerText = game.player1Name + " is the winner!";
            else:
                winnerText = game.player2Name + " is the winner!";
            
            content = fp.read() % (winnerText, table.svg());

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        
        if parsed.path in [ '/game.html' ]:
            global game;
            global table;
            global turn;
            global playerTeams;
            global firstBall;
            global gameStatus;
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']} );
            game = Physics.Game(None, form.getvalue("player1name") + " VS " + form.getvalue("player2name"),form.getvalue("player1name"), form.getvalue("player2name"));
            table = Physics.Table();
            table.setupTable();
            # Players turn
            turn = random.randint(0,1);
            # Players target balls (upper = 1, lower = -1, none = 0)
            playerTeams = [0,0];
            # If first ball is still yet to be sunk
            firstBall = True;
            # Game status (playing = 0, player 1 win = 1, player 2 win = 2)
            gameStatus = 0;

            fp = open( '.'+self.path );
            if (turn == 0):
                content = fp.read() % (table.svg(), game.player1Name, " - YOUR TURN", game.player2Name, "");
            else:
                content = fp.read() % (table.svg(), game.player1Name, "", game.player2Name, " - YOUR TURN");
            
            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        elif parsed.path in [ '/cue-roll' ]:
            content_length = int(self.headers['Content-Length']);
            post_data = self.rfile.read(content_length);
            data = json.loads(post_data.decode('utf-8'));
            #IDArray = game.shoot(game.gameName, game.player1Name, table, data["velx"], data["vely"]);
            tableArray = game.shoot(game.gameName, game.player1Name, table, data["velx"], data["vely"]);

            svgArray = [];
            for t in tableArray:
                table = t;
                svgArray.append(table.svg());
                if (gameStatus == 0 and table.eightBall() == None):
                    winning = eightBallWin(table, playerTeams)
                    if (winning == 0):
                        gameStatus = 1;
                    elif (winning == 1):
                        gameStatus = 2;
                    else:
                        gameStatus = newTurn(turn) + 1;
                if (firstBall):
                    team = determinePlayerTeam(table);
                    if (team != 0):
                        firstBall = False;
                        playerTeams[0] = team * -1;
                        playerTeams[1] = team * -1;
                        playerTeams[turn] = team;

            turn = newTurn(turn);

            data = {
                "tables" : svgArray,
                "turn" : turn,
                "player1Team" : "",
                "player2Team" : "",
                "status" : gameStatus
            };
            
            if (playerTeams[0] == -1):
                data["player1Team"] = "Lower";
                data["player2Team"] = "Upper";
            elif (playerTeams[0] == 1):
                data["player1Team"] = "Upper";
                data["player2Team"] = "Lower";

            self.send_response(200);
            self.send_header('Content-type', 'application/json');
            self.end_headers();
            self.wfile.write(json.dumps(data).encode('utf-8'));

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


if __name__ == "__main__":
    #put the starting svg creation here?
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
