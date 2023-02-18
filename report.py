from datetime import datetime

class report():

    def __init__(self, dir_path, version):

        self._report_path = dir_path + "/_report.html"

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")

        # Init report file
        html = """<!DOCTYPE html>
        <html lang="fi" class="no-js">
        <head>
        <meta charset="UTF-8">
        <title>Baim Report</title>
        <link rel='stylesheet' href='styles.css' media='all' />
        </head>
        <body>
        <h1>""" + dir_path + """</h1>
        <p>Generated """ + current_time + """ with version """ + version + """</p>
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
        h2 {
            margin-top: 2em;
        } 
        .segment {
            background-color: rgb(184, 210, 182);
            padding: 0.5em;
            margin-bottom: 1em;
        }
        .segment p {
            margin: 1em 1em 0 2em;
        }
        .p22, .p23 {
            font-weight: bold;
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
            <figcaption></figcaption>
            <audio
                controls
                src='""" + segment_filename + """'>
            </audio>
        </figure>
        """

#        html += segment_filename
        html += "<p class='p1'><span class='p11'>" + props["scientific_name"] + "</span> <span class='p12'>" + str(props["confidence"]) + "</span></p>"
        html += "<p class='p2'><span class='p21'>" + str(props["file_start_datetime"]) + "</span> / <span class='p22'>" + props["audio_filename"] + "</span> / <span class='p23'>" + props["segment_start"] + "</span></p>"
        
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
