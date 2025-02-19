import json  #libraria JSON : Ofron metoda për punuar me të dhëna në formatin JSON (JavaScript Object Notation). Ky format përdoret shpesh për të serializuar objekte Python në JSON ose për të analizuar të dhëna që vijnë në formatin JSON.
from urllib import request   # urllib.request : Një modul për hapjen dhe leximin e URL-ve. Ai të mundëson të merrni të dhëna nga burime online, kryesisht faqe HTTP dhe HTTPS.
from altair import sequence  # altair :  Një bibliotekë vizualizimi statistikash deklarative për Python. Altair përdoret për të krijuar grafika interaktive dhe informuese me kod relativisht të thjeshtë.
from django.shortcuts import render , redirect # django.shortcuts : Përmban funksione utilitare për të thjeshtuar zhvillimin e pamjeve në Django. Ajo përfshin metoda të përdorura shpesh si render për renditjen e shablloneve dhe redirect për ridrejtuar kërkesat HTTP.
from django.http import HttpResponse, JsonResponse # django.http : Ofron klasa si HttpResponse dhe JsonResponse për kthimin e përgjigjeve HTTP nga pamjet. HttpResponse() për përmbajtje HTML të përgjithshme dhe JsonResponse() për të kthyer përgjigje në format JSON (p.sh., për API).

import requests # requests : Një bibliotekë e thjeshtë dhe shumëpopullore për dërgimin e kërkesave HTTP për API dhe faqe interneti. Përdoret shpesh si zëvendësues për urllib për shkak të thjeshtësisë.
from youtube_transcript_api import YouTubeTranscriptApi # youtube_transcript_api : Një bibliotekë Python që përdoret për të marrë transkripte nga videot në YouTube. Ajo mundëson marrjen e titrave (transkripteve) të videove kur ato janë të disponueshme.
from collections import Counter # collections.Counter : Një klasë e veçantë e fjalorit të Python për numërimin e objekteve që mund të ruhen. Është shumë e dobishme për numërimin e elementeve në një koleksion.
from django.contrib import messages # django.contrib.messages : Një modul i Django-s për trajtimin e mesazheve të përdoruesve në aplikacionet web, shpesh për feedback ose njoftime.
from .forms import ContactForm # është një rresht importimi në Django që tregon se forma ContactForm po importohet nga moduli i formave (forms.py) që ndodhet në të njëjtin direktorium si skripti aktual.
from django.views.decorators.csrf import csrf_exempt # django.views.decorators.csrf : Ky dekorator përdoret për të shënuar pamjet që duhet të përjashtohen nga mbrojtja CSRF (Cross-Site Request Forgery), shpesh i nevojshëm kur trajton kërkesa AJAX ose forma POST në Django.

from collections import defaultdict # collections.defaultdict : Një nënklasë e fjalorit të Python që ofron një vlerë default për një çelës që nuk ekziston. Kjo shmang gabimin KeyError dhe thjeshton kodin kur punon me fjalorë.
import re # re: Një modul për punuar me shprehje të rregullta në Python, që të mundëson të kërkosh, përshtatësh dhe manipuloshtë vargje bazuar në modelet e përcaktuara.


# Create your views here.
def index(request):
    return render(request , 'index.html')

# YouTube API Key
YOUTUBE_API_KEY = 'API_KEY_YOUR'



# Funksioni për të marrë transkriptin dhe numërimin e fjalëve
def get_transcript(video_id):
    try:
        # Merr transkriptin e videos në shqip dhe anglisht
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['sq', 'en'])
        
        # Bashkoni të gjitha pjesët e transkriptit në një tekst të vetëm
        full_text = " ".join([t['text'] for t in transcript])
        
        # Numëroni shpeshtësinë e fjalëve
        word_count = Counter(full_text.split())
        return {'success': True, 'transcript': full_text, 'word_count': word_count}
    except Exception as e:
        # Kap gabimet dhe ktheji te përdoruesi
        return {'success': False, 'error': str(e)}
'''
'''
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

def get_transcript(video_id):
    try:
        # Merrni transkriptin e videos me ID të dhënë
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Këtu mund të keni nevojë të formatoni transkriptin sipas nevojës
        # Për shembull, duke e kthyer në një format më të thjeshtë (tekst të thjeshtë ose SRT)
        formatter = SRTFormatter()
        formatter.format_transcript(transcript)
        formatted_transcript = formatter.get_transcript()
        
        # Kthejeni një përgjigje që përfshin transkriptin dhe numrin e fjalëve
        return {
            'success': True,
            'transcript': formatted_transcript,  # Mund të kthehet si tekst ose SRT
            'word_count': len(formatted_transcript.split())  # Numri i fjalëve
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)  # Nëse ndodh një gabim (p.sh., video nuk ka transkript)
        }


