import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

# Exemple de HTML
html = '''
<html>
<head><title>Example Page</title></head>
<body>
<p class="intro">Roses are {{color}}, violets are {{another_color}}.</p>
<p class="intro">This is a {{test}} paragraph.</p>
</body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

# Find body
element = soup.find('body')

def sub(string):
    return re.sub(r'\{\{([^\{]+?)\}\}', r'<input type="text" class="fill-in-the-blank" placeholder="\1"/>', string)

def replace_placeholders(element):
    # Liste temporaire pour stocker les nouvelles parties
    new_contents = []

    for content in element.contents:
        if isinstance(content, NavigableString):
            new_content = sub(content)
            new_soup = BeautifulSoup(new_content, 'html.parser')
            new_contents.extend(new_soup.contents)
        elif isinstance(content, Tag):
            replace_placeholders(content)
            new_contents.append(content)
        else:
            new_contents.append(content)

    # Vider l'élément original et ajouter les nouvelles parties
    element.clear()
    for new_content in new_contents:
        element.append(new_content)

replace_placeholders(element)

print(soup.prettify())
