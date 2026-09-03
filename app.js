const state = {
  people: [],
  organizations: [],
  events: [],
  affiliations: [],
  sources: [],
  view: 'people'
};

const confidenceRank = {
  confirmed: 4,
  confirmed_for_2024: 4,
  strongly_supported: 3,
  associated: 2,
  unresolved: 1
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function esc(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function byId(items, id) {
  return items.find((item) => item.id === id);
}

function targetName(affiliation) {
  if (affiliation.target_type === 'organization') {
    return byId(state.organizations, affiliation.target_id)?.name ?? affiliation.target_id;
  }
  if (affiliation.target_type === 'event') {
    return byId(state.events, affiliation.target_id)?.name ?? affiliation.target_id;
  }
  if (affiliation.target_type === 'person') {
    return byId(state.people, affiliation.target_id)?.name ?? affiliation.target_id;
  }
  return affiliation.target_id;
}

function organizationName(id) {
  return byId(state.organizations, id)?.name ?? null;
}

function affiliationsFor(personId) {
  return state.affiliations.filter((item) => item.person_id === personId);
}

function scoreFor(personId, affiliations = affiliationsFor(personId)) {
  return affiliations
    .filter((item) => item.score_included)
    .reduce((sum, item) => sum + Number(item.weight || 0), 0);
}

function confidenceLabel(value) {
  return {
    confirmed: 'Confirmed',
    confirmed_for_2024: 'Confirmed for 2024',
    strongly_supported: 'Strongly supported',
    associated: 'Associated',
    unresolved: 'Unresolved'
  }[value] ?? value;
}

function chipClass(value) {
  if (value === 'confirmed_for_2024') return 'confirmed';
  return value || 'associated';
}

function sourceLinks(sourceIds = []) {
  return sourceIds
    .map((sourceId) => byId(state.sources, sourceId))
    .filter(Boolean)
    .map((source) => `<a href="${esc(source.url)}" target="_blank" rel="noopener">${esc(source.title)}</a>`)
    .join('');
}

function connectionOptionLabel(affiliation) {
  if (affiliation.target_type === 'event') {
    const event = byId(state.events, affiliation.target_id);
    if (event?.organization_id) return organizationName(event.organization_id) ?? event.name;
    return event?.name ?? affiliation.target_id;
  }
  return targetName(affiliation);
}

function populateConnectionFilter() {
  const select = $('#connection-filter');
  const values = new Map();
  state.affiliations.forEach((aff) => {
    const label = connectionOptionLabel(aff);
    const key = aff.target_type === 'event'
      ? (byId(state.events, aff.target_id)?.organization_id || aff.target_id)
      : aff.target_id;
    values.set(key, label);
  });

  [...values.entries()]
    .sort((a, b) => a[1].localeCompare(b[1]))
    .forEach(([value, label]) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = label;
      select.append(option);
    });
}

function affiliationMatchesConnection(affiliation, selected) {
  if (selected === 'all') return true;
  if (affiliation.target_id === selected) return true;
  if (affiliation.target_type === 'event') {
    return byId(state.events, affiliation.target_id)?.organization_id === selected;
  }
  return false;
}

function filterAffiliationsByConfidence(affiliations, filter) {
  if (filter === 'all') return affiliations;
  if (filter === 'confirmed') {
    return affiliations.filter((item) => confidenceRank[item.confidence] >= 4);
  }
  if (filter === 'strongly_supported') {
    return affiliations.filter((item) => confidenceRank[item.confidence] >= 3);
  }
  return affiliations;
}

function renderPeople() {
  const search = $('#people-search').value.trim().toLowerCase();
  const connection = $('#connection-filter').value;
  const confidence = $('#confidence-filter').value;
  const sort = $('#people-sort').value;

  let rows = state.people.map((person) => {
    const all = affiliationsFor(person.id);
    const evidence = filterAffiliationsByConfidence(all, confidence);
    return {
      person,
      all,
      evidence,
      score: scoreFor(person.id, evidence)
    };
  });

  if (search) {
    rows = rows.filter(({ person, all }) => {
      const haystack = [
        person.name,
        person.current_role,
        organizationName(person.current_organization),
        person.denominational_status,
        ...all.map((a) => targetName(a)),
        ...all.map((a) => a.role)
      ].filter(Boolean).join(' ').toLowerCase();
      return haystack.includes(search);
    });
  }

  if (connection !== 'all') {
    rows = rows.filter(({ evidence }) => evidence.some((a) => affiliationMatchesConnection(a, connection)));
  }

  if (sort === 'name-asc') rows.sort((a, b) => a.person.name.localeCompare(b.person.name));
  if (sort === 'connections-desc') rows.sort((a, b) => b.evidence.length - a.evidence.length || b.score - a.score || a.person.name.localeCompare(b.person.name));
  if (sort === 'score-desc') rows.sort((a, b) => b.score - a.score || b.evidence.length - a.evidence.length || a.person.name.localeCompare(b.person.name));

  const tbody = $('#people-table');
  tbody.innerHTML = rows.map(({ person, evidence, score }) => {
    const currentOrg = organizationName(person.current_organization);
    const keyEvidence = [...evidence]
      .sort((a, b) => Number(b.weight || 0) - Number(a.weight || 0))
      .slice(0, 4);

    return `<tr data-person-id="${esc(person.id)}" tabindex="0">
      <td>
        <strong>${esc(person.name)}</strong>
        <span class="subtle">${esc(person.ordination || 'Role normalization pending')}</span>
      </td>
      <td>
        ${person.current_role ? `<strong>${esc(person.current_role)}</strong>` : '<span class="subtle">Current role not yet normalized</span>'}
        ${currentOrg ? `<span class="subtle">${esc(currentOrg)}</span>` : ''}
      </td>
      <td><div class="chips">${keyEvidence.map((item) => `<span class="chip ${chipClass(item.confidence)}" title="${esc(confidenceLabel(item.confidence))}">${esc(targetName(item))}</span>`).join('')}</div></td>
      <td class="number">${evidence.length}</td>
      <td class="number"><span class="score">${score}</span></td>
    </tr>`;
  }).join('');

  $('#people-empty').hidden = rows.length !== 0;
  tbody.querySelectorAll('tr').forEach((row) => {
    const open = () => openPerson(row.dataset.personId);
    row.addEventListener('click', open);
    row.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        open();
      }
    });
  });
}

