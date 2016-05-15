/* globals $, Mustache */
'use strict';

function parseTemplate(templateSelector, data) {
  var template = $(templateSelector).html();

  return Mustache.render(template, data);
}

function renderTemplate(templateSelector, data, containerSelector) {
  var html = parseTemplate(templateSelector, data);

  $(containerSelector).html(html);
}
