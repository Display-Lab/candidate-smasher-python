HAS_DISPOSITION_IRI = "http://purl.obolibrary.org/obo/RO_0000091"

def split_by_disposition_attr(performer, attr_uri)
  dispositions = performer[HAS_DISPOSITION_IRI]
  return [performer] if dispositions.nil?

  uniques = dispositions.map{|d| d[attr_uri]}.uniq
  puts(uniques)
  splits = uniques.map do |attr|
    p = performer.dup
    p[HAS_DISPOSITION_IRI] = dispositions.select do |d| 
      d[attr_uri] == attr
    end 
    puts("2-------")
    puts(p.class)
    puts(p)
    p   
  end 
  return splits
end 

def test1
    performer = {}
    attr_uri = ""
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

def test2
    performer = {HAS_DISPOSITION_IRI => []}
    attr_uri = ""
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

def test3
    # expected [{"http://purl.obolibrary.org/obo/RO_0000091"=>[{"uri"=>"a1", "b"=>"b1"}, {"uri"=>"a1", "b"=>"b2"}]}]
    performer = {HAS_DISPOSITION_IRI => [{"uri" =>"a1", "b" =>"b1"}, {"uri" =>"a1", "b" =>"b2"}]}
    attr_uri = "uri"
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

def test4
    # expected
    # {"http://purl.obolibrary.org/obo/RO_0000091"=>[{"uri"=>"a1", "b"=>"b1"}]}
    # {"http://purl.obolibrary.org/obo/RO_0000091"=>[{"uri"=>"a2", "b"=>"b2"}]}
    performer = {HAS_DISPOSITION_IRI => [{"uri" =>"a1", "b" =>"b1"}, {"uri" =>"a2", "b" =>"b2"}]}
    attr_uri = "uri"
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

def test5
    # expected
    # {"http://purl.obolibrary.org/obo/RO_0000091"=>[{"uri"=>"a1", "b"=>"b1"}, {"uri"=>"a1", "b"=>"b1"}]}
    # {"http://purl.obolibrary.org/obo/RO_0000091"=>[{"uri"=>"a1", "b"=>"b2"}]}
    performer = {HAS_DISPOSITION_IRI => [{"uri" =>"a1", "b" =>"b1"}, {"uri" =>"a1", "b" =>"b2"}, {"uri" =>"a5", "b" =>"b1"}]}
    attr_uri = "b"
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

def test6()
    # expected
    performer = {HAS_DISPOSITION_IRI => [{"uri" =>"a1", "b" =>"b1"}, {"uri" =>"a1", "b" =>"b2"}, {"uri" =>"a5", "b" =>"b1"}]}
    attr_uri = "d"
    result = split_by_disposition_attr(performer, attr_uri)
    puts(result.class)
    puts(result)
end

test6()
