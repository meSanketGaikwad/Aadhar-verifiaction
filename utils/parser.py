import re
import unicodedata
AADHAAR_KEYWORDS=['AADHAAR','Aadhaar','Unique Identification Authority of India','GOVERNMENT OF INDIA']


def clean_name(text):
    text = unicodedata.normalize("NFKD", text)
    words = text.split()
    clean_words = []

    for word in words:
        word_clean = re.sub(r'[^A-Za-z]', '', word)
        if len(word_clean) > 1:
            clean_words.append(word_clean)

    if len(clean_words) >= 2:
        return " ".join(clean_words).title()
    return ""



def is_aadhaar_text(text):
    if not text: return False
    t=text.lower()
    has_kw=any(k.lower() in t for k in AADHAAR_KEYWORDS)
    has_num=bool(re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text))
    return has_kw or has_num

def extract_aadhaar_fields(text):
    data={'aadhaar_number':None,'full_name':None,'dob':None,'gender':None,
          'enrollment_no':None,'mobile_no':None,'address':None}

    cleaned='\n'.join([ln.strip() for ln in text.splitlines() if ln.strip()])

    m=re.search(r"\b(\d{4}\s?\d{4}\s?\d{4})\b", cleaned)
    if m: data['aadhaar_number']=m.group(1)

    enr=re.search(r"(\d{4}\/\d{4,6}\/\d{4,6})", cleaned)
    if enr: data['enrollment_no']=enr.group(1)

    mob=re.search(r"\b[6-9]\d{9}\b", cleaned)
    if mob: data['mobile_no']=mob.group(0)

    dob=re.search(r"DOB[:\s]*([0-3]?\d[\/\-][01]?\d[\/\-]\d{4})", cleaned, re.I)
    if dob: data['dob']=dob.group(1)

    g=re.search(r"\b(Male|Female|MALE|FEMALE|Transgender|T)\b", cleaned)
    if g: data['gender']=g.group(1)

    lines=cleaned.split('\n')
    name=None
    for i,ln in enumerate(lines):
        if re.search(r"DOB|Birth", ln, re.I):
            if i>0 and any(c.isalpha() for c in lines[i-1]):
                name=lines[i-1]; break
    if not name:
        for ln in lines[:6]:
            if ln and not re.search(r'AADHAAR|GOVERNMENT|UNIQUE', ln, re.I):
                if any(c.isalpha() for c in ln): name=ln; break
    data['full_name']=name
        
    addr = ""
    for i, ln in enumerate(lines):
        if re.search(r'Address', ln, re.I):  
            collected = []
    
            for j in range(i+1, len(lines)):
                collected.append(lines[j])
    
                if re.search(r'\b\d{6}\b', lines[j]):
                    addr = " ".join(collected)
                    break
            break  


    if not addr:
        for i,ln in enumerate(lines):
            if re.search(r'\b\d{6}\b', ln):
                addr=" ".join(lines[max(0,i-8):i+1]); break

    if addr:
        data['address']=addr

    return data
