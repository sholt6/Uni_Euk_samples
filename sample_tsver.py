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

def GetVals(xml):
    values = {}
    root = et.fromstring(xml)
    tag_vals = GetAttributes(root)

    values['sample_alias'] = root[0].attrib['alias']
    values['tax_id'] = root[0][2][0].text
    values['scientific_name'] = root[0][2][1].text
    values['common_name'] = ''
    values['sample_title'] = root[0][1].text
    values['sample_description'] = ''
    values['size fraction lower threshold'] = ''
    values['size fraction upper threshold'] = ''
    values['target gene'] = tag_vals['target gene']
    values['target subfragment'] = tag_vals['target subfragment']
    values['pcr primers'] = tag_vals['pcr primers']
    values['isolation_source'] = ''
    values['collected_by'] = ''
    values['collection date'] = tag_vals['collection date']
    values['geographic location (altitude)'] = ''
    values['geographic location (country and/or sea)'] = \
        tag_vals['geographic location (country and/or sea)']
    values['geographic location (latitude)'] = \
        tag_vals['geographic location (latitude)']
    values['geographic location (longitude)'] = \
        tag_vals['geographic location (longitude)']
    values['geographic location (region and locality)'] = ''
    values['geographic location (depth)'] = ''
    values['environment (biome)'] = tag_vals['environment (biome)']
    values['environment (feature)'] = tag_vals['environment (feature)']
    values['environment (material)'] = tag_vals['environment (material)']
    values['sample collection device or method'] = ''
    values['environmental_sample'] = tag_vals['environmental_sample']
    values['salinity'] = ''
    values['further details'] = tag_vals['Further Details']

    return values

def GetAttributes(root):
    tag_vals = {}
    for attribute in root[0][3].findall('SAMPLE_ATTRIBUTE'):
        tag_vals[attribute[0].text] = attribute[1].text

    return tag_vals

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

xmls = GetXMLs('test.sql')

for i in range(0, len(xmls)):
    xmls[i] = FixXMLs(xmls[i])

tsv = open("samples.tsv", "w")
tsv.write('\t'.join(header))

for xml in xmls:
    values = GetVals(xml)
    tsv.write('\n')
    for title in header:
        tsv.write(values[title] + '\t')

tsv.close()
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
