import os
import requests
import bs4
import pandas as pd
import pyshorteners
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Helpers:

    # fields
    static_final_links = []
    static_final_headers = []
    static_table_data = []
    page_title = ""
    static_df = pd.DataFrame()
    isArabic = False
    excel_file_path = "./data/excel_files/"
    csv_file_path = "./data/csv_file.csv"
    json_file_path = "./data/json_file.json"

    @staticmethod
    def getTable(url: str, isArabic: bool = None):
        """This method take an url and return a table

        Args:
            url (str): the url to get the table from,
            isArabic (bool): will reverse the order of arrays
            enter false to disable, and if not defined will detect it
            automatically.
        Returns:
            list [str]: return html table
        """
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = "utf-8"
        soup = bs4.BeautifulSoup(res.text, "lxml")
        Helpers.page_title = soup.find("title").text
        Helpers.static_final_links.clear()
        # print(Helpers.page_title)
        if isArabic is None:
            if soup.html["lang"] == "ar":
                Helpers.isArabic = True
        # print(Helpers.isArabic)
        return soup.find("table", class_="wikitable")

    @staticmethod
    def getHeaders(wiki_table: list, final_headers: list):

        table_headers = wiki_table.find_all("th")

        for header in table_headers:
            final_headers.append(header.text.strip())
            Helpers.static_final_headers = final_headers
        if Helpers.isArabic:
            final_headers.reverse()

    @staticmethod
    def getRows(wiki_table: list, final_headers: list, final_rows_data: list):

        table_rows_data = wiki_table.find_all("td")

        for row in range(0, len(table_rows_data), len(final_headers)):
            # final_rows_data.append(table_rows_data[row:])
            temp_l = []
            for t in table_rows_data[row : row + len(final_headers)]:
                temp_l.append(t.text.strip())
                # if Helpers.isArabic
            if Helpers.isArabic:
                temp_l.reverse()
            final_rows_data.append(temp_l.copy())
            temp_l.clear()


    @staticmethod
    def getHyperlinks(wiki_table: list):
        temp_l = []
        links = wiki_table.find_all("a")

        for link in range(0, len(links), 3):
            # print(link)
            for l in links[link : link + 3]:
                # print(l['href'])
                temp_l.append(l["href"])
            # print(temp_l)
            Helpers.static_final_links.append(temp_l.copy())
            temp_l.clear()
        # print(Helpers.final_links_data)
        #   final_links_data.append(temp_l)
        #   temp_l.clear()
        # print(final_links_data)

    @staticmethod
    def pdHtmlToExcelWLinks(url: str, table_index: int = 0):
        """Saves data to excel and merge links into cell values
        Note: *** Works but with some issues ***

        Args:
            url (str): [wikipedia url]
            table_index (int, optional): [description]. Defaults to 0.
        """
        tables = pd.read_html(url, index_col=0, attrs={"class": "wikitable"})
        df_copy = pd.DataFrame()

        file_name = Helpers.excel_file_path
        df_0 = pd.DataFrame(tables[table_index])
        df_copy = df_0.copy()
        temp_l = []
        for i in range(len(df_0.columns)):
            links = [l[i] for l in Helpers.static_final_links]
            lst_col = list(df_0[df_0.columns[i]])
            for idx, val in enumerate(links):
                temp_l.append(Helpers.makeHyperlink(val, lst_col[idx]))
            df_copy[df_0.columns[i]] = temp_l.copy()
            temp_l.clear()
        df_copy.to_excel(file_name, encoding="utf-8")

    @staticmethod
    def pdHtmlToExcel(url: str = None, table_index: int = 0, fileName: str = None):
        # tables = pd.read_html(url, index_col=0, attrs={'class': 'wikitable'})
        if fileName is None:
            file_name = f"{Helpers.excel_file_path}{Helpers.page_title}.xlsx"
        else:
            file_name = f"{Helpers.excel_file_path}{fileName}.xlsx"

        short_links = Helpers.linkShortner(Helpers.static_final_links)

        links_lst = [f'=HYPERLINK("{l}", "Link")' for l in short_links]
        df = Helpers.static_df  # pd.DataFrame(tables[table_index])
        print(len(links_lst) == len(df[df.columns[0]]))
        if len(links_lst) == len(df[df.columns[0]]):
            df["Links"] = links_lst
        df.to_excel(file_name, encoding="utf-8")

    @staticmethod
    def getHtmlTable(url: str, table_index: int = 0):
        tables = pd.read_html(url, index_col=0, attrs={"class": "wikitable"})
        file_name = Helpers.excel_file_path

        df = pd.DataFrame(tables[table_index])

        Helpers.static_df = df.copy()

        return df.to_html()

    @staticmethod
    def readExcelFile(file_name):
        df = pd.read_excel(file_name)
        #print(df.head())

    @staticmethod
    def makeHyperlink(path: str, name: str):
        domain = f"https://ar.wikipedia.org{path}"
        return f'=HYPERLINK("{domain}", "{name}")'

    @staticmethod
    def linkShortner(links: list):
        s = pyshorteners.Shortener()
        short_links = []

        for link in links:
            l = f"https://ar.wikipedia.org{link[0]}"
            if len(l) > 240:
                t = s.tinyurl.short(l)
            else:
                t = l
            short_links.append(t)
        #print(short_links)
        return short_links
