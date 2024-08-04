""" MkDocs plugin to add interactive exercises to the documentation. """
import os
import re
import shutil
import gettext
from pathlib import Path
import jinja2
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.config import base, config_options as c
from mkdocs.config.base import Config as MkDocsConfig
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

log = get_plugin_logger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')


class MyPluginConfig(base.Config):
    exercise_label = c.Type(str, default='')
    submit_label = c.Type(str, default='')


class Exercises(BasePlugin[MyPluginConfig]):
    def __init__(self):
        self.current_exercise_id = 0
        self.enabled = True
        self.static_files = []
        self.total_time = 0
        self._ = gettext.gettext
        self.re_admonition = re.compile(r'((?:\?\?\?|!!!)\s+exercise[^"]+")([^"]+)(")')
        self.re_placeholder = re.compile(r'\{\{([^\{]+?)\}\}')

    def _set_language(self, lang):
        """Set the language for translations."""
        language_code = lang if isinstance(lang, str) else lang.language

        try:
            translation = gettext.translation('messages',
                                              localedir=LOCALES_DIR,
                                              languages=[language_code])
            translation.install()
            self._ = translation.gettext
        except FileNotFoundError:
            gettext.install('messages', localedir=LOCALES_DIR)
            self._ = gettext.gettext

    def _register_static_files(self, config):
        """Find static files to be copied later."""
        path = Path(__file__).parent / 'static'
        for file in path.iterdir():
            if not file.is_file():
                continue
            self.static_files.append(file)
            mapping = [
                ('.css', 'extra_css'),
                ('.js', 'extra_javascript')]
            for ext, key in mapping:
                if file.suffix == ext:
                    if key not in config:
                        config[key] = []
                    config[key].append(file.name)

    def on_config(self, config: MkDocsConfig):
        """ Identify static files to be copied later, update the config
        to include extra js and css files.
        """
        # Configure the language
        lang = config['theme']['locale'] if 'locale' in config['theme'] else 'en'
        self._set_language(lang)

        # Process the plugin configuration
        if self.config.exercise_label == '':
            self.config.exercise_label = self._('Exercise')
        if self.config.submit_label == '':
            self.config.submit_label = self._('Submit')

        # Process extra files
        self._register_static_files(config)

        return config

    def on_post_build(self, config: MkDocsConfig):
        """ Copy static files to the site directory.
        """
        output_dir = Path(config['site_dir'])
        for file in self.static_files:
            log.debug(f"Copying {file.name} to {output_dir.name}")
            shutil.copy(file, output_dir / file.name)

    def on_page_markdown(self, markdown: str, page, config, files):
        """ Prefix the exercises with the exercise label. """
        def add_exercise_title(match):
            self.current_exercise_id += 1
            return f'{match.group(1)}{self.config.exercise_label}: {match.group(2)}{match.group(3)}'
        return self.re_admonition.sub(add_exercise_title, markdown)

    def on_page_content(self, html, page, config, files):
        """ Apply the exercise types to the content. """
        soup = BeautifulSoup(html, 'html.parser')

        for div in soup.find_all('div', class_='exercise'):
            # Add span to display reset button
            element = div.find('p', class_='admonition-title')
            exercise_name = element.get_text()
            element.clear()
            element.append(BeautifulSoup(
                f'{exercise_name}<span class="exercise-title"></span>', 'html.parser'))

            # Detect exercise type based on content
            exercise_type = []
            if re.findall(r'\[[x ]\]', str(div)):
                exercise_type += ['checkbox']
            if re.findall(r'\{\{[^\{]+?\}\}|\[\[[^\{]+?\]\]', str(div)):
                exercise_type += ['fill-in-the-blank']
            if len(exercise_type) > 1:
                log.error(f"Unable to detect exercise type")
            div['class'] += exercise_type

            # Apply the exercise type
            if 'checkbox' in exercise_type:
                # Detect if the exercise is missing correct choices
                if not re.findall(r'\[x\]', str(div)):
                    log.error(f"Exercise '{exercise_name}' in file '{page.file.name}' is missing correct choices")
                self.apply_multiple_choice_type(div)
            if 'fill-in-the-blank' in exercise_type:
                self.apply_fill_in_the_blank_type(div)

        return str(soup)

    def apply_multiple_choice_type(self, div):
        """ Multiple choice exercise type """
        if not hasattr(self, 'multiple_choice_template'):
            template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template("exercise_item.html")
            self.multiple_choice_template = template

        for ul in div.find_all('ul', recursive=False):
            ul['class'] = 'exercise-list'
            for li in ul.find_all('li', recursive=False):
                print(f"li: {li.get_text()}")
                li_content = ''.join(map(str, li.contents))
                is_correct_choice = True if '[x]' in li_content else False
                li_content = re.sub(r'\[(x| )\]', '', li_content)
                rendered = self.multiple_choice_template.render(
                    content=li_content,
                    checked=False,
                    good=is_correct_choice)

                new_li = BeautifulSoup(rendered, 'html.parser')
                li.insert_after(new_li)
                li.decompose()

    def apply_fill_in_the_blank_type(self, element):
        """ Fill in the blank exercise type """
        template = jinja2.Template(
            '<input type="text" style="width: {{width}}ch;" '
            'class="text-with-gap" answer="{{answer}}"/>'
        )

        def add_tag(match):
            return template.render(
                width=len(match.group(1))+2, answer=match.group(1))

        def replace_placeholders(element):
            new_contents = []
            for content in element.contents:
                if isinstance(content, NavigableString):
                    new_content = self.re_placeholder.sub(add_tag, content)
                    new_soup = BeautifulSoup(new_content, 'html.parser')
                    new_contents.extend(new_soup.contents)
                elif isinstance(content, Tag):
                    if content.name not in ['code']:
                        replace_placeholders(content)
                    new_contents.append(content)
                else:
                    new_contents.append(content)
            element.clear()
            for new_content in new_contents:
                element.append(new_content)

        replace_placeholders(element)

        # Add a button in the last position in element
        template = jinja2.Template(
            '<p class="align--right">'
            '<button class="md-button md-button--primary md-button--small '
            'exercise-submit">'
            f'{self.config.submit_label}'
            '</button></p>')
        new_button = BeautifulSoup(template.render(), 'html.parser')
        element.append(new_button)