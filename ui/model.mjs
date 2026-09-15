// Pure view-model helpers. Display filters never redefine canonical scores.
export const groups = {
  network: 'Network membership & leadership',
  action: 'Public coalition actions',
  denomination: 'Denominational actions',
  authored: 'Authored & attributable positions',
  committee: 'Committee service',
  institution: 'Institutional & geographic context',
  family: 'Family & collaboration context',
  other: 'Other documented evidence'
};
export function evidenceGroup(edge) {
  const k = edge.evidence_kind || '';
  if (k.startsWith('network_')) return 'network';
  if (['public_coalition_action', 'coalition_organizing'].includes(k)) return 'action';
  if (k.startsWith('general_assembly_') || k === 'formal_dissent_author') return 'denomination';
  if (k.includes('authored') || k === 'attributable_position') return 'authored';
  if (k.includes('committee')) return 'committee';
  if (['family_relationship', 'collaboration'].includes(k)) return 'family';
  if (k.startsWith('current_') || k === 'geographic_affiliation') return 'institution';
  return 'other';
}
export function included(edge) {
  return edge.score_included === true && edge.confidence !== 'unresolved';
}
export function canonicalScore(personId, affiliations) {
  return affiliations.filter(e => e.person_id === personId && included(e))
    .reduce((sum, e) => sum + Number(e.weight || 0), 0);
}
export function visibleEvidence(edges, confidence = 'all', group = 'all') {
  return edges.filter(e => (confidence === 'all' || e.confidence === confidence ||
    (confidence === 'confirmed' && e.confidence === 'confirmed_for_2024')) &&
    (group === 'all' || evidenceGroup(e) === group));
}
export function peopleRows(people, affiliations, {confidence = 'all', query = '', sort = 'name'} = {}) {
  const q = query.trim().toLowerCase();
  const rows = people.map(person => {
    const all = affiliations.filter(e => e.person_id === person.id);
    return {person, evidence: visibleEvidence(all, confidence), score: canonicalScore(person.id, affiliations)};
  }).filter(r => (!q || [r.person.name, r.person.current_role, r.person.denominational_status].join(' ').toLowerCase().includes(q)) &&
    (confidence === 'all' || r.evidence.length));
  return rows.sort((a,b) => (sort === 'score' ? b.score - a.score : 0) || a.person.name.localeCompare(b.person.name));
}
export function safeUrl(value) {
  if (!value) return null;
  try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : null; }
  catch { return null; }
}
export function percent(numerator, denominator) {
  return denominator ? `${(100 * numerator / denominator).toFixed(2)}%` : 'Not available';
}
export function parseRoute(hash) {
  // Keep links from the original scaffold working.
  if (hash.startsWith('#person=')) return {view:'person', id:decodeURIComponent(hash.slice(8)), params:new URLSearchParams()};
  const [path, query = ''] = hash.replace(/^#\/?/, '').split('?');
  const [view = 'overview', id] = path.split('/');
  return {view: view || 'overview', id: id ? decodeURIComponent(id) : null, params: new URLSearchParams(query)};
}