function openPerson(personId) {
  const person = byId(state.people, personId);
  if (!person) return;
  const affiliations = affiliationsFor(personId)
    .sort((a, b) => Number(b.weight || 0) - Number(a.weight || 0));
  const score = scoreFor(personId);

  $('#dialog-name').textContent = person.name;
  $('#dialog-body').innerHTML = `
    <div class="profile-summary">
      <div><span>Current role</span>${esc(person.current_role || 'Not yet normalized')}</div>
      <div><span>Current organization</span>${esc(organizationName(person.current_organization) || 'Not yet normalized')}</div>
      <div><span>Denominational status</span>${esc(person.denominational_status || 'Not yet normalized')}</div>
      <div><span>Network involvement index</span><strong>${score}</strong></div>
    </div>

    <p class="eyebrow">Evidence connections</p>
    <div class="evidence-list">
      ${affiliations.length ? affiliations.map((item) => `
        <article class="evidence-item">
          <div class="evidence-top">
            <div>
              <strong>${esc(targetName(item))}</strong>
              <div class="subtle">${esc(item.role)}</div>
            </div>
            <span class="chip ${chipClass(item.confidence)}">${esc(confidenceLabel(item.confidence))}</span>
          </div>
          ${item.notes ? `<p>${esc(item.notes)}</p>` : ''}
          <div class="source-links">${sourceLinks(item.source_ids)}</div>
        </article>
      `).join('') : '<p class="empty">No normalized evidence connections yet.</p>'}
    </div>

    ${person.current_role_source_ids?.length ? `
      <p class="eyebrow" style="margin-top:28px">Current-role sources</p>
      <div class="source-links">${sourceLinks(person.current_role_source_ids)}</div>
    ` : ''}
  `;

  const dialog = $('#person-dialog');
  dialog.showModal();
  history.replaceState(null, '', `#person=${encodeURIComponent(person.id)}`);
}

function renderNetworks() {
  const grid = $('#network-grid');
  const organizations = state.organizations.filter((org) => ['network', 'movement', 'public_coalition', 'pca_agency', 'external_network', 'external_nonprofit'].includes(org.type));

  grid.innerHTML = organizations.map((org) => {
    const eventIds = state.events.filter((evt) => evt.organization_id === org.id).map((evt) => evt.id);
    const peopleIds = new Set(
      state.affiliations
        .filter((aff) => aff.target_id === org.id || eventIds.includes(aff.target_id))
        .map((aff) => aff.person_id)
    );
    return `<article class="card">
      <h3>${esc(org.name)}</h3>
      <div class="meta">${esc(org.type.replaceAll('_', ' '))}${org.status ? ` · ${esc(org.status.replaceAll('_', ' '))}` : ''}</div>
      <p>${esc(org.description || 'Institutional node in the research graph.')}</p>
      <div class="count">${peopleIds.size} normalized people connected</div>
    </article>`;
  }).join('');
}

