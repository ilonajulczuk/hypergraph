import os

from IPython.nbformat.current import reads

from hypergraph.notebook_utils import run_notebook


def test_notebooks():
    notebooks_path = 'notebooks'
    paths = os.listdir(notebooks_path)
    notebooks_filenames = [notebooks_path + '/' + name
                           for name in paths if name.endswith('.ipynb')]

    for ipynb in notebooks_filenames:
        print("testing %s" % ipynb)
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
            run_notebook(nb)


