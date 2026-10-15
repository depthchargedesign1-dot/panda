(function(){
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function esc(s){return String(s).replace(/[&<>"]/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]})}

  /* ---------- mobile menu ---------- */
  var top = document.querySelector('.top'), menuBtn = document.getElementById('menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', function(){
    var open = top.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menuBtn.textContent = open ? 'Close' : 'Menu';
  });

  /* ---------- home: storefront switcher ---------- */
  var sw = document.getElementById('switch');
  if (sw) {
    var SHOPS = [
      {k:'Shopify', c:'#43A047', url:'yourshop.co.uk', name:'Your Shop', pill:'Shopify store', head:'New season, now in', sub:'Free UK delivery over £40', p:['#FFB74D','#81C784','#64B5F6'], does:['Theme design','Product pages','Payments','Google channel']},
      {k:'BigCommerce', c:'#1E5BC6', url:'trade.yourshop.co.uk', name:'Your Shop Trade', pill:'BigCommerce', head:'Trade prices for account holders', sub:'2,400 products · bulk ordering', p:['#90CAF9','#B0BEC5','#FFCC80'], does:['Bulk import','Price lists','B2B accounts','Multi-channel']},
      {k:'WordPress', c:'#C2185B', url:'yourbusiness.co.uk', name:'Your Business', pill:'WooCommerce', head:'Handmade in small batches', sub:'Read the blog · Shop the range', p:['#F48FB1','#CE93D8','#FFE082'], does:['Custom theme','WooCommerce','Security','SEO setup']},
      {k:'eBay', c:'#E53935', url:'ebay.co.uk/str/yourshop', name:'yourshop', pill:'eBay shop', head:'Shop by category', sub:'Top Rated · 30-day returns', p:['#EF9A9A','#FFF59D','#A5D6A7'], does:['Shop design','Listing template','Bulk listing','Store categories']},
      {k:'Amazon', c:'#FBC02D', on:'#231942', url:'amazon.co.uk/stores/YourBrand', name:'YourBrand', pill:'Amazon store', head:'Visit the YourBrand Store', sub:'A+ content · Brand Store pages', p:['#FFE082','#BCAAA4','#80DEEA'], does:['Seller Central','Listing feeds','A+ content','Shopify connector']},
      {k:'Etsy', c:'#F26B21', url:'etsy.com/shop/YourStudio', name:'YourStudio', pill:'Etsy shop', head:'Personalised gifts, made to order', sub:'Star Seller · ships in 1 to 2 days', p:['#FFAB91','#C5E1A5','#B39DDB'], does:['Shop setup','Banners & icon','Tags & titles','Variations']}
    ];
    var tabs = sw.querySelector('.tabs'), url = document.getElementById('sw-url'), shop = document.getElementById('sw-shop');
    var show = function(i){
      var s = SHOPS[i];
      Array.prototype.forEach.call(tabs.children,function(t,j){t.setAttribute('aria-selected', j===i?'true':'false'); t.tabIndex = j===i?0:-1});
      sw.style.setProperty('--c', s.c); sw.style.setProperty('--on', s.on||'#fff');
      url.textContent = 'https://' + s.url;
      var names = ['Bestseller','New in','Gift idea'], prices = ['£24.99','£18.50','£12.00'];
      shop.innerHTML =
        '<div class="shop-top"><span class="shop-name">'+esc(s.name)+'</span><span class="shop-pill">'+esc(s.pill)+'</span></div>'+
        '<div class="shop-hero"><strong>'+esc(s.head)+'</strong><small>'+esc(s.sub)+'</small></div>'+
        '<div class="shop-grid">'+s.p.map(function(c,j){return '<div class="prod"><span style="--p:'+c+'"></span>'+names[j]+'<em>'+prices[j]+'</em></div>'}).join('')+'</div>'+
        '<ul class="shop-does" aria-label="What we set up">'+s.does.map(function(d){return '<li>'+esc(d)+'</li>'}).join('')+'</ul>';
    };
    var auto = null, cur = 0;
    var stop = function(){ if(auto){clearInterval(auto); auto=null} };
    SHOPS.forEach(function(s,i){
      var b = document.createElement('button'); b.type='button'; b.className='tab'; b.setAttribute('role','tab'); b.textContent=s.k;
      b.style.setProperty('--c', s.c); if (s.on) b.style.setProperty('--on', s.on);
      b.addEventListener('click',function(){show(i); stop()});
      tabs.appendChild(b);
    });
    show(0);
    if (!still) auto = setInterval(function(){cur=(cur+1)%SHOPS.length; show(cur)}, 3600);
    tabs.addEventListener('keydown',function(e){
      var i = Array.prototype.findIndex.call(tabs.children,function(t){return t.getAttribute('aria-selected')==='true'});
      if(e.key==='ArrowRight'||e.key==='ArrowLeft'){ stop(); i=(i+(e.key==='ArrowRight'?1:-1)+SHOPS.length)%SHOPS.length; show(i); tabs.children[i].focus(); e.preventDefault(); }
    });
  }

  /* ---------- Merchant Center console ---------- */
  var con = document.getElementById('console');
  if (con) {
    var fixBtn = document.getElementById('fix-btn'), score = document.getElementById('score');
    fixBtn.addEventListener('click',function(){
      var on = con.classList.toggle('fixed');
      score.classList.toggle('ok', on);
      score.textContent = on ? '0 issues · all products approved' : '6 issues · 312 products affected';
      fixBtn.textContent = on ? 'Show the problems' : 'Show it fixed';
    });
  }

  /* ---------- quote builder (contact page) ---------- */
  var form = document.getElementById('q-form');
  if (form) {
    var PLATFORMS = [['Shopify','#43A047'],['BigCommerce','#1E5BC6'],['WordPress / WooCommerce','#C2185B'],['Wix / Squarespace','#F26B21'],['Magento / OpenCart','#E53935'],['Custom website','#FBC02D'],['eBay','#E53935'],['Amazon','#FBC02D'],['Etsy','#F26B21'],['Google Shopping','#1E5BC6'],['TikTok Shop','#43A047'],['Facebook / Instagram','#C2185B'],['Not sure yet','#8A82A8']];
    var SERVICES = [['New website','#F26B21'],['Redesign','#C2185B'],['Shop setup','#43A047'],['Shop design','#1E5BC6'],['Product listing','#FBC02D'],['Product page design','#C2185B'],['Marketplace connectors','#1E5BC6'],['Fix a broken site','#E53935'],['Fix Google Shopping','#E53935'],['Move platforms','#F26B21'],['SEO & copy','#43A047'],['Product photos','#FBC02D'],['Personaliser / designer','#C2185B'],['Logo & branding','#F26B21'],['Care plan','#43A047']];
    var chips = function(id, list, name){
      var box = document.getElementById(id);
      list.forEach(function(it,i){
        var d=document.createElement('div'); d.className='chip'; d.style.setProperty('--c', it[1]);
        var inp=document.createElement('input'); inp.type='checkbox'; inp.name=name; inp.value=it[0]; inp.id=name+'-'+i;
        var lab=document.createElement('label'); lab.htmlFor=inp.id; lab.textContent=it[0];
        d.appendChild(inp); d.appendChild(lab); box.appendChild(d);
      });
    };
    chips('chips-platforms', PLATFORMS, 'platform'); chips('chips-services', SERVICES, 'service');
    // links like contact.html?platform=eBay&service=Shop%20setup pre-tick the form
    try {
      var q = new URLSearchParams(location.search);
      ['platform','service'].forEach(function(n){
        q.getAll(n).forEach(function(v){
          form.querySelectorAll('input[name='+n+']').forEach(function(c){ if(c.value.toLowerCase().indexOf(v.toLowerCase())===0) c.checked=true });
        });
      });
    } catch(_){}
    var note=document.getElementById('q-note'), brief=document.getElementById('brief'), bt=document.getElementById('brief-text');
    var vals = function(n){return Array.prototype.map.call(form.querySelectorAll('input[name='+n+']:checked'),function(c){return c.value})};
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var sv=vals('service'), pf=vals('platform'), em=form.email.value.trim();
      if(!sv.length || !/^\S+@\S+\.\S+$/.test(em)){
        note.className='q-err';
        note.textContent = !sv.length ? 'Pick at least one thing you need.' : 'Add an email address so we can reply.';
        return;
      }
      note.className=''; note.textContent='Brief ready below.';
      bt.textContent = [
        'FOXY WEBSITES: PROJECT BRIEF',
        '----------------------------',
        'Name:      '+(form.name.value.trim()||'-'),
        'Email:     '+em,
        'Site/shop: '+(form.site.value.trim()||'-'),
        'Products:  '+form.size.value,
        '',
        'Platforms: '+(pf.join(', ')||'Not sure yet'),
        'Needs:     '+sv.join(', '),
        '',
        'Notes:',
        form.msg.value.trim()||'-'
      ].join('\n');
      brief.hidden=false; brief.scrollIntoView({behavior: still?'auto':'smooth', block:'nearest'});
    });
    document.getElementById('copy-btn').addEventListener('click',function(){
      var btn=this, txt=bt.textContent;
      var sel = function(){var r=document.createRange(); r.selectNodeContents(bt); var s=getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent='Selected, press Ctrl+C'};
      try{ navigator.clipboard.writeText(txt).then(function(){btn.textContent='Copied'},sel) }catch(_){ sel() }
    });
  }
})();
