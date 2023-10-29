from flask import render_template,Flask


def handle_error(app:Flask):
    @app.errorhandler(404)
    def not_found(error):
        return render_template('notfound.html'), 404
    
    @app.errorhandler(403)
    def not_allowed(error):
        return render_template('NotAllowed.html'), 403
    
    @app.errorhandler(401)
    def contact_branch(error):
        return render_template('contactBranch.html') , 401
    return app
