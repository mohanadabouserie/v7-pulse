"""Robust brand and V7-flavour detection for Talabat menu items (v2, 5 Oct 2026).
Reads the item name AND description (meal deals often name the drink only in the description)."""
import re
AR_FI=r'(?:في|فى|ڤي|ڤى|ﭬﻲ|ف)'
V7_RX=re.compile(r'\bv[\s.\-]+(?:pineapple|pomegranate|blue\s*berry|blueberry|pina|piña|pinacolada|lemon\s*(?:with\s*)?mint|mint|pink\s*lemonade|apple\s*malt|pineapple\s*malt|malt|barley)\b|\bv[\s.\-]?(?:7|٧)(?!\s*up)\b|\bv[\s.\-]*seven\b|\bvseven\b|'+AR_FI+r'\s*[-_]?\s*س[فڤ]ن(?!\s*(?:اب|أب|آب))|ڤي\s*(?:7|٧)',re.I)
VCOLA_RX=re.compile(r'\bv[\s.\-]*lemon(?![\s\-]*(?:with[\s\-]*)?mint)(?:[\s\-]*lime)?\b|\bv[\s.\-]*cola\b|\bfa[yi][\s\-]*cola\b|\bv[\s.\-]*(?:diet|zero)[\s.\-]*cola\b|\bv\s*soda\b|\bvcola\b|\bfi[\s.\-]*cola\b|\bv\s*super\s*soda\b|\bv[\s.\-]*(?:7|seven)\.?\s*(?:diet\s*)?(?:super\s*soda\s*)?cola\b|\bcola\s*v[\s\-]*7\b|'+AR_FI+r'[يى]?\s*(?:سفن\s*)?كولا|ڤيكولا',re.I)
BRANDS=[
 ('V Cola','V7', VCOLA_RX),
 ('V7','V7', V7_RX),
 ('Coca-Cola','Coca-Cola', re.compile(r'\bcoca[\s\-]*cola\b|\bcoke\b|\bcoca\b|\bcoka\b|كوكا[\s\-]*كولا|كوكاكولا|\bكوك\b',re.I)),
 ('Sprite','Coca-Cola', re.compile(r'\bsprite?\b|سبرايت|سبريت',re.I)),
 ('Fanta','Coca-Cola', re.compile(r'\bfanta\b|فانتا',re.I)),
 ('Schweppes','Coca-Cola', re.compile(r'schwepp?es|شويبس|شويبز',re.I)),
 ('Pepsi','PepsiCo', re.compile(r'\bp[ae]pe?si\b|\bpebsi\b|بيبسي|بيبسى|بيبس\b',re.I)),
 ('7UP','PepsiCo', re.compile(r'\b7\s*-?\s*up\b|\bseven\s*-?\s*up\b|سفن\s*(?:اب|أب|آب)',re.I)),
 ('Mirinda','PepsiCo', re.compile(r'mirinda|miranda|ميرندا|ميريندا|ميرندة',re.I)),
 ('Mountain Dew','PepsiCo', re.compile(r'mountain\s*dew|\bmtn\s*dew\b|ماونتن\s*ديو|ماونتين\s*ديو',re.I)),
 ('Birell','Other', re.compile(r'\bbirell\b|بيريل|بريل\b',re.I)),
 ('Fayrouz','Other', re.compile(r'\bfayrouz\b|فيروز',re.I)),
 ('Barbican','Other', re.compile(r'\bbarbican\b|باربيكان',re.I)),
 ('Spiro Spathis','Other', re.compile(r'spiro|سبيرو',re.I)),
 ('Big Cola','Other', re.compile(r'\bbig[\s\-]*cola\b|بيج\s*كولا',re.I)),
 ('Maxi Cola','Other', re.compile(r'\bmaxi?[\s\-]*(?:cola|cans?)\b|ماكسي',re.I)),
 ('Green Cola','Other', re.compile(r'\bgreen[\s\-]*cola\b|جرين\s*كولا',re.I)),
]
# Things called "V7" that aren't the drink
NOT_DRINK=re.compile(r'coffee|espresso|latte|blend|قهوة|boba|tapioca|bubble\s*tea',re.I)
SODA_WORDS=re.compile(r'soda|soft|carbonat|sparkl|fizz|can\b|cans\b|300\s*ml|330\s*ml|غاز|كانز|علبة',re.I)
def detect(name,desc=''):
    """Brands named in the item name or description: [(brand, company, where)]"""
    out=[]
    for where,text in (('name',name or ''),('desc',desc or '')):
        for b,co,rx in BRANDS:
            if rx.search(text):
                if b=='V7' and any(x[0]=='V Cola' and x[2]==where for x in out): continue
                if not any(x[0]==b for x in out): out.append((b,co,where))
    return out
def v7_flavour(text):
    """Flavour of a V7-line item from text, or None when the text doesn't say. Order matters."""
    s=(text or '').lower()
    if re.search(r'cola|كولا',s): return 'dcola' if re.search(r'diet|zero|دايت|زيرو|sugar[\s\-]*free',s) else 'cola'
    if re.search(r'malt|barley|شعير',s): return 'amalt' if re.search(r'apple|تفاح',s) else ('pmalt' if re.search(r'pineapple|ananas|أناناس|اناناس',s) else 'malt?')
    if re.search(r'pina|piña|colada|binacolada|penacolada|pinacolada|coconut|بينا|كولادا',s): return 'pina'
    if re.search(r'pomegranate|رمان',s): return 'pom'
    if re.search(r'blue\s*berry|blueberry|\bberry|توت',s): return 'blue'
    if re.search(r'pink|بينك|lemonade|ليموناد',s): return 'pink'
    if re.search(r'mint|نعناع',s): return 'lmint'
    if re.search(r'lime|لايم',s): return 'llime'
    if re.search(r'lemon|ليمون',s): return 'lemon?'
    if re.search(r'pineapple|ananas|أناناس|اناناس',s): return 'pine'
    if re.search(r'apple|تفاح',s): return 'amalt'
    if re.search(r'cream|كريم',s): return 'cream'
    if re.search(r'diet|zero|دايت|زيرو',s): return 'diet?'
    return None
