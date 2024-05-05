from data_pipeline.reporting.pdf import PDF
from data_pipeline.settings import AUTHORS, OUTPUT_DIR, TITLE


class Writer:
    def __init__(self, doc: PDF):
        self.doc = doc
        self.table_count = 0
        self.figure_count = 0

    def prepare_document(self):
        authors = ", ".join(AUTHORS)
        self.doc.add_font("arial", "", fname=r"C:\Windows\Fonts\Arial.ttf", uni=True)
        self.doc.add_font("arial", "B", fname=r"C:\Windows\Fonts\Arial.ttf", uni=True)
        self.doc.set_title(TITLE)
        self.doc.set_author(authors)
        self.doc.add_page()

    def write_markdown_text(self, filename: str, *, title: str = "", subtitle: str = "", new_page: bool = False):
        output_path = OUTPUT_DIR / "md" / filename
        with output_path.open(mode="r") as f:
            md_content = f.read()
        if new_page:
            self.doc.add_page()
        if title:
            self.doc.set_font(size=self.doc.title_font_size)
            self.doc.multi_cell(w=0, text=title.title(), align="L")
            self.doc.ln(1)
        if subtitle:
            self.doc.set_font(size=self.doc.subtitle_font_size)
            self.doc.multi_cell(w=0, text=subtitle.title(), align="L")
            self.doc.ln(1)
        self.doc.set_font(size=self.doc.text_font_size)
        self.doc.multi_cell(w=0, h=self.doc.text_font_size // 2, text=md_content, align="J", markdown=True)
        self.doc.ln(10)

    def write_markdown_table(self, filename: str, new_page: bool = False):
        raise NotImplementedError()
        # self.table_count += 1
        # output_path = OUTPUT_DIR / "md" / filename
        # with output_path.open(mode="r") as f:
        #     md_content = f.read()
        # converter = markdown2.Markdown(extras=["tables"])
        # html_content = converter.convert(md_content)
        # if new_page:
        #     self.doc.add_page()
        # self.doc.write_html(html_content)
        # self.doc.ln(10)

    def write_image(self, filename: str, new_page: bool = False):
        self.figure_count += 1
        img_path = OUTPUT_DIR / "img" / "scatterplot.png"
        if new_page:
            self.doc.add_page()
        self.doc.image(img_path, x=10, y=self.doc.get_y() + 10, w=180)
        self.doc.ln(10)

    def build_document(self, filename: str):
        output_path = OUTPUT_DIR / "pdf" / filename
        self.doc.output(str(output_path))
