import os
import sys
import shutil
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c
from mkdocs.config.base import Config as MkDocsConfig
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import Files
import re

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
import colorama

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import jinja2

log = get_plugin_logger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

class MyPluginConfig(base.Config):
    foo = c.Type(str, default='a default value')
    bar = c.Type(int, default=0)
    baz = c.Type(bool, default=True)

class Exercises(BasePlugin[MyPluginConfig]):

    config_scheme = (
        ('param', config_options.Type(str, default='')),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_config(self, config: MkDocsConfig):
        css_file = 'exercise.css'
        if 'extra_css' not in config:
            config['extra_css'] = []
        config['extra_css'].append(css_file)

        js_file = 'exercise.js'
        if 'extra_javascript' not in config:
            config['extra_javascript'] = []
        config['extra_javascript'].append(js_file)

        return config

    def on_files(self, files, config):
        # for file in files:
        #     if '.md' in file.src_path:
        #         file.content_string = file.content_string.replace('function', 'chocolat')
        #         print(file.content_string)
        # print('on_files', files)
        return files

    def on_nav(self, nav, config, files):
        for page in nav.pages:
            page.exercises_id = 1

        return nav

    def on_page_markdown(self, markdown, page, config, files):
        def add_exercise_title(match):
            page.exercises_id += 1
            return f'{match.group(1)}Exercise {page.exercises_id}: {match.group(2)}{match.group(3)}'

        markdown = re.sub(r'((?:\?\?\?|!!!)\s+exercise[^"]+")([^"]+)(")', add_exercise_title, markdown)
        markdown = markdown.replace('function', 'pomme')

        return markdown

    def on_page_content(self, html, page, config, files):
        html = html.replace('pomme', 'vanille')




        soup = BeautifulSoup(html, 'html.parser')

        for div in soup.find_all('div', class_='admonition solution'):
            div['class'] += ['solution', 'hidden']

        for div in soup.find_all('div', class_='exercise'):
            # Replace text in .admonition-title with an additional <span> element
            element = div.find('p', class_='admonition-title')

            text = element.get_text()
            element.clear()
            element.append(BeautifulSoup(f'{text}<span class="exercise-title"></span>', 'html.parser'))

            # Detect exercise type based on content
            exercise_type = []
            if re.findall(r'\[x\]', str(div)):
                exercise_type += ['checkbox']
            if re.findall(r'\{\{[^\{]+?\}\}|\[\[[^\{]+?\]\]', str(div)):
                exercise_type += ['fill-in-the-blank']
            if len(exercise_type) > 1:
                log.error(f"Unable to detect exercise type")
            log.warning(f"Detected exercise type: {exercise_type}")

            div['class'] += exercise_type

            if 'checkbox' in exercise_type:
                self.applyMultipleChoice(div)
            if 'fill-in-the-blank' in exercise_type:
                self.applyFillInTheBlank(div)


        html = str(soup)
        return html

    def on_post_build(self, config):
        # Copier le fichier CSS dans le répertoire de sortie
        output_dir = config['site_dir']
        static_dir = os.path.join(os.path.dirname(__file__), 'css')
        css_file = os.path.join(static_dir, 'exercise.css')
        if os.path.exists(css_file):
            shutil.copy(css_file, os.path.join(output_dir, 'exercise.css'))

        static_dir = os.path.join(os.path.dirname(__file__), 'js')
        css_file = os.path.join(static_dir, 'exercise.js')
        if os.path.exists(css_file):
            shutil.copy(css_file, os.path.join(output_dir, 'exercise.js'))

    def applyMultipleChoice(self, div):
        if not hasattr(self, 'multiple_choice_template'):
            template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template("exercise_item.html")
            self.multiple_choice_template = template

        for ul in div.find_all('ul'):
            ul['class'] = 'exercise-list'
            for li in ul.find_all('li'):

                li_content = ''.join(map(str, li.contents))
                checked = False
                if '[x]' in li_content:
                    log.error("Found checked")
                    checked = True
                    li_content = li_content.replace('[x]', '')
                if '[ ]' in li_content:
                    log.error("Found unchecked")
                    checked = False
                    li_content = li_content.replace('[ ]', '')

                rendered = self.multiple_choice_template.render(content=li_content,checked=False,good=checked)

                new_li = BeautifulSoup(rendered, 'html.parser')
                #li.replace_with(new_li)
                li.insert_after(new_li)
                li.decompose()

    def applyFillInTheBlank(self, element):
        log.error("TEXT" + str(element))

        template = jinja2.Template('<input type="text" style="width: {{width}}ch;" class="text-with-gap" answer="{{answer}}"/>')

        def add_tag(match):
            return template.render(width=len(match.group(1))+2, answer=match.group(1))

        def replace_placeholders(element):
            # Liste temporaire pour stocker les nouvelles parties
            new_contents = []

            for content in element.contents:
                if isinstance(content, NavigableString):
                    new_content = re.sub(r'\{\{([^\{]+?)\}\}', add_tag, content)
                    new_content = re.sub(r'\[\[([^\{]+?)\]\]', add_tag, new_content)
                    new_soup = BeautifulSoup(new_content, 'html.parser')
                    new_contents.extend(new_soup.contents)
                elif isinstance(content, Tag):
                    if content.name not in ['code']:
                        replace_placeholders(content)
                    new_contents.append(content)
                else:
                    new_contents.append(content)

            # Vider l'élément original et ajouter les nouvelles parties
            element.clear()
            for new_content in new_contents:
                element.append(new_content)

        replace_placeholders(element)

        # Add a button in the last position in element
        template = jinja2.Template('<p class="align--right"><button class="md-button md-button--primary md-button--small exercise-submit">Valider</button></p>')
        new_button = BeautifulSoup(template.render(), 'html.parser')
        element.append(new_button)