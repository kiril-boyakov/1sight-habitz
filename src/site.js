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
const filmToggle=document.querySelector('.video-toggle');
if(hero&&film&&filmToggle){
 film.muted=true;film.defaultMuted=true;
 const icon=(playing)=>{filmToggle.classList.toggle('is-paused',!playing);filmToggle.setAttribute('aria-pressed',String(playing));filmToggle.setAttribute('aria-label',playing?filmToggle.dataset.pause:filmToggle.dataset.play)};
 const play=async()=>{if(!film.getAttribute('src'))film.src=film.dataset.src;try{await film.play()}catch{hero.classList.remove('has-video');icon(false)}};
 film.addEventListener('playing',()=>{hero.classList.add('has-video');icon(true)});
 film.addEventListener('pause',()=>icon(false));
 film.addEventListener('error',()=>{hero.classList.remove('has-video');icon(false)});
 filmToggle.addEventListener('click',()=>{if(film.paused)play();else film.pause()});
 const preference=()=>{filmToggle.hidden=reduced.matches;if(reduced.matches){film.pause();hero.classList.remove('has-video')}else if(!navigator.connection?.saveData)play()};
 reduced.addEventListener?.('change',preference);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)film.pause()});
 preference();
 if('IntersectionObserver'in window)new IntersectionObserver(([entry])=>{if(!entry.isIntersecting)film.pause()},{threshold:0}).observe(hero);
}
const mobileActions=document.querySelector('.mobile-actions');
if(hero&&mobileActions&&'IntersectionObserver'in window)new IntersectionObserver(([e])=>mobileActions.classList.toggle('hidden',e.isIntersecting),{threshold:.15}).observe(hero);
const categoryLinks=[...document.querySelectorAll('.category-links a')];
const sections=[...document.querySelectorAll('.menu-section')];
const categoryNav=document.querySelector('.category-nav');
const search=document.querySelector('#dish-search');
const clearSearch=document.querySelector('.clear-search');
const resultStatus=document.querySelector('.menu-results');
function setCategory(id){
 for(const a of categoryLinks){const active=a.hash==='#'+id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')}
}
const menuOffset=()=>categoryNav?categoryNav.getBoundingClientRect().height+24:115;
if(sections.length){
 const measure=()=>document.documentElement.style.scrollPaddingTop=menuOffset()+'px';
 measure();if('ResizeObserver'in window)new ResizeObserver(measure).observe(categoryNav);
 const update=()=>{const visible=sections.filter(s=>!s.hidden);const active=visible.filter(s=>s.getBoundingClientRect().top<=menuOffset()+5).at(-1)||visible[0];setCategory(active?.id)};
 let scheduled=false;addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{update();scheduled=false})}},{passive:true});
 for(const a of categoryLinks)a.addEventListener('click',e=>{e.preventDefault();if(search?.value){search.value='';filterMenu()}const section=document.getElementById(a.hash.slice(1));history.pushState(null,'',a.hash);section.scrollIntoView({behavior:'instant',block:'start'});setCategory(section.id);const heading=section.querySelector('h2');if(e.detail===0){heading.tabIndex=-1;heading.focus({preventScroll:true})}if(!reduced.matches)section.animate([{opacity:.45},{opacity:1}],{duration:320,easing:'ease-out'})});
 const normalized=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();
 function filterMenu(){
  const query=normalized(search.value.trim());let count=0;
  for(const section of sections){let sectionCount=0;for(const dish of section.querySelectorAll('.dish')){const match=normalized(dish.textContent).includes(query);dish.hidden=!match;if(match)sectionCount++}section.hidden=sectionCount===0;count+=sectionCount}
  clearSearch.hidden=!query;resultStatus.textContent=query?(count?resultStatus.dataset.count+' '+count:resultStatus.dataset.empty):'';update();
 }
 if(search){search.closest('.menu-search').hidden=false;search.addEventListener('input',filterMenu);search.addEventListener('keydown',e=>{if(e.key==='Escape'){search.value='';filterMenu()}});clearSearch.addEventListener('click',()=>{search.value='';filterMenu();search.focus()})}
 document.fonts?.ready.then(update);addEventListener('resize',update,{passive:true});update();
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