# Funksioni kryesor videoshow
def videoshow(request):
    if request.method == "POST":
        link = request.POST.get('link', '')

        # Regex për lidhje të plota, të shkurtuara YouTube dhe linke të YouTube Shorts
        youtube_regex = r'^(https?:\/\/)?(www\.)?(youtube\.com\/(?:watch\?v=|v\/|e\/|embed\/|shorts\/))([a-zA-Z0-9_-]{11})'
        youtube_shorts_regex = r'^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})'
        youtube_shortlink_regex = r'^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})(\?si=[a-zA-Z0-9_-]+)?$'  # Përfshin gjithashtu ?si= parametrin

        match = re.match(youtube_regex, link)
        match_short = re.match(youtube_shorts_regex, link)
        match_shortlink = re.match(youtube_shortlink_regex, link)

        # Nxjerr ID-në e videos nga regex
        if match or match_short or match_shortlink:
            video_id = match.group(4) if match else match_short.group(4) if match_short else match_shortlink.group(4)

            # Verifikimi me YouTube API
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
            response = requests.get(url).json()

            if 'items' in response and len(response['items']) > 0:
                snippet = response['items'][0]['snippet']
                title = snippet['title'].lower()
                description = snippet['description'].lower()

                # Filtrimi për fjalët kyçe
                keywords = ['politikë', 'lajme', 'debat', 'emision', 'integrimi i shqiperise ne bashkimin europian']
                if any(keyword in title or keyword in description for keyword in keywords):
                                             
                    # Merrni transkriptin
                    transcript_data = get_transcript(video_id)
                    if transcript_data['success']:
                        return JsonResponse({
                            'success': True,
                            'video_id': video_id,
                            'title': snippet['title'],
                            'transcript': transcript_data['transcript'],
                            'word_count': transcript_data['word_count']
                        })
                    else:
                        return JsonResponse({'success': False, 'error': transcript_data['error']})
                else:
                    return JsonResponse({'success': False, 'error': 'Videoja nuk është për politika ose lajme!'})
            else:
                return JsonResponse({'success': False, 'error': 'Videoja nuk u gjet!'})
        else:
            return JsonResponse({'success': False, 'error': 'Lidhja nuk është valide!'})



    return render(request, 'videoshow.html')



# pjesa e analizimit te transkriptimit 

