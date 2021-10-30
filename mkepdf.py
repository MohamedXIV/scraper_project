import pdfkit
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# pdfkit.from_url('http://google.com', 'out.pdf')



def makePDFFromFile():
  HTML('./templates/cover.html').write_pdf('website.pdf')


def makePDFFromString():
    fontConfig = FontConfiguration()
    # css = CSS("""
    #     body {
    #       background-color: #fff;
    #     }
    #     """)
    html = HTML(string=""" 
        <center>
      <div class="qr-image">
        <div>
          <a href="https://www.google.com/">
            <img src="./data/qrcodes/0.png" alt="qr-0">
          </a>
          <a href="https://www.google.com/">
            <h2>{{ novel }}</h2>
          </a>
          <link rel=attachment>
          <a rel=attachment>attachment</a>
        </div>
      </div>
      <nav><a href="{{ url_for('hello_pdf', name=name) }}">Get as PDF</a></nav>
    </center>
      """)
    html.write_pdf('example.pdf', font_config=fontConfig)


#makePDFFromFile()
makePDFFromString()

