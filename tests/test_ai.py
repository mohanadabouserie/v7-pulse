import asyncio, json
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
MOCK = r"""
window.__toolReport=[];window.__mode='ok';window.__lastInput=null;
window.claude={use:function(name){return new Promise(function(res){setTimeout(function(){
  if(name!=='sample'){res(null);return;}
  var fn=async function(input,opts){
    window.__lastInput=input;
    if(window.__mode==='deny'){throw {code:'not_granted',message:'no'};}
    var tools=(opts&&opts.tools)||[];
    for(const t of tools){
      var args={};
      if(t.name==='get_breakdown')args={by:'product'};
      if(t.name==='search_posts')args={query:'',sentiment:'neg',limit:5};
      if(t.name==='get_market')args={include_competitors:true};
      if(t.name==='get_restaurants')args={area:'Zamalek'};
      try{var out=await t.execute(args,{signal:new AbortController().signal});var js=JSON.stringify(out);window.__toolReport.push({name:t.name,bytes:js.length,keys:Object.keys(out||{}).slice(0,6)});}
      catch(e){window.__toolReport.push({name:t.name,error:String(e&&e.message||e)});}
    }
    var text='**Short answer:** V7 is on 12% of menus.\n\n### Evidence\n- PepsiCo 21%\n- Coca-Cola 15%\n\n| Area | V7 |\n|---|---|\n| Nasr City | 16% |\n| Zamalek | 13% |\n\n[[web: Coca-Cola Egypt price increase October 2026 | check if rivals raised prices]]\n[[apify: memo23/talabat-scraper | menus for 500 more Zamalek restaurants | $0.50]]\n\n### Recommended actions\n1. **Sales:** offer flavours to V Cola-only restaurants.';
    if(window.__mode==='slow'){
      for(var i=0;i<40;i++){await new Promise(function(r){setTimeout(r,100);});if(opts.signal&&opts.signal.aborted)throw {code:'cancelled',message:'x',text:text.slice(0,30)};if(i===2&&opts.onText)opts.onText({text:text.slice(0,30),delta:text.slice(0,30)});}
    }
    if(opts.onText)opts.onText({text:text,delta:text});
    return {text:text,truncated:false,modelTierApplied:'default'};
  };
  fn.limits=function(){return Promise.resolve({maxPromptBytes:262144,tools:{maxCount:8}});};
  res(fn);
},50);});}};
"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        await ctx.add_init_script(MOCK)
        pg = await ctx.new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        J=pg.evaluate
        await J("document.getElementById('askBtn').click()"); await pg.wait_for_timeout(300)
        print('mode line:', await J("document.getElementById('chatMode').textContent"))
        await pg.fill('#askInput','Are we on restaurant menus?'); await J("document.querySelector('#askForm button[type=submit]').click()")
        await pg.wait_for_timeout(1500)
        rep = await J("window.__toolReport"); 
        for r in rep: print('  tool',r)
        html = await J("document.querySelector('#chatLog .ai-msg:last-child .ai-body').innerHTML")
        print('rendered has table:', '<table' in html, '| cards:', html.count('tcard'), '| h4:', html.count('<h4>'), '| ol:', '<ol>' in html)
        inp = await J("window.__lastInput"); print('instructions bytes:', len(inp[0]['content']), '| turns:', len(inp))
        # follow-up keeps conversation
        await pg.fill('#askInput','And in Zamalek?'); await J("document.querySelector('#askForm button[type=submit]').click()"); await pg.wait_for_timeout(1500)
        inp = await J("window.__lastInput"); print('turns on 2nd question:', len(inp), [t['role'] for t in inp])
        # stop
        await J("window.__mode='slow'")
        await pg.fill('#askInput','Summarize'); await J("document.querySelector('#askForm button[type=submit]').click()"); await pg.wait_for_timeout(600)
        print('button while busy:', await J("document.querySelector('#askForm button[type=submit]').textContent"))
        await J("document.querySelector('#askForm button[type=submit]').click()"); await pg.wait_for_timeout(600)
        print('after stop:', (await J("document.querySelector('#chatLog .ai-msg:last-child').textContent"))[-60:], '| button:', await J("document.querySelector('#askForm button[type=submit]').textContent"))
        # deny -> fallback
        await J("window.__mode='deny'")
        await pg.fill('#askInput','Any false rumors about us?'); await J("document.querySelector('#askForm button[type=submit]').click()"); await pg.wait_for_timeout(800)
        print('after deny mode line:', await J("document.getElementById('chatMode').textContent"))
        print('fallback answer:', (await J("document.querySelector('#chatLog .msg.bot:last-child').textContent"))[:120])
        await pg.screenshot(path='shots5/d-chat-ai.png')
        print('ERRORS', errs)
        await b.close()
asyncio.run(main())
