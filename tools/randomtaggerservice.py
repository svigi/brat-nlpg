#!/usr/bin/env python

'''
An example of a tagging service.

Author:     Pontus Stenetorp    <pontus stenetorp se>
Version:    2012-03-05
'''

from argparse import ArgumentParser
# Do note that we intentionally don't use the brat json here, if you don't
#   have a new enough Python, upgrade it damn it!
from json import dumps
from random import choice, randint
from sys import stderr
from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

### Constants
ARGPARSER = ArgumentParser(description='An example HTTP tagging service, '
        'tagging Confuse-a-Cat **AND** Dead-parrot mentions!')
ARGPARSER.add_argument('-p', '--port', type=int, default=47111,
        help='port to run the HTTP service on (default: 47111)')
###

def _random_span(text):
    # A random span not starting or ending with spaces or including a new-line
    attempt = 1
    while True:
        start = randint(0, len(text))
        end = randint(start + 3, start + 25)

        # Did we violate any constraints?
        if (
                # We landed outside the text!
                end > len(text) or
                # We contain a newline!
                '\n' in text[start:end] or
                # We have a leading or trailing space!
                (text[start:end][-1] == ' ' or text[start:end][0] == ' ')
                ):
            # Well, try again then...?
            if attempt >= 100:
                # Bail, we failed too many times
                return None, None, None
            attempt += 1
            continue
        else:
            # Well done, we got one!
            return start, end, text[start:end]

def _random_tagger(text):
    # Generate some annotations
    anns = {}
    num_anns = randint(1, len(text) / 100)
    for ann_num in xrange(num_anns):
        ann_id = 'T{}'.format(ann_num)
        # Annotation type
        _type = choice(('Confuse-a-Cat', 'Dead-parrot', ))
        start, end, span_text = _random_span(text)
        if start is None:
            # Random failed, continue to the next annotation
            continue
        anns[ann_id] = {
                'type': _type,
                'offsets': ((start, end), ),
                'text': span_text,
                }
    return anns

class RandomTaggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get our query
        query = parse_qs(urlparse(self.path).query)

        # Do your random tagging magic
        try:
            json_dic = _random_tagger(query['text'][0])
        except KeyError:
            # We weren't given any text to tag, such is life, return nothing
            json_dic = {}

        # Write the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        self.wfile.write(dumps(json_dic, encoding='utf-8', indent=4,
                sort_keys=True))
        print >> stderr, ('Generated {} random annotations'
                ).format(len(json_dic))

    def log_message(self, format, *args):
        return # Too much noise from the default implementation

def main(args):
    argp = ARGPARSER.parse_args(args[1:])

    server_class = HTTPServer
    httpd = server_class(('localhost', argp.port), RandomTaggerHandler)
    print >> stderr, 'Random tagger service started'
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print >> stderr, 'Random tagger service stopped'

if __name__ == '__main__':
    from sys import argv
    exit(main(argv))
