from webapp import application

import os
def runserver():
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    runserver()