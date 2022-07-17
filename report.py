#import time
#import datetime
#import json

class report():

    def __init__(self, dir_path):

        self._report_path = dir_path + "/_report.html"

        # Init report file
        html = """<!DOCTYPE html>
        <html lang="fi" class="no-js">
        <head>
        <meta charset="UTF-8">
        <title>Baim Report</title>
        <link rel='stylesheet' href='styles.css' media='all' />
        </head>
        <body>
        """

        f = open(self._report_path, "w+")
        f.write(html)
        f.close()

        # Init css file
        self._css_path = dir_path + "/styles.css"

        css = """
        body {
            font-family: sans-serif;
        }
        """

        f = open(self._css_path, "w+")
        f.write(css)
        f.close()


    def add_segment(self, props, segment_filename):
        html = "" 
        html += "<div class='segment'>\n"

        html += """
        <figure>
            <figcaption>""" + segment_filename + """</figcaption>
            <audio
                controls
                src='""" + segment_filename + """'>
            </audio>
        </figure>
        """

        html += segment_filename
        html += "<p>" + props["scientific_name"] + " " + str(props["confidence"]) + " " + props["audio_filename"] + "</p>"
        html += "</div>\n"

        file = open(self._report_path, "a")
        file.write(html + "\n")
        file.close()

    def add_taxon_divider(self, taxon_name):
        html = ""
        html += f"<h2>{taxon_name}</h2>\n"
        file = open(self._report_path, "a")
        file.write(html + "\n")
        file.close()
