from slurm.types import Tossup

from docx import Document
from docx.text.paragraph import Paragraph
from html.parser import HTMLParser
from typing import List, Optional, Self


class FileWriter:
    """ Interface for writing tossups to a file. """

    def write_tossups(
        self: Self,
        packet_name: str,
        tossups: List[Tossup],
        basename: Optional[str]=None
    ) -> None:
        """ Writes the tossups to a document with the given basename and assigns the given name to the packet. """
        pass


class MicrosoftWordWriter(FileWriter):
    """ File writer which writes tossups to a Microsoft Word document. """

    def write_tossups(
        self: Self,
        packet_name: str,
        tossups: List[Tossup],
        basename: Optional[str]=None
    ) -> None:
        document = Document()
        document.add_heading(packet_name, 0)

        for tossup in tossups:
            self.write_question(document, tossup.question)
            self.write_answerline(document, tossup.formatted_answer)
        
        document.save(f"{basename if basename else packet_name}.docx")
    
    def write_question(self: Self, document: Document, question: str) -> None:
        document.add_paragraph(question, style="List Number")

    def write_answerline(self: Self, document: Document, answerline: str) -> None:
        paragraph = document.add_paragraph("ANSWER: ", style="List Continue")
        parser = self.MicrosoftWordAnswerLineParser(paragraph)
        parser.feed(answerline)

    class MicrosoftWordAnswerLineParser(HTMLParser):
        def __init__(self: Self, paragraph: Paragraph):
            self.paragraph = paragraph
            self.bold = self.underline = False
            super().__init__()

        def handle_starttag(self: Self, tag: str, attrs):
            if tag == "u":
                self.underline = True
            if tag == "b":
                self.bold = True

        def handle_endtag(self: Self, tag: str):
            if tag == "u":
                self.underline = False
            if tag == "b":
                self.bold = False

        def handle_data(self: Self, data: str):
            run = self.paragraph.add_run(data)
            run.underline = self.underline
            run.bold = self.bold