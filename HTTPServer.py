from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request, parse
import logging
import urllib.parse
import io
import os
from os import remove
import cgi

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_HEAD(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            file_to_open = ""
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_PUT(self):
        try:
            ruta = self.path
            file = open(ruta, "w")
            file.close()
            file_to_open = "Created"
            self.send_response(201)
        except:
            file_to_open = "No Content"
            self.send_response(204)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_DELETE(self):
        try:
            ruta = self.path
            remove(ruta)
            self.send_response(200)
        except:
            file_to_open = "No Content"
            self.send_response(204)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage\
            (fp=self.FieldStorage,
             headers=self.headers,
             environ={
                 'REQUEST_METHOD': 'POST',
                 'CONTENT_TYPE': self.headers['Content-Type'],
             })

        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile, encoding='utf-8',
            line_buffering = False,
            write_through = True,
        )

        out.write('Client: {}\n'.format(self.client_address))
        out.write('user-agent: {}\n'.format(self.headers['user-agent']))
        out.write('path: {}\n'.format(self.path))
        out.write('Form data:\n')

        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write('\tUploaded {} as {!r} ({} bytes)\n'.format(field, field_item.filename, file_len))
            else:
                out.write('\t{}={}\n'.format(field, form[field].value))

        out.detach()

PORT = 8080
httpd = HTTPServer(('localhost', PORT), Serv)
httpd.serve_forever()