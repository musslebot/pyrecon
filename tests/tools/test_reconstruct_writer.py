from unittest import TestCase

from lxml import etree

from pyrecon.classes import (
    Contour, Image, Section, Series, Transform, ZContour
)
from pyrecon.tools import reconstruct_reader, reconstruct_writer


def xml_element_to_dict(xml):
    return {k: v for k, v in xml.items()}


class ReconstructWriterTests(TestCase):

    def test_image_to_contour_xml(self):
        xml_in = etree.parse("tests/tools/_image_contour.xml").getroot()
        contour_data = reconstruct_reader.extract_section_contour_attributes(
            xml_in)
        image = Image(**contour_data)
        xml_out = reconstruct_writer.image_to_contour_xml(image)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )


    def test_section_contour_to_xml(self):
        xml_in = etree.parse("tests/tools/_section_contour.xml").getroot()
        contour = Contour(
            **reconstruct_reader.extract_section_contour_attributes(xml_in))
        xml_out = reconstruct_writer.section_contour_to_xml(contour)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_series_contour_to_xml(self):
        xml_in = etree.parse("tests/tools/_series_contour.xml").getroot()
        contour = Contour(
            **reconstruct_reader.extract_series_contour_attributes(xml_in))
        xml_out = reconstruct_writer.series_contour_to_xml(contour)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_image_to_xml(self):
        xml_in = etree.parse("tests/tools/_image.xml").getroot()
        image = Image(
            **reconstruct_reader.extract_image_attributes(xml_in))
        xml_out = reconstruct_writer.image_to_xml(image)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_section_to_xml(self):
        xml_in = etree.parse("tests/tools/_section.xml").getroot()
        section = Section(
            **reconstruct_reader.extract_section_attributes(xml_in))
        xml_out = reconstruct_writer.section_to_xml(section)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_series_to_xml(self):
        xml_in = etree.parse("tests/tools/_series.xml").getroot()
        series = Series(
            **reconstruct_reader.extract_series_attributes(xml_in))
        xml_out = reconstruct_writer.series_to_xml(series)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_transform_to_xml(self):
        xml_in = etree.parse("tests/tools/_transform.xml").getroot()
        transform = Transform(
            **reconstruct_reader.extract_transform_attributes(xml_in))
        xml_out = reconstruct_writer.transform_to_xml(transform)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_zcontour_to_xml(self):
        xml_in = etree.parse("tests/tools/_zcontour.xml").getroot()
        zcontour = ZContour(
            **reconstruct_reader.extract_zcontour_attributes(xml_in))
        xml_out = reconstruct_writer.zcontour_to_xml(zcontour)
        self.assertEqual(
            xml_element_to_dict(xml_in),
            xml_element_to_dict(xml_out),
        )

    def test_entire_section_to_xml(self):
        section_path = "tests/tools/_VRJXH.98"
        xml_in = etree.parse(section_path).getroot()
        section = reconstruct_reader.process_section_file(section_path)
        xml_out = reconstruct_writer.entire_section_to_xml(section)
        # NOTE: need to compare

    def test_entire_series_to_xml(self):
        series_path = "tests/tools/_VRJXH.ser"
        xml_in = etree.parse(series_path).getroot()
        series = reconstruct_reader.process_series_file(series_path)
        xml_out = reconstruct_writer.entire_series_to_xml(series)
        # NOTE: need to compare
