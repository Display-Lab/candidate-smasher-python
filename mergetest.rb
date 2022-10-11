
class MergeTest
  def self.merge_external_templates(spec_templates, ext_templates)
    t_ids = spec_templates.map{|t| t['@id']}
    
    # For every template in spec, lookup from external and merge info.
    merged = spec_templates.map do |t|
      new_t = ext_templates.select{|e| e['@id'] == t['@id']}.first || {}
      #puts("-----")
      #puts(new_t.class)
      #puts(new_t)

      new_t.merge(t) do |key, ext_val, spek_val|
        if spek_val.is_a?(Array) || ext_val.is_a?(Array)
          result = Array(spek_val) + Array(ext_val)
          result.uniq
        else
          spek_val
        end
      end
    end

    merged
  end
end

def RunTest(spec, ext, expected)
    m = MergeTest
    result = m.merge_external_templates(spec, ext)
    #puts(result.class)
    #puts("---spec------------")
    #puts(spec)
    #puts("---ext------------")
    #puts(ext)
    puts("---result-------")
    puts(result)
    puts("----------------")
    puts("---expected-----")
    puts(expected)
    puts("----------------")
    if expected == result
        puts("PASS")
    else
        puts("fail")
    end
end

a = [{'@id' => '1', 'car' => 'ok' , '@type' => '5'}, {'@id' => '2', 'myitem' => 'test item'}]
b = [{'@id' => '1', 'car2' => 'ok2' }]
expected = [{'@id' => '1', 'car' => 'ok' , '@type' => '5', 'car2' => 'ok2'}, {'@id' => '2', 'myitem' => 'test item'}] 
RunTest a, b, expected

a = [{'@id' => '1', 'car' => 'ok' , '@type' => '5'}, {'@id' => '2', 'myitem' => 'test item', "dup" => "testspec"}]
b = [{'@id' => '2', 'car2' => 'ok2', 'dup' => 'testext' }, {'@id' => '3', 'car3' => 'ok3' }] 
expected = [{"@id"=>"1", "car"=>"ok", "@type"=>"5"}, {"@id"=>"2", "car2"=>"ok2", "myitem"=>"test item", "dup" => "testspec"}]
RunTest a, b, expected

# test_merge_ext_try_map()
a = [
    {'@id'=>'1', '@type'=>'test type', 'testitem'=>'test value'},
    {'@id'=>'2', 'test key2'=>'test value2'},
]
b = [
    {'@id'=>'1', 'car2'=>'ok2', 'car'=>'ok', '@type'=>'5'},
]
expected = [
    {'@id'=>'1', 'car2'=>'ok2', 'car'=>'ok', '@type'=>'test type', 'testitem'=>'test value'},
    {'@id'=>'2', 'test key2'=>'test value2'},
]
RunTest a, b, expected

