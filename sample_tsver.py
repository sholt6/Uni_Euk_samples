#!/usr/local/bin/python3
import re
import xml.etree.ElementTree as et
import csv

def GetXMLs(filename):
    with open(filename, 'r') as input:
        sql = input.read()

    xml_start_pattern = re.compile(r'xml version')
    starts = [(m.start(0) - 2) for m in re.finditer(xml_start_pattern, sql)]
    xml_end_pattern = re.compile(r'/SAMPLE_SET')
    ends = [(m.end(0) + 1) for m in re.finditer(xml_end_pattern, sql)]

    sample_xmls = []
    for i in range(0, len(starts)):
        sample_xmls.append(sql[starts[i]:ends[i]])

    return sample_xmls

def FixXMLs(xml):
    xml = xml.replace("''1.0'' encoding = ''UTF-8''", "'1.0' encoding = 'UTF-8'")

    return xml

xmls = GetXMLs('test.sql')
for i in range(0, len(xmls)):
    xmls[i] = FixXMLs(xmls[i])
root = et.fromstring(xmls[0])

sample_data = open('samples.tsv', 'w')
csvwriter = csv.writer(sample_data)



sample_date.close()
