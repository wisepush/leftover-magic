window.renderResults = function(recipes){
  const grid = document.getElementById('grid');
  if (!recipes.length){ grid.innerHTML = '<p>No results yet.</p>'; return; }
  grid.innerHTML = recipes.map(r => `
    <a class="card link" href="/recipe.html?id=${r.id}">
      <div class="card-title">${r.title}</div>
      <div class="card-sub">${r.why_it_works}</div>
      <div class="card-missing">${r.missing && r.missing.length ? 'Missing: ' + r.missing.join(', ') : '&nbsp;'}</div>
    </a>
  `).join('');
};