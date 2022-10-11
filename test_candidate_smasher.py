# !/usr/bin/env python3
# -*- coding: utf-8 -*-
""" tests for CandidateSmasher
    ruby code at https://github.com/Display-Lab/candidate-smasher
    Date: 20220726
    By:
        Scientific Programming and Innovation (SPI)
        Academic IT
        H.I.T.S., Michigan Medicine
        University of Michigan
"""
# pylint: disable=too-many-lines
import json
import pytest
from rdflib import Graph
from candidate_smasher import CandidateSmasher


def test_class_instan():
    """instantiate
    """
    candidate = CandidateSmasher()
    assert candidate


def test_class_contants():
    """class constants
    """
    assert CandidateSmasher.ID_PREFIX
    assert CandidateSmasher.ABOUT_MEASURE_IRI
    assert CandidateSmasher.ABOUT_TEMPLATE_IRI
    assert CandidateSmasher.ANCESTOR_PERFORMER_IRI
    assert CandidateSmasher.ANCESTOR_TEMPLATE_IRI
    assert CandidateSmasher.HAS_CANDIDATE_IRI
    assert CandidateSmasher.HAS_PERFORMER_IRI
    assert CandidateSmasher.REGARDING_COMPARATOR
    assert CandidateSmasher.REGARDING_MEASURE
    assert CandidateSmasher.SPEK_IRI
    assert CandidateSmasher.USES_ISR_IRI
    assert CandidateSmasher.CANDIDATE_IRI
    assert CandidateSmasher.TEMPLATE_CLASS_IRI
    assert CandidateSmasher.HAS_DISPOSITION_IRI
    assert CandidateSmasher.IS_ABOUT_IRI


def test_accessor_spek_hsh_get():
    """ accessor spek_hsh
    """
    candidate = CandidateSmasher()
    spek_hsh = candidate.spek_hsh
    assert isinstance(spek_hsh, dict)
    assert spek_hsh == {}


def test_accessor_spek_hsh_set():
    """ accessor spek_hsh
    """
    candidate = CandidateSmasher()
    test_dict = {"test key": "test value"}
    candidate.spek_hsh = test_dict
    assert candidate.spek_hsh == test_dict


def test_accessor_template_lib_get():
    """ accessor template_lib
    """
    candidate = CandidateSmasher()
    template_lib = candidate.template_lib
    assert isinstance(template_lib, list)
    assert template_lib == []


def test_accessor_template_lib_set():
    """ accessor template_lib
    """
    candidate = CandidateSmasher()
    test_list = ["test1", "test2"]
    candidate.template_lib = test_list
    assert candidate.template_lib == test_list


def test_spek_hsh_init_testdata():
    """ init spek_hsh with test dict
    """
    # test with some json dict string
    test_json_str = '{"test key": "test value"}'
    candidate = CandidateSmasher(input_string=test_json_str)
    spek_hsh = candidate.spek_hsh
    assert spek_hsh == json.loads(test_json_str)


def test_spek_hsh_init_empty():
    """ init spek_hsh with empty dict
    """
    # test with empty json dict
    candidate = CandidateSmasher(input_string='{}')
    spek_hsh = candidate.spek_hsh
    assert spek_hsh == {}


def test_template_lib_init_bad_data():
    """ bad json, expect exception
    """
    test_dict = {}
    candidate = CandidateSmasher(input_string='')
    assert candidate.spek_hsh == test_dict


def test_template_lib_blank_filename_no_such_file():
    """ init template_src
    """
    candidate = CandidateSmasher(templates_src="")
    template_lib = candidate.template_lib
    assert isinstance(template_lib, list)
    assert template_lib == []


def test_template_lib_example_json_file():
    """ init template_src
    """
    candidate = CandidateSmasher(templates_src="example.json")
    template_lib = candidate.template_lib
    assert isinstance(template_lib, list)
    assert template_lib == [{"@id": "http://umich.edu", "name": "umich"}]


def test_valid_blank_type():
    """ valid bool
    """
    spek_hsh_dict = {"@type": ""}
    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str)
    valid = candidate.valid()
    assert valid is False


