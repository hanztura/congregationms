import os
import uuid

from django.conf import settings
from django.db.models import Sum

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

from .models import MonthlyFieldService
from publishers.models import Group


def compute_month_year(date):
    default_month_year = '{}-{}'.format(date.year, date.month)
    return default_month_year


def get_months_and_years(date_from, date_to):
    """
    Return months and years from [date from] and [date to]
    """
    date_from = date_from.split('-')
    date_to = date_to.split('-')

    return {
        'fm': date_from[1],
        'tm': date_to[1],
        'fy': date_from[0],
        'ty': date_to[0]
    }


def get_mfs_data(date_from, date_to, pk, is_publisher=True):
    months_years = get_months_and_years(date_from, date_to)
    from_month, from_year = months_years['fm'], months_years['fy']
    to_month, to_year = months_years['tm'], months_years['ty']

    queryset = MonthlyFieldService.objects.filter(
        month_ending__month__gte=from_month,
        month_ending__year__gte=from_year
    ).order_by(
        '-month_ending', 'publisher__last_name', 'publisher__first_name')

    if is_publisher:
        queryset = queryset.filter(publisher=pk)

    queryset = queryset.filter(
        month_ending__month__lte=to_month,
        month_ending__year__lte=to_year
    )

    if not is_publisher:
        # filter for group only
        group = Group.objects.get(pk=pk)
        queryset = [q for q in queryset if q.publisher.group == group]

    # get totals
    if is_publisher:
        totals = queryset.aggregate(
            Sum('placements'),
            Sum('video_showing'),
            Sum('hours'),
            Sum('return_visits'),
            Sum('bible_study'))
    else:
        totals = {
            'placements__sum': 0,
            'video_showing__sum': 0,
            'hours__sum': 0,
            'return_visits__sum': 0,
            'bible_study__sum': 0,
        }
        for q in queryset:
            totals['placements__sum'] += q.placements
            totals['video_showing__sum'] += q.video_showing
            totals['hours__sum'] += q.hours
            totals['return_visits__sum'] += q.return_visits
            totals['bible_study__sum'] += q.bible_study

    print(totals)
    data = {
        'queryset': queryset,
        'totals': totals,
        'from': '{}-{}'.format(from_month, from_year),
        'to': '{}-{}'.format(to_month, to_year),
    }

    if not is_publisher:
        data['group'] = group

    return data


def generate_mfs(data, report_type='group'):
    title = 'Monthly Field Service Report'
    doc = Document()

    doc.add_heading(
        title, 0).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if report_type == 'group':
        p = doc.add_paragraph(data['group'])
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = 'Congregation: {}'.format(data['congregation'])
    p = doc.add_paragraph(p)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

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


    # totals
    totals = data['totals']
    row_cells = table.add_row().cells
    row_cells[0].text = 'TOTALS'
    row_cells[2].text = str(totals['placements__sum'])
    row_cells[3].text = str(totals['video_showing__sum'])
    row_cells[4].text = str(totals['hours__sum'])
    row_cells[5].text = str(totals['return_visits__sum'])
    row_cells[6].text = str(totals['bible_study__sum'])

    if report_type=='group':
        other_rows = ['PUB.', 'AUXI.', 'RP']
        for row in other_rows:
            row_cells = table.add_row().cells
            row_cells[0].text = row

    doc.add_page_break()

    filename = '{}.docx'.format(str(uuid.uuid1()))
    fullpath = os.path.join(settings.ROOT_DIR, 'media')
    fullpath = os.path.join(fullpath, 'temp--mfs_export')
    if not os.path.exists(fullpath):
        os.mkdir(fullpath)
    fullpath = os.path.join(fullpath, filename)
    doc.save(fullpath)

    return {
        'doc': doc,
        'filename': filename,
        'fullpath': fullpath,
    }


def mfs_stats(month, year):
    q = MonthlyFieldService.objects.filter(month_ending__month=month)
    q = q.filter(month_ending__year=year)
    q = q.aggregate(Sum('hours'), Sum('return_visits'), Sum('bible_study'))

    hours = q['hours__sum']
    return_visits = q['return_visits__sum']
    bible_studies = q['bible_study__sum']
    stats = {
        'hours': hours,
        'return_visits': return_visits,
        'bible_studies': bible_studies
    }
    return stats
