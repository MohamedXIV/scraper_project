from flask import Flask, render_template, request, redirect, send_file, url_for
from flask_weasyprint import HTML, render_pdf
import requests
import json
from helpers import Helpers
from gsheet import saveToGSheet
import webbrowser
from mkepdf import makePDFFromString, makePDFFromFile, makePDFFromTemplate
from mkeqr import saveQRImages
from mkezip import make_zip_file
from io import BytesIO

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        url = request.form["url"]
        wiki_table = Helpers.getTable(url, False)
        Helpers.getHyperlinks(wiki_table)
        return render_template("index.html", table=Helpers.getHtmlTable(url))


@app.route("/loadTable/<string:formUrl>", methods=["POST"])
def load_table(formUrl):
    url = request.form[formUrl]
    wiki_table = Helpers.getTable(url, False)
    Helpers.getHyperlinks(wiki_table)
    return render_template("index.html", table=Helpers.getHtmlTable(url))


@app.route("/downloadExcel", methods=["GET"])
def download_excel():
    # buffer = BytesIO()
    Helpers.pdHtmlToExcel()
    # send_file(buffer, as_attachment=True, attachment_filename='a_file.txt')
    return send_file(
        f"{Helpers.excel_file_path}{Helpers.page_title}.xlsx", as_attachment=True
    )


@app.route("/saveToGSheet")
def save_to_gsheet():
    saveToGSheet()
    webbrowser.open_new_tab(saveToGSheet())
    return redirect(saveToGSheet())


@app.route("/downloadCSV", methods=["GET"])
def download_pdf():
    Helpers.pdHtmlToCsv()
    return send_file(
        f"{Helpers.csv_file_path}{Helpers.page_title}.csv", as_attachment=True
    )


@app.route("/getJson", methods=["GET"])
def get_json():
    return Helpers.pdHtmlToJson()


@app.route("/downloadPDFCovers", methods=["GET"])
@app.route("/downloadPDFCovers/<int:itr>", methods=["GET"])
def download_pdf_covers(itr):
    saveQRImages()
    makePDFFromTemplate(itr)
    make_zip_file()
    return send_file(f"{Helpers.zip_file_path}covers.zip", as_attachment=True)
    # "Congrats!, you have downloaded the PDFs"


def scrape_table(url):
    wiki_table = Helpers.getTable(url, False)
    Helpers.getHyperlinks(wiki_table)
    print(Helpers.static_final_links)


if __name__ == "__main__":
    app.run(debug=True)
