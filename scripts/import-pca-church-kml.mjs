#!/usr/bin/env node

/**
 * Import the PCA Administrative Committee's BatchGeo KML church map.
 *
 * Usage:
 *   node scripts/import-pca-church-kml.mjs /path/to/pca-churches.kml [output-dir]
 *
 * Default output directory:
 *   sources/normalized/church-directory
 *
 * This importer is intentionally conservative. It parses every Placemark and
 * reports likely duplicates, but it does NOT silently merge churches. Every
 * placemark becomes a provisional church entity with a stable source-derived ID.
 * Duplicate review/canonical merge is a separate stage.
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';

const [, , inputArg, outputArg] = process.argv;

if (!inputArg) {
  console.error('Usage: node scripts/import-pca-church-kml.mjs <pca-churches.kml> [output-dir]');
  process.exit(1);
}

const root = process.cwd();
const inputPath = path.resolve(inputArg);
const outputDir = path.resolve(outputArg || path.join(root, 'sources', 'normalized', 'church-directory'));
const presbyteriesPath = path.join(root, 'data', 'presbyteries.json');
const churchesPath = path.join(root, 'data', 'churches.json');

if (!fs.existsSync(inputPath)) {
  console.error(`Input file not found: ${inputPath}`);
  process.exit(1);
}

fs.mkdirSync(outputDir, { recursive: true });

const xml = fs.readFileSync(inputPath, 'utf8');
const sha256 = crypto.createHash('sha256').update(xml).digest('hex');
const presbyteries = JSON.parse(fs.readFileSync(presbyteriesPath, 'utf8'));

const normalize = (value = '') => value
  .toLowerCase()
  .replace(/&amp;/g, '&')
  .replace(/[^a-z0-9]+/g, ' ')
  .trim();

const slug = (value = '') => normalize(value).replace(/\s+/g, '-').slice(0, 64) || 'church';

const decodeXml = (value = '') => value
  .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
  .replace(/&amp;/g, '&')
  .replace(/&lt;/g, '<')
  .replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'")
  .trim();

const presbyteryByNormalizedName = new Map(
  presbyteries.map((p) => [normalize(p.name.replace(/ Presbytery$/i, '')), p.id])
);

const placemarkMatches = [...xml.matchAll(/<Placemark>([\s\S]*?)<\/Placemark>/g)];
const records = [];

for (let index = 0; index < placemarkMatches.length; index += 1) {
  const block = placemarkMatches[index][1];
  const nameMatch = block.match(/<name>([\s\S]*?)<\/name>/);
  const addressMatch = block.match(/<address>([\s\S]*?)<\/address>/);
  const coordMatch = block.match(/<coordinates>\s*([^<]+?)\s*<\/coordinates>/);

  const fields = {};
  for (const dataMatch of block.matchAll(/<Data name=['"]([^'"]+)['"]>[\s\S]*?<value>([\s\S]*?)<\/value>[\s\S]*?<\/Data>/g)) {
    fields[decodeXml(dataMatch[1])] = decodeXml(dataMatch[2]);
  }

  const name = decodeXml(nameMatch?.[1] || '');
  if (!name) continue;

  const coordinates = (coordMatch?.[1] || '').split(',').map((v) => v.trim());
  const longitude = coordinates[0] ? Number(coordinates[0]) : null;
  const latitude = coordinates[1] ? Number(coordinates[1]) : null;
  const presbyteryAsPrinted = fields.Presbytery || '';
  const normalizedPresbytery = normalize(presbyteryAsPrinted.replace(/ Presbytery$/i, ''));
  const presbyteryId = presbyteryByNormalizedName.get(normalizedPresbytery) || null;
  const website = fields['Church Website'] || '';
  const address = decodeXml(addressMatch?.[1] || '');

  const sourceFingerprint = [
    normalize(name),
    normalize(presbyteryAsPrinted),
    normalize(website),
    normalize(fields['Church EMail'] || ''),
    normalize(fields['Church Phone'] || ''),
    normalize(fields.Pastor || ''),
    normalize(address),
  ].join('|');

  const sourceId = crypto.createHash('sha1').update(sourceFingerprint).digest('hex').slice(0, 10);
  const sourceRecordId = `batchgeo-${sourceId}`;

  records.push({
    source_index: index + 1,
    source_record_id: sourceRecordId,
    provisional_church_id: `${slug(name)}-${sourceId.slice(0, 6)}`,
    name,
    address_full: address || null,
    address_2: fields['Address 2'] || null,
    country_as_printed: fields.Country || null,
    phone: fields['Church Phone'] || null,
    email: fields['Church EMail'] || null,
    website: website || null,
    pastor_as_printed: fields.Pastor || null,
    presbytery_as_printed: presbyteryAsPrinted || null,
    presbytery_id: presbyteryId,
    type_org: fields['Type Org'] || null,
    latitude: Number.isFinite(latitude) ? latitude : null,
    longitude: Number.isFinite(longitude) ? longitude : null,
    extra_fields: Object.fromEntries(
      Object.entries(fields).filter(([key]) => ![
        'Address 2', 'Country', 'Church Phone', 'Church EMail', 'Church Website',
        'Pastor', 'Presbytery', 'Type Org'
      ].includes(key))
    ),
  });
}

// Strong duplicate candidates: same normalized name, website, presbytery and pastor.
// These are REVIEW FLAGS, not automatic merges.
const duplicateGroups = new Map();
for (const record of records) {
  const key = [
    normalize(record.name),
    normalize(record.website || ''),
    normalize(record.presbytery_as_printed || ''),
    normalize(record.pastor_as_printed || ''),
  ].join('|');
  if (!duplicateGroups.has(key)) duplicateGroups.set(key, []);
  duplicateGroups.get(key).push(record.source_record_id);
}

const possibleDuplicates = [...duplicateGroups.entries()]
  .filter(([, ids]) => ids.length > 1)
  .map(([key, source_record_ids]) => ({ key, source_record_ids }));

const duplicateRecordIds = new Set(possibleDuplicates.flatMap((group) => group.source_record_ids));
const unresolvedPresbyteries = [...new Set(
  records.filter((r) => r.presbytery_as_printed && !r.presbytery_id).map((r) => r.presbytery_as_printed)
)].sort();

const metadata = {
  source: {
    title: 'PCA Churches — BatchGeo KML export',
    map_url: 'https://batchgeo.com/map/fed353c376144b1fed2f5e29150c2531',
    kml_url: 'https://batchgeo.com/map/kml/fed353c376144b1fed2f5e29150c2531',
    pca_directory_url: 'https://www.pcaac.org/church-directory/',
    directory_database_date: '2026-08-31',
    imported_at: new Date().toISOString(),
    input_filename: path.basename(inputPath),
    sha256,
  },
  counts: {
    placemarks_parsed: records.length,
    possible_duplicate_groups: possibleDuplicates.length,
    unresolved_presbytery_names: unresolvedPresbyteries.length,
  },
  rules: {
    creates_person_nodes_from_pastor_field: false,
    automatically_merges_duplicate_candidates: false,
    provisional_entity_per_placemark: true,
    canonical_merge_review_required: true,
  },
};

const rawOutput = path.join(outputDir, 'pca-church-map-raw.json');
const duplicateOutput = path.join(outputDir, 'possible-duplicates.json');
const metadataOutput = path.join(outputDir, 'import-metadata.json');

fs.writeFileSync(rawOutput, JSON.stringify(records, null, 2) + '\n');
fs.writeFileSync(duplicateOutput, JSON.stringify(possibleDuplicates, null, 2) + '\n');
fs.writeFileSync(metadataOutput, JSON.stringify({ ...metadata, unresolved_presbyteries: unresolvedPresbyteries }, null, 2) + '\n');

const churches = records.map((record) => ({
  id: record.provisional_church_id,
  name: record.name,
  type: record.type_org || 'Church',
  status: 'current_directory_2026_08_31',
  presbytery_id: record.presbytery_id,
  presbytery_as_printed: record.presbytery_as_printed,
  address_full: record.address_full,
  phone: record.phone,
  email: record.email,
  website: record.website,
  latitude: record.latitude,
  longitude: record.longitude,
  pastor_as_printed: record.pastor_as_printed,
  source_record_id: record.source_record_id,
  source_snapshot: 'pca-batchgeo-kml-2026-09-03',
  duplicate_review_required: duplicateRecordIds.has(record.source_record_id),
  canonical_status: duplicateRecordIds.has(record.source_record_id) ? 'provisional_duplicate_review' : 'provisional_unique',
}));

fs.writeFileSync(churchesPath, JSON.stringify(churches, null, 2) + '\n');

console.log(`Parsed ${records.length} KML placemarks.`);
console.log(`Flagged ${possibleDuplicates.length} possible duplicate group(s).`);
console.log(`Unresolved presbytery names: ${unresolvedPresbyteries.length}.`);
console.log(`Wrote:\n- ${rawOutput}\n- ${duplicateOutput}\n- ${metadataOutput}\n- ${churchesPath}`);
