#!/usr/bin/env node
'use strict';
const config = Object.assign(require('../conf.json'),process.env);
module.exports = config;