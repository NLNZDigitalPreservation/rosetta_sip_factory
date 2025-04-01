import glob
import json
import os
from os.path import join

import pytest
from lxml import etree as ET

from rosetta_sip_factory import sip_builder as sb
from tests import INPUTS_PATH
from tests.utils import read_json


class TestBatchTwo:
    ie_dc_dict = {"dc:title": "test title"}
    input_dir = join(INPUTS_PATH, "test_batch_2")
    general_ie_characteristics = [
        {"submissionReason": "bornDigitalContent", "IEEntityType": "periodicIE"}
    ]
    titles = ["Test_IE_0", "Another_test", "test with spaces", "camelCaseTest"]
    pres_master_json = read_json(join(INPUTS_PATH, "pres_masters", "batch_2.json"))

    def test_sip_single_rep_multi_folder_hierarchy(self, outputs_path):
        """Build SIP with single representation in a complex folder structure"""
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=join(self.input_dir, "root_folder"),
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
        )

        streams_dir = join(outputs_path, "content", "streams")
        input_contents = os.listdir(self.input_dir)
        streams_contents = os.listdir(streams_dir)
        for input_content in input_contents:
            assert input_content in streams_contents

    def test_multiple_JSON_IEs_in_one_SIP_folder(self, outputs_path):
        glob_path = join(self.input_dir, "**", "*.jpg")
        jpg_paths = glob.glob(glob_path, recursive=True)

        for i, path in enumerate(jpg_paths):
            self.pres_master_json[i]["physical_path"] = path

        for title in self.titles:
            ie_dc_dict = {"dc:title": title}
            sb.build_sip_from_json(
                ie_dmd_dict=ie_dc_dict,
                pres_master_json=json.dumps(self.pres_master_json),
                input_dir=self.input_dir,
                generalIECharacteristics=self.general_ie_characteristics,
                output_dir=outputs_path,
                mets_filename=title,
            )

        expected_xmls = [f"{t}.xml" for t in self.titles] + ["streams"]
        for file in os.listdir(join(outputs_path, "content")):
            assert file in expected_xmls

    @pytest.mark.parametrize(
        "structmap_type, expected_structmaps_count, expected_structmap_types",
        [
            pytest.param("DEFAULT", 1, ["LOGICAL"]),
            pytest.param("PHYSICAL", 1, ["PHYSICAL"]),
            pytest.param("BOTH", 2, ["LOGICAL", "PHYSICAL"]),
        ],
    )
    def test_multi_folder(
        self,
        outputs_path,
        structmap_type,
        expected_structmaps_count,
        expected_structmap_types,
    ):
        sb.build_sip(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_dir=join(self.input_dir, "root_folder"),
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
            structmap_type=structmap_type,
        )
        input_content = os.listdir(self.input_dir)
        streams_content = os.listdir(join(outputs_path, "content", "streams"))
        for thing in input_content:
            assert thing in streams_content

        mets = ET.parse(join(outputs_path, "content", "mets.xml"))
        structmaps = mets.findall("{http://www.loc.gov/METS/}structMap")
        assert len(structmaps) == expected_structmaps_count

        structmap_types = sorted([s.attrib["TYPE"].upper() for s in structmaps])
        assert structmap_types == expected_structmap_types

    @pytest.mark.parametrize(
        "structmap_type, expected_structmaps_count, expected_structmap_types",
        [
            pytest.param("DEFAULT", 1, ["LOGICAL"]),
            pytest.param("PHYSICAL", 1, ["PHYSICAL"]),
            pytest.param("BOTH", 2, ["LOGICAL", "PHYSICAL"]),
        ],
    )
    def test_multi_hierarchical_json(
        self,
        outputs_path,
        structmap_type,
        expected_structmaps_count,
        expected_structmap_types,
    ):
        """multi-hierarchical json SIPs get a physical and logical SM when 'both' is flagged"""

        glob_path = join(self.input_dir, "**", "*.jpg")
        jpg_paths = glob.glob(glob_path, recursive=True)

        for i, path in enumerate(jpg_paths):
            self.pres_master_json[i]["physical_path"] = path

        sb.build_sip_from_json(
            ie_dmd_dict=self.ie_dc_dict,
            pres_master_json=json.dumps(self.pres_master_json),
            input_dir=self.input_dir,
            generalIECharacteristics=self.general_ie_characteristics,
            output_dir=outputs_path,
            structmap_type=structmap_type,
        )
        mets = ET.parse(join(outputs_path, "content", "mets.xml"))
        structmaps = mets.findall("{http://www.loc.gov/METS/}structMap")
        assert len(structmaps) == expected_structmaps_count

        structmap_types = sorted([s.attrib["TYPE"].upper() for s in structmaps])
        assert structmap_types == expected_structmap_types
