// Self-check for the progression tools (Gear next, Next unlock, Checkup, Arcana, Rift/Abyss timers, Tonight's plan).
// Run: python3 -m http.server 8765 &  then  NODE_PATH=$(npm root -g) node check.js   (needs Playwright installed globally)
const { chromium } = require('playwright');
const assert = require('assert');
(async () => {
  const b = await chromium.launch(), p = await b.newPage(), errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.route(/workers\.dev|plaync|playnccdn/, r => r.fulfill({ status: 200, body: '{}' }));
  await p.addInitScript(() => localStorage.setItem('lpc-aion-tickets', JSON.stringify({
    a: { id: 60000001, left: 840, max: 840, at: Date.now() }, b: { id: 4, left: 14, max: 14, at: Date.now() }, c: { id: 101, left: 9, max: 14, at: Date.now() },
    d: { id: 1, left: 1, max: 7, at: Date.now() }, e: { id: 80000001, left: 2, max: 3, at: 1 } })));
  await p.goto('http://localhost:8765/#/today');
  await p.waitForFunction(() => LIST.length);
  const r = await p.evaluate(() => {
    const g = (slot, grade, e, max) => ({ slotPosName: slot, name: slot, grade, enchantLevel: e, max, slots: 0, stones: [], godSlots: 0, god: [] });
    const m = { name: 'T', il: 2700, history: [{ date: '2026-11-01', il: 2630 }, { date: '2026-11-08', il: 2700 }], gear: [
      g('Torso', 'Unique', 13, 15), g('Pants', 'Unique', 11, 15), g('Helmet', 'Unique', 7, 15), g('Boots', 'Legend', 5, 10),
      { ...g('Arcana1', 'Unique', 0, 5), name: 'Chalice of Vigor' }, { ...g('Arcana2', 'Rare', 1, 3), name: 'Bell of Magic' }, { ...g('Arcana3', 'Legend', 0, 4), name: 'Mirror of Vigor' }] };
    const t = Date.UTC(2026, 10, 7, 4, 10);  // Saturday 04:10 UTC
    return { t11: TRIES[11], t15: TRIES[15], to15: triesTo(13, 15), steps: gearSteps(m).map(s => s.text), arc: arcana(m), unlock: nextUnlock(m),
      rift: nextEvent(EVENTS[0], t).t - t, riftOpen: nextEvent(EVENTS[0], Date.UTC(2026, 10, 10, 22, 1)).last, kaira: nextEvent(EVENTS[1], t).t - t, nahma: new Date(nextEvent(EVENTS[2], t).t).toISOString(),
      argo: new Date(nextEvent(EVENTS[3], t).t).toISOString(), plan: planItems() };
  });
  // 65%, then 70% and so on: 1 + 0.35 + 0.35*0.3 + 0.35*0.3*0.25 + ... = 1.4874
  assert(Math.abs(r.t11 - 1.4874) < 1e-3, r.t11);
  assert(r.t15 > 3.3 && r.t15 < 3.5, r.t15);
  assert(Math.abs(r.to15 - (r.t15 + await p.evaluate(() => TRIES[14]))) < 1e-9);
  assert.deepStrictEqual(r.steps, ['Replace Boots (Legend) with a Unique', 'Helmet +7 → +10', 'Pants +11 → +12', 'Torso +13 → +14']);  // no enchant for the Boots being replaced
  assert.strictEqual(r.arc.set, 2); assert.strictEqual(r.arc.weak.name, 'Bell of Magic');
  assert(/Ludra Normal at item level 2,800/.test(r.unlock) && /about 10 days/.test(r.unlock), r.unlock);  // 100 to go at +10 a day
  assert.strictEqual(r.rift, 170 * 6e4); assert.strictEqual(r.riftOpen, Date.UTC(2026, 10, 10, 22));  // seen open 22:00 UTC assert.strictEqual(r.kaira, 170 * 6e4);
  assert.strictEqual(r.nahma, '2026-11-08T12:00:00.000Z'); assert.strictEqual(r.argo, '2026-11-07T12:30:00.000Z');
  assert(r.plan.caps.some(c => /^Odyle is full/.test(c)) && r.plan.caps.some(c => /^Nightmare 14 of 14: 2 lost/.test(c)), r.plan.caps);
  assert(!r.plan.caps.some(c => /Shugo/.test(c)));
  assert.strictEqual(r.plan.stale, 1);  // the Ascension trial count from long ago is left out
  assert(!r.plan.pace.some(c => /Ascension/.test(c)));
  assert(r.plan.pace.some(c => /^Daily dungeon: 9 left, [1-9] a day/.test(c)), r.plan.pace);
  assert(r.plan.soon.some(x => x.n === 'Shugo Festival') && r.plan.soon.some(x => x.n === 'Dimensional Invasion'));
  for (const h of ['#/member/' + encodeURIComponent(await p.evaluate(() => LIST[0].name)), '#/member/' + encodeURIComponent(await p.evaluate(() => LIST[0].name)) + '/gear', '#/today']) {
    await p.goto('http://localhost:8765/' + h); await p.waitForTimeout(300);
  }
  assert(await p.locator('text=Tonight’s plan').count());
  // Premade's overlay panels: every one there, each line text with no HTML left in it
  const prog = await p.evaluate(() => progPanels());
  assert.deepStrictEqual(prog.map(x => x.id).slice(-2), ['events', 'plan']);
  assert(prog.every(x => x.title && x.lines.length && x.lines.every(l => l.length === 3 && !/[<>]/.test(l[0] + l[1]))), JSON.stringify(prog));
  assert(prog.find(x => x.id === 'events').lines.some(l => /^Spacetime Rift (open now|in )/.test(l[0])));
  assert.deepStrictEqual(errs, []);
  console.log('progression check: ok');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
