import os
from flask import Flask, Response, render_template, make_response, jsonify
import pdfkit
import pymysql
from fpdf import FPDF
from flaskext.mysql import MySQL

from helper import add_pdf_footer, add_pdf_header, build_response
from tempalate import CPDF

app = Flask(__name__)
mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'personal'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/ping', methods=['GET'])
def ping():
    response = make_response(
        jsonify({'status': 'success', 'message': 'pong', 'developer': 'Devesh Kumar'}), 200)
    return response


# http: // 127.0.0.1: 5000/generate_pdf/file_name
@app.route('/generate_pdf/<string:file_name>', methods=['GET', 'POST'])
def generate_pdf(file_name):
    renderer = render_template('generatepdf.html', file_name=file_name)
    options = {
        'page-size': 'A4',
        'margin-top': '0.25in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.25in',
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [],
        'no-outline': None
    }

    add_pdf_header(options, file_name)
    add_pdf_footer(options)

    try:
        pdf = pdfkit.from_string(renderer, False, options=options)
    finally:
        os.remove(options['--header-html'])
        os.remove(options['--footer-html'])

    response = build_response(pdf, file_name)

    return response


@app.route('/download/report', methods=['GET', 'POST'])
def download_report():
    conn = None
    cursor = None

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            "SELECT emp_id, emp_first_name, emp_last_name, emp_designation FROM employee")
        result = cursor.fetchall()

        pdf = CPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 18.0)
        pdf.ln(10)
        pdf.cell(page_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)
        col_width = page_width / 4

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['emp_id']), border=1)
            pdf.cell(col_width, th, row['emp_first_name'], border=1)
            pdf.cell(col_width, th, row['emp_last_name'], border=1)
            pdf.cell(col_width, th, row['emp_designation'], border=1)
            pdf.ln(th)

        pdf.ln(50)

        pdf.set_font('Courier', '', 10)
        pdf.cell(page_width, 0.0, 'Authorized Signature', align='R')
        pdf.ln(15)
        pdf.cell(page_width, 0.0, '- end of report -', align='C')

        # return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})
        return Response(pdf.output(dest='S'), mimetype='application/pdf', headers={'Content-Disposition': 'inline;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
