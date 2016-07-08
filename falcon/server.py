import falcon
import json

# local import
from TextSummarizer import TextSummarizer

def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook

class ParseText(object):                    
    @falcon.before(max_body(1024 * 1024))
    def on_post(self, req, resp):
      text = req.stream.read()
      corpus = TextSummarizer.from_text(text.decode('utf-8','ignore')).summarize();
      resp.body = json.dumps(corpus.pack())


# falcon.API instances are callable WSGI apps
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/', ParseText())