# test_merge_ext_two_ids_each()
a = [
        {'@id'=>'1', 'car'=>'ok', '@type'=>'5'},
        {'@id'=>'2', 'myitem'=>'test item', "dup"=>"testspec"}
]
b = [
        {'@id'=>'2', 'car2'=>'ok2', "dup"=>"testtext"},
        {"@id"=>'3', 'car2'=>'ok3'}
]
expected = [
        {'@id'=>'1', 'car'=>'ok', '@type'=>'5'},
        {"@id"=>"2", "car2"=>"ok2", "dup"=>"testspec", "myitem"=>"test item"}
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_ext_1_extra_id()
a = [
  {'@id'=>'1', 'car'=>[1, 2, 3], '@type'=>'5'},
  {'@id'=>'2', "dup"=>"testspec"}
]
b = [
    {'@id'=>'1', 'car'=>[4, 5], "dup"=>"testtext"},
    {"@id"=>'3', 'car2'=>'ok3'}
]
expected = [
    {'@id'=>'1', 'car'=>[1, 2, 3, 4, 5], '@type'=>'5', "dup"=>"testtext"},
    {'@id'=>'2', "dup"=>"testspec"}
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_ext_2_extra_ids()
a = [
    {'@id'=>'1', 'car'=>[1, 2, 3], '@type'=>'5'},
    {'@id'=>'2', "dup"=>"testspec"}
]
b = [
    {'@id'=>'1', 'car'=>[4, 5], "dup"=>"testtext"},
    {"@id"=>'3', 'car2'=>'ok3'},
    {"@id"=>'4', 'car4list'=>[8, 5, 6]}
]
expected = [
    {'@id'=>'1', 'car'=>[1, 2, 3, 4, 5], '@type'=>'5', "dup"=>"testtext"},
    {'@id'=>'2', "dup"=>"testspec"},
]
RunTest a, b, expected

# def test_merge_ext_two_ids_lists_spec_2_extra_ids()
a = [
    {'@id'=>'1', 'car'=>[1, 2, 3], '@type'=>'5'},
    {'@id'=>'2', "dup"=>"testspec"},
    {"@id"=>'5', 'c5list'=>[8, 5, 6]},
    {"@id"=>'6', 'c6list'=>[9, 9, 6]}  # this one is not in ext
]
b = [
    {'@id'=>'1', 'car'=>[4, 5], "dup"=>"testtext"},
    {"@id"=>'3', 'car2'=>'ok3'},  # this one is not in spec, IT GETS DROPPED
    {"@id"=>'5', 'c5list'=>[7, 5, 8, 6], 'extra_item'=>"extra"},  # this one need to merge the list, plus this one has an extra item
]
expected = [
    {'@id'=>'1', 'car'=>[1, 2, 3, 4, 5], '@type'=>'5', "dup"=>"testtext"},
    {'@id'=>'2', "dup"=>"testspec"},
    {"@id"=>'5', 'c5list'=>[8, 5, 6, 7], "extra_item"=>"extra"},
    {"@id"=>'6', 'c6list'=>[9, 9, 6]}
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_spec_2_extra_ids_extra()
a = [
        {'@id'=>'1', 'car'=>[1, 2, 3], '@type'=>'5'},
        {'@id'=>'2', "dup"=>"testspec"},
        {"@id"=>'5', 'c5list'=>[8, 5, 6], "extra_one"=>"extra1"},  # this one need to merge the list, plus this one has an extra item
        {"@id"=>'6', 'c6list'=>[9, 9, 6]}  # this one is not in ext
]
b = [
        {'@id'=>'1', 'car'=>[4, 5], "dup"=>"testtext"},
        {"@id"=>'3', 'car2'=>'ok3'},  # this one is not in spec
        {"@id"=>'5', 'c5list'=>[7, 5, 8, 6]},
]
expected = [
        {'@id'=>'1', 'car'=>[1, 2, 3, 4, 5], "dup"=>"testtext", '@type'=>'5'},
        {'@id'=>'2', "dup"=>"testspec"},
        {"@id"=>'5', 'c5list'=>[8, 5, 6, 7], "extra_one"=>"extra1"},
        {"@id"=>'6', 'c6list'=>[9, 9, 6]}
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_spec_mix()
a = [
        {'@id'=>'1', 'car'=>'spec', '@type'=>'5'},
]
b = [
        {'@id'=>'1', 'car'=>[4, 5], "dup"=>"testtext"},
]
expected = [
        {'@id'=>'1', 'car'=>['spec', 4, 5], "dup"=>"testtext", '@type'=>'5'},
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_spec_mix_ext()
a = [
        {'@id'=>'1', 'car'=>[4,5], '@type'=>'5'},
]
b = [
        {'@id'=>'1', 'car'=>'ext', "dup"=>"testtext"},
]
expected = [
        {'@id'=>'1', 'car'=>[4, 5, 'ext'], "dup"=>"testtext", '@type'=>'5'},
]
RunTest a, b, expected

# test_merge_ext_two_ids_lists_dup()
a = [
        {'@id'=>'1', 'car'=>[4,6], '@type'=>'5'},
]
b = [
        {'@id'=>'1', 'car'=>[1,2,4,5,6,7], "dup"=>"testtext"},
]
expected = [
        {'@id'=>'1', 'car'=>[4,6,1,2,5,7], "dup"=>"testtext", '@type'=>'5'},
]
RunTest a, b, expected

# test_merge_dups_in_spec()
a = [
        {'@id'=>'1', 'car'=>[4,6,4,6], '@type'=>'5'},
]
b = [
        {'@id'=>'1', 'car'=>[1,2,4], "dup"=>"testtext"},
]
expected = [
        {'@id'=>'1', 'car'=>[4,6,1,2], "dup"=>"testtext", '@type'=>'5'},
]
RunTest a, b, expected