# Fjalor me shpjegime për termat dhe frazat
term_explanations = {
    "BE": "Bashkimi Europian",
    "AI": "Inteligjenca Artificiale",
    "UN": "Organizata e Kombeve të Bashkuara",
    "USA": "Shtetet e Bashkuara të Amerikës",
    "EU": "Bashkimi Europian",
    "NATO": "Organizata e Traktatit të Atlantikut Verior",
    "KE": "Komisioni Europian",
    "PE": "Parlamenti Europian",
    "KiE": "Këshilli i Europës",
    "Antaresimi ne Bashkimin Europian": "është procesi me të cilin një shtet bëhet pjesë e kësaj organizate ndërkombëtare, duke pranuar detyrimet dhe përfitimet që vijnë nga statusi i një vendi anëtar. Ai përfshin disa faza dhe kushte që një shtet duhet të plotësojë për t'u integruar në strukturat politike, ekonomike dhe ligjore të BE-së",
    "Integrimi": "Në një kontekst politik, ekonomik ose social, integrimi përfshin harmonizimin e sistemeve, politikave dhe kulturave për të krijuar një unitet funksional.",
    "Antaresimi ne BE":"Antaresimi ne Bashkimin Europian",
    "Negociatat":"Janë procesi i diskutimeve dhe bisedimeve midis dy ose më shumë palëve, me qëllim arritjen e një marrëveshjeje që plotëson interesat ose nevojat e të gjitha palëve të përfshira",
    "Hapja e Negociatave":"është faza fillestare formale e procesit të bisedimeve midis një vendi kandidat dhe Bashkimit Europian (BE) për anëtarësim. Kjo ndodh pasi vendi kandidat ka marrë statusin zyrtar të kandidatit dhe ka përmbushur disa kushte bazë të përcaktuara nga BE-ja",
    "Vend Kandidat":"është një shtet që ka aplikuar për t'u anëtarësuar në Bashkimin Europian (BE) dhe ka marrë miratimin për të vazhduar në këtë proces nga Këshilli Europian. Ky status tregon se vendi ka një perspektivë të qartë për t'u bërë anëtar i BE-së, por duhet të përmbushë një sërë kushtesh për të vazhduar drejt anëtarësimit të plotë.",
    "Procesi i Antaresimit":"është një rrugëtim formal dhe i strukturuar që një vend ndjek për t'u bërë pjesë e Bashkimit Europian (BE). Ky proces përfshin disa faza dhe kërkesa që synojnë të sigurojnë se vendi është i përgatitur për të përmbushur standardet dhe detyrimet e BE-së si një vend anëtar",
    "Hapja e Kapitujve":" është një fazë e rëndësishme në procesin e negociatave për anëtarësim në Bashkimin Europian (BE). Kapitujt përfaqësojnë fushat kryesore të politikave dhe legjislacionit të BE-së që një vend kandidat duhet të harmonizojë dhe zbatojë për t'u bërë anëtar i plotë i Unionit",
    "Permbushja e Standarteve":"është procesi në të cilin një vend kandidat zbaton reformat dhe ndryshimet e nevojshme për të arritur kriteret dhe normat që kërkon BE-ja në fusha të ndryshme. Këto standarde, të njohura si acquis communautaire, përfaqësojnë legjislacionin, rregullat dhe praktikat që vendet anëtare të BE-së duhet të ndjekin",
    "Bisedimet me Bashkimin Europian":"janë një proces i strukturuar dhe zyrtar që ndodh ndërmjet një vendi kandidat dhe BE-së gjatë rrugëtimit të tij drejt anëtarësimit në Union. Këto bisedime zakonisht quhen negociata për anëtarësim dhe përqendrohen në përshtatjen e politikave, institucioneve dhe legjislacionit të vendit kandidat me standardet e BE-së",
    "Statusi Kandidat":"është një fazë zyrtare në procesin e integrimit të një vendi në Bashkimin Europian (BE). Ky status i jepet një vendi që ka aplikuar për anëtarësim dhe është vlerësuar nga BE-ja si i aftë për të filluar procesin e negociatave për anëtarësim, nëse përmbush disa kushte të caktuara",
    "Lideret e Ballkanit":"janë figura të shquara politike që udhëhoqën ose udhëhoqen shtetet e rajonit të Ballkanit, një zonë që përfshin vende si Shqipëria, Serbia, Bosnje e Hercegovina, Kroacia, Maqedonia e Veriut, Mali i Zi, Kosova, dhe të tjerë. Ata luajnë një rol të rëndësishëm në politikën rajonale dhe ndërkombëtare dhe ndikojnë në zhvillimet sociale, ekonomike dhe politike në këtë rajon",
    "Komisioneri i Zgjerimit":"është një pozicion i rëndësishëm brenda Komisionit Europian, i cili është organi ekzekutiv i Bashkimit Europian (BE). Ky komisioner është përgjegjës për menaxhimin dhe mbikëqyrjen e procesit të zgjerimit të BE-së, që përfshin çdo iniciativë për të pranuar shtete të reja në Union dhe për të mbështetur vendet kandidate në përmbushjen e kushteve të anëtarësimit",
    "Konferenca Western Ballkans":"është një ngjarje diplomatike dhe politike që ka për qëllim të sjellë së bashku liderët e vendeve të Ballkanit Perëndimor dhe ata të Bashkimit Europian (BE) për të diskutuar çështje të ndryshme të rëndësishme, si dhe për të avancuar procesin e integrimit të rajonit në BE",
    "Bashkimi Europian":" është një organizatë ndërkombëtare dhe një bashkësi politike, ekonomike dhe juridike që përfshin 27 shtete anëtare të Evropës. BE ka si qëllim të promovojë paqen, stabilitetin dhe prosperitetin në rajon dhe përtej tij, duke krijuar një treg të përbashkët, duke siguruar lëvizjen e lirë të njerëzve, mallrave, shërbimeve dhe kapitaleve, dhe duke koordinuar politikën e jashtme dhe mbrojtjen e përbashkët",
    "Komisioni Europian":"është një organ ekzekutiv i Bashkimit Europian (BE), i cili ka një rol kyç në propozimin dhe zbatimin e legjislacionit të BE-së, administrimin e politikave të BE-së dhe menaxhimin e buxhetit të BE-së. Komisioni është përgjegjës për të siguruar që politikat dhe ligjet e miratuara nga institucionet e tjera të BE-së zbatohet në të gjitha shtetet anëtare",
    "Parlamenti Europian":"është një nga tre institucionet kryesore të Bashkimit Europian (BE) dhe luan një rol kyç në procesin legjislativ të BE-së. Ai përfaqëson qytetarët e BE-së dhe ka përgjegjësinë për miratimin e ligjeve, rishikimin e buxhetit dhe mbikëqyrjen e politikave të BE-së. Parlamenti Europian ka të drejtën të shqyrtojë dhe të miratojë propozimet e ligjeve të bëra nga Komisionin Europian dhe ka një ndikim të konsiderueshëm në procesin e vendimmarrjes të Bashkimit Europian",
}

