'use strict';

const retext = require('retext');
const english = require('retext-english');

const nlcstToString = require('nlcst-to-string');
const visit = require('unist-util-visit');

const sentiment = require('retext-sentiment');
const keywords = require('retext-keywords');
const pos = require('retext-pos');

module.exports = do_retext;

function do_retext(text, reply){
  let map_pos;

  retext()
    .use(english)
    .use(pos)
    .use(sentiment)
    .use(keywords)
    .use(function(){return collect})
    .process(text,cb);


  function cb(err,file){
    if (err) {
      console.error(err);
    }
    try{
      let space = file.namespace('retext');
      let keywords = space.keywords.map(_keyword);
      let keyphrases = space.keyphrases.map(_keyphrase);
      reply({text,keywords,keyphrases,map_pos});
    }catch(err){
      console.error(err);
    }
  }

  function collect(cst){
    map_pos = {};
    visit(cst,'WordNode',function(node){
      map_pos[nlcstToString(node)] = node.data;
    });
  }
  
  function _keyword(keyword){
    let score = keyword.score;
    let key = nlcstToString(keyword.matches[0].node);
    return {key,score};
  }

  function _keyphrase(keyphrase){
    let score = keyphrase.score;
    let weight = keyphrase.weight;
    let key = keyphrase.matches[0].nodes.map(nlcstToString).join('');
    return {key,score,weight};
  }
  
}