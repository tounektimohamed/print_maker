from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------------------
# TEMPLATE HTML POUR RAPPORT COMPLET
# --------------------------------------------------------------------------
COMPLETE_REPORT_TEMPLATE = '''
<!DOCTYPE html>
<html dir="{{ text_direction }}" lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: {{ font_family }};
            line-height: 1.6;
            background-color: white;
            color: #333;
            padding: 20px;
            font-size: 11pt;
        }

        .header {
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
            border-bottom: 3px double #2c3e50;
        }

        .header h1 {
            font-size: 18pt;
            margin-bottom: 8px;
            color: #2c3e50;
            font-weight: bold;
        }

        .header-info {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 10pt;
            color: #555;
        }

        .section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 14pt;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 5px;
            border-bottom: 2px solid #3498db;
            font-weight: bold;
            text-align: {{ text_align }};
        }

        .group-section {
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }

        .group-header {
            padding: 15px;
            color: white;
            font-size: 13pt;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .group-treatment .group-header {
            background-color: #e74c3c;
        }

        .group-support .group-header {
            background-color: #f39c12;
        }

        .group-excellence .group-header {
            background-color: #27ae60;
        }

        .student-count {
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 10pt;
        }

        .students-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10pt;
            margin: 20px;
        }

        .students-table th {
            background-color: #f8f9fa;
            padding: 10px;
            text-align: {{ text_align }};
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }

        .students-table td {
            padding: 8px 10px;
            border-bottom: 1px solid #eee;
            text-align: {{ text_align }};
        }

        .students-table tr:nth-child(even) {
            background-color: #fafafa;
        }

        .solutions-section, .problems-section {
            margin: 20px;
        }

        .content-title {
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            padding-{{ text_align }}: 10px;
            border-{{ text_align }}: 3px solid;
        }

        .solutions-section .content-title {
            border-color: #27ae60;
            color: #27ae60;
        }

        .problems-section .content-title {
            border-color: #e74c3c;
            color: #e74c3c;
        }

        .item-list {
            list-style-type: none;
            padding: 0;
        }

        .item-list li {
            margin-bottom: 12px;
            padding: 12px;
            border-radius: 4px;
            background-color: #f8f9fa;
            border-{{ border_side }}: 3px solid;
        }

        .solutions-section .item-list li {
            border-color: #27ae60;
        }

        .problems-section .item-list li {
            border-color: #e74c3c;
        }

        .item-text {
            font-size: 10.5pt;
            line-height: 1.5;
        }

        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10.5pt;
            margin-bottom: 30px;
        }

        .info-table td {
            padding: 8px;
            border-bottom: 1px solid #eee;
        }

        .info-label {
            font-weight: bold;
            width: 25%;
            background-color: #f8f9fa;
        }

        @media print {
            @page {
                size: A4;
                margin: 1.5cm;
            }
            
            body {
                padding: 0;
                margin: 0;
                font-size: 10pt;
            }
            
            .print-button {
                display: none;
            }
            
            .group-section {
                page-break-inside: avoid;
                margin-bottom: 25px;
            }
        }

        .print-button {
            position: fixed;
            top: 20px;
            {{ print_button_position }}: 20px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 10pt;
            z-index: 1000;
        }

        .print-button:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>

<button class="print-button" onclick="window.print()">
    {{ print_button_text }}
</button>

<div class="header">
    <h1>{{ main_title }}</h1>
    <div class="header-info">
        <div>{{ school_label }}: {{ schoolName }}</div>
        <div>{{ date_label }}: {{ date }}</div>
    </div>
</div>

<div class="section">
    <h2 class="section-title">{{ basic_info_title }}</h2>
    
    <table class="info-table">
        <tr>
            <td class="info-label">{{ teacher_label }}</td>
            <td>{{ profName }}</td>
            <td class="info-label">{{ class_label }}</td>
            <td>{{ className }}</td>
        </tr>
        <tr>
            <td class="info-label">{{ subject_label }}</td>
            <td>{{ matiereName }}</td>
            <td class="info-label">{{ criteria_label }}</td>
            <td>{{ baremeName }}</td>
        </tr>
        {% if sousBaremeName %}
        <tr>
            <td class="info-label">{{ sub_criteria_label }}</td>
            <td colspan="3">{{ sousBaremeName }}</td>
        </tr>
        {% endif %}
    </table>
</div>

<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>
    
    {% for group_key, group_data in groups.items() %}
    {% if group_data.students or group_data.solutions or group_data.problems %}
    <div class="group-section group-{{ group_key }}">
        <div class="group-header">
            <span>{{ group_titles[group_key] }}</span>
            <span class="student-count">{{ group_data.students|length }} {{ student_label }}</span>
        </div>
        
        {% if group_data.students %}
        <div style="margin: 20px;">
            <h3 style="font-size: 11pt; margin-bottom: 10px; color: #555;">{{ students_list_label }}</h3>
            <table class="students-table">
                <thead>
                    <tr>
                        <th style="width: 10%">#</th>
                        <th style="width: 90%">{{ student_name_label }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in group_data.students %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ student }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        
        {% if group_data.solutions %}
        <div class="solutions-section">
            <h3 class="content-title">{{ solutions_title }}</h3>
            <ul class="item-list">
                {% for solution in group_data.solutions %}
                <li>
                    <div class="item-text">{{ solution.text }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        {% if group_data.problems %}
        <div class="problems-section">
            <h3 class="content-title">{{ problems_title }}</h3>
            <ul class="item-list">
                {% for problem in group_data.problems %}
                <li>
                    <div class="item-text">{{ problem.text }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
    {% endif %}
    {% endfor %}
</div>

</body>
</html>
'''

