from flask import render_template,Flask


def handle_error(app:Flask):
    @app.errorhandler(404)
    def not_found(error):
        return render_template('notfound.html'), 404
    
    return app
