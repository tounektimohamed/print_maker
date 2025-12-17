from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------------------
# TEMPLATE HTML COMPLET AVEC CLASSIFICATION
# --------------------------------------------------------------------------
TREATMENT_PLAN_TEMPLATE = '''
<!DOCTYPE html>
<html dir="{{ text_direction }}" lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
    <style>
        /* ====================== RESET ====================== */
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

        /* ====================== HEADER ====================== */
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

        /* ====================== INFO GRID ====================== */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .info-item {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 4px;
            background: #f9f9f9;
        }

        .info-label {
            font-weight: bold;
            color: #444;
            font-size: 9pt;
            margin-bottom: 5px;
        }

        .info-value {
            font-size: 10pt;
        }

        /* ====================== SECTIONS ====================== */
        .section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 14pt;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #3498db;
            font-weight: bold;
            text-align: {{ text_align }};
        }

        /* ====================== CLASSIFICATION TABLES ====================== */
        .classification-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 10pt;
        }

        .classification-table thead {
            background-color: #2c3e50;
            color: white;
        }

        .classification-table th {
            padding: 12px;
            text-align: {{ text_align }};
            font-weight: bold;
            border: 1px solid #2c3e50;
        }

        .classification-table td {
            padding: 10px 12px;
            border: 1px solid #ddd;
            text-align: {{ text_align }};
        }

        .classification-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .group-section {
            margin-bottom: 25px;
        }

        .group-header {
            font-size: 13pt;
            font-weight: bold;
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 4px;
            color: white;
        }

        .group-treatment {
            background-color: #e74c3c;
        }

        .group-support {
            background-color: #f39c12;
        }

        .group-excellence {
            background-color: #27ae60;
        }

        /* ====================== SOLUTIONS AND PROBLEMS ====================== */
        .content-block {
            margin-bottom: 25px;
        }

        .block-title {
            font-size: 13pt;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
        }

        .item-list {
            list-style-type: none;
            padding: 0;
        }

        .solution-item, .problem-item {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 4px;
            border-{{ border_side }}: 4px solid;
            text-align: {{ text_align }};
        }

        .solution-item {
            background-color: #f8fff8;
            border-color: #27ae60;
        }

        .problem-item {
            background-color: #fff8f8;
            border-color: #e74c3c;
        }

        .item-text {
            font-size: 11pt;
            line-height: 1.6;
        }

        /* ====================== SIGNATURE ====================== */
        .signature-area {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: {{ text_align }};
        }

        .signature-line {
            display: inline-block;
            width: 200px;
            border-bottom: 1px solid #333;
            margin: 0 30px;
        }

        .signature-label {
            font-size: 9pt;
            color: #555;
            margin-top: 5px;
        }

        /* ====================== PRINT ====================== */
        @media print {
            @page {
                size: A4;
                margin: 1.5cm;
            }
            
            body {
                padding: 0;
                margin: 0;
                font-size: 11pt;
            }
            
            .print-button {
                display: none;
            }
            
            .section {
                margin-bottom: 20px;
            }
            
            .solution-item, .problem-item {
                page-break-inside: avoid;
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
    
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label">{{ teacher_label }}</div>
            <div class="info-value">{{ profName }}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">{{ class_label }}</div>
            <div class="info-value">{{ className }}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">{{ subject_label }}</div>
            <div class="info-value">{{ matiereName }}</div>
        </div>
        
        <div class="info-item">
            <div class="info-label">{{ criteria_label }}</div>
            <div class="info-value">{{ baremeName }}</div>
        </div>
        
        {% if sousBaremeName %}
        <div class="info-item">
            <div class="info-label">{{ sub_criteria_label }}</div>
            <div class="info-value">{{ sousBaremeName }}</div>
        </div>
        {% endif %}
        
        {% if groupName %}
        <div class="info-item">
            <div class="info-label">{{ group_label }}</div>
            <div class="info-value">{{ groupName }}</div>
        </div>
        {% endif %}
    </div>
</div>

{% if groups and (groups.treatment or groups.support or groups.excellence) %}
<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>
    
    {% if groups.treatment %}
    <div class="group-section">
        <div class="group-header group-treatment">{{ treatment_group_label }} ({{ groups.treatment|length }})</div>
        <table class="classification-table">
            <thead>
                <tr>
                    <th style="width: 5%">#</th>
                    <th style="width: 85%">{{ student_name_label }}</th>
                    <th style="width: 10%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.treatment %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ treatment_level_label }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    
    {% if groups.support %}
    <div class="group-section">
        <div class="group-header group-support">{{ support_group_label }} ({{ groups.support|length }})</div>
        <table class="classification-table">
            <thead>
                <tr>
                    <th style="width: 5%">#</th>
                    <th style="width: 85%">{{ student_name_label }}</th>
                    <th style="width: 10%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.support %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ support_level_label }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    
    {% if groups.excellence %}
    <div class="group-section">
        <div class="group-header group-excellence">{{ excellence_group_label }} ({{ groups.excellence|length }})</div>
        <table class="classification-table">
            <thead>
                <tr>
                    <th style="width: 5%">#</th>
                    <th style="width: 85%">{{ student_name_label }}</th>
                    <th style="width: 10%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.excellence %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ excellence_level_label }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
</div>
{% endif %}

{% if solutions %}
<div class="section">
    <h2 class="section-title">{{ solutions_title }}</h2>
    
    <ul class="item-list">
        {% for item in solutions %}
        <li class="solution-item">
            <div class="item-text">{{ item.text }}</div>
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

{% if problems %}
<div class="section">
    <h2 class="section-title">{{ problems_title }}</h2>
    
    <ul class="item-list">
        {% for item in problems %}
        <li class="problem-item">
            <div class="item-text">{{ item.text }}</div>
        </li>
        {% endfor %}
    </ul>
</div>
{% endif %}

<div class="signature-area">
    <div style="display: inline-block; text-align: center; margin: 0 50px;">
        <div class="signature-line"></div>
        <div class="signature-label">{{ signature_label }}</div>
    </div>
    
    <div style="display: inline-block; text-align: center; margin: 0 50px;">
        <div class="signature-line"></div>
        <div class="signature-label">{{ date_label }}</div>
    </div>
</div>

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
    # Supprimer les caractères spéciaux inutiles
    unwanted = ['ـ', '●', '★', '◆', '■', '▲', '»', '«']
    for u in unwanted:
        text = text.replace(u, '')
    # Nettoyer les espaces multiples
    text = ' '.join(text.split())
    return text.strip()


def get_language_context(data):
    """Déterminer le contexte linguistique (français ou arabe)"""
    
    french_subjects = {
        "expression orale et récitation", "lecture", "production écrite",
        "écriture", "dictée", "langue", "langue française", "français",
        "communication orale", "mathématiques", "éveil scientifique",
        "éducation islamique", "éducation technologique", "éducation musicale",
        "éducation artistique", "éducation physique", "grammaire", "anglais",
        "histoire", "géographie", "éducation civique"
    }

    matiere = data.get('matiereName', '').lower()
    
    # Vérifier si la matière est en français
    is_fr = any(keyword in matiere.lower() for keyword in french_subjects)
    
    # Vérifier aussi si le nom de la matière est déjà en français
    if not is_fr:
        # Vérifier les mots clés français
        french_keywords = ['expression', 'oral', 'lecture', 'production', 'écrit', 
                          'écriture', 'dictée', 'langue', 'français', 'anglais',
                          'mathématiques', 'histoire', 'géographie']
        is_fr = any(keyword in matiere for keyword in french_keywords)

    if is_fr:
        return {
            'lang': 'fr',
            'text_direction': 'ltr',
            'text_align': 'left',
            'border_side': 'left',
            'print_button_position': 'right',
            'font_family': "'Calibri', 'Arial', sans-serif",

            # Texts
            'page_title': "Rapport Pédagogique - Plan de Traitement",
            'main_title': "RAPPORT PÉDAGOGIQUE",
            'print_button_text': "Imprimer",
            'basic_info_title': "INFORMATIONS GÉNÉRALES",
            'classification_title': "CLASSIFICATION DES APPRENANTS",
            'solutions_title': "SOLUTIONS PROPOSÉES",
            'problems_title': "ANALYSE DES DIFFICULTÉS",

            # Labels
            'school_label': "Établissement",
            'teacher_label': "Enseignant(e)",
            'class_label': "Classe",
            'subject_label': "Matière",
            'criteria_label': "Critère d'évaluation",
            'sub_criteria_label': "Sous-critère",
            'group_label': "Groupe",
            'date_label': "Date",
            'student_name_label': "Nom de l'apprenant",
            'level_label': "Niveau",
            
            # Group labels
            'treatment_group_label': "GROUPE DE TRAITEMENT",
            'support_group_label': "GROUPE DE SOUTIEN", 
            'excellence_group_label': "GROUPE D'EXCELLENCE",
            'treatment_level_label': "Traitement",
            'support_level_label': "Soutien",
            'excellence_level_label': "Excellence",
            
            # Signature
            'signature_label': "Signature et cachet",
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

        # Labels
        'school_label': "المؤسسة",
        'teacher_label': "الأستاذ(ة)",
        'class_label': "القسم",
        'subject_label': "المادة",
        'criteria_label': "معيار التقويم",
        'sub_criteria_label': "المعيار الفرعي",
        'group_label': "المجموعة",
        'date_label': "التاريخ",
        'student_name_label': "اسم المتعلم",
        'level_label': "المستوى",
        
        # Group labels
        'treatment_group_label': "مجموعة العلاج",
        'support_group_label': "مجموعة الدعم",
        'excellence_group_label': "مجموعة التميز",
        'treatment_level_label': "علاج",
        'support_level_label': "دعم",
        'excellence_level_label': "تميز",
        
        # Signature
        'signature_label': "التوقيع والختم",
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
    print(f"   - École: {data.get('schoolName')}")
    print(f"   - Professeur: {data.get('profName')}")
    print(f"   - Classe: {data.get('className')}")
    print(f"   - Matière: {data.get('matiereName')}")
    print(f"   - Groupe spécifique: {data.get('groupName', 'Non spécifié')}")

    # Vérification des champs requis
    required = ['schoolName', 'profName', 'className', 'matiereName', 'baremeName']
    if any(key not in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    # Contexte linguistique
    lang_ctx = get_language_context(data)

    # Initialiser le contexte
    context = {
        **lang_ctx,
        'date': datetime.now().strftime('%d/%m/%Y'),
        'schoolName': data['schoolName'],
        'profName': data['profName'],
        'className': data['className'],
        'matiereName': data['matiereName'],
        'baremeName': data['baremeName'],
        'sousBaremeName': data.get('sousBaremeName', ''),
        'groupName': data.get('groupName', '')
    }

    # Gestion des groupes d'étudiants
    groups = {
        'treatment': [],
        'support': [],
        'excellence': []
    }
    
    if 'groups' in data:
        groups = {
            'treatment': [{'name': n} for n in data['groups'].get('treatment', [])],
            'support': [{'name': n} for n in data['groups'].get('support', [])],
            'excellence': [{'name': n} for n in data['groups'].get('excellence', [])]
        }
        print(f"📊 Classification reçue:")
        print(f"   - Groupe traitement: {len(groups['treatment'])} élèves")
        print(f"   - Groupe soutien: {len(groups['support'])} élèves")
        print(f"   - Groupe excellence: {len(groups['excellence'])} élèves")
    
    context['groups'] = groups

    # Préparation des solutions et problèmes
    solutions = []
    problems = []
    
    # Mode sélection personnalisée
    if 'selectedItems' in data:
        print("🔄 Mode: Sélection personnalisée")
        
        # Solutions sélectionnées
        selected_solutions = data['selectedItems'].get('solutions', [])
        print(f"   - Solutions sélectionnées: {len(selected_solutions)}")
        
        for sol in selected_solutions:
            if isinstance(sol, dict):
                text = sol.get('text', sol.get('solution', ''))
            else:
                text = sol
            
            cleaned_text = clean_text(text)
            if cleaned_text:
                solutions.append({
                    'text': cleaned_text,
                })
                print(f"     ✓ Solution: {cleaned_text[:50]}...")
        
        # Problèmes sélectionnés
        selected_problems = data['selectedItems'].get('problems', [])
        print(f"   - Problèmes sélectionnés: {len(selected_problems)}")
        
        for prob in selected_problems:
            if isinstance(prob, dict):
                text = prob.get('text', prob.get('probleme', ''))
            else:
                text = prob
            
            cleaned_text = clean_text(text)
            if cleaned_text:
                problems.append({
                    'text': cleaned_text,
                })
                print(f"     ✓ Problème: {cleaned_text[:50]}...")
    
    # Mode complet (toutes les données)
    elif 'solutions' in data:
        print("🔄 Mode: Toutes les données")
        
        # Solutions par défaut
        default = data['solutions'].get('default', {})
        if default.get('solution'):
            cleaned = clean_text(default['solution'])
            if cleaned:
                solutions.append({
                    'text': cleaned,
                    'source': 'default',
                })
        
        if default.get('probleme'):
            cleaned = clean_text(default['probleme'])
            if cleaned:
                problems.append({
                    'text': cleaned,
                    'source': 'default',
                })
        
        # Propositions utilisateur
        for proposal in data['solutions'].get('userProposals', []):
            if proposal.get('solution'):
                cleaned = clean_text(proposal['solution'])
                if cleaned:
                    solutions.append({
                        'text': cleaned,
                        'source': 'personal',
                    })
            
            if proposal.get('probleme'):
                cleaned = clean_text(proposal['probleme'])
                if cleaned:
                    problems.append({
                        'text': cleaned,
                        'source': 'personal',
                    })
        
        # Propositions globales
        for proposal in data['solutions'].get('globalProposals', []):
            if proposal.get('solution'):
                cleaned = clean_text(proposal['solution'])
                if cleaned:
                    solutions.append({
                        'text': cleaned,
                        'source': 'global',
                    })
            
            if proposal.get('probleme'):
                cleaned = clean_text(proposal['probleme'])
                if cleaned:
                    problems.append({
                        'text': cleaned,
                        'source': 'global',
                    })

    print(f"📊 Contenu du rapport:")
    print(f"   - Solutions totales: {len(solutions)}")
    print(f"   - Problèmes totaux: {len(problems)}")

    # Ajouter au contexte
    context['solutions'] = solutions
    context['problems'] = problems

    # Générer le HTML
    html = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