# --------------------------------------------------------------------------
# TEMPLATE HTML POUR RAPPORT DE GROUPE UNIQUE
# --------------------------------------------------------------------------
SINGLE_GROUP_TEMPLATE = '''
<!DOCTYPE html>
<html dir="{{ text_direction }}" lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: {{ font_family }};
            line-height: 1.6;
            background-color: white;
            color: #333;
            padding: 20px;
            font-size: 12pt;
        }

        .header {
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
            border-bottom: 3px double #2c3e50;
        }

        .header h1 {
            font-size: 18pt;
            margin-bottom: 8px;
            color: #2c3e50;
            font-weight: bold;
        }

        .header h2 {
            font-size: 16pt;
            color: {{ group_color }};
            margin-top: 10px;
        }

        .header-info {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 10pt;
            color: #555;
        }

        .section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 14pt;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid {{ group_color }};
            font-weight: bold;
            text-align: {{ text_align }};
        }

        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10.5pt;
            margin-bottom: 30px;
        }

        .info-table td {
            padding: 8px;
            border-bottom: 1px solid #eee;
        }

        .info-label {
            font-weight: bold;
            width: 25%;
            background-color: #f8f9fa;
        }

        .students-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10pt;
            margin-bottom: 20px;
        }

        .students-table th {
            background-color: #f8f9fa;
            padding: 10px;
            text-align: {{ text_align }};
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }

        .students-table td {
            padding: 8px 10px;
            border-bottom: 1px solid #eee;
            text-align: {{ text_align }};
        }

        .students-table tr:nth-child(even) {
            background-color: #fafafa;
        }

        .content-block {
            margin-bottom: 25px;
        }

        .block-title {
            font-size: 13pt;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            padding-{{ text_align }}: 10px;
            border-{{ text_align }}: 3px solid;
        }

        .solutions-title {
            border-color: #27ae60;
            color: #27ae60;
        }

        .problems-title {
            border-color: #e74c3c;
            color: #e74c3c;
        }

        .item-list {
            list-style-type: none;
            padding: 0;
        }

        .solution-item, .problem-item {
            margin-bottom: 12px;
            padding: 12px;
            border-radius: 4px;
        }

        .solution-item {
            background-color: #f8fff8;
            border-{{ border_side }}: 3px solid #27ae60;
        }

        .problem-item {
            background-color: #fff8f8;
            border-{{ border_side }}: 3px solid #e74c3c;
        }

        .item-text {
            font-size: 10.5pt;
            line-height: 1.5;
        }

        .item-source {
            font-size: 9pt;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }

        @media print {
            @page {
                size: A4;
                margin: 1.5cm;
            }
            
            body {
                padding: 0;
                margin: 0;
                font-size: 10pt;
            }
            
            .print-button {
                display: none;
            }
        }

        .print-button {
            position: fixed;
            top: 20px;
            {{ print_button_position }}: 20px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 10pt;
            z-index: 1000;
        }
    </style>
</head>
<body>

<button class="print-button" onclick="window.print()">
    {{ print_button_text }}
</button>

<div class="header">
    <h1>{{ main_title }}</h1>
    <h2>{{ group_name }}</h2>
    <div class="header-info">
        <div>{{ school_label }}: {{ schoolName }}</div>
        <div>{{ date_label }}: {{ date }}</div>
    </div>
</div>

<div class="section">
    <h2 class="section-title">{{ basic_info_title }}</h2>
    
    <table class="info-table">
        <tr>
            <td class="info-label">{{ teacher_label }}</td>
            <td>{{ profName }}</td>
            <td class="info-label">{{ class_label }}</td>
            <td>{{ className }}</td>
        </tr>
        <tr>
            <td class="info-label">{{ subject_label }}</td>
            <td>{{ matiereName }}</td>
            <td class="info-label">{{ criteria_label }}</td>
            <td>{{ baremeName }}</td>
        </tr>
        {% if sousBaremeName %}
        <tr>
            <td class="info-label">{{ sub_criteria_label }}</td>
            <td colspan="3">{{ sousBaremeName }}</td>
        </tr>
        {% endif %}
    </table>
</div>

{% if groups.treatment.students or groups.support.students or groups.excellence.students %}
<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>
    
    {% for group_key, group_data in groups.items() %}
    {% if group_data.students %}
    <div style="margin-bottom: 20px;">
        <h3 style="font-size: 12pt; color: {{ group_color }}; margin-bottom: 10px;">
            {{ group_titles[group_key] }} ({{ group_data.students|length }} {{ student_label }})
        </h3>
        <table class="students-table">
            <thead>
                <tr>
                    <th style="width: 10%">#</th>
                    <th style="width: 90%">{{ student_name_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in group_data.students %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ student }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    {% endfor %}
</div>
{% endif %}

{% if groups[active_group].solutions %}
<div class="content-block">
    <h3 class="block-title solutions-title">{{ solutions_title }}</h3>
    <ul class="item-list">
        {% for solution in groups[active_group].solutions %}
        <li class="solution-item">
            <div class="item-text">{{ solution.text }}</div>
            {% if solution.source %}
            <div class="item-source">({{ get_source_text(solution.source) }})</div>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{% if groups[active_group].problems %}
<div class="content-block">
    <h3 class="block-title problems-title">{{ problems_title }}</h3>
    <ul class="item-list">
        {% for problem in groups[active_group].problems %}
        <li class="problem-item">
            <div class="item-text">{{ problem.text }}</div>
            {% if problem.source %}
            <div class="item-source">({{ get_source_text(problem.source) }})</div>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

</body>
</html>
'''

