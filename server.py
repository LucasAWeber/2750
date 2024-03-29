import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
import os;
import math;
import Physics;
import json;

from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

def openFile(string, num):
    file = open("table-%d.svg" % num, "w");
    file.write(string);
    file.close();
    return num+1;

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/game.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            #MAYBE CHANGE??
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
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg') and os.path.exists('.'+self.path):

            # retreive the HTML file & insert form data into the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
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
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']} );
            global game;
            game = Physics.Game(None, form.getvalue("player1name") + " VS " + form.getvalue("player2name"),form.getvalue("player1name"), form.getvalue("player2name"));
            global table;
            table = Physics.Table();
            table.setupTable();

            fp = open( '.'+self.path );
            content = fp.read() % table.svg();
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

            self.send_response(200);
            self.send_header('Content-type', 'application/json');
            self.end_headers();
            self.wfile.write(json.dumps(svgArray).encode('utf-8'));

        elif parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']} );

            # Deletes existing svg files
            i = 0;
            while (os.path.exists("table-%d.svg" % i)):
                os.remove("table-%d.svg" % i);
                i += 1;
            
            content = "<h1>Pool Simulator</h1><h2>Initial Values</h2>";
            table = Physics.Table();
            number = int(form.getvalue('sb_number'));
            pos = Physics.Coordinate(float(form.getvalue('sb_x')), float(form.getvalue('sb_y')));
            sb = Physics.StillBall(number, pos);
            content += "<b>Still Ball</b><label> | Number: %d, Position: (%6.1lf, %6.1lf)</label></br>" % (number, pos.x, pos.y);
            number = int(form.getvalue('rb_number'));
            pos = Physics.Coordinate(float(form.getvalue('rb_x')), float(form.getvalue('rb_y')));
            vel = Physics.Coordinate(float(form.getvalue('rb_dx')), float(form.getvalue('rb_dy')));
            speed_a = Physics.phylib.phylib_length(vel);
            if (speed_a > Physics.VEL_EPSILON):
                acc = Physics.Coordinate(-1.0 * vel.x / speed_a * Physics.DRAG, -1.0 * vel.y / speed_a * Physics.DRAG);
            rb = Physics.RollingBall(number, pos, vel, acc);
            content += "<b>Rolling Ball</b><label> | Number: %d, Position: (%6.1lf, %6.1lf), Velocity: (%6.1lf, %6.1lf), Acceleration: (%6.1lf, %6.1lf)</label></br>" % (number, pos.x, pos.y, vel.x, vel.y, acc.x, acc.y);
            table += sb;
            table += rb;
            
            content += "<h2>Visualization</h2>"
            num = 0;
            #  Rolling balls loop
            while (table != None):
                content = content + '<img src="table-%d.svg" width="425" style="margin: 10px 10px 10px 10px;"/>' % num;
                num = openFile(table.svg(), num);
                table = table.segment();

            content += '</br><a href="/shoot.html">Back</a></br>';

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );

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
