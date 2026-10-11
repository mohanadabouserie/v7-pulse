import re
AR_FI=r'(?:في|فى|ڤي|ڤى|ﭬﻲ)'
BRANDS=[ # (brand, company, regex) — order matters: V Cola before V7, Coke Zero etc. are Coca-Cola
 ('V Cola','V7', re.compile(r'\bv[\s.\-]*cola\b|\bvcola\b|\bv\s*super\s*soda\b|\bv[\s.\-]*(?:7|seven)\.?\s*(?:diet\s*)?(?:super\s*soda\s*)?cola\b|\bcola\s*v[\s\-]*7\b|'+AR_FI+r'\s*(?:سفن\s*)?كولا|ڤيكولا',re.I)),
 ('V7','V7', re.compile(r'\bv[\s.\-]?7\b|\bv\s*seven\b|'+AR_FI+r'\s*سفن(?!\s*(?:اب|أب|آب))',re.I)),
 ('Coca-Cola','Coca-Cola', re.compile(r'\bcoca[\s\-]*cola\b|\bcoke\b|\bcoca\b|كوكا[\s\-]*كولا|كوكاكولا|\bكوك\b',re.I)),
 ('Sprite','Coca-Cola', re.compile(r'\bsprite\b|سبرايت|سبريت',re.I)),
 ('Fanta','Coca-Cola', re.compile(r'\bfanta\b|فانتا',re.I)),
 ('Schweppes','Coca-Cola', re.compile(r'schwepp?es|شويبس|شويبز',re.I)),
 ('Pepsi','PepsiCo', re.compile(r'\bpepsi\b|بيبسي|بيبسى|بيبس\b',re.I)),
 ('7UP','PepsiCo', re.compile(r'\b7\s*-?\s*up\b|\bseven\s*-?\s*up\b|سفن\s*(?:اب|أب|آب)',re.I)),
 ('Mirinda','PepsiCo', re.compile(r'mirinda|ميرندا|ميريندا|ميرندة',re.I)),
 ('Mountain Dew','PepsiCo', re.compile(r'mountain\s*dew|\bmtn\s*dew\b|ماونتن\s*ديو|ماونتين\s*ديو',re.I)),
 ('Birell','Other', re.compile(r'\bbirell\b|بيريل|بريل\b',re.I)),
 ('Fayrouz','Other', re.compile(r'\bfayrouz\b|فيروز',re.I)),
 ('Barbican','Other', re.compile(r'\bbarbican\b|باربيكان',re.I)),
 ('Spiro Spathis','Other', re.compile(r'spiro|سبيرو',re.I)),
 ('Big Cola','Other', re.compile(r'\bbig\s*cola\b|بيج\s*كولا',re.I)),
]
DRINK_CAT=re.compile(r'drink|beverage|cold|soft|soda|refresh|مشروب|مشروبات|عصائر|بارد|المشروبات',re.I)
SIZE=re.compile(r'\d+([.,]\d+)?\s*(ml|m\.l|مل|م|l\b|ltr|liter|litre|لتر|ل\b)|\b(can|cans|bottle|glass|small|medium|large|regular|diet|zero|light|free|sugar|original|classic|orange|lemon|lime|pineapple|pomegranate|apple|strawberry|gold|tonic|soda|drink|drinks|cold|ice|iced|family|size|pack|x\d+)\b|كانز|كان|زجاجة|ازازة|إزازة|دايت|زيرو|لايت|برتقال|ليمون|كبير|صغير|وسط|عائلي|مشروب|مشروبات|غازي|غازية|بارد',re.I)
LARGE=re.compile(r'\b(1|1[.,]25|1[.,]5|2|2[.,]25)\s*(l|ltr|liter|litre|لتر)\b|family|لتر|عائلي|1000\s*ml|1250|1500|2000',re.I)
def classify_item(name,cat=''):
    n=name or ''
    found=[]
    for b,co,rx in BRANDS:
        if rx.search(n):
            if b=='V7' and any(x[0]=='V Cola' for x in found): continue
            found.append((b,co))
    return found
def standalone(name,found):
    n=name or ''
    for b,co,rx in BRANDS: n=rx.sub(' ',n)
    n=SIZE.sub(' ',n); n=re.sub(r'[^\w؀-ۿ]+',' ',n).strip()
    return len(n)<=6 and len(found)==1