# --------------------------------------------------------------------------
# UTILITAIRES
# --------------------------------------------------------------------------

def clean_text(text):
    """Nettoyer le texte des caractères indésirables"""
    if not text:
        return ""
    unwanted = ['ـ', '●', '★', '◆', '■', '▲', '»', '«']
    for u in unwanted:
        text = text.replace(u, '')
    text = ' '.join(text.split())
    return text.strip()

def get_source_text(source):
    """Traduire le type de source"""
    source_map = {
        'json': 'Recommandé',
        'global': 'Approuvé',
        'personal': 'Personnel',
        'new': 'Nouveau'
    }
    return source_map.get(source, source)

def get_language_context(data):
    """Déterminer le contexte linguistique (français ou arabe)"""
    
    # Vérifier d'abord si la matière est en français
    matiere = data.get('matiereName', '').lower()
    
    # Liste des matières françaises
    french_subjects = [
        "communication orale", "lecture", "production écrite",
        "mathématiques", "éveil scientifique", "éducation islamique",
        "éducation technologique", "éducation musicale", "éducation artistique",
        "éducation physique", "grammaire", "expression orale et récitation",
        "écriture", "dictée", "langue", "anglais", "histoire", "géographie",
        "éducation civique", "français"
    ]
    
    # Mots-clés français
    french_keywords = ['expression', 'oral', 'lecture', 'production', 'écrit',
                      'écriture', 'dictée', 'langue', 'français', 'anglais',
                      'mathématiques', 'histoire', 'géographie']
    
    # Vérifier si la matière est dans la liste française
    is_fr = any(subject in matiere for subject in french_subjects)
    
    # Sinon, vérifier les mots-clés
    if not is_fr:
        is_fr = any(keyword in matiere for keyword in french_keywords)
    
    # Pour le nom du groupe, vérifier aussi les traductions
    group_name = data.get('groupName', '').lower()
    french_group_keywords = ['groupe de traitement', 'groupe de soutien', 
                            "groupe d'excellence", 'traitement', 'soutien', 
                            'excellence']
    
    if not is_fr and group_name:
        is_fr = any(keyword in group_name for keyword in french_group_keywords)

    if is_fr:
        return {
            'lang': 'fr',
            'text_direction': 'ltr',
            'text_align': 'left',
            'border_side': 'left',
            'print_button_position': 'right',
            'font_family': "'Calibri', 'Arial', sans-serif",

            'page_title': "Rapport Pédagogique - Plan de Traitement",
            'main_title': "RAPPORT PÉDAGOGIQUE",
            'print_button_text': "Imprimer",
            'basic_info_title': "INFORMATIONS GÉNÉRALES",
            'classification_title': "CLASSIFICATION DES APPRENANTS",
            'solutions_title': "SOLUTIONS PROPOSÉES",
            'problems_title': "ANALYSE DES DIFFICULTÉS",

            'school_label': "Établissement",
            'teacher_label': "Enseignant(e)",
            'class_label': "Classe",
            'subject_label': "Matière",
            'criteria_label': "Critère d'évaluation",
            'sub_criteria_label': "Sous-critère",
            'group_label': "Groupe",
            'date_label': "Date",
            'student_name_label': "Nom de l'apprenant",
            'student_label': "élève(s)",
            'students_list_label': "Liste des apprenants",
            'level_label': "Niveau",
            
            'group_titles': {
                'treatment': "GROUPE DE TRAITEMENT",
                'support': "GROUPE DE SOUTIEN", 
                'excellence': "GROUPE D'EXCELLENCE",
            },
            'treatment_level_label': "Traitement",
            'support_level_label': "Soutien",
            'excellence_level_label': "Excellence",
            
            # Fonction pour les templates
            'get_source_text': get_source_text,
        }

    # Arabic
    return {
        'lang': 'ar',
        'text_direction': 'rtl',
        'text_align': 'right',
        'border_side': 'right',
        'print_button_position': 'left',
        'font_family': "'Traditional Arabic', 'Arial', sans-serif",

        'page_title': "تقرير تربوي - خطة العلاج",
        'main_title': "تقرير تربوي",
        'print_button_text': "طباعة",
        'basic_info_title': "المعلومات العامة",
        'classification_title': "تصنيف المتعلمين",
        'solutions_title': "الحلول المقترحة",
        'problems_title': "تحليل الصعوبات",

        'school_label': "المؤسسة",
        'teacher_label': "الأستاذ(ة)",
        'class_label': "القسم",
        'subject_label': "المادة",
        'criteria_label': "معيار التقويم",
        'sub_criteria_label': "المعيار الفرعي",
        'group_label': "المجموعة",
        'date_label': "التاريخ",
        'student_name_label': "اسم المتعلم",
        'student_label': "طالب(ة)",
        'students_list_label': "قائمة المتعلمين",
        'level_label': "المستوى",
        
        'group_titles': {
            'treatment': "مجموعة العلاج",
            'support': "مجموعة الدعم",
            'excellence': "مجموعة التميز",
        },
        'treatment_level_label': "علاج",
        'support_level_label': "دعم",
        'excellence_level_label': "تميز",
        
        # Fonction pour les templates
        'get_source_text': lambda source: {
            'json': 'موصى به',
            'global': 'معتمد',
            'personal': 'شخصي',
            'new': 'جديد'
        }.get(source, source),
    }

