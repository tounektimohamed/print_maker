from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Configuration CORS simple pour le développement

TREATMENT_PLAN_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>خطة العلاج - طباعة</title>
    <style>
        /* Reset amélioré */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Amiri', 'Traditional Arabic', sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f9f9f9;
            padding: 20px;
            font-size: 16pt;
        }
        
        /* En-tête amélioré */
        .header {
            text-align: center;
            margin: 0 auto 30px;
            padding: 20px;
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 1000px;
        }
        
        .header h1 {
            font-size: 28pt;
            margin-bottom: 10px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .header .date {
            font-size: 14pt;
            opacity: 0.9;
        }
        
        /* Sections améliorées */
        .section {
            background: white;
            margin: 0 auto 30px;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            max-width: 1000px;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 22pt;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            position: relative;
        }
        
        .section-title::after {
            content: "";
            position: absolute;
            right: 0;
            bottom: -2px;
            width: 150px;
            height: 3px;
            background: #3498db;
        }
        
        /* Grille d'informations améliorée */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .info-item {
            margin-bottom: 15px;
        }
        
        .info-label {
            font-weight: bold;
            color: #555;
            font-size: 14pt;
            margin-bottom: 5px;
        }
        
        .info-value {
            padding: 10px;
            background: #f8f8f8;
            border-radius: 6px;
            border-right: 3px solid #3498db;
            font-size: 15pt;
        }
        
        /* Groupes d'élèves améliorés */
        .groups-container {
            margin-top: 30px;
        }
        
        .group {
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }
        
        .group-title {
            font-size: 18pt;
            padding: 15px;
            margin: 0;
        }
        
        .group.treatment .group-title {
            background-color: #e74c3c;
            color: white;
        }
        
        .group.support .group-title {
            background-color: #f39c12;
            color: white;
        }
        
        .group.excellence .group-title {
            background-color: #2ecc71;
            color: white;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14pt;
        }
        
        th {
            background-color: #f5f5f5;
            padding: 12px 15px;
            text-align: right;
            font-weight: bold;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Blocs de solutions améliorés */
        .solution-block {
            background: #f8f9fa;
            margin-bottom: 25px;
            padding: 20px;
            border-radius: 8px;
            border-right: 4px solid #9b59b6;
        }
        
        .solution-block-title {
            font-size: 18pt;
            color: #9b59b6;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .solution-block-title::before {
            content: "";
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #9b59b6;
            border-radius: 50%;
            margin-left: 10px;
        }
        
        .solution-point {
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            padding: 8px 0;
        }
        
        .bullet {
            color: #9b59b6;
            font-weight: bold;
            margin-left: 10px;
            margin-right: 8px;
            font-size: 16pt;
        }
        
        .point-number {
            color: #e74c3c;
            font-weight: bold;
            margin-left: 10px;
            margin-right: 8px;
            font-size: 16pt;
        }
        
        .point-content {
            flex: 1;
            font-size: 15pt;
        }
        
        /* Pied de page amélioré */
        .footer {
            text-align: center;
            margin: 40px auto 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #777;
            font-size: 12pt;
            max-width: 1000px;
        }
        
        /* Bouton d'impression amélioré */
        .print-button {
            position: fixed;
            top: 20px;
            left: 20px;
            padding: 12px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            z-index: 1000;
            font-size: 14pt;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        
        .print-button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Styles d'impression améliorés */
       /* Styles d'impression - Même style et couleurs */
@media print {
    /* Suppression complète des marges et en-têtes/pieds de page */
    @page {
        size: A4;
        margin: 0 !important;
        padding: 0 !important;
        @top-left { content: none !important; }
        @top-center { content: none !important; }
        @top-right { content: none !important; }
        @bottom-left { content: none !important; }
        @bottom-center { content: none !important; }
        @bottom-right { content: none !important; }
    }
    
    /* Styles du body - aucune marge externe */
    body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        background-color: #f9f9f9 !important;
        font-size: 16pt !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* Conteneur principal */
    body > *:not(.print-button) {
        margin: 0 !important;
        padding: 20px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Masquer le bouton d'impression et les liens blob */
    .print-button,
    a[href^="blob:"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
    }
    
    /* Conserver tous les styles visuels */
    .header {
        background: linear-gradient(135deg, #2c3e50, #3498db) !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        padding: 20px !important;
        margin: 0 !important;
    }
    
    .section {
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        background: white !important;
        padding: 25px !important;
        margin: 0 !important;
        page-break-inside: avoid !important;
    }
    
    /* Styles des groupes */
    .group.treatment .group-title {
        background-color: #e74c3c !important;
        color: white !important;
    }
    
    .group.support .group-title {
        background-color: #f39c12 !important;
        color: white !important;
    }
    
    .group.excellence .group-title {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    
    /* Blocs de solutions */
    .solution-block {
        background: #f8f9fa !important;
        border-right: 4px solid #9b59b6 !important;
    }
    
    .solution-block-title {
        color: #9b59b6 !important;
    }
    
    /* Styles des tableaux */
    th {
        background-color: #f5f5f5 !important;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9 !important;
    }
    
    /* Gestion des sauts de page */
    .page-break {
        page-break-before: always !important;
    }
}

    </style>
</head>
<body>
    <!-- Bouton d'impression (masqué lors de l'impression) -->
    <button class="print-button no-print" onclick="window.print()">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
            <path d="M5 1a2 2 0 0 0-2 2v1h10V3a2 2 0 0 0-2-2H5zm6 8H5a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1z"/>
            <path d="M0 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-1v-2a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2H2a2 2 0 0 1-2-2V7zm2.5 1a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
        </svg>
        طباعة التقرير
    </button>

    <div class="header">
        <h1>تقرير خطة العلاج وأصل الخطأ</h1>
        <div class="date">تاريخ التقرير: {{ date }}</div>
    </div>
    
    <div class="section">
        <h2 class="section-title">المعلومات الأساسية</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">المؤسسة التعليمية:</div>
                <div class="info-value">{{ schoolName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">الأستاذ(ة):</div>
                <div class="info-value">{{ profName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">المستوى الدراسي:</div>
                <div class="info-value">{{ className }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">المادة الدراسية:</div>
                <div class="info-value">{{ matiereName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">المعيار المعتمد:</div>
                <div class="info-value">{{ baremeName }}</div>
            </div>
            {% if sousBaremeName %}
            <div class="info-item">
                <div class="info-label">المعيار الفرعي:</div>
                <div class="info-value">{{ sousBaremeName }}</div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <div class="section groups-container">
        <h2 class="section-title">تصنيف المتعلمين حسب مستوى التحصيل</h2>
        
        <div class="group treatment">
            <h3 class="group-title">مجموعة العلاج (صعوبات كبيرة)</h3>
            <table>
                <thead>
                    <tr>
                        <th>اسم التلميذ(ة)</th>
                        <th>المجموعة</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.treatment %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>مجموعة العلاج</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="group support">
            <h3 class="group-title">مجموعة الدعم (صعوبات متوسطة)</h3>
            <table>
                <thead>
                    <tr>
                        <th>اسم التلميذ(ة)</th>
                        <th>المجموعة</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.support %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>مجموعة الدعم</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="group excellence">
            <h3 class="group-title">مجموعة التميز (تحصيل جيد)</h3>
            <table>
                <thead>
                    <tr>
                        <th>اسم التلميذ(ة)</th>
                        <th>المجموعة</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.excellence %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>مجموعة التميز</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="section">
    <h2 class="section-title">تحليل الأخطاء واقتراحات العلاج</h2>
    
    <div class="solution-block">
        <h3 class="solution-block-title">الحلول المقترحة</h3>
        {% for item in solutions_unified.solution %}
        <div class="solution-point">
            <span class="point-number">{{ loop.index }}.</span>
            <span class="point-content">{{ item }}</span>
        </div>
        {% else %}
        <p>لا توجد حلول متاحة</p>
        {% endfor %}
    </div>

    <div class="solution-block">
        <h3 class="solution-block-title">تحليل الأخطاء</h3>
        {% for item in solutions_unified.probleme %}
        <div class="solution-point">
            <span class="point-number">{{ loop.index }}.</span>
            <span class="point-content">{{ item }}</span>
        </div>
        {% else %}
        <p>لا توجد تحليلات للأخطاء متاحة</p>
        {% endfor %}
    </div>
</div>
    
    
    <div class="footer">
        <p>تم إنشاء هذا التقرير آلياً - جميع الحقوق محفوظة © {{ date[:4] }}</p>
    </div>

    <script>
        window.onload = function() {
            // Option d'impression automatique
            // setTimeout(window.print, 1000);
        };
    </script>
    
</body>
</html>
'''
def unify_solutions(data):
    """Élimine les doublons et nettoie les solutions"""
    def clean_text(text):
        if not text:
            return []
        text = text.replace('ـ', '').replace('●', '').replace('★', '').strip()
        return [line.strip() for line in text.split('\n') if line.strip()]
    
    # Utilisation d'un set pour éliminer les doublons
    solutions = set()
    problemes = set()

    # Traitement des données par défaut
    default = data['solutions'].get('default', {})
    for item in clean_text(default.get('solution', '')):
        solutions.add(item)
    for item in clean_text(default.get('probleme', '')):
        problemes.add(item)

    # Traitement des propositions utilisateur
    for prop in data['solutions'].get('userProposals', []):
        if 'solution' in prop:
            for item in clean_text(prop['solution']):
                solutions.add(item)
        if 'probleme' in prop:
            for item in clean_text(prop['probleme']):
                problemes.add(item)

    # Traitement des propositions globales
    for prop in data['solutions'].get('globalProposals', []):
        if 'solution' in prop:
            for item in clean_text(prop['solution']):
                solutions.add(item)
        if 'probleme' in prop:
            for item in clean_text(prop['probleme']):
                problemes.add(item)

    return {
        'solution': [s for s in solutions if s],
        'probleme': [p for p in problemes if p]
    }
@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['schoolName', 'profName', 'className', 
                         'matiereName', 'baremeName', 'groups', 'solutions']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Unification des solutions
        solutions_unified = unify_solutions(data)

        context = {
            'date': datetime.now().strftime('%Y/%m/%d à %H:%M'),
            'schoolName': data['schoolName'],
            'profName': data['profName'],
            'className': data['className'],
            'matiereName': data['matiereName'],
            'baremeName': data['baremeName'],
            'sousBaremeName': data.get('sousBaremeName', ''),
            'groups': {
                'treatment': [{'name': name} for name in data['groups'].get('treatment', [])],
                'support': [{'name': name} for name in data['groups'].get('support', [])],
                'excellence': [{'name': name} for name in data['groups'].get('excellence', [])]
            },
            'solutions_unified': solutions_unified
        }

        html_content = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)