#!/usr/bin/env node
'use strict';

const Hapi = require('hapi');
const Logger = require('./modules/logger.js').Logger;

var cors = {
  origin: ['*'],
  matchOrigin: true,
  isOriginExposed: false,
  credentials: true
};

var route_404 = {
  method: '*',
  path: '/{p*}',
  handler: function (request, reply) {
    return reply('Not Found').code(404);
  }
};

var server = new Hapi.Server();
server.connection({ port: 80 });
server.route([
  require('./routes/retext.js'),
  route_404
]);

server.start(function() {
  Logger.debug('Hapi service started @ '+ server.info.uri);
});