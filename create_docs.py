from sphinx.ext.apidoc import main
import sphinx.application as sphinx
import conf as conf

# create sphinx documentation for the project
def create_sphinx_docs(project_path):
    # create rst files for each python class
    main(['-o', './source', project_path])
    # create index.rst
    

def sphinx_build():
    # sphinx.builders.Builder.build(['main.rst'], "summary")
    conf.project = input("Enter the project name: ")
    conf.copyright = input("Enter copyright/license: ")
    conf.copyright = input("Enter author(s): ")

    app = sphinx.Sphinx(srcdir="./source", confdir=".", outdir="./build/html", doctreedir="./build/doctrees", buildername="html")
    app.build()

if __name__ == "__main__":
    create_sphinx_docs('.')
    sphinx_build()