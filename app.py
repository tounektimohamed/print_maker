from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------------------
# TEMPLATE HTML PRINCIPAL
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
            font-size: 11pt;
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

        .header .subtitle {
            font-size: 14pt;
            color: #7f8c8d;
            margin-bottom: 10px;
        }

        .header-info {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 10pt;
            color: #555;
        }

        /* ====================== SECTIONS ====================== */
        .section {
            margin-bottom: 25px;
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 14pt;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
            text-align: {{ text_align }};
        }

        /* ====================== INFO GRID ====================== */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
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

        /* ====================== GROUP TABLES ====================== */
        .group-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 9pt;
        }

        .group-table thead {
            background-color: #2c3e50;
            color: white;
        }

        .group-table th {
            padding: 10px;
            text-align: {{ text_align }};
            font-weight: bold;
            border: 1px solid #2c3e50;
        }

        .group-table td {
            padding: 8px 10px;
            border: 1px solid #ddd;
            text-align: {{ text_align }};
        }

        .group-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .group-title {
            font-size: 12pt;
            font-weight: bold;
            margin: 15px 0 8px 0;
            color: #2c3e50;
            padding-{{ text_align }}: 10px;
            border-{{ text_align }}: 3px solid;
        }

        .group-title.treatment {
            border-color: #e74c3c;
            color: #e74c3c;
        }

        .group-title.support {
            border-color: #f39c12;
            color: #f39c12;
        }

        .group-title.excellence {
            border-color: #27ae60;
            color: #27ae60;
        }

        /* ====================== SOLUTIONS AND PROBLEMS ====================== */
        .content-block {
            margin-bottom: 25px;
        }

        .block-title {
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 12px;
            color: #2c3e50;
            padding-bottom: 5px;
            border-bottom: 2px solid #3498db;
        }

        .solution-item, .problem-item {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 4px;
            position: relative;
        }

        .solution-item {
            background-color: #f8f9fa;
            border-{{ border_side }}: 4px solid #27ae60;
        }

        .problem-item {
            background-color: #fff8f8;
            border-{{ border_side }}: 4px solid #e74c3c;
        }

        .item-content {
            font-size: 10pt;
            line-height: 1.5;
        }

        .item-source {
            position: absolute;
            {{ source_position }}: 10px;
            top: 10px;
            font-size: 8pt;
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: bold;
        }

        .source-default {
            background-color: #f39c12;
            color: white;
        }

        .source-global {
            background-color: #27ae60;
            color: white;
        }

        .source-personal {
            background-color: #3498db;
            color: white;
        }

        /* ====================== SIGNATURE AREA ====================== */
        .signature-area {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
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

        /* ====================== FOOTER ====================== */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #ddd;
            font-size: 8pt;
            color: #777;
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
                font-size: 10pt;
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
    <div class="subtitle">{{ report_subtitle }}</div>
    
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
    <div>
        <h3 class="group-title treatment">{{ treatment_group_label }}</h3>
        <table class="group-table">
            <thead>
                <tr>
                    <th style="width: 80%">{{ student_name_label }}</th>
                    <th style="width: 20%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.treatment %}
                <tr>
                    <td>{{ student.name }}</td>
                    <td>{{ treatment_level_label }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    
    {% if groups.support %}
    <div>
        <h3 class="group-title support">{{ support_group_label }}</h3>
        <table class="group-table">
            <thead>
                <tr>
                    <th style="width: 80%">{{ student_name_label }}</th>
                    <th style="width: 20%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.support %}
                <tr>
                    <td>{{ student.name }}</td>
                    <td>{{ support_level_label }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    
    {% if groups.excellence %}
    <div>
        <h3 class="group-title excellence">{{ excellence_group_label }}</h3>
        <table class="group-table">
            <thead>
                <tr>
                    <th style="width: 80%">{{ student_name_label }}</th>
                    <th style="width: 20%">{{ level_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups.excellence %}
                <tr>
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

<div class="section">
    <h2 class="section-title">{{ analysis_title }}</h2>
    
    <div class="content-block">
        <h3 class="block-title">{{ solutions_title }}</h3>
        
        {% if solutions %}
            {% for item in solutions %}
            <div class="solution-item">
                {% if item.source %}
                <div class="item-source source-{{ item.source }}">
                    {{ item.source_label }}
                </div>
                {% endif %}
                <div class="item-content">
                    {{ loop.index }}. {{ item.text }}
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div style="text-align: center; color: #777; font-style: italic; padding: 20px;">
                {{ no_solutions_text }}
            </div>
        {% endif %}
    </div>
    
    <div class="content-block">
        <h3 class="block-title">{{ problems_title }}</h3>
        
        {% if problems %}
            {% for item in problems %}
            <div class="problem-item">
                {% if item.source %}
                <div class="item-source source-{{ item.source }}">
                    {{ item.source_label }}
                </div>
                {% endif %}
                <div class="item-content">
                    {{ loop.index }}. {{ item.text }}
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div style="text-align: center; color: #777; font-style: italic; padding: 20px;">
                {{ no_problems_text }}
            </div>
        {% endif %}
    </div>
</div>

<div class="signature-area" style="text-align: {{ text_align }};">
    <div style="display: inline-block; text-align: center; margin: 0 50px;">
        <div class="signature-line"></div>
        <div class="signature-label">{{ signature_label }}</div>
    </div>
    
    <div style="display: inline-block; text-align: center; margin: 0 50px;">
        <div class="signature-line"></div>
        <div class="signature-label">{{ date_label }}</div>
    </div>
</div>

<div class="footer">
    <p>{{ footer_text }}</p>
    <p>{{ page_label }}: <span class="page-number"></span></p>
</div>

<script>
    // Numérotation des pages
    document.addEventListener('DOMContentLoaded', function() {
        const pageNumbers = document.querySelectorAll('.page-number');
        pageNumbers.forEach(el => {
            el.textContent = '1/1';
        });
        
        // Ajouter les sauts de page si nécessaire
        const items = document.querySelectorAll('.solution-item, .problem-item');
        let pageHeight = 0;
        const maxPageHeight = 900; // Hauteur approximative d'une page A4 en pixels
        
        items.forEach((item, index) => {
            const itemHeight = item.offsetHeight;
            if (pageHeight + itemHeight > maxPageHeight && index > 0) {
                item.style.pageBreakBefore = 'always';
                item.style.marginTop = '30px';
                pageHeight = itemHeight;
            } else {
                pageHeight += itemHeight;
            }
        });
    });
</script>

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
            'source_position': 'right',
            'print_button_position': 'right',
            'font_family': "'Calibri', 'Arial', sans-serif",

            # Texts
            'page_title': "Rapport Pédagogique - Plan de Traitement",
            'main_title': "RAPPORT PÉDAGOGIQUE",
            'report_subtitle': "Plan de traitement et analyse des difficultés",
            'print_button_text': "Imprimer",
            'basic_info_title': "INFORMATIONS GÉNÉRALES",
            'classification_title': "CLASSIFICATION DES APPRENANTS",
            'analysis_title': "ANALYSE ET PROPOSITIONS",
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
            
            # Source labels
            'source_default_label': "Recommandation",
            'source_global_label': "Approuvé",
            'source_personal_label': "Personnel",
            
            # Empty states
            'no_solutions_text': "Aucune solution proposée",
            'no_problems_text': "Aucune difficulté identifiée",
            
            # Signature
            'signature_label': "Signature et cachet",
            
            # Footer
            'footer_text': "Document administratif - Usage pédagogique interne",
            'page_label': "Page"
        }

    # Arabic
    return {
        'lang': 'ar',
        'text_direction': 'rtl',
        'text_align': 'right',
        'border_side': 'right',
        'source_position': 'left',
        'print_button_position': 'left',
        'font_family': "'Traditional Arabic', 'Arial', sans-serif",

        'page_title': "تقرير تربوي - خطة العلاج",
        'main_title': "تقرير تربوي",
        'report_subtitle': "خطة العلاج وتحليل الصعوبات",
        'print_button_text': "طباعة",
        'basic_info_title': "المعلومات العامة",
        'classification_title': "تصنيف المتعلمين",
        'analysis_title': "التحليل والاقتراحات",
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
        
        # Source labels
        'source_default_label': "موصى به",
        'source_global_label': "معتمد",
        'source_personal_label': "شخصي",
        
        # Empty states
        'no_solutions_text': "لا توجد حلول مقترحة",
        'no_problems_text': "لا توجد صعوبات محددة",
        
        # Signature
        'signature_label': "التوقيع والختم",
        
        # Footer
        'footer_text': "وثيقة إدارية - للاستخدام التربوي الداخلي",
        'page_label': "صفحة"
    }


# --------------------------------------------------------------------------
# ROUTE PRINCIPALE
# --------------------------------------------------------------------------
@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

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
    
    context['groups'] = groups

    # Préparation des solutions et problèmes
    solutions = []
    problems = []
    
    # Mode sélection personnalisée
    if 'selectedItems' in data:
        # Solutions sélectionnées
        for sol in data['selectedItems'].get('solutions', []):
            if isinstance(sol, dict):
                text = sol.get('text', sol.get('solution', ''))
                source = sol.get('source', 'default')
            else:
                text = sol
                source = 'default'
            
            cleaned_text = clean_text(text)
            if cleaned_text:
                solutions.append({
                    'text': cleaned_text,
                    'source': source,
                    'source_label': lang_ctx.get(f'source_{source}_label', '')
                })
        
        # Problèmes sélectionnés
        for prob in data['selectedItems'].get('problems', []):
            if isinstance(prob, dict):
                text = prob.get('text', prob.get('probleme', ''))
                source = prob.get('source', 'default')
            else:
                text = prob
                source = 'default'
            
            cleaned_text = clean_text(text)
            if cleaned_text:
                problems.append({
                    'text': cleaned_text,
                    'source': source,
                    'source_label': lang_ctx.get(f'source_{source}_label', '')
                })
    
    # Mode complet (toutes les données)
    elif 'solutions' in data:
        # Solutions par défaut
        default = data['solutions'].get('default', {})
        if default.get('solution'):
            cleaned = clean_text(default['solution'])
            if cleaned:
                solutions.append({
                    'text': cleaned,
                    'source': 'default',
                    'source_label': lang_ctx.get('source_default_label', '')
                })
        
        if default.get('probleme'):
            cleaned = clean_text(default['probleme'])
            if cleaned:
                problems.append({
                    'text': cleaned,
                    'source': 'default',
                    'source_label': lang_ctx.get('source_default_label', '')
                })
        
        # Propositions utilisateur
        for proposal in data['solutions'].get('userProposals', []):
            if proposal.get('solution'):
                cleaned = clean_text(proposal['solution'])
                if cleaned:
                    solutions.append({
                        'text': cleaned,
                        'source': 'personal',
                        'source_label': lang_ctx.get('source_personal_label', '')
                    })
            
            if proposal.get('probleme'):
                cleaned = clean_text(proposal['probleme'])
                if cleaned:
                    problems.append({
                        'text': cleaned,
                        'source': 'personal',
                        'source_label': lang_ctx.get('source_personal_label', '')
                    })
        
        # Propositions globales
        for proposal in data['solutions'].get('globalProposals', []):
            if proposal.get('solution'):
                cleaned = clean_text(proposal['solution'])
                if cleaned:
                    solutions.append({
                        'text': cleaned,
                        'source': 'global',
                        'source_label': lang_ctx.get('source_global_label', '')
                    })
            
            if proposal.get('probleme'):
                cleaned = clean_text(proposal['probleme'])
                if cleaned:
                    problems.append({
                        'text': cleaned,
                        'source': 'global',
                        'source_label': lang_ctx.get('source_global_label', '')
                    })

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
