from fpdf import FPDF


class CPDF(FPDF):

    def header(self):
        self.set_font('helvetica', 'BU', 15)
        self.cell(20)
        self.cell(170, 10, 'Employee Labs', 0, 0,
                  'R', False, 'https://google.com')
        # self.set_font('helvetica', 'B', 10)
        # self.cell(10)
        # self.cell(170, 10, 'Mountain View, California', 0, 0,
        #           'R')
        # self.set_font('helvetica', 'B', 10)
        # self.cell(10)
        # self.cell(170, 10, 'USA', 0, 0, 'R')

        self.image('static/images/logo.png', 10, 1, 33)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'R')
        self.set_author('Devesh Kumar')
