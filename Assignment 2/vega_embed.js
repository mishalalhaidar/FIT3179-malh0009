var vg_1 = "state_budget_map.vg.json";
var vg_2 = "heat_map.vg.json";
var vg_3 = "state_budget_stacked_chart.vg.json";
var vg_4 = "donut_chart.vg.json";
vegaEmbed("#geo-graph", vg_1,{render:"svg",actions:false}).then(function(result){}).catch(console.error)
vegaEmbed("#heat-graph", vg_2,{render:"svg",actions:false}).then(function(result){}).catch(console.error)
vegaEmbed("#area-line-graph", vg_3,{render:"svg",actions:false}).then(function(result){}).catch(console.error)
vegaEmbed("#donut-graph", vg_4,{render:"svg",actions:false}).then(function(result){}).catch(console.error)