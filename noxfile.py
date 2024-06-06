import os
import pathlib
import shutil
import nox

nox.options.reuse_existing_virtualenvs = True

## Sphinx related options

# Sphinx output and source directories
BUILD_DIR = '_build'
OUTPUT_DIR = pathlib.Path(BUILD_DIR, "html")
SOURCE_DIR = pathlib.Path(".")

# Location of the translation templates
TRANSLATION_TEMPLATE_DIR = pathlib.Path(BUILD_DIR, "gettext")

# Sphinx build commands
SPHINX_BUILD = "sphinx-build"
SPHINX_AUTO_BUILD = "sphinx-autobuild"

# Sphinx parameters used to build the guide
BUILD_PARAMETERS = ["-b", "html"]

# Sphinx parameters used to test the build of the guide
TEST_PARAMETERS = ['-W', '--keep-going', '-E', '-a']

# Sphinx parameters to generate translation templates
TRANSLATION_TEMPLATE_PARAMETERS = ["-b", "gettext"]

# Sphinx-autobuild ignore and include parameters
AUTOBUILD_IGNORE = [
    "_build",
    "build_assets",
    "tmp",
]
AUTOBUILD_INCLUDE = [
    pathlib.Path("_static", "pyos.css")
]

## Internationalization options (translations)

# List of languages for which locales will be generated in (/locales/<lang>)
LANGUAGES = ["es"]

# List of languages to build, a subset of LANGUAGES including the language translations that are ready to publish
EXCLUDE_FROM_BUILD_LANGUAGES = []


@nox.session
def docs(session):
    """Build the packaging guide."""
    session.install("-e", ".")
    session.run(SPHINX_BUILD, *BUILD_PARAMETERS, SOURCE_DIR, OUTPUT_DIR, *session.posargs)
    # When building the guide, also build the translations
    session.notify("translation-build")

@nox.session(name="docs-test")
def docs_test(session):
    """Build the packaging guide with additional parameters."""
    session.install("-e", ".")
    session.run(SPHINX_BUILD, *BUILD_PARAMETERS, *TEST_PARAMETERS, SOURCE_DIR, OUTPUT_DIR, *session.posargs)
    # When building the guide with testing parameters, also build the translations with those parameters
    session.notify("translation-build", TEST_PARAMETERS)

@nox.session(name="docs-live")
def docs_live(session):
    """Build and launch a local copy of the guide."""
    session.install("-e", ".")
    cmd = [SPHINX_AUTO_BUILD, *BUILD_PARAMETERS, SOURCE_DIR, OUTPUT_DIR, *session.posargs]
    for folder in AUTOBUILD_IGNORE:
        cmd.extend(["--ignore", f"*/{folder}/*"])
    session.run(*cmd)

@nox.session(name="docs-clean")
def clean_dir(session):
    """Clean out the docs directory used in the live build."""
    session.warn(f"Cleaning out {OUTPUT_DIR}")
    dir_contents = OUTPUT_DIR.glob('*')
    for content in dir_contents:
        session.log(f'removing {content}')
        if content.is_dir():
            shutil.rmtree(content)
        else:
            os.remove(content)

@nox.session(name="translation-update")
def translation_update(session):
    """Update the templates (.pot), and translation files (.po) for each of the languages."""
    session.install("-e", ".")
    session.install("sphinx-intl")
    session.log("Updating gettext templates (.pot)")
    session.run(SPHINX_BUILD, *TRANSLATION_TEMPLATE_PARAMETERS, SOURCE_DIR, TRANSLATION_TEMPLATE_DIR, *session.posargs)
    for lang in LANGUAGES:
        session.log(f"Updating .po files for [{lang}] translation")
        session.run("sphinx-intl", "update", "-p", TRANSLATION_TEMPLATE_DIR, "-l", lang)

@nox.session(name="translation-build")
def translation_build(session):
    """
    Build the translations for the project
    """
    BUILD_LANGUAGES = [lang for lang in LANGUAGES if lang not in EXCLUDE_FROM_BUILD_LANGUAGES]
    if not BUILD_LANGUAGES:
        session.warn("No languages specified for translation build")
        return
    session.install("-e", ".")
    for lang in BUILD_LANGUAGES:
        session.log(f"Building [{lang}] guide")
        session.run(SPHINX_BUILD, *BUILD_PARAMETERS, "-D", f"language={lang}", ".", OUTPUT_DIR / lang, *session.posargs)
