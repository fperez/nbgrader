from IPython.nbformat.current import read as read_nb
from nbgrader.preprocessors import IncludeHeaderFooter


class TestIncludeHeaderFooter(object):

    def setup(self):
        with open("tests/files/test.ipynb", "r") as fh:
            self.nb = read_nb(fh, 'ipynb')
        self.preprocessor = IncludeHeaderFooter()

    def test_concatenate_nothing(self):
        """Are the cells the same if there is no header/footer?"""
        nb, resources = self.preprocessor.preprocess(self.nb, {})
        assert nb == self.nb

    def test_concatenate_header(self):
        """Is the header prepended correctly?"""
        self.preprocessor.header = "tests/files/test.ipynb"
        cells = self.nb.worksheets[0].cells
        self.nb.worksheets[0].cells = cells[:-1]
        nb, resources = self.preprocessor.preprocess(self.nb, {})
        assert nb.worksheets[0].cells == (cells + cells[:-1])

    def test_concatenate_footer(self):
        """Is the footer appended correctly?"""
        self.preprocessor.footer = "tests/files/test.ipynb"
        cells = self.nb.worksheets[0].cells
        self.nb.worksheets[0].cells = cells[:-1]
        nb, resources = self.preprocessor.preprocess(self.nb, {})
        assert nb.worksheets[0].cells == (cells[:-1] + cells)

    def test_concatenate_header_and_footer(self):
        """Is the header and footer concatenated correctly?"""
        self.preprocessor.header = "tests/files/test.ipynb"
        self.preprocessor.footer = "tests/files/test.ipynb"
        cells = self.nb.worksheets[0].cells
        self.nb.worksheets[0].cells = cells[:-1]
        nb, resources = self.preprocessor.preprocess(self.nb, {})
        assert nb.worksheets[0].cells == (cells + cells[:-1] + cells)
