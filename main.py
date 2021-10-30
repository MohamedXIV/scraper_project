from flask import Flask, render_template, request, redirect, send_file, url_for
from flask_weasyprint import HTML, render_pdf
import requests
import json
from helpers import Helpers
from gsheet import saveToGSheet
import webbrowser
from mkepdf import makePDFFromString, makePDFFromFile, makePDFFromTemplate
from mkeqr import saveQRImages

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "GET":
      # url = request.form['url']
      # scrape_table(url)
      # redirect('/')
      return render_template("index.html")
  elif request.method == "POST":
    url = request.form['url']
    wiki_table = Helpers.getTable(url, False)
    Helpers.getHyperlinks(wiki_table)
    return render_template('index.html', table=Helpers.getHtmlTable(url)) 

@app.route('/download', methods=['GET', 'POST'])
def download_excel():
  if request.method == 'GET':
    Helpers.pdHtmlToExcel()

    return send_file(f'{Helpers.excel_file_path}{Helpers.page_title}.xlsx', as_attachment=True)
  elif request.method == 'POST':
    return 'Downloaded'


@app.route('/saveToGSheet')
def save_to_gsheet():
    saveToGSheet()
    webbrowser.open_new_tab(saveToGSheet())
    return redirect(saveToGSheet())


@app.route('/downloadPDF', methods=['GET'])
def download_pdf():
    makePDFFromFile()
    return send_file('website.pdf', as_attachment=True)

@app.route('/hello_<name>.pdf')
def hello_pdf(name):
    # Make a PDF from another view
    return render_pdf(url_for('hello_html', name=name))


@app.route('/downloadPDFCovers', methods=['GET'])
def download_pdf_covers():
    saveQRImages()
    makePDFFromTemplate()
    return "Congrats!, you have downloaded the PDFs"




def scrape_table(url):
  wiki_table = Helpers.getTable(url, False)
  Helpers.getHyperlinks(wiki_table)
  print(Helpers.static_final_links)


if __name__ == "__main__":
    app.run(debug=True)
