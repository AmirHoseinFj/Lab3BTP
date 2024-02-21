# Amirhossein Ghaffarzadeh
# 120734223

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mysql.connector


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        cnx = mysql.connector.connect(user='admin', password='admin',
                                      host='127.0.0.1',
                                      database='notes_db')
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM notes"
        cursor.execute(query)
        notes = cursor.fetchall()

        self._set_headers()
        self.wfile.write(json.dumps(notes).encode('utf-8'))

        cursor.close()
        cnx.close()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Get the data
        data = json.loads(post_data)  # Convert data to JSON

        # Connect to the MySQL database
        cnx = mysql.connector.connect(user='username', password='password',
                                      host='127.0.0.1', database='notes_db')
        cursor = cnx.cursor()

        # Insert new note into the database
        add_note = ("INSERT INTO notes (title, content) VALUES (%s, %s)")
        note_data = (data['title'], data['content'])
        cursor.execute(add_note, note_data)
        cnx.commit()

        self.send_response(201)  # Created
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Note created'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

        cursor.close()
        cnx.close()


    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data)

        # Extracting the note ID from the URL
        path_parts = self.path.strip('/').split('/')
        note_id = path_parts[-1]  # Assuming URL pattern: /notes/{id}

        cnx = mysql.connector.connect(user='username', password='password',
                                    host='127.0.0.1', database='notes_db')
        cursor = cnx.cursor()

        # Update the note in the database
        update_note = ("UPDATE notes SET title = %s, content = %s WHERE id = %s")
        note_data = (data['title'], data['content'], note_id)
        cursor.execute(update_note, note_data)
        cnx.commit()

        self.send_response(200)  # OK
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Note updated'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

        cursor.close()
        cnx.close()    
    

    def do_DELETE(self):
        path_parts = self.path.strip('/').split('/')
        note_id = path_parts[-1]  # Assuming URL pattern: /notes/{id}

        cnx = mysql.connector.connect(user='username', password='password',
                                    host='127.0.0.1', database='notes_db')
        cursor = cnx.cursor()

        # Delete the note from the database
        delete_note = ("DELETE FROM notes WHERE id = %s")
        cursor.execute(delete_note, (note_id,))
        cnx.commit()

        self.send_response(204)  # No Content
        self.end_headers()

        cursor.close()
        cnx.close()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