def test_valid_ok_with_about_template_iri():
    """ valid bool
    """
    spek_hsh_dict = {
        "@type": "http://example.com/slowmo#spek",
        "http://example.com/slowmo#IsAboutPerformer": "",
        "http://example.com/slowmo#IsAboutTemplate": ""
    }
    # these are driving this test
    assert spek_hsh_dict['@type'] == "http://example.com/slowmo#spek"
    assert "http://example.com/slowmo#IsAboutPerformer" in spek_hsh_dict
    assert "http://example.com/slowmo#IsAboutTemplate" in spek_hsh_dict

    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str)
    valid = candidate.valid()
    assert valid is True


def test_valid_ok_with_template_lib():
    """ valid bool
    """
    spek_hsh_dict = {
        "@type": "http://example.com/slowmo#spek",
        "http://example.com/slowmo#IsAboutPerformer": ""
    }

    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str, templates_src="example.json")

    # these are driving this test
    assert spek_hsh_dict['@type'] == "http://example.com/slowmo#spek"
    assert "http://example.com/slowmo#IsAboutPerformer" in spek_hsh_dict
    assert "http://example.com/slowmo#IsAboutTemplate" not in spek_hsh_dict
    assert len(candidate.template_lib) != 0
    assert candidate.template_lib != []

    valid = candidate.valid()
    assert valid is True


def test_list_missing_none_missing():
    """ list_missing()
    """
    spek_hsh_dict = {
        "@type": "http://example.com/slowmo#spek",
        "http://example.com/slowmo#IsAboutPerformer": "",
        "http://example.com/slowmo#IsAboutTemplate": ""
    }

    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str)
    missing = candidate.list_missing()
    assert missing == []


def test_list_missing_about_temp():
    """ list_missing()
    """
    spek_hsh_dict = {
        "@type": "http://example.com/slowmo#spek",
        "http://example.com/slowmo#IsAboutPerformer": ""
    }

    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str)
    missing = candidate.list_missing()
    assert missing == ["http://example.com/slowmo#IsAboutTemplate"]


def test_list_missing_2():
    """ list_missing()
    """
    spek_hsh_dict = {
        "@type": "http://example.com/slowmo#spek",
    }

    spek_hsh_str = json.dumps(spek_hsh_dict)
    candidate = CandidateSmasher(input_string=spek_hsh_str)
    missing = candidate.list_missing()
    assert len(missing) == 2
    assert "http://example.com/slowmo#IsAboutTemplate" in missing
    assert "http://example.com/slowmo#IsAboutPerformer" in missing


def test_load_ext_templ_empty():
    """ load_ext_templates()
    """
    candidate = CandidateSmasher()
    templates = candidate.load_ext_templates("ext_templates_empty.json")
    assert templates == []


def test_load_ext_templ_example():
    """ load_ext_templates()
    """
    candidate = CandidateSmasher()
    templates = candidate.load_ext_templates("example.json")
    assert len(templates) != 0
    assert "@id" in templates[0]


def test_load_ext_templ_rdf_empty():
    """ load_ext_templates_rdf()
    """
    candidate = CandidateSmasher()
    templates = candidate.load_ext_templates_rdf("")
    assert isinstance(templates, Graph)


def test_load_ext_templ_rdf_doap_nt():
    """ try reading an N3 format .nt file
    """
    candidate = CandidateSmasher()
    graph = candidate.load_ext_templates_rdf("doap.nt")
    assert isinstance(graph, Graph)
    assert len(graph) > 0


def test_merge_ext_empty():
    """ self.merge_external_templates()
    """
    spec_templates = []
    ext_templates = []
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)


