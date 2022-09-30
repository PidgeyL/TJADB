from flask  import Blueprint, render_template
from zenora import APIClient
from lib.Config import Configuration

conf     = Configuration()
d_api    = APIClient(conf.discord_bot_key)
app_disc = Blueprint('discord_data', __name__, url_prefix="")

@app_disc.route('/thanks')
def get_sponsor_profiles():
    sponsors = []
    ids = [] # TODO: change to db call
    for id in ids:
        try:
            u  = d_api.users.get_user(id)
            sponsors.append( {'name': u.username, 'pfp_url': u.avatar_url} )
        except Exception as e:
            print(f"Error getting info for {id}")
            print(e)
    print(sponsors)
    return render_template('subpages/thanks.html', accounts=sponsors)
