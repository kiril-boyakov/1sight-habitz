function setFragment(hash, replace = false) {
 try { history[replace ? 'replaceState' : 'pushState'](null, '', hash); } catch { /* File previews can block history changes. */ }
}
const dialog=document.querySelector('#mobile-navigation');
const toggle=document.querySelector('.menu-toggle');
if(dialog&&toggle){
 const close=()=>{dialog.close();document.body.classList.remove('locked');toggle.setAttribute('aria-expanded','false');toggle.focus({preventScroll:true})};
 toggle.addEventListener('click',()=>{dialog.showModal();document.body.classList.add('locked');toggle.setAttribute('aria-expanded','true');dialog.querySelector('.close-nav').focus()});
 dialog.querySelector('.close-nav').addEventListener('click',close);
 dialog.addEventListener('cancel',e=>{e.preventDefault();close()});
 dialog.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{dialog.close();document.body.classList.remove('locked');toggle.setAttribute('aria-expanded','false')}));
}
for(const a of document.querySelectorAll('[data-language]'))a.addEventListener('click',()=>{a.href=a.dataset.language+(location.hash||'')});
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
if('IntersectionObserver'in window&&!reduced.matches){
 const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('waiting');observer.unobserve(e.target)}}),{threshold:.08});
 document.querySelectorAll('.scene-large,.reveal').forEach(el=>{el.classList.add('waiting');observer.observe(el)});
}
const hero=document.querySelector('.hero');
const film=document.querySelector('.hero-film');
if (hero && film) {
 film.muted = true;
 film.defaultMuted = true;
 let heroVisible = true;
 const play = async () => {
  if (!film.getAttribute('src')) film.src = film.dataset.src;
  try { await film.play(); } catch { hero.classList.remove('has-video'); }
 };
 film.addEventListener('playing', () => hero.classList.add('has-video'));
 film.addEventListener('error', () => hero.classList.remove('has-video'));
 const updatePlayback = () => {
  if (document.hidden || !heroVisible || reduced.matches || navigator.connection?.saveData) film.pause();
  else play();
 };
 reduced.addEventListener?.('change', updatePlayback);
 document.addEventListener('visibilitychange', updatePlayback);
 if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {
  heroVisible = entry.isIntersecting;
  updatePlayback();
 }, {threshold: 0}).observe(hero);
 updatePlayback();
}
const mobileActions=document.querySelector('.mobile-actions');
if(hero&&mobileActions&&'IntersectionObserver'in window)new IntersectionObserver(([e])=>mobileActions.classList.toggle('hidden',e.isIntersecting),{threshold:.15}).observe(hero);
const categoryLinks=[...document.querySelectorAll('.category-links a')];
const sections=[...document.querySelectorAll('.menu-section')];
const categoryNav=document.querySelector('.category-nav');
function setCategory(id){
 for(const a of categoryLinks){const active=a.hash==='#'+id;const changed=active&&!a.classList.contains('active');a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');if(changed){const row=a.parentElement,box=row.getBoundingClientRect(),item=a.getBoundingClientRect();if(item.left<box.left)row.scrollBy({left:item.left-box.left-2,behavior:'instant'});else if(item.right>box.right)row.scrollBy({left:item.right-box.right+2,behavior:'instant'})}}
}
const menuOffset=()=>categoryNav?categoryNav.getBoundingClientRect().height+24:115;
if(sections.length){
 const measure=()=>document.documentElement.style.scrollPaddingTop=menuOffset()+'px';
 measure();if('ResizeObserver'in window)new ResizeObserver(measure).observe(categoryNav);
 const update=()=>{const visible=sections.filter(s=>!s.hidden);const active=visible.filter(s=>s.getBoundingClientRect().top<=menuOffset()+5).at(-1)||visible[0];setCategory(active?.id)};
 let scheduled=false;addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{update();scheduled=false})}},{passive:true});
 for(const a of categoryLinks)a.addEventListener('click',e=>{e.preventDefault();const section=document.getElementById(a.hash.slice(1));setFragment(a.hash);section.scrollIntoView({behavior:'instant',block:'start'});setCategory(section.id);const heading=section.querySelector('h2');if(e.detail===0){heading.tabIndex=-1;heading.focus({preventScroll:true})}if(!reduced.matches)section.animate([{opacity:.45},{opacity:1}],{duration:320,easing:'ease-out'})});
 const followHash=()=>{const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target)target.scrollIntoView({behavior:'instant',block:'start'});update()};
 if(document.fonts)document.fonts.ready.then(followHash);else followHash();addEventListener('hashchange',followHash);addEventListener('resize',update,{passive:true});update();
}

