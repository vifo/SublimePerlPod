# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from perl_pod import *
from perl_pod.preview_renderers.base import PerlPodBasePreviewRenderer
from bs4 import BeautifulSoup

try:
    import requests
    HTTP_LIBRARY = 'requests'
except (ImportError) as e:
    import urllib2
    import uuid
    HTTP_LIBRARY = 'urllib2'


CPAN_RENDERER_URL = 'http://search.cpan.org/pod2html'


class PerlPodCpanPreviewRenderer(PerlPodBasePreviewRenderer):

    def __init__(self, view, input, **options):
        super(PerlPodCpanPreviewRenderer, self).__init__(view, input, **options)
        self.set_output_syntax('html')

    def render(self):
        try:
            url = CPAN_RENDERER_URL
            headers = {
                'User-Agent': "{0}/{1}".format(PLUGIN_NAME, PLUGIN_VERSION),
                'Referer': url,
            }
            files = {
                'file': ('PerlPodPreviewCommand.pm', self.input)
            }

            if HTTP_LIBRARY == 'requests':
                PerlPod().log('trace', 'Using requests library for requests to CPAN')
                args = {'files': files}

                res = requests.post(url, **args)
                in_soup = BeautifulSoup(res.text)
            else:
                PerlPod().log('trace', 'Using urllib2 library for requests to CPAN')
                req = self.create_urllib2_multipart_form_data_request(
                    url=url,
                    headers=headers,
                    files=files
                )

                res = urllib2.urlopen(req)
                html = res.read()
                in_soup = BeautifulSoup(html)

            # Extract HTML elements, we're interested in and put them into a
            # new HTML document.
            out_soup = BeautifulSoup("""
                <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                <html>
                <head>
                    <meta charset="utf8">
                    <title>%s</title>
                    <style type="text/css">
                        div.path { margin: 0; }
                    </style>
                </head>
                <body>
                    <div class="path">%s</div>
                </body>
                </html>
                """ % (self.filename, self.filename)
            )

            # Add stylesheets from CPAN html output.
            for tag in in_soup.select('link[rel=stylesheet]'):
                out_soup.head.append(tag)

            for tag in in_soup.select('div.pod'):
                out_soup.body.append(tag)

            self.output = out_soup.prettify()
            return True

        except Exception as e:
            print(repr(e))
            self.errors.append(repr(e))
            return False

    def create_urllib2_multipart_form_data_request(self, url, headers={}, fields={}, files={}):
        boundary = '--%s' % (uuid.uuid4().hex)
        body = []

        for key, value in fields.items():
            body.append('--%s' % (boundary))
            body.append('Content-Disposition: form-data; name="%s"' % (key))
            body.append('')
            body.append(value)

        for key, value in files.items():
            body.append('--%s' % (boundary))

            if isinstance(value, tuple):
                if len(value) == 3:
                    filename, data, content_type = value
                else:
                    filename, data = value
                    content_type = 'application/octet-stream'

                body.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            else:
                body.append('Content-Disposition: form-data; name="%s"' % (key))
                data = value

            body.append('Content-Type: %s' % (content_type))
            body.append('')
            body.append(data)

        body.append('--%s--' % (boundary))
        body.append('')

        # Convert to bytes and create request
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % (boundary)
        body = "\r\n".join(body).encode('utf-8')

        return urllib2.Request(url, body, headers)
