require "rdf"
require "json/ld"

 # interrim hack until everything is RDF from the get go
 def templates_rdf_to_json(graph)
   puts("1")
   ld_tmpl = JSON::LD::API.fromRdf(graph).compact
   puts("2")
   ld_tmpl.each do |template|
     puts("3")
     template.transform_values! do |v|
       puts("4")
       if(v.respond_to?(:first) && v.length == 1)
         v.first
       else
         v
       end
     end
   end
 end

#rdfjson = RDFtoJSONtest
#g = RDF::Graph.new
g = RDF::Graph.load("doap_small_sample.nt")
result = templates_rdf_to_json(g)
puts(result)
#puts(result.class)
result.each do |r|
    puts(r.class)
end