# Fjalor për vendodhjet e shteteve
country_locations = {
    "Shqiperi": "Ballkani Perendimor",
    "Austri": "Qendër e Evropës, kufizohet me Gjermaninë, Çekinë, Sllovakinë, Hungarinë, Slloveninë, Italinë dhe Lihtenshtajnin",
    "Belgjike":"Perëndim të Evropës, kufizohet me Francën, Luksemburgun, Gjermaninë dhe Holandën",
    "Bullgari":"Juglindje të Evropës, kufizohet me Rumani, Serbi, Maqedoninë e Veriut, Greqinë dhe Turqinë",
    "Kroaci":"Juglindje të Evropës, kufizohet me Slloveninë, Hungarinë, Serbinë, Bosnjë-Hercegovinën dhe Malin e Zi",
    "Qipro":"Ishull në Mesdhe, juglindje të Evropës, afër Turqisë",
    "Çeki":"Qendër të Evropës, kufizohet me Poloninë, Austrinë, Gjermaninë dhe Sllovakinë",
    "Danimarke":"Veri i Evropës, kufizohet me Gjermaninë dhe ka një shumëllojshmëri ishujsh në Detin e Veriut dhe Detin Baltik",
    "Estoni":"Veriperëndim të Evropës, në bregun lindor të Detit Baltik, kufizohet me Letoninë dhe Rusinë",
    "Finlande":"Veriperëndim të Evropës, kufizohet me Suedinë, Norvegjinë dhe Rusinë",
    "France":"Perëndim të Evropës, kufizohet me Belgjikën, Luksemburgun, Gjermaninë, Zvicrën, Italinë, Monakon dhe Andorrën",
    "Gjermani":"Qendër të Evropës, kufizohet me Danimarkën, Poloninë, Çekinë, Austrinë, Zvicrën, Francën, Luksemburgun, Belgjikën dhe Holandën",
    "Greqi":"Juglindje të Evropës, kufizohet me Bullgarinë, Turqinë dhe Maqedoninë e Veriut",
    "Hungari":"Qendër të Evropës, kufizohet me Austri, Sllovaki, Ukrainë, Rumani, Serbi dhe Kroaci",
    "Irlande":"Ishull në perëndim të Evropës, kufizohet me Britaninë e Madhe në Veri",
    "Itali":"Jug të Evropës, kufizohet me Francën, Zvicrën, Austrinë dhe Slloveninë",
    "Letoni":"Veriperëndim të Evropës, kufizohet me Estoninë, Rusinë, Lituaninë dhe Detin Baltik",
    "Lituani":"Veriperëndim të Evropës, kufizohet me Letoninë, Poloninë, Bjellorusinë dhe Detin Baltik",
    "Luksemburg":"Perëndim të Evropës, kufizohet me Belgjikën, Francën dhe Gjermaninë",
    "Malte":"Ishull në Mesdhe, jug të Italisë",
    "Holande":"Perëndim të Evropës, kufizohet me Gjermaninë dhe Belgjikën",
    "Poloni":"Qendër të Evropës, kufizohet me Gjermaninë, Çekinë, Sllovakinë, Ukrainën, Bjellorusinë, Lituaninë dhe Detin Baltik",
    "Portugali":"Perëndim të Evropës, kufizohet me Spanjën dhe Oqeanin Atlantik",
    "Rumani":"Juglindje të Evropës, kufizohet me Bullgarinë, Serbinë, Hungarinë, Ukrainën dhe Moldavinë",
    "Sllovaki":"Qendër të Evropës, kufizohet me Poloninë, Çekinë, Austrinë, Hungarinë dhe Ukrainën",
    "Slloveni":"Juglindje të Evropës, kufizohet me Austri, Hungari, Kroaci dhe Itali",
    "Spanje":"Perëndim të Evropës, kufizohet me Francën, Portugalin, Andorrën dhe Gjirin e Gjelbër",
    "Suedi":"Veriperëndim të Evropës, kufizohet me Norvegjinë, Finlandën dhe Detin Baltik",
   
}

