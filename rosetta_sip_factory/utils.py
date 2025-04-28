import os
import shutil

from lxml import etree as ET

from rosetta_sip_factory.static import DC_NS, DC_NSMAP


def clean_title(title):
    if title:
        replacements = {"-": ["–"]}
        for replacement, targets in replacements.items():
            for target in targets:
                title = title.replace(target, replacement)

    return title


def build_dc_sip(output_dir, sip_title, encoding="unicode"):
    dc_xml = ET.Element("{%s}record" % DC_NS, nsmap=DC_NSMAP)
    title = ET.SubElement(dc_xml, "{%s}title" % DC_NS, nsmap=DC_NSMAP)
    title.text = sip_title
    if encoding in ["unicode"]:
        with open(os.path.join(output_dir, "content", "dc.xml"), "w") as dc_file:
            dc_file.write(ET.tostring(dc_xml, encoding=encoding))
    else:
        with open(os.path.join(output_dir, "content", "dc.xml"), "wb") as dc_file:
            dc_file.write(ET.tostring(dc_xml, xml_declaration=True, encoding=encoding))


def copy_tree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            # 2017-03-21: change to check if file exists first.
            # WARNING: THIS IS NOT IMMUNE TO RACE CONDITIONS!
            if os.path.isfile(d):
                raise Exception("{} already exists.".format(d))
            else:
                shutil.copy2(s, d)