def test_merge_ext_try_map():
    """ self.merge_external_templates()

        spec has id's [1,2], ext has id's [1], expected has id's [1-merge,2]
    """
    spec_templates = [
        {'@id': '1', '@type': 'test type', 'testitem': 'test value'},
        {'@id': '2', 'test key2': 'test value2'},
    ]
    ext_templates = [
        {'@id': '1', 'car2': 'ok2', 'car': 'ok', '@type': '5'},
    ]
    expected = [
        {'@id': '1', 'car2': 'ok2', 'car': 'ok', '@type': 'test type', 'testitem': 'test value'},
        {'@id': '2', 'test key2': 'test value2'},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_each():
    """ self.merge_external_templates()

        spec has id's [1,2], ext has id's [2,3], expected has id's [1,2-merge]

    """
    spec_templates = [
        {'@id': '1', 'car': 'ok', '@type': '5'},
        {'@id': '2', 'myitem': 'test item', "dup": "testspec"}
    ]
    ext_templates = [
        {'@id': '2', 'car2': 'ok2', "dup": "testtext"},
        {"@id": '3', 'car2': 'ok3'}
    ]
    expected = [
        {'@id': '1', 'car': 'ok', '@type': '5'},
        {"@id": "2", "car2": "ok2", "dup": "testspec", "myitem": "test item"}
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_ext_1_extra_id():
    """ lists with ext having id=3 that is not in spec
    """
    spec_templates = [
        {'@id': '1', 'car': [1, 2, 3], '@type': '5'},
        {'@id': '2', "dup": "testspec"}
    ]
    ext_templates = [
        {'@id': '1', 'car': [4, 5], "dup": "testtext"},
        {"@id": '3', 'car2': 'ok3'}
    ]
    expected = [
        {'@id': '1', 'car': [1, 2, 3, 4, 5], '@type': '5', "dup": "testtext"},
        {'@id': '2', "dup": "testspec"}
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_ext_2_extra_ids():
    """ lists with ext having id=3 and id=4 that is not in spec
    """
    spec_templates = [
        {'@id': '1', 'car': [1, 2, 3], '@type': '5'},
        {'@id': '2', "dup": "testspec"}
    ]
    ext_templates = [
        {'@id': '1', 'car': [4, 5], "dup": "testtext"},
        {"@id": '3', 'car2': 'ok3'},
        {"@id": '4', 'car4list': [8, 5, 6]}
    ]
    expected = [
        {'@id': '1', 'car': [1, 2, 3, 4, 5], '@type': '5', "dup": "testtext"},
        {'@id': '2', "dup": "testspec"},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_spec_2_extra_ids():
    """ spec has str, ext has list []
    """
    spec_templates = [
        {'@id': '1', 'car': [1, 2, 3], '@type': '5'},
        {'@id': '2', "dup": "testspec"},
        {"@id": '5', 'c5list': [8, 5, 6]},
        {"@id": '6', 'c6list': [9, 9, 6]}  # this one is not in ext
    ]
    ext_templates = [
        {'@id': '1', 'car': [4, 5], "dup": "testtext"},
        {"@id": '3', 'car2': 'ok3'},  # this one is not in spec, IT GETS DROPPED
        {"@id": '5', 'c5list': [7, 5, 8, 6], 'extra_item': "extra"},  # this one need to merge the list, plus this one has an extra item
    ]
    expected = [
        {'@id': '1', 'car': [1, 2, 3, 4, 5], '@type': '5', "dup": "testtext"},
        {'@id': '2', "dup": "testspec"},
        {"@id": '5', 'c5list': [8, 5, 6, 7], "extra_item": "extra"},
        {"@id": '6', 'c6list': [9, 9, 6]}
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_spec_2_extra_ids_extra():
    """ lists with spec having extra id=6 and ext extra id=3
    """
    spec_templates = [
        {'@id': '1', 'car': [1, 2, 3], '@type': '5'},
        {'@id': '2', "dup": "testspec"},
        {"@id": '5', 'c5list': [8, 5, 6], "extra_one": "extra1"},  # this one need to merge the list, plus this one has an extra item
        {"@id": '6', 'c6list': [9, 9, 6]}  # this one is not in ext
    ]
    ext_templates = [
        {'@id': '1', 'car': [4, 5], "dup": "testtext"},
        {"@id": '3', 'car2': 'ok3'},  # this one is not in spec
        {"@id": '5', 'c5list': [7, 5, 8, 6]},
    ]
    expected = [
        {'@id': '1', 'car': [1, 2, 3, 4, 5], "dup": "testtext", '@type': '5'},
        {'@id': '2', "dup": "testspec"},
        {"@id": '5', 'c5list': [8, 5, 6, 7], "extra_one": "extra1"},
        {"@id": '6', 'c6list': [9, 9, 6]}
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_spec_mix():
    """ lists with spec having extra id=6 and ext extra id=3
    """
    spec_templates = [
        {'@id': '1', 'car': 'spec', '@type': '5'},
    ]
    ext_templates = [
        {'@id': '1', 'car': [4, 5], "dup": "testtext"},
    ]
    expected = [
        {'@id': '1', 'car': ['spec', 4, 5], "dup": "testtext", '@type': '5'},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_spec_mix_ext():
    """ lists with spec having extra id=6 and ext extra id=3
    """
    spec_templates = [
        {'@id': '1', 'car': [4, 5], '@type': '5'},
    ]
    ext_templates = [
        {'@id': '1', 'car': 'ext', "dup": "testtext"},
    ]
    expected = [
        {'@id': '1', 'car': [4, 5, 'ext'], "dup": "testtext", '@type': '5'},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_ext_two_ids_lists_dup():
    """ lists with spec having extra id=6 and ext extra id=3
    """
    spec_templates = [
        {'@id': '1', 'car': [4, 6], '@type': '5'},
    ]
    ext_templates = [
        {'@id': '1', 'car': [1, 2, 4, 5, 6, 7], "dup": "testtext"},
    ]
    expected = [
        {'@id': '1', 'car': [4, 6, 1, 2, 5, 7], "dup": "testtext", '@type': '5'},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_merge_dups_in_spec():
    """ lists with spec having extra id=4,6 and ext having dup id=4
    """
    spec_templates = [
        {'@id': '1', 'car': [4, 6, 4, 6], '@type': '5'},
    ]
    ext_templates = [
        {'@id': '1', 'car': [1, 2, 4], "dup": "testtext"},
    ]
    expected = [
        {'@id': '1', 'car': [4, 6, 1, 2], "dup": "testtext", '@type': '5'},
    ]
    merged = CandidateSmasher.merge_external_templates(spec_templates, ext_templates)
    assert isinstance(merged, list)
    print("-merged------", merged)
    print("-expected----", expected)
    for mer in merged:
        for exp in expected:
            if mer['@id'] == exp['@id']:
                assert mer == exp
    assert len(merged) == len(expected)


def test_templates_rdf_to_json_small_sample():
    """ small example data
    """
    input_filename = "doap_small_sample.nt"
    expected = [
        {
            "@id": "_:g6720",
            "http://xmlns.com/foaf/0.1/name": {"@value": "Hellekin O. Wolf"},
            "http://xmlns.com/foaf/0.1/mbox_sha1sum": {"@value": "c69f3255ff0639543cc5edfd8116eac8df16fab8"},
            "@type": "http://xmlns.com/foaf/0.1/Person"
        },
        {
            "@id": "_:g6680",
            "http://xmlns.com/foaf/0.1/name": {"@value": "Fumihiro Kato"},
            "http://xmlns.com/foaf/0.1/mbox_sha1sum": {"@value": "d31fdd6af7a279a89bf09fdc9f7c44d9d08bb930"},
            "@type": "http://xmlns.com/foaf/0.1/Person"
        },
        {
            "@id": "https://bhuga.net/#ben",
            "http://xmlns.com/foaf/0.1/homepage": {"@id": "https://bhuga.net/"},
            "http://xmlns.com/foaf/0.1/name": {"@value": "Ben Lavender"},
            "http://xmlns.com/foaf/0.1/mbox": {"@id": "mailto:blavender@gmail.com"},
            "http://xmlns.com/foaf/0.1/mbox_sha1sum": {"@value": "dbf45f4ffbd27b67aa84f02a6a31c144727d10af"},
            "@type": "http://xmlns.com/foaf/0.1/Person"
        },
        {
            "@id": "_:g6660",
            "http://xmlns.com/foaf/0.1/name": {"@value": "Joey Geiger"},
            "http://xmlns.com/foaf/0.1/mbox_sha1sum": {"@value": "f412d743150d7b27b8468d56e69ca147917ea6fc"},
            "@type": "http://xmlns.com/foaf/0.1/Person"
        },
        {
            "@id": "_:g6740",
            "http://xmlns.com/foaf/0.1/name": {"@value": "John Fieber"},
            "http://xmlns.com/foaf/0.1/mbox_sha1sum": {"@value": "f7653fc1ac0e82ebb32f092389bd5fc728eaae12"},
            "@type": "http://xmlns.com/foaf/0.1/Person"
        }
    ]

    def find_correct_element_in_expected(elem):
        """ linear search through expected items to find the one that matches the arg
        """
        for exp in expected:
            elem_key = "http://xmlns.com/foaf/0.1/mbox_sha1sum"
            if exp[elem_key] == elem[elem_key]:
                return exp
        return None

    candidate = CandidateSmasher()
    graph = Graph()
    graph.parse(input_filename, format='n3')
    result = candidate.templates_rdf_to_json(graph)
    print(json.dumps(result, indent=4))
    # assert result == expected  # cannot just compare, because the json-ld creates all new ID's
    print("-result--------", type(result))
    for elem in result:
        print("--item---------", type(elem))

        correct_elem = find_correct_element_in_expected(elem)

        for result_k, result_v in elem.items():
            if result_k != '@id':
                print("--v and -------", result_v)
                print("--v elem-------", elem)
                print("--v and exp----", correct_elem[result_k])
                assert result_v == correct_elem[result_k]


def test_split_by_disp_empty():
    """ split_by_disposition_attr
    """
    candidate = CandidateSmasher()
    performer = {}
    attr_ui = {}
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == [{}]


def test_split_by_disp_iri_none():
    """ split_by_disposition_attr
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: None}
    attr_ui = ""
    expected = [performer]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_disp_iri_one_item_together():
    """ split_by_disposition_attr
        keep both elems in same row
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}]}
    attr_ui = "uri"
    expected = [{CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}]}]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_disp_iri_one_item_split():
    """ split_by_disposition_attr
        split two elems into to rows
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a2", "b": "b2"}]}
    attr_ui = "uri"
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}]},
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a2", "b": "b2"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_disp_iri_combine1():
    """ split_by_disposition_attr
        split three elems, two into one row and one into another row
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}, {"uri": "a5", "b": "b1"}]}
    attr_ui = "b"
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a5", "b": "b1"}]},
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b2"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_disp_none():
    """ split_by_disposition_attr
        no elem has the attr
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}, {"uri": "a5", "b": "b1"}]}
    attr_ui = "d"
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}, {"uri": "a5", "b": "b1"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_measure_none():
    """ split_by_measure - no split, no CandidateSmasher.REGARDING_MEASURE attribute
    """
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}, {"uri": "a5", "b": "b1"}]}
    candidate = CandidateSmasher()
    result = candidate.split_by_measure(performer)
    expected = [{CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", "b": "b1"}, {"uri": "a1", "b": "b2"}, {"uri": "a5", "b": "b1"}]}]
    assert result == expected


def test_split_by_disp_iri_rm():
    """ split_by_disposition_attr
        split three elems, two into one row and one into another row

        same test as below
    """
    keya = CandidateSmasher.REGARDING_MEASURE
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    attr_ui = keya
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a5", keya: "b1"}]},
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b2"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_disposition_attr(performer, attr_ui)
    assert result == expected


def test_split_by_measure_one():
    """ split_by_measure - split, CandidateSmasher.REGARDING_MEASURE attribute

        same test as above
    """
    keya = CandidateSmasher.REGARDING_MEASURE
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a5", keya: "b1"}]},
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b2"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_measure(performer)
    assert result == expected


def test_split_by_comparator():
    """ split_by_comparator - CandidateSmasher.REGARDING_COMPARATOR attribute

        same test as above
    """
    keya = CandidateSmasher.REGARDING_COMPARATOR
    performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    expected = [
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a5", keya: "b1"}]},
        {CandidateSmasher.HAS_DISPOSITION_IRI: [{"uri": "a1", keya: "b2"}]}
    ]
    candidate = CandidateSmasher()
    result = candidate.split_by_comparator(performer)
    assert result == expected


def test_reg_meas_no_key():
    """ regarding_measure() no key
    """
    split_performer = {"a": "p"}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = ""
    assert result == expected


def test_reg_meas_empty_list():
    """ regarding_measure() empty list
    """
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: []}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = ""
    assert result == expected


def test_reg_meas_first_is_empty():
    """ regarding_measure() first item is empty
    """
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{}]}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = ""
    assert result == expected


def test_reg_meas_no_id():
    """ regarding_measure() no @id
    """
    keya = CandidateSmasher.REGARDING_MEASURE
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1"}}]}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = ""
    assert result == expected


def test_reg_meas_has_id_is_blank():
    """ regarding_measure() @id is blank
    """
    keya = CandidateSmasher.REGARDING_MEASURE
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1", "@id": ""}}]}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = ""
    assert result == expected


def test_reg_meas_has_id_not_blank():
    """ regarding_measure() has @id
    """
    keya = CandidateSmasher.REGARDING_MEASURE
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1", "@id": "the_id"}}]}
    result = CandidateSmasher.regarding_measure(split_performer)
    expected = "the_id"
    assert result == expected


def test_reg_comp_no_key():
    """ regarding_comparator() no key
    """
    split_performer = {"a": "p"}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = ""
    assert result == expected


def test_reg_comp_empty_list():
    """ regarding_comarator() empty list
    """
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: []}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = ""
    assert result == expected


def test_reg_comp_first_is_empty():
    """ regarding_comarator() first item is empty
    """
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{}]}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = ""
    assert result == expected


def test_reg_comp_no_id():
    """ regarding_comarator() no @id
    """
    keya = CandidateSmasher.REGARDING_COMPARATOR
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1"}}]}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = ""
    assert result == expected


def test_reg_comp_has_id_is_blank():
    """ regarding_comarator() has @id
    """
    keya = CandidateSmasher.REGARDING_COMPARATOR
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1", "@id": ""}}]}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = ""
    assert result == expected


def test_reg_comp_has_id_not_blank():
    """ regarding_comarator() has @id
    """
    keya = CandidateSmasher.REGARDING_COMPARATOR
    split_performer = {CandidateSmasher.HAS_DISPOSITION_IRI: [{keya: {"a1": "b1", "@id": "the_id"}}]}
    result = CandidateSmasher.regarding_comparator(split_performer)
    expected = "the_id"
    assert result == expected


# @pytest.mark.skip
def test_make_cand_empty():
    """ make_candidate()
    """
    template = {}
    performer = {}
    expected = {
        "@type": CandidateSmasher.CANDIDATE_IRI,
        "@id": "_:cd41d8cd98f00b204e9800998ecf8427e",
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: None,
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: None
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_empty_and_blank_templ():
    """ make_candidate()
    """
    template = {"@id": ""}
    performer = {}
    expected = {
        "@type": CandidateSmasher.CANDIDATE_IRI,
        "@id": "_:cd41d8cd98f00b204e9800998ecf8427e",
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: None,
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: ""
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_empty_and_blank_perf():
    """ make_candidate()
    """
    template ={}
    performer = {"@id": ""}
    expected = {
        "@type": CandidateSmasher.CANDIDATE_IRI,
        "@id": "_:cd41d8cd98f00b204e9800998ecf8427e",
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: None
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_blank():
    """ make_candidate()
    """
    template = {"@id": ""}
    performer = {"@id": ""}
    expected = {
        "@id": "_:cd41d8cd98f00b204e9800998ecf8427e",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: ""
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_id_only():
    """ make_candidate()
    """
    template = {"@id": "1"}
    performer = {"@id": "2"}
    expected = {
        "@id": "_:cc20ad4d76fe97759aa27a0c99bff6710",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1"
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_measure_id():
    """ make_candidate()
    """
    template = {"@id": "1"}
    performer = {"@id": "2", CandidateSmasher.HAS_DISPOSITION_IRI: [{CandidateSmasher.REGARDING_MEASURE: {"@id": "11"}}]}
    expected = {
        "@id": "_:c285ab9448d2751ee57ece7f762c39095",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1",
        CandidateSmasher.HAS_DISPOSITION_IRI: [{CandidateSmasher.REGARDING_MEASURE: {"@id": "11"}}]
    }
    result = CandidateSmasher.make_candidate(template, performer)
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_make_cand_comparator_id():
    """ make_candidate()
    """
    template = {"@id": "1"}
    performer = {"@id": "2", CandidateSmasher.HAS_DISPOSITION_IRI: [{CandidateSmasher.REGARDING_COMPARATOR: {"@id": "23"}}]}
    expected = {
        "@id": "_:c43cca4b3de2097b9558efefd0ecc3588",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1",
        CandidateSmasher.HAS_DISPOSITION_IRI: [{CandidateSmasher.REGARDING_COMPARATOR: {"@id": "23"}}]
    }
    result = CandidateSmasher.make_candidate(template, performer)
    assert result == expected


def test_make_cand_id_and_other_elems():
    """ make_candidate()
    """
    template = {"@id": "1", "test1": "value1"}
    performer = {"@id": "2", "test2": "value2"}
    expected = {
        "@id": "_:cc20ad4d76fe97759aa27a0c99bff6710",
        "test1": "value1",
        "test2": "value2",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1"
    }
    result = CandidateSmasher.make_candidate(template, performer)
    # print("-result------", result)
    # print("-expected------", expected)
    assert result == expected


def test_make_cand_dup_elems():
    """ make_candidate()
    """
    template = {"@id": "1", "test1": "value1"}
    performer = {"@id": "2", "test1": "value2"}
    expected = {
        "@id": "_:cc20ad4d76fe97759aa27a0c99bff6710",
        "test1": "value2",
        "@type": CandidateSmasher.CANDIDATE_IRI,
        CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
        CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1"
    }
    result = CandidateSmasher.make_candidate(template, performer)
    # print("-result------", result)
    # print("-expected------", expected)
    assert result == expected


def test_generate_candidate_empty():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    result = candidate.generate_candidates()
    expected = []
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_set_spek_hsh():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    candidate.spek_hsh = {}
    result = candidate.generate_candidates()
    expected = []
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_set_IRI_empty():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    candidate.spek_hsh = {candidate.HAS_PERFORMER_IRI: ""}
    result = candidate.generate_candidates()
    expected = []
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_set_IRI_list():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    keya = CandidateSmasher.REGARDING_MEASURE
    candidate.spek_hsh = {candidate.HAS_PERFORMER_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    result = candidate.generate_candidates()
    expected = []
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_about_none():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    keya = CandidateSmasher.REGARDING_MEASURE
    candidate.spek_hsh = {candidate.ABOUT_TEMPLATE_IRI: [], candidate.HAS_PERFORMER_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    result = candidate.generate_candidates()
    expected = []
    print("-result--none----", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_about_empty():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    keya = CandidateSmasher.REGARDING_MEASURE
    candidate.spek_hsh = {candidate.ABOUT_TEMPLATE_IRI: [{}], candidate.HAS_PERFORMER_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}
    result = candidate.generate_candidates()
    expected = []
    print("-result------", result)
    print("-expected------", expected)
    assert result == expected


def test_generate_candidate_about_str():
    """ generate_candidates()
    """
    candidate = CandidateSmasher()
    keya = CandidateSmasher.REGARDING_MEASURE
    candidate.spek_hsh = {candidate.ABOUT_TEMPLATE_IRI: [{"@id": "1", "url": "one"}, {"@id": "2", "url": "two"}], candidate.HAS_PERFORMER_IRI: [{"uri": "a1", keya: "b1"}, {"uri": "a1", keya: "b2"}, {"uri": "a5", keya: "b1"}]}


    # driver for this test
    assert candidate.spek_hsh[candidate.ABOUT_TEMPLATE_IRI][0]["@id"] == "1"
    assert candidate.spek_hsh[candidate.ABOUT_TEMPLATE_IRI][1]["@id"] == "2"

    result = candidate.generate_candidates()
    # expected from running Ruby code
    expected = [{'@id': '_:cc4ca4238a0b923820dcc509a6f75849b', 'url': 'one', 'uri': 'a1', 'http://example.com/slowmo#RegardingMeasure': 'b1', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '1'}, {'@id': '_:cc81e728d9d4c2f636f067f89cc14862c', 'url': 'two', 'uri': 'a1', 'http://example.com/slowmo#RegardingMeasure': 'b1', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '2'}, {'@id': '_:cc4ca4238a0b923820dcc509a6f75849b', 'url': 'one', 'uri': 'a1', 'http://example.com/slowmo#RegardingMeasure': 'b2', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '1'}, {'@id': '_:cc81e728d9d4c2f636f067f89cc14862c', 'url': 'two', 'uri': 'a1', 'http://example.com/slowmo#RegardingMeasure': 'b2', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '2'}, {'@id': '_:cc4ca4238a0b923820dcc509a6f75849b', 'url': 'one', 'uri': 'a5', 'http://example.com/slowmo#RegardingMeasure': 'b1', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '1'}, {'@id': '_:cc81e728d9d4c2f636f067f89cc14862c', 'url': 'two', 'uri': 'a5', 'http://example.com/slowmo#RegardingMeasure': 'b1', '@type': 'http://purl.obolibrary.org/obo/cpo_0000053', 'http://example.com/slowmo#AncestorPerformer': None, 'http://example.com/slowmo#AncestorTemplate': '2'}]
    # print("-result------", result)
    # print("-expected------", expected)
    assert result == expected


def test_smash_blank():
    """ smash
    """
    candidate = CandidateSmasher()
    result = candidate.smash()
    expected = "{" + f'"{candidate.HAS_CANDIDATE_IRI}": []' + "}"
    print("-r----------", result)
    print("-e----------", expected)
    assert result == expected