function renderTimeline() {
  const timeline = $('#timeline');
  const events = [...state.events].sort((a, b) => {
    const av = a.date || String(a.year || a.start_year || '9999');
    const bv = b.date || String(b.year || b.start_year || '9999');
    return av.localeCompare(bv);
  });

  timeline.innerHTML = events.map((event) => {
    const year = event.date || event.year || (event.end_year ? `${event.start_year}–${event.end_year}` : event.start_year);
    const participantCount = new Set(state.affiliations.filter((aff) => aff.target_type === 'event' && aff.target_id === event.id).map((aff) => aff.person_id)).size;
    return `<article class="timeline-item">
      <div class="timeline-year">${esc(year)}</div>
      <h3>${esc(event.name)}</h3>
      <p>${esc(event.notes || `${participantCount} normalized participant${participantCount === 1 ? '' : 's'} currently represented in the dataset.`)}</p>
      <div class="source-links">${sourceLinks(event.source_ids)}</div>
    </article>`;
  }).join('');
}

function renderSources() {
  $('#source-list').innerHTML = state.sources.map((source) => `
    <article class="source-item">
      <div>
        <div class="source-type">${esc(source.source_type.replaceAll('_', ' '))}</div>
        <strong>${esc(source.title)}</strong>
        <p>${esc(source.publisher)}${source.date ? ` · ${esc(source.date)}` : ''}${source.notes ? ` · ${esc(source.notes)}` : ''}</p>
      </div>
      <div><a href="${esc(source.url)}" target="_blank" rel="noopener">Open source ↗</a></div>
    </article>
  `).join('');
}

function renderMetrics() {
  $('#metric-people').textContent = state.people.length;
  $('#metric-affiliations').textContent = state.affiliations.length;
  $('#metric-organizations').textContent = state.organizations.length;
  $('#metric-sources').textContent = state.sources.length;
}

function showView(view) {
  state.view = view;
  $$('.view').forEach((section) => {
    const active = section.id === `view-${view}`;
    section.hidden = !active;
    section.classList.toggle('active-view', active);
  });
  $$('.nav-link').forEach((button) => button.classList.toggle('active', button.dataset.view === view));
  if (!location.hash.startsWith('#person=')) history.replaceState(null, '', `#${view}`);
}

function bindControls() {
  ['#people-search', '#connection-filter', '#confidence-filter', '#people-sort'].forEach((selector) => {
    $(selector).addEventListener(selector === '#people-search' ? 'input' : 'change', renderPeople);
  });

  $$('.nav-link').forEach((button) => button.addEventListener('click', () => showView(button.dataset.view)));

  $('#dialog-close').addEventListener('click', () => $('#person-dialog').close());
  $('#person-dialog').addEventListener('close', () => {
    if (location.hash.startsWith('#person=')) history.replaceState(null, '', '#people');
  });
}

async function loadData() {
  const paths = ['people', 'organizations', 'events', 'affiliations', 'sources'];
  const payloads = await Promise.all(paths.map(async (name) => {
    const response = await fetch(`data/${name}.json`);
    if (!response.ok) throw new Error(`Could not load data/${name}.json (${response.status})`);
    return response.json();
  }));
  paths.forEach((name, index) => { state[name] = payloads[index]; });
}

async function init() {
  try {
    await loadData();
    renderMetrics();
    populateConnectionFilter();
    renderPeople();
    renderNetworks();
    renderTimeline();
    renderSources();
    bindControls();

    if (location.hash.startsWith('#person=')) {
      const id = decodeURIComponent(location.hash.slice('#person='.length));
      openPerson(id);
    } else if (['#networks', '#timeline', '#sources'].includes(location.hash)) {
      showView(location.hash.slice(1));
    }
  } catch (error) {
    console.error(error);
    document.querySelector('main').innerHTML = `<section class="shell view"><h2>Data could not be loaded</h2><p>${esc(error.message)}</p><p>This site must be served over HTTP, such as through GitHub Pages.</p></section>`;
  }
}

init();
