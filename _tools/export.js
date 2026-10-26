// يطلع كل المنتجات من الموقع في products.json (يحتاج playwright)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/fonts\.g/,r=>r.abort());
const root=path.resolve(__dirname,'..');await p.goto('file://'+root+'/index.html');await p.waitForTimeout(400);
const d=await p.evaluate(()=>({products:PRODUCTS.map(x=>({...x,catId:(catOf(x)||{}).id,catName:(catOf(x)||{}).name,extra:pdExtras(x),stats:pdStats(x),brandId:(brandOf(x)||{}).id,freq:freqOf(x)?FREQ[freqOf(x)]:"",type:x.t&&TYPES[x.t]?TYPES[x.t]:"",use:USE[x.t]||""})),cats:CATS,brands:BRANDS.map(b=>({id:b.id,en:b.en,ar:b.ar})),faq:FAQ}));
fs.writeFileSync(path.join(__dirname,'products.json'),JSON.stringify(d));console.log(d.products.length);await b.close()})();
