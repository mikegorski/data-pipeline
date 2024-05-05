from fpdf import FPDF

from data_pipeline.settings import AUTHORS, TITLE


class PDF(FPDF):
    text_font_size: int = 12
    title_font_size: int = 16
    subtitle_font_size: int = 14
    blue = (1, 45, 72)
    orange = (236, 104, 57)

    def header(self):
        self.set_left_margin(0)
        self.set_right_margin(0)
        self.set_font("arial", "", 15)
        self.set_y(0)
        self.set_draw_color(*self.blue)
        self.set_fill_color(*self.blue)
        self.set_text_color(*self.orange)
        self.set_line_width(1)

        doc_width = 210
        self.cell(
            w=doc_width,
            h=20,
            text="",
            border=0,
            align="C",
            fill=True,
        )
        self.set_left_margin(10)
        self.set_right_margin(10)

        title_width = self.get_string_width(TITLE) + 6
        self.set_y(5)
        self.cell(
            w=title_width,
            h=10,
            text=self.title,
            border=0,
            align="L",
            fill=True,
        )
        authors = ", ".join(AUTHORS)
        authors_width = self.get_string_width(authors) + 6
        self.set_y(5)  # set y position first as setting it sets x back to left margin
        self.set_x(-50)
        self.cell(
            w=authors_width,
            h=10,
            text=self.author,
            border=0,
            align="L",
            fill=True,
        )
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("arial", "B", 12)
        self.set_text_color(*self.orange)
        self.cell(0, 10, str(self.page_no()), 0, 0, "R")
        self.set_margin(40)
        self.set_left_margin(10)
        self.set_right_margin(10)
