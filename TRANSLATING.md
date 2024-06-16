---
orphan: true
---
# Translation Guide for the Python Packaging Guide

This guide will help you get started contributing to the translation of the Python Packaging Guide.

The process of contributing to the translation of the guide is similar to the process of contributing to the guide itself, except that instead of working on the guide source files directly, you will be working on the translation files.

## Overview of the translation process

The process of preparing software for translation is called internationalization, or i18n for short. Internationalization makes sure that the software is designed in a way that makes it easy to translate into different languages without having to modify the source code, or in our case, the source files of the guide.

Sphinx, the documentation engine we use to build the Python Package Guide, has built-in support for internationalization and localization, so the process is very straightforward.

The process of actually translating the software into different languages is called localization, or l10n for short. That is the step you will be helping with.

Here is an overview of the localization workflow for the Python Packaging Guide:

1. The guide is originally written in English and stored in a set of MarkDown files.
2. The source files are processed by Sphinx to generate a set of translation files stored in the `./locale` folder.
3. Contributors (like you!) translated these files into different languages.
4. When the guide is build, Sphinx creates a version of the guide in the original language (English) and the translated versions for the languages defined in the configuration.

```{note}
You don't need to understand the technical details to contribute! But if you are interested in learning how Sphinx handles internationalization and localization, you can find more information [here](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html).
```

## Setting up your local environment

Before you start, you need to set up your local work environment.

First, fork the guide repository into your personal GitHub account. Then, clone the repository to your local computer.

Once you have the repository cloned to your local computer, follow these steps to set up a virtual environment for working on translations:

```shell
$ cd ./python-package-guide
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .[dev]
```

This will create a virtual environment in the `.venv` directory, activate this virtual environment, and install the guide's development dependencies required to build the guide and its translations locally.


## Starting a new language translation

If you are going to work on an existing translation, you can skip this step and go directly to the next section.

Before starting the translation of a new language, you need to add the new language to the `LANGUAGES` list in the `noxfile.py` configuration file. Nox is the tool we use to manage the building of the guide and its translations.

Inside `noxfile.py`, find the `LANGUAGES` list and add the two-letter code corresponding to the new language.

For example, if you want to start the translation of the guide into French, you would add `'fr'`:

```python
## Localization options (translations)

# List of languages for which locales will be generated in (/locales/<lang>)
LANGUAGES = ["es", "fr"]

```

```{note}
You can find a list of the two-letter ISO language codes [here](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).
```

## Preparing the translation files

```{admonition} IMPORTANT
This step is important to ensure that the translation files are up to date with the latest version of the guide!
```

The translation files contain the original English text and a space for you to enter the translated text. Before starting to translate, you need to make sure the translation files are up to date with the latest changes to the guide.

You can do this by running the following command:

```shell
$ nox -s update-translations
```

This command will create the translation files if you are just starting the translation of a new language, or update the existing translation files for the existing translations (defined in the `LANGUAGES` list in `noxfile.py`).

The translation files are text files with the `.po` extension, and contain the original English text and a space for you to enter the translated text. They are stored in the `locale` subdirectory corresponding to each language. For example, the translation files for Spanish are stored in the `locale/es/LC_MESSAGES` directory.

Because the translation files map the original English text to translated text, they are sometimes referred to as "catalog" files or "portable object" files.

```{note}
You don't need to know the details about the PO format, but you can find more information in the [GNU gettext documentation](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).
```

## Working on a translation

Okay, you are all set up and ready to start working on a translation!

Go to the `locale` subdirectory for the language you are working on (for example, `./locale/es/LC_MESSAGES/` for the Spanish translation).

You will find a set of `.po` files corresponding to the different sections of the guide:

```shell
$ cd ./locales/es/LC_MESSAGES/
$ ls *.po

./locales/es/LC_MESSAGES/CONTRIBUTING.po
./locales/es/LC_MESSAGES/index.po
./locales/es/LC_MESSAGES/tests.po
./locales/es/LC_MESSAGES/tutorials.po
./locales/es/LC_MESSAGES/documentation.po
./locales/es/LC_MESSAGES/package-structure-code.po
./locales/es/LC_MESSAGES/TRANSLATING.po
```