# --------------------------------------------------------------------------
# ROUTE PRINCIPALE
# --------------------------------------------------------------------------
@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    
    print("📥 Données reçues:")
    print(f"   - Mode: {'Complet' if data.get('isCompleteReport', False) else 'Groupe unique'}")
    print(f"   - École: {data.get('schoolName')}")
    print(f"   - Classe: {data.get('className')}")
    print(f"   - Matière: {data.get('matiereName')}")
    print(f"   - Groupe: {data.get('groupName', 'Non spécifié')}")

    required = ['schoolName', 'profName', 'className', 'matiereName', 'baremeName']
    if any(key not in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    lang_ctx = get_language_context(data)

    # Mode rapport complet
    if data.get('isCompleteReport', False):
        print("🔄 Génération du rapport COMPLET")
        
        context = {
            **lang_ctx,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'schoolName': data['schoolName'],
            'profName': data['profName'],
            'className': data['className'],
            'matiereName': data['matiereName'],
            'baremeName': data['baremeName'],
            'sousBaremeName': data.get('sousBaremeName', ''),
            'is_complete_report': True,
        }

        # Initialiser les groupes
        groups = {
            'treatment': {'students': [], 'solutions': [], 'problems': []},
            'support': {'students': [], 'solutions': [], 'problems': []},
            'excellence': {'students': [], 'solutions': [], 'problems': []},
        }
        
        # Remplir avec les données reçues
        if 'groups' in data:
            for group_key in ['treatment', 'support', 'excellence']:
                if group_key in data['groups']:
                    group_data = data['groups'][group_key]
                    
                    # Étudiants
                    groups[group_key]['students'] = group_data.get('students', [])
                    
                    # Solutions
                    solutions = []
                    for sol in group_data.get('solutions', []):
                        if isinstance(sol, dict):
                            text = clean_text(sol.get('text', ''))
                            source = sol.get('source', '')
                        else:
                            text = clean_text(str(sol))
                            source = ''
                        if text:
                            solutions.append({'text': text, 'source': source})
                    groups[group_key]['solutions'] = solutions
                    
                    # Problèmes
                    problems = []
                    for prob in group_data.get('problems', []):
                        if isinstance(prob, dict):
                            text = clean_text(prob.get('text', ''))
                            source = prob.get('source', '')
                        else:
                            text = clean_text(str(prob))
                            source = ''
                        if text:
                            problems.append({'text': text, 'source': source})
                    groups[group_key]['problems'] = problems
        
        context['groups'] = groups
        
        print("📊 Statistiques du rapport complet:")
        for group_key in ['treatment', 'support', 'excellence']:
            print(f"   - {group_key}: {len(groups[group_key]['students'])} élèves, "
                  f"{len(groups[group_key]['solutions'])} solutions, "
                  f"{len(groups[group_key]['problems'])} problèmes")

        html = render_template_string(COMPLETE_REPORT_TEMPLATE, **context)
    
    # Mode groupe unique
    else:
        print("🔄 Génération du rapport GROUPE UNIQUE")
        
        # Déterminer quel groupe est actif
        active_group = None
        group_color = '#3498db'  # Couleur par défaut (bleu)
        
        if 'groups' in data:
            for group_key in ['treatment', 'support', 'excellence']:
                if group_key in data['groups'] and data['groups'][group_key]:
                    active_group = group_key
                    if group_key == 'treatment':
                        group_color = '#e74c3c'  # Rouge
                    elif group_key == 'support':
                        group_color = '#f39c12'  # Orange
                    else:
                        group_color = '#27ae60'  # Vert
                    break
        
        if not active_group:
            return jsonify({'error': 'No active group found'}), 400
        
        context = {
            **lang_ctx,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'schoolName': data['schoolName'],
            'profName': data['profName'],
            'className': data['className'],
            'matiereName': data['matiereName'],
            'baremeName': data['baremeName'],
            'sousBaremeName': data.get('sousBaremeName', ''),
            'group_name': data.get('groupName', lang_ctx['group_titles'].get(active_group, '')),
            'group_color': group_color,
            'active_group': active_group,
        }

        # Initialiser tous les groupes
        groups = {
            'treatment': {'students': [], 'solutions': [], 'problems': []},
            'support': {'students': [], 'solutions': [], 'problems': []},
            'excellence': {'students': [], 'solutions': [], 'problems': []},
        }
        
        # Remplir les données
        if 'groups' in data:
            for group_key in ['treatment', 'support', 'excellence']:
                if group_key in data['groups']:
                    group_data = data['groups'][group_key]
                    
                    # Étudiants
                    groups[group_key]['students'] = group_data.get('students', [])
                    
                    # Solutions
                    solutions = []
                    for sol in group_data.get('solutions', []):
                        if isinstance(sol, dict):
                            text = clean_text(sol.get('text', ''))
                            source = sol.get('source', '')
                        else:
                            text = clean_text(str(sol))
                            source = ''
                        if text:
                            solutions.append({'text': text, 'source': source})
                    groups[group_key]['solutions'] = solutions
                    
                    # Problèmes
                    problems = []
                    for prob in group_data.get('problems', []):
                        if isinstance(prob, dict):
                            text = clean_text(prob.get('text', ''))
                            source = prob.get('source', '')
                        else:
                            text = clean_text(str(prob))
                            source = ''
                        if text:
                            problems.append({'text': text, 'source': source})
                    groups[group_key]['problems'] = problems
        
        context['groups'] = groups
        
        print(f"📊 Statistiques du groupe {active_group}:")
        print(f"   - Élèves: {len(groups[active_group]['students'])}")
        print(f"   - Solutions: {len(groups[active_group]['solutions'])}")
        print(f"   - Problèmes: {len(groups[active_group]['problems'])}")

        html = render_template_string(SINGLE_GROUP_TEMPLATE, **context)

    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
