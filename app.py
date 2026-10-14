from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Common Sinhala / Romanized Sinhala words with preferred Tamil-letter spellings.
KNOWN = {
    "amma": "அம்மா", "ammaa": "அம்மா",
    "appa": "அப்பா", "appaa": "அப்பா",
    "amma kiyala": "அம்மா கியலா", "appa kiyala": "அப்பா கியலா",
    "kiyala": "கியலா", "kiyaala": "கியாலா",
    "thaththa": "தாத்தா", "ayya": "அய்யா", "akka": "அக்கா",
    "nangi": "நங்கி", "malli": "மல்லி",
    "vandanawa": "வந்தனாவ", "sadu": "சாது", "saadu": "சாது",
    "ayubowan": "ஆயுபோவன்", "hari": "ஹரி", "kohomada": "கொஹொமத",
    "budun vandeema": "புதுன் வெதீம",
    "அම්මා": "அம்மா", "අම්මා": "அம்மா", "අප්පා": "அப்பா",
    "තාත්තා": "தாத்தா", "අක්කා": "அக்கா",
}

# Approximate character mapping for Sinhala-script input.
SINHALA_MAP = {
    "අ":"அ","ආ":"ஆ","ඇ":"அ","ඈ":"ஆ","ඉ":"இ","ඊ":"ஈ","උ":"உ","ඌ":"ஊ",
    "එ":"எ","ඒ":"ஏ","ඔ":"ஒ","ඕ":"ஓ","ක":"க","ග":"க","ච":"ச","ජ":"ஜ",
    "ට":"ட","ඩ":"ட","ත":"த","ද":"த","න":"ன","ප":"ப","බ":"ப","ම":"ம",
    "ය":"ய","ර":"ர","ල":"ல","ව":"வ","ස":"ஸ","හ":"ஹ","ළ":"ள","ණ":"ண",
    "ඞ":"ங","ඤ":"ஞ","ශ":"ஷ","ෂ":"ஷ","ෆ":"ஃப","්":"்","ා":"ா","ැ":"ெ",
    "ෑ":"ே","ි":"ி","ී":"ீ","ු":"ு","ූ":"ூ","ෙ":"ெ","ේ":"ே","ො":"ொ",
    "ෝ":"ோ","ෘ":"ரு","ං":"ம்","ඃ":"ஃ"," ":" "
}

def roman_word(word: str) -> str:
    """Approximate Romanized Sinhala-to-Tamil letters conversion."""
    w = word.lower()
    if w in KNOWN:
        return KNOWN[w]
    # Convert consonant + vowel chunks; best for phonetic typing, not translation.
    consonants = [
        ("kh","க"),("gh","க"),("ng","ங"),("ch","ச"),("sh","ஷ"),("zh","ழ"),
        ("th","த"),("dh","த"),("ph","ப"),("bh","ப"),("ny","ஞ"),
        ("k","க"),("g","க"),("c","க"),("j","ஜ"),("t","ட"),("d","ட"),
        ("n","ன"),("p","ப"),("b","ப"),("m","ம"),("y","ய"),("r","ர"),
        ("l","ல"),("v","வ"),("w","வ"),("s","ஸ"),("h","ஹ"),("f","ஃப"),
        ("q","க"),("x","க்ஸ")
    ]
    vowels = [
        ("aa","ா"),("ii","ீ"),("ee","ீ"),("uu","ூ"),("oo","ூ"),
        ("ai","ை"),("au","ௌ"),("ae","ே"),("ā","ா"),("ī","ீ"),
        ("ū","ூ"),("ē","ே"),("ō","ோ"),("a",""),("i","ி"),
        ("u","ு"),("e","ெ"),("o","ொ")
    ]
    out, i = [], 0
    while i < len(w):
        if w[i].isspace():
            out.append(w[i]); i += 1; continue
        cons = next(((src, dst) for src, dst in consonants if w.startswith(src, i)), None)
        if cons:
            src, dst = cons
            i += len(src)
            vowel = next(((srcv, sign) for srcv, sign in vowels if w.startswith(srcv, i)), None)
            if vowel:
                srcv, sign = vowel
                out.append(dst + sign)
                i += len(srcv)
            else:
                out.append(dst + "்")
            continue
        vowel = next(((srcv, sign) for srcv, sign in vowels if w.startswith(srcv, i)), None)
        if vowel:
            srcv, sign = vowel
            independent = {"":"அ","ா":"ஆ","ி":"இ","ீ":"ஈ","ு":"உ","ூ":"ஊ",
                           "ெ":"எ","ே":"ஏ","ொ":"ஒ","ோ":"ஓ","ை":"ஐ","ௌ":"ஔ"}
            out.append(independent.get(sign, "அ"))
            i += len(srcv)
        else:
            out.append(w[i]); i += 1
    return "".join(out)

def transliterate(text: str) -> str:
    s = text.strip()
    if not s:
        return ""
    key = s.lower()
    if key in KNOWN:
        return KNOWN[key]
    if any("\u0D80" <= ch <= "\u0DFF" for ch in s):
        return "".join(SINHALA_MAP.get(ch, ch) for ch in s)
    return " ".join(KNOWN.get(word.lower(), roman_word(word)) for word in s.split(" "))

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/convert")
def convert():
    data = request.get_json(silent=True) or {}
    return jsonify({"result": transliterate(str(data.get("text", "")))})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= int(os.environ.get("PORT", 5000)), debug=True)
