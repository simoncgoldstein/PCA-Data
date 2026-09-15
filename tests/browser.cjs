// End-to-end acceptance, run in CI with an isolated headless browser.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const out=process.env.UI_ARTIFACTS||'ui-artifacts';
fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1050}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.UI_BASE_URL||'http://127.0.0.1:8765/';
 const check=async(hash,heading)=>{await page.goto(base+'#'+hash);await page.locator('main[aria-busy]').waitFor({state:'detached'});await page.locator('h1').waitFor();if(heading)assert.match(await page.locator('h1').innerText(),heading);assert.ok(!(await page.locator('h1').innerText()).includes('could not'));};
 const text=()=>page.locator('main').innerText();
 await check('overview',/Follow the evidence/);await page.getByRole('link',{name:'Skip to content'}).focus();await page.keyboard.press('Enter');assert.equal(await page.locator('main').evaluate(el=>el===document.activeElement),true);assert.match(await page.locator('h1').innerText(),/Follow the evidence/);await page.screenshot({path:path.join(out,'overview-desktop.png'),fullPage:true});
 await check('person/mike-khandjian',/Mike Khandjian/);assert.match(await text(),/Participant \/ recruiter/);assert.match(await text(),/independent group/);assert.match(await text(),/Chapelgate/);const score=await page.locator('[data-canonical-score]').innerText();
 await page.getByRole('combobox',{name:'Confidence',exact:true}).selectOption('confirmed');await page.getByRole('button',{name:'Apply',exact:true}).click();await page.waitForURL(/confidence=confirmed/);assert.equal(await page.locator('[data-canonical-score]').innerText(),score);assert.match(await text(),/Index unchanged/);
 await check('person/david-cassidy',/David Cassidy/);assert.match(await text(),/membership is not established/);assert.match(await text(),/McGowan/);assert.match(await text(),/Spanish River/);
 await check('person/jeffrey-choi',/Jeffrey Choi/);assert.match(await text(),/Pacific Presbytery/);assert.match(await text(),/Co-author and submitter/);assert.match(await text(),/local-session discretion/);await page.screenshot({path:path.join(out,'choi-desktop.png'),fullPage:true});
 await check('person/kathy-keller',/Kathy Keller/);assert.equal(await page.locator('[data-canonical-score]').innerText(),'0');assert.match(await text(),/Spouse/);assert.match(await text(),/male-only authoritative/);
 await check('person/tim-keller',/Tim Keller/);assert.equal(await page.locator('[data-canonical-score]').innerText(),'0');assert.equal(await page.locator('#positions').count(),0);
 await check('person/hansoo-jin?section=occurrences',/Hansoo Jin/);assert.match(await text(),/Korean Capitol/);
 await check('person/james-kessler',/James Kessler/);assert.match(await text(),/Founder \/ principal organizer/);assert.match(await text(),/Included · weight 5/);
 for(const [n,total,linked]of[[1,60,25],[2,21,21]]){
  await check('event/evt-garris-letter-'+n,/public letter/);assert.equal(await page.locator('[data-roster] tbody > tr').count(),total);assert.equal(await page.locator('[data-roster] tbody > tr[data-identity="resolved"]').count(),linked);
 }
 await check('dataset/garris_letter_1?q=Jeff+White');assert.equal(await page.locator('[data-roster] tbody > tr').count(),1);assert.match(await text(),/New City Fellowship/);assert.match(await text(),/Identity unresolved/);assert.equal(await page.locator('[data-roster] a[href="#person/jeff-white-redeemer-downtown"]').count(),0);
 await check('analysis',/Overlap/);assert.match(await text(),/68 \/ 151/);assert.match(await text(),/Confirmed lower bound/);await page.screenshot({path:path.join(out,'analysis-desktop.png'),fullPage:true});
 await check('source/src-np-local-archive');assert.match(await text(),/Registered local\/archive provenance/);assert.equal(await page.locator('a[href=""]').count(),0);
 await check('map?q=Khandjian&depth=2',/Detective map/);await page.locator('[data-node]').first().waitFor();const svg=page.locator('.map-canvas svg');
 await page.screenshot({path:path.join(out,'map-desktop.png'),fullPage:true});
 const before=await svg.getAttribute('viewBox');await page.getByRole('button',{name:'Zoom in',exact:true}).click();assert.notEqual(await svg.getAttribute('viewBox'),before);
 const node=page.locator('[data-node="person:mike-khandjian"]');await node.press('Enter');assert.match(await page.locator('.map-inspector').innerText(),/Mike Khandjian/);
 await page.locator('[data-inspect-edge="aff-khandjian-np"]').click();assert.match(await page.locator('.map-inspector').innerText(),/Participant \/ recruiter/);assert.match(await page.locator('.map-inspector').innerText(),/weight 4/);
 await page.getByRole('button',{name:'Fit all',exact:true}).click();
 const bounds=await node.locator('circle').boundingBox();const prior=await node.getAttribute('transform');await page.mouse.move(bounds.x+bounds.width/2,bounds.y+bounds.height/2);await page.mouse.down();await page.mouse.move(bounds.x+70,bounds.y+30,{steps:8});await page.mouse.up();assert.notEqual(await node.getAttribute('transform'),prior);
 // Background panning and line inspection must work with pointer capture.
 const area=await svg.boundingBox();const old=await svg.getAttribute('viewBox');await page.mouse.move(area.x+12,area.y+12);await page.mouse.down();await page.mouse.move(area.x+80,area.y+65,{steps:5});await page.mouse.up();assert.notEqual(await svg.getAttribute('viewBox'),old);
 await check('map?layer=source&unresolved=show&focus=dataset:garris_letter_1');assert.equal(await page.locator('.map-node.occurrence').count(),35);assert.equal(await page.locator('.map-edge').count(),60);
 await page.locator('.map-edge').first().press('Enter');assert.match(await page.locator('.map-inspector').innerText(),/Source occurrence, excluded/);
 await check('map?q=not-a-real-name');assert.match(await page.locator('.map-inspector').innerText(),/No matching connections/);
 // Entity navigation and browser history.
 await check('organizations');await page.getByRole('link',{name:'Alliance for Mission & Renewal',exact:true}).click();await page.waitForURL(/#organization\/amr/);await page.goBack();await page.waitForURL(/#organizations/);
 await check('does-not-exist');assert.match(await text(),/not in the current index/);
 await page.setViewportSize({width:390,height:844});
 for(const [view,label]of[['overview','overview-mobile'],['event/evt-garris-letter-1','garris-mobile'],['map?q=Khandjian&depth=1','map-mobile']]){
  await check(view);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1));await page.screenshot({path:path.join(out,label+'.png'),fullPage:true});
 }
 assert.deepEqual(errors,[]);
 await browser.close();fs.writeFileSync(path.join(out,'acceptance.txt'),'All representative UI, graph, score/filter, mobile overflow, and navigation checks passed.\n');console.log('Browser acceptance passed.');
})().catch(e=>{console.error(e);process.exit(1);});