// Scroll is always native. Only the visible photographs respond to its position.
const drifts=[...document.querySelectorAll('[data-drift]')];
const expandingScene=document.querySelector('[data-scroll-scene]');
const eveningScene=document.querySelector('[data-evening]');
const motionScenes=[...drifts,expandingScene,eveningScene].filter(Boolean);
if(motionScenes.length&&'IntersectionObserver'in window){
 const active=new Set();let frame=0;
 const clamp=x=>Math.max(0,Math.min(1,x));
 const draw=()=>{frame=0;if(reduced.matches)return;const vh=innerHeight;
  for(const el of active){const r=el.getBoundingClientRect();const progress=clamp((vh-r.top)/(vh+r.height));
   if(el.hasAttribute('data-drift'))el.style.setProperty('--drift-y',(-Number(el.dataset.drift)*(.2+.8*progress))+'px');
   if(el===expandingScene){const entry=clamp((vh-r.top)/(vh*.9));el.style.setProperty('--scene-inset',(8*(1-entry))+'%');el.style.setProperty('--scene-scale',String(1.14-.14*entry))}
   if(el===eveningScene){const entry=clamp((vh-r.top)/(vh*.85));el.style.setProperty('--evening-inset',(14*(1-entry))+'%');el.style.setProperty('--evening-y',(30*(1-entry))+'px')}
  }
 };
 const schedule=()=>{if(!frame&&!reduced.matches)frame=requestAnimationFrame(draw)};
 const motionObserver=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting)active.add(entry.target);else active.delete(entry.target)}schedule()},{rootMargin:'100px'});
 motionScenes.forEach(el=>motionObserver.observe(el));addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});reduced.addEventListener?.('change',()=>{if(reduced.matches){if(frame)cancelAnimationFrame(frame);frame=0;for(const el of motionScenes)for(const key of ['--drift-y','--scene-inset','--scene-scale','--evening-inset','--evening-y'])el.style.removeProperty(key)}else schedule()});
}

const pathButtons = [...document.querySelectorAll('[data-path]')];
if (pathButtons.length) {
  function selectPath(key, animate = false) {
    const selected = pathButtons.find(button => button.dataset.path === key) || pathButtons[0];
    for (const button of pathButtons) {
      const active = button === selected;
      document.getElementById(button.getAttribute('aria-controls')).hidden = !active;
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
    }
    if (animate && !reduced.matches) {
      const panel = document.getElementById(selected.getAttribute('aria-controls'));
      panel.querySelectorAll('.instant-photo figure').forEach((figure, index) => {
        figure.getAnimations().forEach(animation => animation.cancel());
        figure.animate([
          {opacity: 0, transform: 'translate3d(0,18px,0) scale(.98)'},
          {opacity: 1, transform: 'translate3d(0,0,0) scale(1)'}
        ], {duration: 600, delay: index * 65, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards'});
      });
    }
  }
  selectPath(location.hash.replace('#path-', ''));
  addEventListener('hashchange', () => {
    if (location.hash.startsWith('#path-')) selectPath(location.hash.slice(6));
  });
  pathButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
      selectPath(button.dataset.path, true);
      setFragment('#path-' + button.dataset.path, true);
    });
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % pathButtons.length;
      if (event.key === 'ArrowLeft') next = (index + pathButtons.length - 1) % pathButtons.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = pathButtons.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      pathButtons[next].focus();
      pathButtons[next].click();
    });
  });
}

for (const gallery of document.querySelectorAll('.instant-gallery')) {
  const wall = gallery.querySelector('.instant-wall');
  const updateControls = () => {
    if (!wall.clientWidth) return;
    gallery.querySelector('.gallery-arrows').hidden = wall.scrollWidth <= wall.clientWidth + 2;
    gallery.querySelector('[data-gallery-step="-1"]').disabled = wall.scrollLeft <= 1;
    gallery.querySelector('[data-gallery-step="1"]').disabled = wall.scrollLeft + wall.clientWidth >= wall.scrollWidth - 1;
  };
  wall.addEventListener('scroll', updateControls, {passive: true});
  if ('ResizeObserver' in window) new ResizeObserver(updateControls).observe(wall);
  updateControls();
  const scrollWall = direction => wall.scrollBy({
    left: direction * Math.max(230, wall.clientWidth * .75),
    behavior: reduced.matches ? 'instant' : 'smooth'
  });
  gallery.querySelectorAll('[data-gallery-step]').forEach(button => {
    button.addEventListener('click', () => scrollWall(Number(button.dataset.galleryStep)));
  });
  wall.addEventListener('keydown', event => {
    if (event.target !== wall || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    scrollWall(event.key === 'ArrowLeft' ? -1 : 1);
  });
}
