import sys,json,time; sys.path.insert(0,'gt')
import gtclient as g
NOISE='-haval -هافال -changan -شانجان -شنجان -alsvin -vivo -honor -midjourney -uuid'
V7CLEAN='v7 '+NOISE
COMPANY=V7CLEAN+' + في سفن + ڤي سفن + فى سفن + v cola + vcola + في كولا + ڤي كولا'
P={
 'cola':'v cola + vcola + v7 cola + في كولا + ڤي كولا + فى كولا + في سفن كولا',
 'cream':'v7 cream soda + v7 كريم صودا + كريم صودا v7 + في سفن كريم صودا + كريم صودا في سفن',
 'pink':'pink lemonade v7 + v7 pink lemonade + بينك ليمونيد v7 + في سفن بينك ليمونيد + بينك ليمونيد في سفن',
 'pom':'v7 رمان + v7 pomegranate + في سفن رمان + رمان في سفن',
 'pina':'v7 pina colada + v7 piña colada + v7 بينا كولادا + في سفن بينا كولادا',
 'malt':'v7 malt + v7 شعير + في سفن شعير + شعير في سفن + v7 بيرة',
 'blue':'v7 blueberry + v7 توت + في سفن توت + في سفن بلوبيري',
 'lmint':'v7 lemon mint + v7 ليمون نعناع + في سفن ليمون نعناع',
 'pine':'v7 pineapple + v7 اناناس + v7 أناناس + في سفن اناناس',
 'llime':'v7 lemon lime + v7 ليمون لايم + في سفن ليمون لايم',
}
out={'noise_terms':NOISE,'company_term':COMPANY,'product_terms':P}
out['noise']=g.series(['v7',V7CLEAN,'في سفن + ڤي سفن + فى سفن'])
out['company']=g.series([COMPANY])
out['company_related']=g.related(COMPANY)
out['b1']=g.series([COMPANY,P['cola'],P['cream'],P['pink'],P['pom']])
out['b2']=g.series([COMPANY,P['pina'],P['malt'],P['blue'],P['lmint']])
out['b3']=g.series([COMPANY,P['pine'],P['llime']])
json.dump(out,open('gt/pull.json','w'),ensure_ascii=False)
def avg(v): return round(sum(v)/len(v),1)
n=out['noise']; print('noise weeks',len(n['weeks']))
for i,k in enumerate(n['keywords']): print('  ',k[:40],'avg',avg([x[i] for x in n['values']]))
c=out['company']; print('company avg',avg([x[0] for x in c['values']]),'geo',c.get('geo',[])[:6])
print('related top',out['company_related'].get('top',[])[:20])
for b in ['b1','b2','b3']:
    s=out[b]
    for i,k in enumerate(s['keywords']): print(b,k[:30],'avg',avg([x[i] for x in s['values']]),'zeros',sum(1 for x in s['values'] if x[i]==0))
