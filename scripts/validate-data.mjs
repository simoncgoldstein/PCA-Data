import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, 'data', `${name}.json`), 'utf8'));

const people = readJson('people');
const organizations = readJson('organizations');
const events = readJson('events');
const affiliations = readJson('affiliations');
const sources = readJson('sources');

const errors = [];

function indexById(items, label) {
  const map = new Map();
  for (const item of items) {
    if (!item.id) {
      errors.push(`${label}: record missing id`);
      continue;
    }
    if (map.has(item.id)) errors.push(`${label}: duplicate id ${item.id}`);
    map.set(item.id, item);
  }
  return map;
}

const personMap = indexById(people, 'people');
const organizationMap = indexById(organizations, 'organizations');
const eventMap = indexById(events, 'events');
const sourceMap = indexById(sources, 'sources');
indexById(affiliations, 'affiliations');

function checkSources(owner, sourceIds = []) {
  for (const sourceId of sourceIds) {
    if (!sourceMap.has(sourceId)) errors.push(`${owner}: unknown source_id ${sourceId}`);
  }
}

for (const person of people) {
  if (!person.name) errors.push(`people:${person.id}: missing name`);
  if (person.current_organization && !organizationMap.has(person.current_organization)) {
    errors.push(`people:${person.id}: unknown current_organization ${person.current_organization}`);
  }
  checkSources(`people:${person.id}`, person.current_role_source_ids);
}

for (const event of events) {
  if (!event.name) errors.push(`events:${event.id}: missing name`);
  if (event.organization_id && !organizationMap.has(event.organization_id)) {
    errors.push(`events:${event.id}: unknown organization_id ${event.organization_id}`);
  }
  checkSources(`events:${event.id}`, event.source_ids);
}

for (const affiliation of affiliations) {
  if (!personMap.has(affiliation.person_id)) {
    errors.push(`affiliations:${affiliation.id}: unknown person_id ${affiliation.person_id}`);
  }

  if (affiliation.target_type === 'organization' && !organizationMap.has(affiliation.target_id)) {
    errors.push(`affiliations:${affiliation.id}: unknown organization target ${affiliation.target_id}`);
  } else if (affiliation.target_type === 'event' && !eventMap.has(affiliation.target_id)) {
    errors.push(`affiliations:${affiliation.id}: unknown event target ${affiliation.target_id}`);
  } else if (affiliation.target_type === 'person' && !personMap.has(affiliation.target_id)) {
    errors.push(`affiliations:${affiliation.id}: unknown person target ${affiliation.target_id}`);
  } else if (!['organization', 'event', 'person'].includes(affiliation.target_type)) {
    errors.push(`affiliations:${affiliation.id}: unsupported target_type ${affiliation.target_type}`);
  }

  if (!affiliation.role) errors.push(`affiliations:${affiliation.id}: missing role`);
  if (!['confirmed', 'confirmed_for_2024', 'strongly_supported', 'associated', 'unresolved'].includes(affiliation.confidence)) {
    errors.push(`affiliations:${affiliation.id}: unsupported confidence ${affiliation.confidence}`);
  }
  if (typeof affiliation.weight !== 'number' || affiliation.weight < 0) {
    errors.push(`affiliations:${affiliation.id}: weight must be a nonnegative number`);
  }
  checkSources(`affiliations:${affiliation.id}`, affiliation.source_ids);
}

for (const source of sources) {
  if (!source.title) errors.push(`sources:${source.id}: missing title`);
  if (!source.url) errors.push(`sources:${source.id}: missing url`);
  if (source.url && !/^https:\/\//.test(source.url)) errors.push(`sources:${source.id}: URL must use https`);
}

if (errors.length) {
  console.error(`Validation failed with ${errors.length} error(s):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`Validated ${people.length} people, ${organizations.length} organizations, ${events.length} events, ${affiliations.length} affiliations, and ${sources.length} sources.`);
