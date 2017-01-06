import io
from pdfminer import high_level as pdf

class PDFDocument:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_text(self, output_file=None):
        if output_file:
            output = open(output_file, 'wb')
        else:
            output = io.StringIO()

        in_file = open(self.filepath, 'rb')
        pdf.extract_text_to_fp(in_file, output)

        if not output_file:
            content = output.getvalue()
            output.close()
            return content
