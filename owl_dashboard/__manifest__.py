{
    "name":  "Owl Dashboard",
    "version": '1.0',
    "summary": 'OWL dashboard',
    "data": [
        'views/sales_dashboard.xml',
    ],
    'depends': ['base', 'web', 'sale', 'board'],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_dashboard/static/src/components/**/*.js',
            'owl_dashboard/static/src/components/**/*.xml',
            'owl_dashboard/static/src/components/**/*.scss'
        ]
    },
    "license": "LGPL-3"
}