```{note}
You may also see some `.mo` files in the same directory. These are compiled versions of the `.po` files create by Sphinx during the build process and used to generate the translated versions of the guide. These files are not meant to be edited directly and are not be stored in the repository.
```

If you are working on a new translation, choose one of the `.po` files to start with. If you are working on an existing translation, you can start with the `.po` files that need the most work.

To see statistics about the translation files, you can run the `sphinx-intl stat` command. It will list the number of translated, fuzzy, and untranslated strings in each `.po` file. For example, to see the statistics for the Spanish translation, you would run:

```shell
$ sphinx-intl stat -l es

locales/es/LC_MESSAGES/tutorials.po: 0 translated, 0 fuzzy, 950 untranslated.
locales/es/LC_MESSAGES/TRANSLATING.po: 0 translated, 0 fuzzy, 44 untranslated.
locales/es/LC_MESSAGES/package-structure-code.po: 0 translated, 0 fuzzy, 885 untranslated.
locales/es/LC_MESSAGES/CONTRIBUTING.po: 0 translated, 0 fuzzy, 38 untranslated.
locales/es/LC_MESSAGES/documentation.po: 0 translated, 0 fuzzy, 430 untranslated.
locales/es/LC_MESSAGES/tests.po: 155 translated, 2 fuzzy, 3 untranslated.
locales/es/LC_MESSAGES/index.po: 88 translated, 0 fuzzy, 5 untranslated.
```

- Translated strings are strings that have been translated into the target language.
- Fuzzy strings are strings that have been translated but need to be reviewed because the original English string in the guide changed.
- Untranslated strings are strings that have not been translated yet.

```{note}
When Sphinx is building the guide in another language, it will look into the corresponding directory in `./locales/` for the translated strings and use them if they are available, or default to the original English strings if they are not.
```

## Editing the translation files

You can use any text editor to edit the `.po` files directly, but if you prefer, you can use a tool like [Poedit](https://poedit.net/) to help you manage the translation process.

Depending on your text editor of choice, you may be able to install a plugin or extension that will make it easier to work with `.po` files. For example, if you are using Visual Studio Code, you can install the ADD LINK AND DETAILS HERE extension.

If you are working on Visual Studio Code and have access to Github Copilot, you can use the `po` language mode to get suggestions for translations, which can help speed up the translation process significantly. You will still have to review and edit the suggestions to make sure they are accurate and appropriate for the context.

## Building the translated documentation locally on your computer

Once you have made changes to the translation files, you can build the translated versions of the guide locally on your computer to see how the changes look. In order to do this, you will need to run the following command:

```
nox -s translations-build
```

This will build the translated versions of the guide for all languages defined in the `LANGUAGES` list in `noxfile.py`. You can find the output in the `_build/html` directory. The translations will be in subdirectories named after the language code (e.g., `es`, `fr`, etc.).

You can also build a live version of the documentation that updates when you update local files by running the following command, if you want to build the translation for Spanish:

```
nox -s docs-live-lang -- es
```

Notice that in this case you need to pass the language code of the translation you want to build. And you need to remember to use `--` to indicate that the following arguments are meant to the commands inside the session, not to `nox`.

When you build the documentation like this, you can access a live version of the translated guide at a localhost address, generally http://localhost:8000. Sphinx will rebuild the documentation whenever you make changes to the translation files, so you can see the changes in real time on your browser.


## Submitting a PR for your translation

Before you submit a PR for your translation, you should make sure that the translated version of the guide build correctly and looks good in the browser:

1. Build the guide with additional warnings enabled using the following command:

```
nox -s docs-test
```

2. Make sure there are no warnings or errors in the output. If there are, you will need to fix them before submitting the PR.
3. Make sure the translated version of the guide looks good in the browser. Check that all the text is translated correctly and that the formatting looks good. You can do this by opening the `_build/html/<lang>/index.html` file, where `<lang>` is the language you have been working on, in your browser and navigating through the guide to find the sections you have translated.

Once you have verified that the translated version of the guide looks good and builds correctly, you can submit a PR to the main repository with your translation.

## The review process for translations

## Frequently Asked Questions (FAQ)
