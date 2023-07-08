from sphinx.ext.apidoc import main
import sphinx.builders
import sphinx.application

# create sphinx documentation for the project
def create_sphinx_docs(project_path):
    main(['-o', './docs', '.'])

def sphinx_build():
    # sphinx.builders.Builder.build(['main.rst'], "summary")
    pass

create_sphinx_docs('')
sphinx_build()