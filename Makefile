# Makefile
# ruby code at https://github.com/Display-Lab/candidate-smasher
#
# Date: 20220726
# By:
#   Scientific Programming and Innovation (SPI)
#   Academic IT
#   H.I.T.S., Michigan Medicine
#   University of Michigan

.PHONY: all
all: lint mypy pytest

.PHONY: t
t:
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_try_map
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_each
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_lists_ext_1_extra_id
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_lists_ext_2_extra_ids
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_lists_ext_2_extra_ids
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_lists_spec_2_extra_ids
	#-python3 -m pytest -s test_candidate_smasher.py::test_merge_ext_two_ids_lists_spec_2_extra_ids_extra
	#-python3 -m pytest -s test_candidate_smasher.py::test_make_cand_empty
	#-python3 -m pytest -s test_candidate_smasher.py::test_make_cand_empty_and_blank_templ
	#-python3 -m pytest -s test_candidate_smasher.py::test_make_cand_measure_id
	#-python3 -m pytest -s test_candidate_smasher.py::test_make_cand_comparator_id
	#-python3 -m pytest -s test_candidate_smasher.py::test_make_cand_id_and_other_elems
	# -python3 -m pytest -s test_candidate_smasher.py::test_make_cand_dup_elems
	#-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_empty
	#-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_set_spek_hsh
	#-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_set_IRI_empty
	#-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_set_IRI_list
	-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_about_none
	-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_about_empty
	-python3 -m pytest -s test_candidate_smasher.py::test_generate_candidate_about_str

.PHONY: lint
lint: pylint flake8

.PHONY: mypy
mypy: candidate_smasher.py_mypy.txt test_candidate_smasher.py_mypy.txt

.PHONY: pylint
pylint: candidate_smasher.py_pylint.txt test_candidate_smasher.py_pylint.txt

.PHONY: flake8
flake8: candidate_smasher.py_flake8.txt test_candidate_smasher.py_flake8.txt

candidate_smasher.py_pylint.txt: candidate_smasher.py pylintrc
	-python3 -m pylint candidate_smasher.py > candidate_smasher.py_pylint.txt
	@cat candidate_smasher.py_pylint.txt

test_candidate_smasher.py_pylint.txt: test_candidate_smasher.py pylintrc
	-python3 -m pylint test_candidate_smasher.py > test_candidate_smasher.py_pylint.txt
	@cat test_candidate_smasher.py_pylint.txt

candidate_smasher.py_flake8.txt: candidate_smasher.py
	-python3 -m flake8 --ignore=E501 candidate_smasher.py > candidate_smasher.py_flake8.txt

test_candidate_smasher.py_flake8.txt: test_candidate_smasher.py
	-python3 -m flake8 --ignore=E501 test_candidate_smasher.py > test_candidate_smasher.py_flake8.txt

.PHONY: pytest
pytest: test_candidate_smasher.py_log.txt

test_candidate_smasher.py_log.txt: test_candidate_smasher.py candidate_smasher.py example.json
	-python3 -m pytest test_candidate_smasher.py
	-python3 -m pytest test_candidate_smasher.py > test_candidate_smasher.py_log.txt

candidate_smasher.py_mypy.txt: candidate_smasher.py
	-python3 -m mypy candidate_smasher.py &> candidate_smasher.py_mypy.txt

test_candidate_smasher.py_mypy.txt: test_candidate_smasher.py
	-python3 -m mypy test_candidate_smasher.py &> test_candidate_smasher.py_mypy.txt

.PHONY: clean
clean:
	-rm -f *_pylint.txt *_flake8.txt *_log.txt *_mypy.txt
