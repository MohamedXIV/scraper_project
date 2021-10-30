#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fpdf import FPDF, HTMLMixin
import pandas as pd

from helpers import Helpers


"""




    *** NOT F#$%*&$ USABLE, I'M GIVEN UP TO MAKE IT WORK ARABIC ***




"""











class MyFPDF(FPDF, HTMLMixin):
    pass


TAJWAL_MEDIUM_FONT = "static/fonts/Tajawal-Medium.ttf"
text = "مرحبا العالم"
# utext = text.decode("utf-8").encode("windows-1252").decode("utf-8")
url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"

# Helpers.getHtmlTable(url)

# df = Helpers.static_df
n_text = "الصلاصية"  # (df.iloc[0].iloc[0])

with open("readme.txt", "w", encoding="utf-8") as f:
    f.write(n_text)


s_text = "العالم"

html = f"""
<H1 align="center">{s_text}</H1>
<h2>Basic usage</h2>
"""


pdf = MyFPDF()
pdf.set_doc_option('core_fonts_encoding', 'utf-8')
# First page
pdf.add_page()
pdf.write_html(html)
pdf.output("html.pdf", "F")
# pdf = FPDF()
# 
# pdf.add_page()
# pdf.add_font('TAJWAL', '', TAJWAL_MEDIUM_FONT, uni=True)
# pdf.set_font('TAJWAL', '', 14)
# pdf.cell(0, 60, 'Hello World!', 1, 1, 'C')
# pdf.cell(0, 60, 'Second!', 1, 1, 'C')
# pdf.cell(0, 60, s_text, 1, 1, 'C')
# # #pdf.cell(0, 10, 'Powered by FPDF.', 0, 1, 'C')
# pdf.output('tuto1.pdf', 'F')

# print(utext)
