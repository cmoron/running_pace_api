import pytest
from bs4 import BeautifulSoup as bs
from running_pace_api.core.scrapper import (
    wa_convert_time_to_seconds,
    ba_convert_time_to_seconds,
    extract_time_and_convert_to_seconds,
    parse_records_table,
    scrap_records_page,
)

def test_wa_convert_time_to_seconds():
    assert wa_convert_time_to_seconds("1:30:05") == 5405
    assert wa_convert_time_to_seconds("30:05") == 1805
    assert wa_convert_time_to_seconds("30:05.50") == 1805.5
    assert wa_convert_time_to_seconds("5.50") == 5.5

def test_ba_convert_time_to_seconds():
    assert ba_convert_time_to_seconds("1h30'05\"") == 5405
    assert ba_convert_time_to_seconds("30'05\"") == 1805
    assert ba_convert_time_to_seconds("30'05\"50") == 1805.5
    assert ba_convert_time_to_seconds("5\"50") == 5.5

def test_extract_time_and_convert_to_seconds():
    assert extract_time_and_convert_to_seconds("1:30:05") == 5405
    assert extract_time_and_convert_to_seconds("30:05") == 1805
    assert extract_time_and_convert_to_seconds("30:05.5") == 1805.5
    assert extract_time_and_convert_to_seconds("5.5") == 5.5
    assert extract_time_and_convert_to_seconds("1:30:05 WR") == 5405
    assert extract_time_and_convert_to_seconds("30:05 WR") == 1805
    assert extract_time_and_convert_to_seconds("30:05.5 WR") == 1805.5
    assert extract_time_and_convert_to_seconds("5.5 WR") == 5.5

def test_parse_records_table():
    html = """
    <table class="records-table">
        <tr>
            <td><a href="/disciplines/100-metres">100 Metres</a></td>
            <td data-th="PERF">9.58</td>
        </tr>
        <tr>
            <td><a href="/disciplines/200-metres">200 Metres</a></td>
            <td data-th="PERF">19.19</td>
        </tr>
    </table>
    """
    soup = bs(html, "lxml")
    records = parse_records_table(soup)
    assert records[100] == 9.58
    assert records[200] == 19.19
