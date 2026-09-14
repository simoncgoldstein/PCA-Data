import {included, evidenceGroup} from './model.mjs';
const escape = v=>String(v??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const key=(kind,id)=>`${kind}:${id}`;
export function buildGraph(state, filters={}) {
 const nodes=new Map(),edges=[];
 const add=(kind,id,label)=>{const k=key(kind,id);if(!nodes.has(k))nodes.set(k,{key:k,kind,id,label});return k;};
 const person=id=>{const p=state.people.find(p=>p.id===id);return p?add('person',id,p.name):null;};
 const names={organization:state.organizations,event:state.events,church:state.churches||[],presbytery:state.presbyteries||[],person:state.people};
 for(const a of state.affiliations){
  if(filters.layer==='source')continue;
  if(filters.confidence&&filters.confidence!=='all'&&a.confidence!==filters.confidence)continue;
  if(filters.context==='hide'&&!included(a))continue;
  if(filters.kind&&filters.kind!=='all'&&evidenceGroup(a)!==filters.kind)continue;
  const s=person(a.person_id);const t=add(a.target_type,a.target_id,names[a.target_type]?.find(x=>x.id===a.target_id)?.name||a.target_id);
  if(s)edges.push({id:a.id,source:s,target:t,layer:'canonical',context:!included(a),label:a.role,evidence:a});
 }
 if(filters.layer!=='canonical'&&(!filters.kind||filters.kind==='all')&&(!filters.confidence||filters.confidence==='all')){
  for(const d of state.datasets.filter(d=>filters.scope==='all'||d.target_id)){
   const target=add('dataset',d.id,d.label);
   const seen=new Set();
   for(const r of state.occurrences[d.id]||[]){
    if(!r.person_id&&filters.unresolved!=='show')continue;
    const s=r.person_id?person(r.person_id):add('occurrence',r.id,`${r.name_as_printed} [unresolved]`);
    if(!s||seen.has(s))continue;seen.add(s);
    edges.push({id:`source-${d.id}-${r.id}`,source:s,target,layer:'source',context:true,label:r.evidence_kind.replaceAll('_',' '),occurrence:r,dataset:d});
   }
  }
 }
 // Event ownership is metadata, not a person membership edge.
 if(filters.layer!=='source'&&filters.context!=='hide')for(const e of state.events){if(e.organization_id&&nodes.has(key('event',e.id))){const t=add('organization',e.organization_id,state.organizations.find(o=>o.id===e.organization_id)?.name||e.organization_id);edges.push({id:`event-org-${e.id}`,source:key('event',e.id),target:t,layer:'structure',context:true,label:'Related organizational event',event:e});}}
 let keep=new Set(edges.flatMap(e=>[e.source,e.target]));
 const q=(filters.q||'').trim().toLowerCase();
 if(filters.focus||q){let frontier=new Set([...nodes.values()].filter(n=>filters.focus?n.key===filters.focus:n.label.toLowerCase().includes(q)).map(n=>n.key));keep=new Set(frontier);for(let depth=0;depth<Number(filters.depth||1);depth++){const next=new Set();for(const e of edges){if(frontier.has(e.source))next.add(e.target);if(frontier.has(e.target))next.add(e.source);}for(const k of next)keep.add(k);frontier=next;}}
 const visibleEdges=edges.filter(e=>keep.has(e.source)&&keep.has(e.target));const connected=new Set(visibleEdges.flatMap(e=>[e.source,e.target]));
 return {nodes:[...nodes.values()].filter(n=>keep.has(n.key)&&(connected.has(n.key)||filters.focus===n.key||q)),edges:visibleEdges};
}
function layout(graph){
 const groups=graph.nodes.filter(n=>n.kind!=='person'&&n.kind!=='occurrence');
 const people=graph.nodes.filter(n=>n.kind==='person'||n.kind==='occurrence');
 groups.forEach((n,i)=>{const a=2*Math.PI*i/Math.max(groups.length,1);n.x=500+Math.cos(a)*330;n.y=370+Math.sin(a)*260;});
 people.forEach((n,i)=>{const a=i*2.399963;n.x=500+Math.cos(a)*(80+Math.sqrt(i)*20);n.y=370+Math.sin(a)*(80+Math.sqrt(i)*17);});
 const map=new Map(graph.nodes.map(n=>[n.key,n]));
 for(let iteration=0;iteration<150;iteration++){
  const cooling=1-iteration/170;
  for(const n of graph.nodes){n.fx=(500-n.x)*.003;n.fy=(370-n.y)*.003;}
  for(let i=0;i<graph.nodes.length;i++)for(let j=i+1;j<graph.nodes.length;j++){const a=graph.nodes[i],b=graph.nodes[j];let dx=a.x-b.x,dy=a.y-b.y;const d2=Math.max(80,dx*dx+dy*dy);const f=550/d2;a.fx+=dx*f;a.fy+=dy*f;b.fx-=dx*f;b.fy-=dy*f;}
  for(const e of graph.edges){const a=map.get(e.source),b=map.get(e.target);const dx=b.x-a.x,dy=b.y-a.y,d=Math.max(1,Math.hypot(dx,dy));const f=(d-105)*.015;a.fx+=dx/d*f;a.fy+=dy/d*f;b.fx-=dx/d*f;b.fy-=dy/d*f;}
  for(const n of graph.nodes){n.x+=Math.max(-16,Math.min(16,n.fx))*cooling;n.y+=Math.max(-16,Math.min(16,n.fy))*cooling;}
 }
 return map;
}
export function mountGraph(host,state,params){
 const filters=Object.fromEntries(params);const graph=buildGraph(state,filters);
 if(graph.nodes.length>700){host.querySelector('[data-map-status]').textContent=`${graph.nodes.length} matching nodes. Narrow the neighborhood before laying out this map.`;host.querySelector('.map-inspector').innerHTML='<h3>Choose a smaller neighborhood</h3><p>Search for a name or group, or hide unresolved rows. The full source rosters remain available in the dataset directory.</p>';return;}
 const nodes=layout(graph);
 const svg=host.querySelector('svg');const viewport=svg.querySelector('.map-viewport');const inspector=host.querySelector('.map-inspector');const status=host.querySelector('[data-map-status]');
 status.textContent=`${graph.nodes.length} nodes · ${graph.edges.length} connections. Layout distance has no evidentiary meaning.`;
 const route=n=>n.kind==='occurrence'?`#dataset/${graph.edges.find(e=>e.source===n.key)?.dataset.id}`:`#${n.kind}/${encodeURIComponent(n.id)}`;
 const nodeLink=n=>`<a href="${route(n)}">${escape(n.label)} →</a>`;
 viewport.innerHTML=`<g class="map-edges">${graph.edges.map(e=>`<g class="map-edge ${e.context?'context':''} ${e.layer}" data-edge="${escape(e.id)}" role="button" tabindex="0" aria-label="${escape(nodes.get(e.source).label+' · '+e.label+' · '+nodes.get(e.target).label)}"><line class="edge-hit"/><line class="edge-line"/><title>${escape(e.label)} · ${escape(e.layer)}</title></g>`).join('')}</g><g class="map-nodes">${graph.nodes.map(n=>`<g class="map-node ${n.kind}" data-node="${escape(n.key)}" role="button" tabindex="0" aria-label="${escape(n.label)}"><circle r="${n.kind==='person'?6:n.kind==='occurrence'?5:10}"/><text x="14" y="4">${escape(n.label)}</text><title>${escape(n.label)}</title></g>`).join('')}</g>`;
 const nodeEls=new Map([...viewport.querySelectorAll('[data-node]')].map(el=>[el.dataset.node,el]));
 const edgeEls=new Map([...viewport.querySelectorAll('[data-edge]')].map(el=>[el.dataset.edge,el]));
 function positions(){for(const [k,el]of nodeEls){const n=nodes.get(k);el.setAttribute('transform',`translate(${n.x},${n.y})`);}for(const e of graph.edges){const a=nodes.get(e.source),b=nodes.get(e.target);for(const l of edgeEls.get(e.id).querySelectorAll('line')){l.setAttribute('x1',a.x);l.setAttribute('y1',a.y);l.setAttribute('x2',b.x);l.setAttribute('y2',b.y);}}}
 let camera={x:0,y:0,w:1000,h:740};
 function cameraUpdate(){svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`);host.querySelector('[data-zoom-level]').textContent=`${Math.round(100000/camera.w)}%`;}
 function fit(){if(!graph.nodes.length)return;const xs=graph.nodes.map(n=>n.x),ys=graph.nodes.map(n=>n.y);const x=Math.min(...xs)-50,y=Math.min(...ys)-50;const w=Math.max(...xs)-x+270,h=Math.max(...ys)-y+70;camera={x,y,w:Math.max(w,h*1000/740),h:Math.max(h,w*740/1000)};cameraUpdate();}
 function point(event){const p=svg.createSVGPoint();p.x=event.clientX;p.y=event.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
 function zoom(factor,center){const w=Math.max(140,Math.min(7000,camera.w*factor));const f=w/camera.w;const c=center||{x:camera.x+camera.w/2,y:camera.y+camera.h/2};camera={x:c.x-(c.x-camera.x)*f,y:c.y-(c.y-camera.y)*f,w,h:camera.h*f};cameraUpdate();}
 function selectNode(k){const n=nodes.get(k);const es=graph.edges.filter(e=>e.source===k||e.target===k);const neighbors=new Set(es.flatMap(e=>[e.source,e.target]));for(const [id,el]of nodeEls){el.classList.toggle('dimmed',!neighbors.has(id)&&id!==k);el.classList.toggle('selected',id===k);}for(const e of graph.edges)edgeEls.get(e.id).classList.toggle('dimmed',!es.includes(e));
  inspector.innerHTML=`<p class="eyebrow">${escape(n.kind==='occurrence'?'Unresolved source row':n.kind)}</p><h3>${escape(n.label)}</h3><p>${nodeLink(n)}</p><button data-focus="${escape(k)}">Focus this neighborhood</button><h4>${es.length} documented connections</h4>${es.map(e=>`<button class="inspect-edge" data-inspect-edge="${escape(e.id)}">${escape(nodes.get(e.source===k?e.target:e.source).label)}<small>${escape(e.label)} · ${escape(e.layer)}</small></button>`).join('')}`;
 }
 function selectEdge(id){const e=graph.edges.find(e=>e.id===id);if(!e)return;for(const [k,el]of nodeEls)el.classList.toggle('dimmed',k!==e.source&&k!==e.target);for(const [k,el]of edgeEls)el.classList.toggle('dimmed',k!==id);
  const a=e.evidence;const sourceLinks=ids=>(ids||[]).map(id=>`<a href="#source/${encodeURIComponent(id)}">${escape(state.sources.find(s=>s.id===id)?.title||id)}</a>`).join('<br>');
  inspector.innerHTML=`<p class="eyebrow">${escape(e.layer)} connection</p><h3>${escape(e.label)}</h3><p>${nodeLink(nodes.get(e.source))}</p><p>${nodeLink(nodes.get(e.target))}</p>${a?`<p><strong>${escape(a.confidence.replaceAll('_',' '))}</strong> · ${escape(a.evidence_kind.replaceAll('_',' '))}</p><p>${included(a)?'Included':'Excluded'} from index · weight ${a.weight}</p><p>${escape(a.notes||'')}</p><div class="source-links">${sourceLinks(a.source_ids)}</div>`:e.occurrence?`<p>Source occurrence, excluded from index. ${e.occurrence.person_id?'Canonical identity linked.':'Canonical identity unresolved; this is not a canonical person.'}</p><p>Locator: ${escape(e.occurrence.source_locator)}</p><p>${escape(e.dataset.boundary)}</p><div class="source-links">${sourceLinks(e.dataset.source_ids)}</div><p><a href="#dataset/${e.dataset.id}">Inspect complete roster and source fields →</a></p>`:`<p>Event-to-organization metadata, excluded from index. This line does not assert person membership.</p>${sourceLinks(e.event.source_ids)}`}`;
 }
 let drag=null;const pointers=new Map();let pinch=null;
 svg.addEventListener('pointerdown',e=>{if(e.button!==0)return;const p=point(e);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});svg.setPointerCapture(e.pointerId);if(pointers.size===2){const a=[...pointers.values()];pinch={distance:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)};drag=null;return;}const el=e.target.closest('[data-node]');drag={pointer:e.pointerId,node:el?.dataset.node,edge:e.target.closest('[data-edge]')?.dataset.edge,start:p,last:p,moved:false};});
 svg.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const p=point(e);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pinch&&pointers.size===2){const a=[...pointers.values()],distance=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);if(distance>0){zoom(pinch.distance/distance,point({clientX:(a[0].x+a[1].x)/2,clientY:(a[0].y+a[1].y)/2}));pinch.distance=distance;}return;}if(!drag)return;const dx=p.x-drag.last.x,dy=p.y-drag.last.y;if(Math.hypot(p.x-drag.start.x,p.y-drag.start.y)>3)drag.moved=true;if(drag.node){const n=nodes.get(drag.node);n.x+=dx;n.y+=dy;positions();drag.last=p;}else{camera.x-=dx;camera.y-=dy;cameraUpdate();drag.last=point(e);}});
 svg.addEventListener('pointerup',e=>{if(drag&&!drag.moved){if(drag.node)selectNode(drag.node);else{const id=drag.edge;if(id)selectEdge(id);}}pointers.delete(e.pointerId);if(pointers.size<2)pinch=null;drag=null;});
 svg.addEventListener('pointercancel',e=>{pointers.delete(e.pointerId);pinch=null;drag=null;});
 svg.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY>0?1.12:1/1.12,point(e));},{passive:false});
 svg.addEventListener('keydown',e=>{const n=e.target.closest('[data-node]')?.dataset.node,edge=e.target.closest('[data-edge]')?.dataset.edge;if(['Enter',' '].includes(e.key)&&(n||edge)){e.preventDefault();n?selectNode(n):selectEdge(edge);}else if(['+','=','-','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();if(e.key==='+'||e.key==='=')zoom(.8);else if(e.key==='-')zoom(1.25);else{const step=camera.w*.08;camera.x+=e.key==='ArrowRight'?step:e.key==='ArrowLeft'?-step:0;camera.y+=e.key==='ArrowDown'?step:e.key==='ArrowUp'?-step:0;cameraUpdate();}}});
 host.addEventListener('click',e=>{const control=e.target.closest('[data-map-control]')?.dataset.mapControl;if(control==='in')zoom(.8);if(control==='out')zoom(1.25);if(control==='fit')fit();if(control==='reset'){for(const el of [...nodeEls.values(),...edgeEls.values()])el.classList.remove('dimmed','selected');inspector.innerHTML='<h3>Inspect a connection</h3><p>Select a name or line to trace its evidence.</p>';}
  const edge=e.target.closest('[data-inspect-edge]')?.dataset.inspectEdge;if(edge)selectEdge(edge);const focus=e.target.closest('[data-focus]')?.dataset.focus;if(focus){const p=new URLSearchParams(params);p.set('focus',focus);p.delete('q');location.hash='map?'+p;}
 });
 positions();fit();if(!graph.nodes.length)inspector.innerHTML='<h3>No matching connections</h3><p>Clear filters or search for a different name.</p>';
}
