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

def GetVals(header, root):
    val = root.findall(header[0])[0].text
    print(val)

xmls = GetXMLs('test.sql')
for i in range(0, len(xmls)):
    xmls[i] = FixXMLs(xmls[i])
root = et.fromstring(xmls[0])
print(root.findall('SAMPLE')[1].text)
quit()
sample_data = open('samples.tsv', 'w')
csvwriter = csv.writer(sample_data)
header = ['sample_alias', 'tax_id', 'scientific_name', 'common_name',
          'sample_title', 'sample_description', 'size fraction lower threshold',
          'size fraction upper threshold', 'target gene', 'target subfragment',
          'pcr primers', 'isolation_source', 'collected_by', 'collection date',
          'geographic location (altitude)',
          'geographic location (country and/or sea)',
          'geographic location (latitude)', 'geographic location (longitude)',
          'geographic location (region and locality)',
          'geographic location (depth)', 'environment (biome)',
          'environment (feature)', 'environment (material)',
          'sample collection device or method', 'environmental_sample',
          'salinity', 'further details']
#header = "sample_alias\ttax_id\tscientific_name\tcommon_name\tsample_title\t"\
#         "sample_description\tsize fraction lower threshold\t"\
#         "size fraction upper threshold\ttarget gene\ttarget subfragment\t"\
#         "pcr primers\tisolation_source\tcollected_by\tcollection date\t"\
#         "geographic location (altitude)\t"\
#         "geographic location (country and/or sea)\t"\
#         "geographic location (latitude)\tgeographic location (longitude)\t"\
#         "geographic location (region and locality)\t"\
#         "geographic location (depth)\tenvironment (biome)\t"\
#         "environment (feature)\tenvironment (material)\t"\
#         "sample collection device or method\tenvironmental_sample\t"\
#         "salinity\tfurther details" # May need newline"\
print(header)

GetVals(header, root)

sample_data.close()
