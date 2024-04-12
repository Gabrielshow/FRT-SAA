import os
import json
import cherrypy
import subprocess
from FRT import SeatAssignmentApp

class FileServer(object):
    @cherrypy.expose
    def index(self):
        return open('templates/index.html', 'r').read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_grid_data(self, selected_hall=None, selected_pattern=None):
        if not selected_hall or not selected_pattern:
            return {'error': 'Invalid selection'}, 400

        grid_data = self.get_grid_data_json(selected_hall, selected_pattern)
        return grid_data

    @cherrypy.expose
    def exam_hall(self):
        return open('templates/exam_hall.html', 'r').read()

    @cherrypy.expose
    def run_saa(self, selected_hall=None, selected_pattern=None):
        if not selected_hall or not selected_pattern:
            return {'error': 'Invalid selection'}, 400

        subprocess.run(["python", "FRT.py", selected_hall, selected_pattern])
        grid_data = self.get_grid_data_json(selected_hall, selected_pattern)
        return open('templates/exam_hall.html', 'r').read()

    def get_grid_data_json(self, selected_hall, selected_pattern):
        root = cherrypy.thread_data.root
        app = SeatAssignmentApp(root)
        return json.loads(app.get_grid_data_json(selected_hall, selected_pattern))

if __name__ == '__main__':
    # Configure CherryPy server
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})

    # Mount the FileServer class as the root of the CherryPy application
    cherrypy.quickstart(FileServer(), '/', config={
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })
