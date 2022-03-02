import tempfile

from flask import make_response, render_template


def add_pdf_header(options, bar):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['--header-html'] = header.name
        header.write(render_template(
            '/templates/header.html', bar=bar).encode('utf-8'))
    return


def add_pdf_footer(options):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['--header-html'] = header.name
        header.write(render_template('/templates/footer.html').encode('utf-8'))
    return


def build_response(pdf, file_name):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % file_name
    return response
