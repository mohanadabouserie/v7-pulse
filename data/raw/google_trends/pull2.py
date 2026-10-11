import sys,json,os; sys.path.insert(0,'gt')
import gtclient as g
F='gt/pull2.json'; out=json.load(open(F)) if os.path.exists(F) else {}
def save(): json.dump(out,open(F,'w'),ensure_ascii=False)
T1='v7 -haval -هافال -changan -شانجان -شنجان -alsvin -vivo -honor -midjourney -uuid'
T2='في سفن + ڤي سفن + فى سفن + v cola + vcola + في كولا + ڤي كولا'
P={'cola':'v cola + vcola + v7 cola + في كولا + ڤي كولا + فى كولا + في سفن كولا',
 'cream':'v7 cream soda + v7 كريم صودا + كريم صودا v7 + في سفن كريم صودا + كريم صودا في سفن',
 'pink':'pink lemonade v7 + v7 pink lemonade + بينك ليمونيد v7 + في سفن بينك ليمونيد',
 'pom':'v7 رمان + v7 pomegranate + في سفن رمان + رمان في سفن',
 'pina':'v7 pina colada + v7 piña colada + v7 بينا كولادا + في سفن بينا كولادا',
 'malt':'v7 malt + v7 شعير + في سفن شعير + شعير في سفن + v7 بيرة',
 'blue':'v7 blueberry + v7 توت + في سفن توت + في سفن بلوبيري',
 'lmint':'v7 lemon mint + v7 ليمون نعناع + في سفن ليمون نعناع',
 'pine':'v7 pineapple + v7 اناناس + v7 أناناس + في سفن اناناس',
 'llime':'v7 lemon lime + v7 ليمون لايم + في سفن ليمون لايم'}
for k,v in list(P.items())+[('T1',T1),('T2',T2)]: assert len(v)<=100,(k,len(v))
out['T1'],out['T2'],out['P']=T1,T2,P
jobs=[('noise',['v7',T1,T2]),('b1',[T1,T2,P['cola'],P['cream'],P['pink']]),('b2',[T1,T2,P['pom'],P['pina'],P['malt']]),('b3',[T1,T2,P['blue'],P['lmint'],P['pine']]),('b4',[T1,T2,P['llime']]),('geoT1',[T1]),('geoT2',[T2])]
for name,kws in jobs:
    if name in out: continue
    out[name]=g.series(kws); save(); print('got',name)
if 'related' not in out:
    out['related']={'T1':g.related(T1),'T2':g.related(T2)}; save(); print('got related')
