import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canonicalScore,peopleRows,visibleEvidence,safeUrl,parseRoute} from '../ui/model.mjs';
import {buildGraph} from '../ui/graph.mjs';
const load=p=>JSON.parse(readFileSync(new URL('../'+p,import.meta.url),'utf8'));
const state=Object.fromEntries(['people','affiliations','organizations','events','churches','presbyteries'].map(k=>[k,load('data/'+k+'.json')]));
state.datasets=load('data/explorer.json').datasets;
state.occurrences=load('data/source-occurrences.json').datasets;
test('canonical score and score ordering are independent of confidence visibility',()=>{
 const all=peopleRows(state.people,state.affiliations,{sort:'score'});
 for(const confidence of ['all','confirmed','strongly_supported','associated','unresolved']){
  const filtered=peopleRows(state.people,state.affiliations,{sort:'score',confidence});
  for(const row of filtered)assert.equal(row.score,all.find(r=>r.person.id===row.person.id).score);
  assert.deepEqual(filtered.map(r=>r.person.id),all.filter(r=>filtered.some(f=>f.person.id===r.person.id)).map(r=>r.person.id));
 }
 const mk=state.affiliations.filter(a=>a.person_id==='mike-khandjian');
 assert.ok(visibleEvidence(mk,'confirmed').length<mk.length);
 assert.equal(canonicalScore('kathy-keller',state.affiliations),0);
 assert.equal(canonicalScore('tim-keller',state.affiliations),0);
});
test('unresolved claims cannot contribute even with a malformed inclusion flag',()=>assert.equal(canonicalScore('x',[{person_id:'x',confidence:'unresolved',weight:99,score_included:true}]),0));
test('unsafe source URLs are rejected and legacy person links survive',()=>{
 for(const u of ['',null,'javascript:alert(1)','data:text/html,hello','//example.com'])assert.equal(safeUrl(u),null);
 assert.ok(safeUrl('https://example.com'));
 assert.equal(parseRoute('#person=mike-khandjian').id,'mike-khandjian');
});
test('map preserves canonical evidence without transferring family or network membership',()=>{
 const g=buildGraph(state,{layer:'canonical'});
 const cassidy=g.edges.filter(e=>e.source==='person:david-cassidy');
 assert.ok(cassidy.length>0);assert.ok(!cassidy.some(e=>e.target==='organization:national-partnership'));
 const spouse=g.edges.filter(e=>e.evidence?.evidence_kind==='family_relationship');assert.equal(spouse.length,2);assert.ok(spouse.every(e=>e.context));
 const kessler=g.edges.find(e=>e.evidence?.person_id==='james-kessler'&&e.target==='organization:national-partnership');assert.equal(kessler.evidence.weight,5);
 assert.ok(g.nodes.some(n=>n.key==='organization:khandjian-fellowship'));
});
test('map shows unresolved Garris occurrences as source rows, not fabricated people',()=>{
 const g=buildGraph(state,{layer:'source',unresolved:'show',focus:'dataset:garris_letter_1'});
 assert.equal(g.edges.length,60);assert.equal(g.nodes.filter(n=>n.kind==='occurrence').length,35);
 assert.ok(g.edges.every(e=>e.layer==='source'&&e.context));
 const jeff=g.edges.find(e=>e.occurrence.name_as_printed==='Jeff White');assert.equal(jeff.occurrence.person_id,null);
 const hidden=buildGraph(state,{layer:'source',focus:'dataset:garris_letter_1'});assert.equal(hidden.edges.length,25);
});
test('map confidence filtering hides supplemental rows rather than implying confidence',()=>{
 const g=buildGraph(state,{confidence:'confirmed'});assert.ok(g.edges.filter(e=>e.layer==='canonical').every(e=>e.evidence.confidence==='confirmed'));assert.equal(g.edges.filter(e=>e.layer==='source').length,0);
});
