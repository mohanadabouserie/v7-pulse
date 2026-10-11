"""Cost calculator (V7_Pulse_Costs.html): presets, the three Claude model pickers, saved settings, phone width."""
import asyncio, json, os
from playwright.async_api import async_playwright
# COSTS_SRC=... runs the same checks on the hosted copy (deploy/v7-pulse-costs/index.html)
import pathlib
SRC=os.environ.get('COSTS_SRC',pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Costs.html').as_uri())
fails=0
def check(name,ok,info=''):
    global fails
    if not ok: fails+=1
    print(('  ok ' if ok else 'FAIL ')+name+(' :: '+str(info) if info!='' else ''))
def usd(t): return int(t.replace('$','').replace(',','').replace('−','-').replace('+',''))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        ctx=await b.new_context(viewport={'width':1440,'height':900})
        pg=await ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        await pg.goto(SRC); await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(700)
        total=lambda: J("document.getElementById('tTotal').textContent")
        pressed=lambda: J("[...document.querySelectorAll('[data-preset][aria-pressed=true]')].map(b=>b.dataset.preset)")
        line=lambda n: J(f"[...document.querySelectorAll('.line')].find(l=>l.querySelector('.nm').textContent=={n!r})")
        lineEx=lambda n: J(f"[...document.querySelectorAll('.line')].find(l=>l.querySelector('.nm').textContent=={n!r}).querySelector('.ex').textContent")
        lineAmt=lambda n: J(f"[...document.querySelectorAll('.line')].find(l=>l.querySelector('.nm').textContent=={n!r}).querySelector('.amt').firstChild.textContent")
        table=lambda: J("[...document.querySelectorAll('#cmpModel tbody tr')].map(r=>[...r.cells].map(c=>c.textContent))")
        async def pick(id,v): await pg.select_option('#'+id,v); await pg.wait_for_timeout(150)
        # presets keep their totals
        for k,want in (('lean','$902'),('heavy','$11,792'),('rec','$2,497')):
            await pg.click(f'[data-preset={k}]'); await pg.wait_for_timeout(150)
            check(f'{k} preset total {want}', await total()==want, await total())
        check('Recommended is highlighted', await pressed()==['rec'], await pressed())
        # all three model pickers in one panel, none left in the assumptions
        panel=await J("['model','nModel','rModel','batch'].map(id=>document.getElementById(id).closest('.panel').querySelector('h2,summary').textContent)")
        check('answers, analysis and reading models and batch sit in the Claude models panel', set(panel)=={'Claude models'}, panel)
        check('nothing model-related left in the assumptions', await J("!document.querySelector('#adv select, #adv #batch')"))
        opts=await J("['model','nModel','rModel'].map(id=>[...document.getElementById(id).options].map(o=>o.value).join())")
        check('each picker offers the same four models', len(set(opts))==1 and opts[0]=='opus5,opus55,sonnet5,haiku45', opts)
        vals=await J("['model','nModel','rModel'].map(id=>document.getElementById(id).value)")
        check('defaults: Opus 5, Opus 5, Haiku 4.5', vals==['opus5','opus5','haiku45'], vals)
        order=await J("[...document.querySelectorAll('.line .nm')].map(x=>x.textContent).filter(t=>/answers|Analysis|Reading/.test(t))")
        check('variable lines follow the picker order', order==['Ask V7 Pulse answers','Analysis runs','Reading posts and comments'], order)
        # model table: one row per model, a column per job
        hdr=await J("[...document.querySelectorAll('#cmpModel th')].map(x=>x.textContent)")
        check('model table has Answers, Analysis and Reading columns', hdr==['Model','Answers','Analysis','Reading'], hdr)
        cur=await table()
        check('current picks marked', cur[0][1:3]==['current','current'] and cur[3][3]=='current', cur)
        check('caption names the currency', 'US dollars' in await J("document.getElementById('cmpModelCap').textContent"))
        son=[r for r in cur if r[0]=='Sonnet 5'][0]; opus=cur[0]
        before=usd(await total()); an_save=-usd(son[2]); rd_up=usd(son[3])
        check('Sonnet 5 saves on answers and analysis, costs more for reading', usd(son[1])<0 and an_save>0 and rd_up>0, son)
        check('reading on Opus 5 costs more than on Sonnet 5', usd(opus[3])>rd_up, (opus[3],son[3]))
        # analysis model alone
        await pick('nModel','sonnet5')
        check('analysis on Sonnet 5 lowers the total by the table amount', abs((before-usd(await total()))-an_save)<=1, (before,await total(),an_save))
        check('analysis line names Sonnet 5', 'Claude Sonnet 5' in await lineEx('Analysis runs'))
        await pick('nModel','opus5')
        # reading model alone
        await pick('rModel','sonnet5')
        check('reading on Sonnet 5 raises the total by the table amount', abs((usd(await total())-before)-rd_up)<=1, (before,await total(),rd_up))
        ex=await lineEx('Reading posts and comments')
        check('reading line names Sonnet 5 and batches', 'Claude Sonnet 5 in batches' in ex, ex)
        ansl=await lineEx('Ask V7 Pulse answers')
        check('answers line still on Opus 5', 'Claude Opus 5' in ansl and 'Sonnet' not in ansl, ansl)
        facts=await J("[...document.querySelectorAll('.fact')].map(f=>f.innerText.replace(/\\n/g,' | '))")
        check('per-unit cards: question, analysis run, reading, social refresh', len(facts)==4 and facts[0].startswith('One question') and facts[1].startswith('One analysis run') and facts[2].startswith('Reading 1,000 posts') and 'Sonnet 5, in batches' in facts[2] and facts[3].startswith('One social refresh'), facts)
        check('no preset highlighted after a custom change', await pressed()==[], await pressed())
        # batches halve the reading cost
        a1=usd(await lineAmt('Reading posts and comments')); await pg.click('#batch'); await pg.wait_for_timeout(150)
        a2=usd(await lineAmt('Reading posts and comments'))
        check('reading without batches costs twice as much', abs(a2-2*a1)<=1, (a1,a2))
        check('reading line drops "in batches"', 'in batches' not in await lineEx('Reading posts and comments'))
        # saved settings survive a reload
        await pick('nModel','haiku45'); await pg.reload(); await pg.wait_for_timeout(600)
        vals=await J("['model','nModel','rModel'].map(id=>document.getElementById(id).value).concat(document.getElementById('batch').checked)")
        check('model picks and batch setting are remembered', vals==['opus5','haiku45','sonnet5',False], vals)
        await pg.click('[data-preset=rec]'); await pg.wait_for_timeout(150)
        vals=await J("['model','nModel','rModel'].map(id=>document.getElementById(id).value).concat(document.getElementById('batch').checked)")
        check('preset resets all three models and batches', vals==['opus5','opus5','haiku45',True] and await total()=='$2,497', vals)
        # settings saved before analysis had its own model: analysis follows the old answers model
        st=json.loads(await J("localStorage.getItem('v7costs')")); st['model']='sonnet5'; st.pop('nModel',None)
        await J(f"localStorage.setItem('v7costs',{json.dumps(json.dumps(st))})"); await pg.reload(); await pg.wait_for_timeout(600)
        check('old saved settings: analysis uses the old answers model', await J("document.getElementById('nModel').value")=='sonnet5')
        await J("localStorage.clear()")
        # widths and currency, with the largest numbers (Heavy) too
        for w in (390,820,1100):
            q=await ctx.new_page(); await q.set_viewport_size({'width':w,'height':900}); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(600)
            for preset in ('rec','heavy'):
                await q.click(f'[data-preset={preset}]'); await q.wait_for_timeout(150)
                for c in ('usd','egp'):
                    await q.click(f'label[for=cur{c.capitalize()}]'); await q.wait_for_timeout(150)
                    fits=await q.evaluate("[...document.querySelectorAll('.cmp')].every(t=>t.scrollWidth<=t.parentElement.clientWidth+1)")
                    page=await q.evaluate("document.documentElement.scrollWidth")
                    check(f'[{w} {preset} {c}] tables and page fit', fits and page<=w, page)
            await q.evaluate("localStorage.clear()"); await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
