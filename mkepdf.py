import pdfkit
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from helpers import Helpers

# pdfkit.from_url('http://google.com', 'out.pdf')



def makePDFFromFile(fileName: str):
  HTML('./data/cover_templates/base_cover.html').write_pdf(f"{Helpers.pdf_file_path}{fileName}.pdf")


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

def makePDFFromTemplate():
    if Helpers.static_df is None:
      return
    novels = Helpers.static_df[Helpers.static_df.columns[0]].tolist()
    authors = Helpers.static_df[Helpers.static_df.columns[1]].tolist()
    links = Helpers.static_final_links
    file = open('static/base.txt', 'r', encoding='utf-8')
    base_file = file.read()
    file.close()
    for idx, novel in enumerate(novels):
      text_file = open('./data/cover_templates/base_cover.html', 'w', encoding='utf-8')
      text_file.write(f"{base_file}"+f"""
          <body>
            <center>
              <div>
                <div>
                  <a href="link">
                    <img src="../qrcodes/{idx}.png" alt="qr-{idx}">
                  </a>
                  <a href="{links[idx]}">
                    <h1>{novel}</h1>
                  </a>
                  <h2>
                    {authors[idx]}
                  </h2>
                </div>
              </div>
            </center>
          </body>

          </html>
                """)
      text_file.close()
      makePDFFromFile(novel)
