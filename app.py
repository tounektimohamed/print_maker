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
</div>

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

<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>

    {% for group_key, group_title in group_titles.items() %}
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
    {% endfor %}
</div>

<div class="section">
    <h2 class="section-title">{{ analysis_title }}</h2>

    {% for block_title, items in solution_blocks.items() %}
    <div class="solution-block">
        <h3 class="solution-block-title">{{ block_title }}</h3>

        {% if items %}
            {% for item in items %}
            <div class="solution-point">
                <span class="point-number">{{ loop.index }}.</span>
                <span class="point-content">{{ item }}</span>
            </div>
            {% endfor %}
        {% else %}
            <p>{{ no_items_text }}</p>
        {% endif %}
    </div>
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
    if not text:
        return []
    unwanted = ['ـ', '●', '★']
    for u in unwanted:
        text = text.replace(u, '')
    return [line.strip() for line in text.split('\n') if line.strip()]


def unify_solutions(data):
    solutions = set()
    problems = set()

    blocks = (
        data['solutions'].get('default', {}),
        *data['solutions'].get('userProposals', []),
        *data['solutions'].get('globalProposals', [])
    )

    for block in blocks:
        for item in clean_text(block.get('solution', '')):
            solutions.add(item)
        for item in clean_text(block.get('probleme', '')):
            problems.add(item)

    return {
        'solution': sorted(solutions),
        'probleme': sorted(problems)
    }


def get_language_context(data):

    french_subjects = {
        "expression orale et récitation", "lecture", "production écrite",
        "écriture", "dictée", "langue", "langue française", "français"
    }

    matiere = data.get('matiereName', '').lower()
    is_fr = any(key in matiere for key in french_subjects)

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
            'solutions_title': "Solutions proposées",
            'problems_title': "Analyse des erreurs",

            # Labels (manquants corrigés)
            'school_label': "Établissement",
            'teacher_label': "Enseignant(e)",
            'class_label': "Classe",
            'subject_label': "Matière",
            'criteria_label': "Barème",
            'sub_criteria_label': "Sous-barème",

            'group_titles': {
                'treatment': "Groupe de traitement",
                'support': "Groupe de soutien",
                'excellence': "Groupe d'excellence"
            },
            'student_name_label': "Nom de l'élève",
            'group_label': "Groupe",
            'no_items_text': "Aucune donnée disponible",
            'footer_text': "Rapport généré automatiquement"
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
        'solutions_title': "الحلول المقترحة",
        'problems_title': "تحليل الأخطاء",

        # Labels (manquants corrigés)
        'school_label': "المؤسسة",
        'teacher_label': "الأستاذ(ة)",
        'class_label': "المستوى",
        'subject_label': "المادة",
        'criteria_label': "المعيار",
        'sub_criteria_label': "المعيار الفرعي",

        'group_titles': {
            'treatment': "مجموعة العلاج",
            'support': "مجموعة الدعم",
            'excellence': "مجموعة التميز"
        },
        'student_name_label': "اسم المتعلم(ة)",
        'group_label': "المجموعة",
        'no_items_text': "لا توجد بيانات",
        'footer_text': "تم إنشاء التقرير تلقائياً"
    }


# --------------------------------------------------------------------------
# ROUTE PRINCIPALE
# --------------------------------------------------------------------------
@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    required = ['schoolName', 'profName', 'className', 'matiereName', 'baremeName', 'groups', 'solutions']
    if any(key not in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    # Nettoyage et fusion
    solutions_unified = unify_solutions(data)

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

    context = {
        **lang_ctx,
        'date': datetime.now().strftime('%Y/%m/%d %H:%M'),
        'info_items': info_items,
        'groups': {
            'treatment': [{'name': n} for n in data['groups'].get('treatment', [])],
            'support': [{'name': n} for n in data['groups'].get('support', [])],
            'excellence': [{'name': n} for n in data['groups'].get('excellence', [])]
        },
        'solution_blocks': {
            lang_ctx['solutions_title']: solutions_unified['solution'],
            lang_ctx['problems_title']: solutions_unified['probleme']
        }
    }

    html = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(debug=True)
