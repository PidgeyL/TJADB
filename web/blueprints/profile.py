
from flask        import Blueprint, render_template, request, flash, redirect, url_for
from flask_login  import current_user, login_required

from lib.DatabaseLayer import DatabaseLayer

app_profile = Blueprint('profile', __name__, url_prefix="/profile",
                        template_folder='templates/profile')
dbl  = DatabaseLayer()

@login_required
@app_profile.route('/', methods=['GET'])
def profile():
    songs = dbl.songs.get_by_charter_id(current_user.id)
    return render_template('profile/index.html', user=current_user, songs=songs)

@login_required
@app_profile.route('/update', methods=['POST'])
def update():
    try:
        charter_name = request.form.get('p_c_name').strip()
        email        = request.form.get('p_email').strip()
        about        = request.form.get('p_bio').strip()
        image_url    = request.form.get('p_image').strip()
    except:
        flash("Invalid user input!")
    flash("Profile updated")
    return redirect(url_for('profile.profile'))
