import yaml
import re

def convert_markdown_to_html(text):
    """ Converts basic Markdown formatting to HTML equivalents. """
    if not text:
        return ""

    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)  # Bold
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)  # Italic
    return text

# Load YAML file
with open("data.yaml", "r") as f:
    data = yaml.safe_load(f)

# Start HTML output with improved styling
html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <link rel="stylesheet" href="https://edwardtufte.github.io/tufte-css/tufte.css">
    <style>
        body {{
            background-color: #fdfdfd;
            font-family: "Georgia", serif;
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }}
        h1, h2 {{
            color: #333;
            font-weight: bold;
        }}
        .epigraph {{
            font-style: italic;
            text-align: center;
            border-left: 4px solid #ccc;
            padding-left: 15px;
            margin: 30px auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        figure {{
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
        }}
        figure img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }}
        figcaption {{
            font-size: 0.85rem;
            color: #555;
            margin-top: 5px;
            text-align: center;
        }}
        .two-figures {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            margin: 20px auto;
            max-width: 100%;
        }}
        .two-figures figure {{
            flex: 1;
            text-align: center;
        }}
        .sidenote, .marginnote {{
            font-size: 0.85rem;
            color: #666;
        }}
        blockquote {{
            font-style: italic;
            border-left: 4px solid #888;
            padding-left: 15px;
            margin: 20px 0;
            color: #444;
        }}
    </style>
</head>
<body>
    <article>
        <h1>{data['title']}</h1>
        <p><em>{data['author']} - {data['date']}</em></p>
"""

# Add epigraph if present
if "epigraph" in data:
    html_output += f"""
    <blockquote class="epigraph">
        <p>{data['epigraph']['text']}</p>
        <footer>— <cite>{data['epigraph']['author']}</cite></footer>
    </blockquote>
    """

# Iterate through sections
for section in data.get("sections", []):
    html_output += f"<h2>{section['heading']}</h2>\n"

    if "content" in section:
        formatted_content = convert_markdown_to_html(section["content"])
        html_output += f"<p>{formatted_content}</p>\n"

    if "sidenote" in section:
        html_output += f'<p><span class="sidenote">{section["sidenote"]}</span></p>\n'

    if "margin_note" in section:
        html_output += f'<p><span class="marginnote">{section["margin_note"]}</span></p>\n'

    if "key_metrics" in section:
        html_output += "<table>\n<tr><th>Metric</th><th>Value</th><th>Change</th></tr>\n"
        for metric in section["key_metrics"]:
            html_output += f'<tr><td>{metric["name"]}</td><td>{metric["value"]}</td><td>{metric["change"]}</td></tr>\n'
        html_output += "</table>\n"

    if "figure" in section:
        fig = section["figure"]
        html_output += f'<figure><img src="{fig["src"]}" alt="{fig["caption"]}" style="top:10px"><figcaption>{fig["caption"]}</figcaption></figure>\n'

    if "figures" in section:
        html_output += '<div class="two-figures">\n'
        for fig in section["figures"]:
            html_output += f'<figure><img src="{fig["src"]}" alt="{fig["caption"]}"><figcaption>{fig["caption"]}</figcaption></figure>\n'
        html_output += '</div>\n'

    if "blockquote" in section:
        quote = section["blockquote"]
        html_output += f"""
        <blockquote>
            <p>{quote['text']}</p>
            <footer>— <cite>{quote['author']}</cite></footer>
        </blockquote>
        """

# Append footnotes
if "footnotes" in data:
    html_output += "<h2>Footnotes</h2>\n<ul>\n"
    for footnote in data["footnotes"]:
        html_output += f'<li id="fn-{footnote["label"]}">{footnote["text"]}</li>\n'
    html_output += "</ul>\n"

# Close HTML
html_output += """
    </article>
</body>
</html>
"""

# Save HTML file
with open("fpna_report.html", "w") as f:
    f.write(html_output)

print("HTML file created: fpna_report.html")

