from gluon.contrib.pyfpdf import FPDF, HTMLMixin
from datetime import date

# create a custom class with the required functionalities 
class Relatorio(FPDF, HTMLMixin):

    def header(self): 
        self.set_font('Arial','B',15)
        #self.cell(65) # padding
        self.cell(0,10,response.title,1,0,'C')
        hoje = date.today()
        self.cell(0,10,'Emitido em ' + hoje.strftime('%d/%m/%Y'),align='R')
        self.ln(20)
        
    def footer(self):
        "hook to draw custom page footer (printing page numbers)"
        self.set_y(-15)
        self.set_font('Arial','I',8)
        txt = 'Página %s de %s' % (self.page_no(), self.alias_nb_pages())
        self.cell(0,10,txt,0,0,'C')

