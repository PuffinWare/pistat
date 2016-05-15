/* globals $, d3 */
'use strict';

function prepGraph(res) {
  var nodeIndexMap = {},
    entityTypeNames = {
      btid: 'BTID',
      client: 'Client',
      vendor: 'Vendor',
      contributor: 'Contributor'
    },
    nodes = res.nodes.slice(),
    links = res.links.slice();

  nodes.forEach(function (node, i) {
    nodeIndexMap[node.name] = i;
    node.isPrimary = node.entity_id === btid;
    node.entityTypeName = entityTypeNames[node.entity_type];
  });

  links.forEach(function (link) {
    var targetNode = nodes[nodeIndexMap[link.target]],
      connectsToPrimary = link.source === btid;

    targetNode.connectsToPrimary = targetNode.connectsToPrimary || connectsToPrimary;
    link.connectsToPrimary = connectsToPrimary;
    link.source = nodeIndexMap[link.source];
    link.target = nodeIndexMap[link.target];
  });

  return {
    nodes: nodes,
    links: links
  };
}

function freezeLayout(force) {
  force.start();
  for (var i = 0; i < 1000; ++i) force.tick();
  force.stop();
}

function renderGraph(res, clickNodeCallback) {
  var graph = prepGraph(res),
    $svg = $('svg'),
    force = d3.layout.force()
      .size([$svg.width(), $svg.height()])
      .linkDistance(40)
      .charge(-1000)
      .chargeDistance(160)
      .nodes(graph.nodes)
      .links(graph.links),
    svg = d3.select('svg .graph');

  $svg.find('.graph').html('');

  var link = svg.selectAll('.link')
    .data(graph.links)
      .enter().append('line')
        .attr({
          class: 'link',
          'stroke-dasharray': function (d) {
            return d.connectsToPrimary ? false : '2,2';
          }
        });

  var node = svg.selectAll('.node')
    .data(graph.nodes)
      .enter().append('circle')
        .attr({
          r: 16,
          class: function (d) { return 'node ' + d.entity_type; }
        })
        .classed('primary', function (d) { return d.isPrimary; })
        .classed('connects-to-primary', function (d) { return d.connectsToPrimary; })
        .on('click', clickNodeCallback || showTooltip);

  node.append('title')
    .text(function (d) { return d.entityTypeName + ': ' + d.entity_label; });

  freezeLayout(force);

  link.attr({
    x1: function (d) { return d.source.x; },
    y1: function (d) { return d.source.y; },
    x2: function (d) { return d.target.x; },
    y2: function (d) { return d.target.y; }
  });

  node.attr({
    cx: function (d) { return d.x; },
    cy: function (d) { return d.y; }
  });
}

function showTooltip(node) {
  var templateSelector = node.entity_type === 'btid' ? '#btid-node-info-template' : '#node-info-template',
    $nodeInfoContent = $('#node-info-content');

  d3.select('#node-info').attr({
    x: node.x,
    y: node.y
  });
  renderTemplate(templateSelector, node, $nodeInfoContent);
  $nodeInfoContent.show();
}

$(document)
  .on('click', function (event) {
    if (!$(event.target).is('.node')) {
      $('#node-info-content').hide();
    }
  });