# Merr input nga përdoruesi
sequence=input("Enter Sentence: ")


# Funksion për normalizimin e fjalëve (heqja e prapashtesave dhe parashtesave)
def normalize_word(word):
    # Trajton fjalët si "antaresuar", "antaresim", etj.
    # Për të trajtuar prapashtesat dhe parashtesat që ndryshojnë kuptimin e fjalëve
    stem_variants = {
        "antaresuar": "antaresim",   # Trajton variantet e fjalës 'antaresuar'
        "integruar": "integrim",     # Trajton variantet e fjalës 'integruar'
        # Shtoni edhe variante të tjera fjalësh këtu
    }
    word = word.lower()  # Përshtat fjalën në minuskulë për krahasim më të thjeshtë
    if word in stem_variants:
        return stem_variants[word]
    return word

# Inicializon një dictionary për të numëruar frekuencat dhe kontekstin
frequency = defaultdict(lambda: {
    'count': 0,
    'originals': set(),
    'meanings': set(),
    'explanation': None,
    'location': None
})

# Përpuno frazat dhe fjalët
words = sequence.split()
# Use the transcript as input for word processing
#ords = transcript_text.split()



# Ndihmës për të kontrolluar fraza
def check_phrase(word):
    for phrase in term_explanations:
        if phrase.lower() == word.lower():
            return phrase
    return None

# Përpuno çdo fjalë dhe frazë
i = 0
while i < len(words):
    word = words[i]

    # Normalizo fjalët që mund të kenë prapashtesa ose parashtesa
    normalized_word = normalize_word(word)

    # Kontrollo nëse fjala është pjesë e një fraze
    phrase = check_phrase(" ".join(words[i:i+len(max(term_explanations.keys(), key=lambda k: len(k.split())))]))  # Kërkoni për fraza me më shumë fjalë
    if phrase:
        frequency[normalized_word]['count'] += 1
        frequency[normalized_word]['originals'].add(phrase)
        frequency[normalized_word]['meanings'].add(f"Përdoret me: {' '.join(words[max(0, i - 2):min(len(words), i + 3)])}")
        frequency[normalized_word]['explanation'] = term_explanations[phrase]
        i += len(phrase.split())  # Hiko sa fjalë ka fraza
    else:
        frequency[normalized_word]['count'] += 1
        frequency[normalized_word]['originals'].add(word)
        frequency[normalized_word]['meanings'].add(f"Përdoret me: {' '.join(words[max(0, i - 2):min(len(words), i + 3)])}")
        if word.capitalize() in country_locations:
            frequency[normalized_word]['location'] = country_locations[word.capitalize()]
        i += 1

# Formo tabelën me rendin e fjalëve
#print("\nTabela e rezultateve:\n")
#print(f"{'Rendi':<6}{'Fjala (Origjinale)':<20}{'Frekuenca':<10}{'Formatet':<30}{'Konteksti / Kuptimi':<40}{'Shpjegimi':<30}{'Vendodhja':<20}")
print("-" * 180)

# Inicializo një variabël për të mbajtur rendin
order = 1
for word in sorted(frequency.keys()):
    original_str = ", ".join(sorted(frequency[word]['originals']))
    meaning_str = "; ".join(sorted(frequency[word]['meanings']))
    explanation_str = frequency[word]['explanation'] if frequency[word]['explanation'] else "—"
    location_str = frequency[word]['location'] if frequency[word]['location'] else "—"
    
    # Printo tabelën me rendin
    #print(f"{order:<6}{word:<20}{frequency[word]['count']:<10}{original_str:<30}{meaning_str:<40}{explanation_str:<30}{location_str:<20}")
    
    # Rrit rendin për fjalën tjetër
    order += 1


#funksioni i kontaktit
def contact(request):
    if request.method == "POST": 
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Ruaj të dhënat në databazë
            messages.success(request, "Faleminderit që na kontaktuat! Mesazhi juaj është dërguar.")
            return redirect('contact')
        else:
            messages.error(request, "Ka ndodhur një gabim. Ju lutemi kontrolloni të dhënat tuaja.")
    else:
        form = ContactForm()
        return render(request , 'contact.html' ,{'form': form} )


