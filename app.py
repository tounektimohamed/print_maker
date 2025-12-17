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
            line-height: 1.8;
            background-color: #f9f9f9;
            color: #333;
            padding: 20px;
            font-size: 16pt;
        }

        /* ====================== HEADER ====================== */
        .header {
            text-align: center;
            padding: 25px;
            margin: 0 auto 30px;
            border-radius: 10px;
            max-width: 1000px;
            color: white;
            background: linear-gradient(135deg, #2c3e50, #3498db);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .header h1 {
            font-size: 30pt;
            margin-bottom: 10px;
        }

        .date {
            font-size: 14pt;
            opacity: 0.9;
        }

        /* ====================== SECTIONS ====================== */
        .section {
            background: white;
            padding: 25px;
            margin: 0 auto 30px;
            border-radius: 10px;
            max-width: 1000px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            page-break-inside: avoid;
        }

        .section-title {
            font-size: 22pt;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
            text-align: {{ text_align }};
            position: relative;
        }

        .section-title::after {
            content: "";
            position: absolute;
            {{ section_after_position }}: 0;
            bottom: -2px;
            width: 150px;
            height: 3px;
            background: #3498db;
        }

        /* ====================== GRID ====================== */
        .info-grid {
            display: grid;
            gap: 15px;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            margin-top: 20px;
        }

        .info-label {
            font-weight: bold;
            color: #444;
            font-size: 15pt;
            margin-bottom: 5px;
        }

        .info-value {
            background: #f4f6f7;
            padding: 12px;
            border-radius: 8px;
            border-{{ border_side }}: 3px solid #3498db;
            font-size: 15pt;
        }

        /* ====================== GROUP TABLES ====================== */
        .group {
            margin-bottom: 35px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .group-title {
            font-size: 18pt;
            padding: 15px;
            text-align: {{ text_align }};
        }

        .group.treatment .group-title { background: #e74c3c; color: white; }
        .group.support .group-title   { background: #f39c12; color: white; }
        .group.excellence .group-title { background: #2ecc71; color: white; }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14pt;
        }

        th, td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            text-align: {{ text_align }};
        }

        th {
            background-color: #f5f5f5;
            font-weight: bold;
        }

        tr:nth-child(even) { background-color: #fafafa; }

        /* ====================== SOLUTIONS ====================== */
        .solution-block {
            background: #fbfcfd;
            border-{{ border_side }}: 4px solid #9b59b6;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
        }

        .solution-block-title {
            font-size: 18pt;
            color: #9b59b6;
            margin-bottom: 15px;
        }

        .solution-point {
            font-size: 15pt;
            margin: 10px 0;
            display: flex;
            gap: 10px;
        }

        .point-number {
            font-weight: bold;
            color: #9b59b6;
        }

        /* ====================== SELECTION SUMMARY ====================== */
        .selection-summary {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            text-align: {{ text_align }};
        }

        .summary-title {
            font-size: 18pt;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .stat-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 20pt;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 12pt;
            opacity: 0.9;
        }

        /* ====================== SOURCE BADGES ====================== */
        .source-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 10pt;
            font-weight: bold;
            margin: 5px;
        }

        .badge-json {
            background-color: #f39c12;
            color: white;
        }

        .badge-global {
            background-color: #2ecc71;
            color: white;
        }

        .badge-personal {
            background-color: #3498db;
            color: white;
        }

        /* ====================== FOOTER ====================== */
        .footer {
            text-align: center;
            padding-top: 20px;
            margin: 40px auto 20px;
            border-top: 1px solid #ccc;
            color: #777;
            font-size: 13pt;
            max-width: 1000px;
        }

        /* ====================== PRINT ====================== */
        @media print {
            @page { size: A4; margin: 0; }
            .print-button { display: none !important; }
            body { padding: 0; margin: 0; }
        }
    </style>
</head>
<body>

<button class="print-button" onclick="window.print()">
    {{ print_button_text }}
</button>

<div class="header">
    <h1>{{ main_title }}</h1>
    <div class="date">{{ report_date_label }}: {{ date }}</div>
    {% if group_name %}
    <div class="date" style="margin-top: 10px;">
        <strong>{{ group_name_label }}:</strong> {{ group_name }}
    </div>
    {% endif %}
</div>

{% if selection_counts %}
<div class="selection-summary">
    <h2 class="summary-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        {{ selection_title }}
    </h2>
    <div class="summary-stats">
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.total }}</div>
            <div class="stat-label">{{ total_selected_label }}</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.solutions }}</div>
            <div class="stat-label">{{ solutions_label }}</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.problems }}</div>
            <div class="stat-label">{{ problems_label }}</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.json }}</div>
            <div class="stat-label">{{ json_label }}</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.global }}</div>
            <div class="stat-label">{{ global_label }}</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{{ selection_counts.personal }}</div>
            <div class="stat-label">{{ personal_label }}</div>
        </div>
    </div>
