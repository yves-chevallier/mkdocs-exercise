# Mkdocs Exercise Plugin

This plugin is a simple exercise plugin for MkDocs. It allows you to add exercises to your markdown files and have them automatically checked when the page is loaded.

## Development

```bash
poetry install
pip install -e .
poetry run python serve.py
```

## To Do

- [ ] Use local copy of octicons
- [ ] Independent of theme
- [ ] Reapply js on page change

### Mutable observer ?

It seems that mkdocs material is quite dummy. It is not a SPA, so the content is reloaded on each page change. This means that the MutationObserver is lost on each page change. But why script is not reloaded ? Does it use some kind of PJAX" (PushState + AJAX) ?

```js
document$.subscribe(() => {
    console.log("Hello je recharge une page");
});
```
