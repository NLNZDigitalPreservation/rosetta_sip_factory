Rosetta SIP Factory
===================
Generate Rosetta-compliant Submission Information Packages

Background
----------
The Rosetta digital preservation application provides multiple different avenues for depositing digital content, including a web interface deposit, csv and METS XML. The METS XML process lends itself well to processing large numbers of records, and Ex Libris (the developers of Rosetta) provide a Java-based SDK for constructing deposit mechanisms (available at https://github.com/ExLibrisGroup/Rosetta.dps-sdk-projects).  
The Rosetta SIP Factory provides functionality for creating METS XML deposits for the Rosetta application, but it is built with Python rather than Java. While it does not offer the full range of options that are available with the Java-based deposit SDK, it aims to provide a quick and easy mechanism for common use cases. It also aims to appeal to people who prefer working with Python rather than Java.


Usage
-----
To use as part of a different program:
.. code-block: python
    python
    from rosetta_sip_factory import sip_builder

    sip_builder.build_sip(
        ie_dmd_dict=None,
        pres_master_dir=None,
        modified_master_dir=None,
        access_derivative_dir=None,
        cms=None,
        generalIECharacteristics=None,
        objectIdentifier=None,
        accessRightsPolicy=None,
        eventList=None,
        input_dir=None,
        digital_original=False,
        sip_title=None,
        output_folder=None
    )

The above arguments (if required) should be submitted in the following format:

**ie_dmd_dict** = dictionary, such as follows::

    {"dc:title": "Title of record", "dcterms:isPartOf": "19926",
     "dc:identifier xsi:type=InstitionalIdentifier": "A1234",
     "dcterms:provenance": "Transferred from Agency ABCD"}

(See below in the "dc, dcterms and xsi mapping in ie_dmd" description for more
details about building an ie_dmd section)  
**pres_master_dir** = string  
**modified_master_dir** = string  
**access_derivative_dir** = string  
**cms** = dictionary inside list, such as follows::

    [{'system': <system name>, 'recordId': <CMS ID> },]
 
**generalIECharacteristics** = dictionary inside list, such as follows:  

    [{'IEEntityType': <entity type>, 'submissionReason': <submission reason>},]
  
**objectIdentifier** = dictionary inside list, such as follows::  

    [{'policyId': <policy ID>, 'policyDescription': <policy description>},]

**eventList** = dictionary inside list, such as follows::  

    [{'eventDateTime': <event datetime>, 
      'eventType': <event type>,
      'eventIdentifierType': <event identifier type>, 
      'eventIdentifierValue': <event identifier value>,
      'eventOutcome1': <event outcome 1>,
      'eventOutcomeDetail1': <event outcome detail 1>,
      'eventDescription': <event description>,
      'linkingAgentIdentifierType1': <linking agent identifier type 1>,
      'linkingAgentIdentifierValue1': <linking agent identifier value 1>
      },]

(**Note**: Not all key/value pairs are required for events.)  
**input_dir** = string  
**digital_original** = Boolean (default is False)  
**sip_title** = String
**output_folder** = string  

Typical SIP folder structure
----------------------------
The build_sip function creates a SIP struture that is compliant with what the Rosetta application expects to see. Below is an example of how a single-representation SIP would look:
(Note: in all of these examples, the sip_title parameter has been supplied, which results in the dc.xml file being generated)::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |  
             |_streams
             |   |
             |   |_file1.txt
             |   |
             |   |_file2.txt
             |
             |_mets.xml
             |
             |_dc.xml

Below is an example of a multi-representation SIP::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |
             |_streams
             |   |
             |   |_pres_master
             |   |    |
             |   |    |_file1.tif
             |   |    |
             |   |    |_file2.tif
             |   |
             |   |_modified_master
             |   |    |
             |   |    |_file1.jpg
             |   |    |
             |   |    |_file2.jpg
             |   |
             |   |_access_derivative
             |        |
             |        |_file1.pdf
             |    
             |_mets.xml
             |
             |_dc.xml


You can have as many "sip_folder" folders in the "Base_location_on_server" as you like.  
Depending on your mode of deposit, you may want to add a settings folder and settings.properties file. If that is the case, you should add them so the SIP structure looks like this::

    Base_location_on_server
    |
    |_sip_folder
        |
        |_content
             |
             |_settings
             |   |
             |   |_settings.properties
             |
             |_streams
             |   |
             |   |_file1.txt
             |   |
             |   |_file2.txt
             |
             |_mets.xml
             |
             |_dc.xml

The "settings.properties" file should look like this::

    material_flow_id=12345
    deposit_set_id=1
    user_name=username
    user_password=password
    user_institution=INS00
    user_producer_id=99999

with your appropriate values instead of the placeholder values.

dc, dcterms and xsi mapping in ie_dmd
-------------------------------------
The ie_dmd component does some behind-the scenes parsing of namespace prefixes 
and attributes. Specifically, the following three namespaces are supported:   
dc - is mapped to "http://purl.org/dc/elements/1.1/"   
dcterms - is mapped to "http://purl.org/dc/terms/"   
xsi - is mapped to "http://www.w3.org/2001/XMLSchema-instance", and is
      intended only for use with attributes, not the element names.

Installing Rosetta SIP Factory
------------------------------
If you have downloaded the package, unzip it and execute the following command::  
    python setup.py install  
This package will also install the most recent lxml library via pip if it is
not already installed.