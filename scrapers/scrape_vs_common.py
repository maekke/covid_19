#!/usr/bin/env python

import re
import datetime

from bs4 import BeautifulSoup

import scrape_common as sc


def get_vs_latest_weekly_pdf_url():
    return get_vs_weekly_pdf_urls()[0]


def get_vs_weekly_pdf_urls():
    base_url = 'https://www.vs.ch'
    url = base_url + '/de/web/coronavirus/statistiques'
    content = sc.download(url, silent=True)
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all(href=re.compile(r'Synthese.*Woche'))
    result = []
    for link in links:
        url = base_url + link['href'].replace(' ', '%20')
        result.append(url)
    return result


def get_vs_weekly_general_data(pdf):
    content = sc.pdftotext(pdf, page=1)
    week = sc.find(r'Epidemiologische Situation Woche (\d+)', content)
    end_date = sc.find(r'(\d+\.\d+\.\d{4})', content)
    end_date = sc.date_from_text(end_date)
    start_date = end_date - datetime.timedelta(days=7)
    year = start_date.year
    return week, year


def get_vs_all_daily_pdf_url():
    base_url = 'https://www.vs.ch'
    url = f'{base_url}/web/coronavirus/statistiques'
    content = sc.download(url, silent=True)
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a', string=re.compile(r'20\d{2}.*Sit Epid.*'))
    pdf_urls = []
    for link in links:
        pdf_urls.append(f"{base_url}{link.get('href')}")
    return pdf_urls


def get_vs_daily_pdf_url():
    urls = get_vs_all_daily_pdf_url()
    return urls[0]


def strip_value(value):
    if value:
        return re.sub(r'[^0-9]', '', value)
    return None
