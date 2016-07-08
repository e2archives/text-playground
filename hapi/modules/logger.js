#!/usr/bin/env node
'use strict';

const path = require('path');
const bunyan = require('bunyan');
const LOG_PATH = require('./config.js').LOG_PATH;

const Logger = bunyan.createLogger({
  name: 'textanalytics-manager',
  streams: [
    {
      level: 'debug',
      stream: process.stdout
    },
    {
      level: 'debug',
      path: path.join(LOG_PATH,'debug.log')
    },
    {
      level: 'error',
      path: path.join(LOG_PATH,'error.log')
    }
  ]
});

function handleError(err){
  Logger.error(err);
}

module.exports = {Logger,handleError};