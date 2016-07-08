'use strict';

const Logger = require('../modules/logger.js').Logger;
const retext = require('../modules/retext.js');

const route = 'retext';

module.exports = {
  method  : "POST",
  path    : "/"+route,
  handler : handleRoute
};


function handleRoute(request,reply){
  retext(request.payload,reply);
}