</div>
{% endif %}

<div class="section">
    <h2 class="section-title">{{ basic_info_title }}</h2>
    <div class="info-grid">
        {% for label, value in info_items %}
        <div>
            <div class="info-label">{{ label }}</div>
            <div class="info-value">{{ value }}</div>
        </div>
        {% endfor %}
    </div>
</div>

{% if groups and (groups.treatment or groups.support or groups.excellence) %}
<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>

    {% for group_key, group_title in group_titles.items() %}
    {% if groups[group_key] %}
    <div class="group {{ group_key }}">
        <h3 class="group-title">{{ group_title }}</h3>

        <table>
            <thead>
                <tr>
                    <th>{{ student_name_label }}</th>
                    <th>{{ group_label }}</th>
                </tr>
            </thead>
            <tbody>
                {% for student in groups[group_key] %}
                <tr>
                    <td>{{ student.name }}</td>
                    <td>{{ group_title }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
    {% endfor %}
</div>
{% endif %}

<div class="section">
    <h2 class="section-title">{{ analysis_title }}</h2>

    {% for block_title, items in solution_blocks.items() %}
    {% if items %}
    <div class="solution-block">
        <h3 class="solution-block-title">{{ block_title }}</h3>

        {% for item in items %}
        <div class="solution-point">
            <span class="point-number">{{ loop.index }}.</span>
            <span class="point-content">{{ item.text }}</span>
            {% if item.source %}
            <span class="source-badge badge-{{ item.source }}">
                {{ item.source_label }}
            </span>
            {% endif %}
            {% if item.is_problem %}
            <span class="source-badge" style="background-color: #e74c3c; color: white;">
                {{ problem_label }}
            </span>
            {% else %}
            <span class="source-badge" style="background-color: #2ecc71; color: white;">
                {{ solution_label }}
            </span>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}
    {% endfor %}
</div>

