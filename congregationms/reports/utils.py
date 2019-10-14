from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches


def compute_month_year(date):
    default_month_year = '{}-{}'.format(date.year, date.month)
    return default_month_year

def generate_mfs(data):
    title = 'Monthly Field Service Report'
    doc = Document()

    doc.add_heading(title, 0).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(data['group']).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(data['congregation']).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph('For the month {}'.format(data['month']))
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    reports = data['queryset']

    headers = [
        ('Month', 'Month'),
        ('Name', 'Name'),
        ('P', 'Placements'),
        ('VS', 'Video Showings'),
        ('H', 'Hours'),
        ('RV', 'Return Visits'),
        ('BS', 'Bible Studies'),
        ('Comment', 'Comments')
    ]

    table = doc.add_table(rows=1, cols=len(headers))

    hdr = table.rows[0].cells
    for i in range(len(headers)):
        label = headers[i][0]
        hdr[i].text = label

    for report in reports:
        row_cells = table.add_row().cells
        row_cells[0].text = report.month_ending.strftime('%b-%Y')
        row_cells[1].text = str(report.publisher.name)
        row_cells[2].text = str(report.placements)
        row_cells[3].text = str(report.video_showing)
        row_cells[4].text = str(report.hours)
        row_cells[5].text = str(report.return_visits)
        row_cells[6].text = str(report.bible_study)
        row_cells[7].text = str(report.comments)

    doc.add_page_break()

    return doc