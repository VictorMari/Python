import win32com.client as ComAPI
import os.path as path
 
class MsWord:
    def __init__(self, *args, **kwargs):
        self.instance = ComAPI.gencache.EnsureDispatch('Word.Application')
        self.htmlFolder = kwargs["out-html"]
        for documentPath in args:
            self.instance.Documents.Open(documentPath)

    def convertDocumentsToHTML(self):
        for document in self.instance.Documents:
            destination = path.join(self.htmlFolder, f"{document.Name[:-5]}.html")
            document.SaveAs(destination, ComAPI.constants.wdFormatFilteredHTML)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.instance.Quit()


if __name__ == '__main__':
    File = path.join(path.curdir, "Test_File.docx")
    conf = {
        "out-html": path.abspath(path.curdir)
    }

    with MsWord(path.abspath(File), **conf) as office:
        office.convertDocumentsToHTML()
    