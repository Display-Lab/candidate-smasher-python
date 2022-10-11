
require '../candidate-smasher/lib/candidate_smasher'


c = CandidateSmasher.new("../candidate-smasher/lib/candidate_smasher/spek/fixtures/spek.json")
# puts(c.class)
g = c.list_missing()
#puts(g.class)
#puts(g)
#g = c.generate_candidates()
#p(g.class)
#p(g)

p("none")
c.spek_hsh = {}
c.spek_hsh = {"http://example.com/slowmo#IsAboutTemplate"=>[], "http://example.com/slowmo#IsAboutPerformer"=>[{"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b1"}, {"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b2"}, {"uri"=>"a5", "http://example.com/slowmo#RegardingMeasure"=>"b1"}]}
g = c.generate_candidates()
p(g.class)
p(g)

p("empty hash")
c.spek_hsh = {}
c.spek_hsh = {"http://example.com/slowmo#IsAboutTemplate"=>[{}], "http://example.com/slowmo#IsAboutPerformer"=>[{"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b1"}, {"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b2"}, {"uri"=>"a5", "http://example.com/slowmo#RegardingMeasure"=>"b1"}]}
g = c.generate_candidates()
p(g.class)
p(g)

c.spek_hsh = {}
c.spek_hsh = {"http://example.com/slowmo#IsAboutTemplate"=>[{"@id"=>"1"}], "http://example.com/slowmo#IsAboutPerformer"=>[{"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b1"}, {"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b2"}, {"uri"=>"a5", "http://example.com/slowmo#RegardingMeasure"=>"b1"}]}
g = c.generate_candidates()
p(g.class)
p(g)

c.spek_hsh = {"http://example.com/slowmo#IsAboutTemplate"=>[{"@id"=>1, "url"=>"one"}, {"@id"=>2, "url"=>"two"}], "http://example.com/slowmo#IsAboutPerformer"=>[{"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b1"}, {"uri"=>"a1", "http://example.com/slowmo#RegardingMeasure"=>"b2"}, {"uri"=>"a5", "http://example.com/slowmo#RegardingMeasure"=>"b1"}]}
g = c.generate_candidates()
p(g.class)
p(g)