<div class="footer">
    <p>{{ footer_text }} © {{ date[:4] }}</p>
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
    unwanted = ['ـ', '●', '★']
    for u in unwanted:
        text = text.replace(u, '')
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
            'section_after_position': 'left',
            'flex_direction': 'row',
            'bullet_margin_side': 'right',
            'font_family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",

            # Texts
            'page_title': "Plan de traitement et origine de l'erreur",
            'main_title': "Rapport du Plan de Traitement",
            'print_button_text': "Imprimer",
            'report_date_label': "Date du rapport",
            'basic_info_title': "Informations générales",
            'classification_title': "Classification des apprenants",
            'analysis_title': "Analyse des erreurs et propositions",
            'selection_title': "Résumé de la sélection",
            'solutions_title': "Solutions proposées",
            'problems_title': "Analyse des erreurs",

            # Labels
            'school_label': "Établissement",
            'teacher_label': "Enseignant(e)",
            'class_label': "Classe",
            'subject_label': "Matière",
            'criteria_label': "Barème",
            'sub_criteria_label': "Sous-barème",
            'group_name_label': "Groupe",

            'group_titles': {
                'treatment': "Groupe de traitement",
                'support': "Groupe de soutien",
                'excellence': "Groupe d'excellence"
            },
            
            'student_name_label': "Nom de l'élève",
            'group_label': "Groupe",
            'no_items_text': "Aucune donnée disponible",
            'footer_text': "Rapport généré automatiquement",
            
            # Nouveaux labels pour la sélection
            'total_selected_label': "Éléments sélectionnés",
            'solutions_label': "Solutions",
            'problems_label': "Problèmes",
            'json_label': "Recommandés",
            'global_label': "Approuvés",
            'personal_label': "Personnels",
            
            # Labels des sources
            'json_source_label': "Recommandé",
            'global_source_label': "Approuvé",
            'personal_source_label': "Personnel",
            
            # Labels type
            'solution_label': "Solution",
            'problem_label': "Problème"
        }

    # Arabic
    return {
        'lang': 'ar',
        'text_direction': 'rtl',
        'text_align': 'right',
        'border_side': 'right',
        'section_after_position': 'right',
        'flex_direction': 'row-reverse',
        'bullet_margin_side': 'left',
        'font_family': "'Amiri', 'Traditional Arabic', serif",

        'page_title': "خطة العلاج وأصل الخطأ",
        'main_title': "تقرير خطة العلاج",
        'print_button_text': "طباعة",
        'report_date_label': "تاريخ التقرير",
        'basic_info_title': "المعلومات الأساسية",
        'classification_title': "تصنيف المتعلمين",
        'analysis_title': "تحليل الأخطاء والاقتراحات",
        'selection_title': "ملخص التحديد",
        'solutions_title': "الحلول المقترحة",
        'problems_title': "تحليل الأخطاء",

        # Labels
        'school_label': "المؤسسة",
        'teacher_label': "الأستاذ(ة)",
        'class_label': "المستوى",
        'subject_label': "المادة",
        'criteria_label': "المعيار",
        'sub_criteria_label': "المعيار الفرعي",
        'group_name_label': "المجموعة",

        'group_titles': {
            'treatment': "مجموعة العلاج",
            'support': "مجموعة الدعم",
            'excellence': "مجموعة التميز"
        },
        
        'student_name_label': "اسم المتعلم(ة)",
        'group_label': "المجموعة",
        'no_items_text': "لا توجد بيانات",
        'footer_text': "تم إنشاء التقرير تلقائياً",
        
        # Nouveaux labels pour la sélection
        'total_selected_label': "العناصر المحددة",
        'solutions_label': "حلول",
        'problems_label': "مشاكل",
        'json_label': "موصى بها",
        'global_label': "معتمدة",
        'personal_label': "شخصية",
        
        # Labels des sources
        'json_source_label': "موصى به",
        'global_source_label': "معتمد",
        'personal_source_label': "شخصي",
        
        # Labels type
        'solution_label': "حل",
        'problem_label': "مشكلة"
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

    # Info affichées
    info_items = [
        (lang_ctx['school_label'], data['schoolName']),
        (lang_ctx['teacher_label'], data['profName']),
        (lang_ctx['class_label'], data['className']),
        (lang_ctx['subject_label'], data['matiereName']),
        (lang_ctx['criteria_label'], data['baremeName'])
    ]

    if data.get('sousBaremeName'):
        info_items.append(
            (lang_ctx['sub_criteria_label'], data['sousBaremeName'])
        )

    # Initialiser le contexte
    context = {
        **lang_ctx,
        'date': datetime.now().strftime('%Y/%m/%d %H:%M'),
        'info_items': info_items,
    }

    # Gestion des groupes d'étudiants
    if 'groups' in data:
        context['groups'] = {
            'treatment': [{'name': n} for n in data['groups'].get('treatment', [])],
            'support': [{'name': n} for n in data['groups'].get('support', [])],
            'excellence': [{'name': n} for n in data['groups'].get('excellence', [])]
        }
    else:
        context['groups'] = {
            'treatment': [],
            'support': [],
            'excellence': []
        }

    # Gestion du nom du groupe
    if 'groupName' in data:
        context['group_name'] = data['groupName']

    # Gestion des sélections (mode personnalisé)
    if 'selectedItems' in data:
        # Mode personnalisé : seulement les éléments sélectionnés
        context['selection_counts'] = data.get('selectionCounts', {})
        
        # Organiser les éléments par type (solution/problème)
        solution_blocks = {}
        
        # Solutions sélectionnées
        selected_solutions = data['selectedItems'].get('solutions', [])
        if selected_solutions:
            solution_items = []
            for sol in selected_solutions:
                # Vérifier si c'est un dict avec source ou juste une string
                if isinstance(sol, dict):
                    solution_items.append({
                        'text': clean_text(sol.get('text', sol.get('solution', ''))),
                        'source': sol.get('source', 'json'),
                        'source_label': lang_ctx.get(f"{sol.get('source', 'json')}_source_label", ""),
                        'is_problem': False
                    })
                else:
                    solution_items.append({
                        'text': clean_text(sol),
                        'source': 'json',
                        'source_label': lang_ctx.get('json_source_label', ""),
                        'is_problem': False
                    })
            
            if solution_items:
                solution_blocks[lang_ctx['solutions_title']] = solution_items
        
        # Problèmes sélectionnés
        selected_problems = data['selectedItems'].get('problems', [])
        if selected_problems:
            problem_items = []
            for prob in selected_problems:
                if isinstance(prob, dict):
                    problem_items.append({
                        'text': clean_text(prob.get('text', prob.get('probleme', ''))),
                        'source': prob.get('source', 'json'),
                        'source_label': lang_ctx.get(f"{prob.get('source', 'json')}_source_label", ""),
                        'is_problem': True
                    })
                else:
                    problem_items.append({
                        'text': clean_text(prob),
                        'source': 'json',
                        'source_label': lang_ctx.get('json_source_label', ""),
                        'is_problem': True
                    })
            
            if problem_items:
                solution_blocks[lang_ctx['problems_title']] = problem_items
        
        context['solution_blocks'] = solution_blocks
        
    else:
        # Mode complet : toutes les solutions fusionnées
        if 'solutions' in data:
            # Organiser les solutions par source
            all_solutions = []
            all_problems = []
            
            # Solutions par défaut (JSON)
            default = data['solutions'].get('default', {})
            if default.get('solution'):
                all_solutions.append({
                    'text': clean_text(default['solution']),
                    'source': 'json',
                    'source_label': lang_ctx.get('json_source_label', ""),
                    'is_problem': False
                })
            if default.get('probleme'):
                all_problems.append({
                    'text': clean_text(default['probleme']),
                    'source': 'json',
                    'source_label': lang_ctx.get('json_source_label', ""),
                    'is_problem': True
                })
            
            # Propositions utilisateur
            user_proposals = data['solutions'].get('userProposals', [])
            for proposal in user_proposals:
                if proposal.get('solution'):
                    all_solutions.append({
                        'text': clean_text(proposal['solution']),
                        'source': 'personal',
                        'source_label': lang_ctx.get('personal_source_label', ""),
                        'is_problem': False
                    })
                if proposal.get('probleme'):
                    all_problems.append({
                        'text': clean_text(proposal['probleme']),
                        'source': 'personal',
                        'source_label': lang_ctx.get('personal_source_label', ""),
                        'is_problem': True
                    })
            
            # Propositions globales
            global_proposals = data['solutions'].get('globalProposals', [])
            for proposal in global_proposals:
                if proposal.get('solution'):
                    all_solutions.append({
                        'text': clean_text(proposal['solution']),
                        'source': 'global',
                        'source_label': lang_ctx.get('global_source_label', ""),
                        'is_problem': False
                    })
                if proposal.get('probleme'):
                    all_problems.append({
                        'text': clean_text(proposal['probleme']),
                        'source': 'global',
                        'source_label': lang_ctx.get('global_source_label', ""),
                        'is_problem': True
                    })
            
            context['solution_blocks'] = {
                lang_ctx['solutions_title']: all_solutions,
                lang_ctx['problems_title']: all_problems
            }
        else:
            context['solution_blocks'] = {
                lang_ctx['solutions_title']: [],
                lang_ctx['problems_title']: []
            }

    # Générer le HTML
    html = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(debug=True)
