import pdfkit
from weasyprint import HTML

# pdfkit.from_url('http://google.com', 'out.pdf')



def makePDF():
  HTML('./templates/cover.html').write_pdf('website.pdf')

