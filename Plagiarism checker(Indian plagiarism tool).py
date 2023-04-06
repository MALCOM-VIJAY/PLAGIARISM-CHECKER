from flask import Flask, request, render_template
from keybert import KeyBERT
import requests
import re
from bs4 import BeautifulSoup as bs
import difflib


import PyPDF2
app = Flask(__name__)


@app.route('/status')
def status():
    return "Backend is up and running"


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/plagiarism', methods=['POST'])
def check_plag():
    if request.method == 'POST':

        # getting file
        f = request.files['file']
        inp_txt = ''

        if ('.txt' in str(f)):
            inp_txt = f.read()

        if ('.pdf' in str(f)):
            pdfReader = PyPDF2.PdfReader(f)
            for i in range(len(pdfReader.pages)):
                inp_txt += str(pdfReader.pages[i].extract_text())

        # Extracting keywords
        language = "en"
        max_ngram_size = 3
        deduplication_threshold = 0.05
        numOfKeywords = 20
        kw_model = KeyBERT()

        # custom_kw_extractor = yake.KeywordExtractor(
        #     lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
        keywords = kw_model.extract_keywords(str(inp_txt))

        # Scraping websites for each keyword
        plag_score = {}
        for title in keywords:

            regex = re.compile(r'<[^>]+>')

            url = [r"https://en.wikipedia.org/wiki/", r"https://www.britannica.com/topic/", r"https://deletionpedia.org/en/",
                   r"https://en.citizendium.org/wiki/", r"https://www.infoplease.com/encyclopedia/science/engineering/computer/"]

            for site in url:
                if 'wikipedia' or 'deletionpedia' or 'citizendium' in site:
                    site = site+title[0].capitalize().replace(' ', '_')
                elif 'britannica' or 'encyclopedia' in site:
                    site = site+title[0].replace(' ', '-')

                result = requests.get(site)
                doc = bs(result.text, "html.parser")

                str_htm = ''
                for i in doc.find_all(['p', 'h']):
                    str_htm += str(i)

                cmp_txt = regex.sub('', str_htm)

                similarity = difflib.SequenceMatcher(
                    None, str(inp_txt), str(cmp_txt)).ratio()
        plag_score[site] = similarity*100

    max_value = round(max(plag_score.values()), 4)

    for key, value in plag_score.items():
        if max_value == round(max(plag_score.values()), 4):
            max_key = key

    return render_template("results.html", plag_score=max_value, matched_site=max_key)


if __name__ == "__main__":
    app.run()
