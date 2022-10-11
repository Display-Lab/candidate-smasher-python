require '../candidate-smasher/lib/candidate_smasher'


# test_make_cand_empty()
template = {}
performer = {}
g = CandidateSmasher.make_candidate(template, performer)
# expected {"@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "@id"=>"_:cd41d8cd98f00b204e9800998ecf8427e", "http://example.com/slowmo#AncestorPerformer"=>nil, "http://example.com/slowmo#AncestorTemplate"=>nil}
puts(g.class)
puts(g)

# test_make_cand_empty()
template = {"@id"=>nil}
performer = {"@id"=>nil}
g = CandidateSmasher.make_candidate(template, performer)
# expected {"@id"=>"_:cd41d8cd98f00b204e9800998ecf8427e", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>nil, "http://example.com/slowmo#AncestorTemplate"=>nil}
puts(g.class)
puts(g)

# test_make_cand_()
template = {"@id"=>""}
performer = {"@id"=>nil}
g = CandidateSmasher.make_candidate(template, performer)
# {"@id"=>"_:cd41d8cd98f00b204e9800998ecf8427e", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>nil, "http://example.com/slowmo#AncestorTemplate"=>""}
puts(g.class)
puts(g)

# test_make_cand_()
template = {"@id"=>nil}
performer = {"@id"=>""}
g = CandidateSmasher.make_candidate(template, performer)
# {"@id"=>"_:cd41d8cd98f00b204e9800998ecf8427e", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"", "http://example.com/slowmo#AncestorTemplate"=>nil}
puts(g.class)
puts(g)


# test_make_cand_id_only()
template = {"@id"=>"1"}
performer = {"@id"=>"2"}
g = CandidateSmasher.make_candidate(template, performer)
# expected {"@id"=>"_:cc20ad4d76fe97759aa27a0c99bff6710", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"2", "http://example.com/slowmo#AncestorTemplate"=>"1"}
puts(g.class)
puts(g)


# test_make_cand_measure_id()
template = {"@id"=>"1"}
HAS_DISPOSITION_IRI = "http://purl.obolibrary.org/obo/RO_0000091"
REGARDING_MEASURE = "http://example.com/slowmo#RegardingMeasure"
CANDIDATE_IRI = "http://purl.obolibrary.org/obo/cpo_0000053"
performer = {"@id"=>"2", HAS_DISPOSITION_IRI=>[{REGARDING_MEASURE=>{"@id"=>"11"}}]}
#expected = {
#    "@id"=>"_:c285ab9448d2751ee57ece7f762c39095",
#    "@type"=>CandidateSmasher.CANDIDATE_IRI,
#    CandidateSmasher.ANCESTOR_PERFORMER_IRI=>"2",
#    CandidateSmasher.ANCESTOR_TEMPLATE_IRI=>"1",
#    CandidateSmasher.HAS_DISPOSITION_IRI=>[{CandidateSmasher.REGARDING_MEASURE=>{"@id"=>"11"}}]
#}
# expected {"@id"=>"_:c285ab9448d2751ee57ece7f762c39095", "http://purl.obolibrary.org/obo/RO_0000091"=>[{"http://example.com/slowmo#RegardingMeasure"=>{"@id"=>"11"}}], "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"2", "http://example.com/slowmo#AncestorTemplate"=>"1"}
g = CandidateSmasher.make_candidate(template, performer)
puts(g.class)
puts(g)


# test_make_cand_comparator_id()
REGARDING_COMPARATOR = "http://example.com/slowmo#RegardingComparator"
template = {"@id"=>"1"}
performer = {"@id"=>"2", HAS_DISPOSITION_IRI=>[{REGARDING_COMPARATOR=>{"@id"=>"23"}}]}
#expected = {
#    "@id": "_:c43cca4b3de2097b9558efefd0ecc3588",
#    "@type": CandidateSmasher.CANDIDATE_IRI,
#    CandidateSmasher.ANCESTOR_PERFORMER_IRI: "2",
#    CandidateSmasher.ANCESTOR_TEMPLATE_IRI: "1",
#    CandidateSmasher.HAS_DISPOSITION_IRI: [{CandidateSmasher.REGARDING_COMPARATOR: {"@id": "23"}}]
#}
# expected {"@id"=>"_:c43cca4b3de2097b9558efefd0ecc3588", "http://purl.obolibrary.org/obo/RO_0000091"=>[{"http://example.com/slowmo#RegardingComparator"=>{"@id"=>"23"}}], "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"2", "http://example.com/slowmo#AncestorTemplate"=>"1"}
g = CandidateSmasher.make_candidate(template, performer)
puts(g.class)
puts(g)

# test_make_cand_id_and_other_elems()
template = {"@id"=>"1", "test1"=>"value1"}
performer = {"@id"=>"2", "test2"=>"value2"}
g = CandidateSmasher.make_candidate(template, performer)
# expected {"@id"=>"_:cc20ad4d76fe97759aa27a0c99bff6710", "test1"=>"value1", "test2"=>"value2", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"2", "http://example.com/slowmo#AncestorTemplate"=>"1"}
puts(g.class)
puts(g)

# 
template = {"@id"=>"1", "test2"=>"value1"}
performer = {"@id"=>"2", "test2"=>"value2"}
g = CandidateSmasher.make_candidate(template, performer)
# expected {"@id"=>"_:cc20ad4d76fe97759aa27a0c99bff6710", "test2"=>"value2", "@type"=>"http://purl.obolibrary.org/obo/cpo_0000053", "http://example.com/slowmo#AncestorPerformer"=>"2", "http://example.com/slowmo#AncestorTemplate"=>"1"}
puts(g.class)
puts(g)
