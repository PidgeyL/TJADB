
from flask        import Blueprint, render_template, request, flash, redirect, url_for
from flask_login  import current_user, login_required, logout_user, login_user

from lib.DatabaseLayer   import DatabaseLayer
from lib.functions       import is_image_url, _url_for
from lib.objects         import User
from web.blueprints.auth import AppUser

app_profile = Blueprint('profile', __name__, url_prefix="/profile",
                        template_folder='templates/profile')
dbl  = DatabaseLayer()

@login_required
@app_profile.route('/', methods=['GET'])
def profile():
    if not current_user.is_authenticated:
        return redirect(_url_for('app_auth.discord_login'))
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
        return redirect(_url_for('profile.profile'))
    if not is_image_url(image_url):
        image_url=''
    dbl.users.update(User(id=current_user.id, charter_name=charter_name,
                          email=email, about=about, image_url=image_url))
    flash("Profile updated")
    return redirect(_url_for('profile.profile'))
