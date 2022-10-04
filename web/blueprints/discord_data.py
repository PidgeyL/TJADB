from flask  import Blueprint, render_template
from lib.Config    import Configuration
from lib.functions import discord_profile

conf     = Configuration()
app_disc = Blueprint('discord_data', __name__, url_prefix="")

@app_disc.route('/thanks')
def get_sponsor_profiles():
    sponsors = {}
    for key, value in conf.sponsors.items():
        sponsors[key] = []
        for id in value:
            try:
                sponsors[key].append(discord_profile(id))
            except:
                print(f"Error getting info for {id}")

    return render_template('subpages/thanks.html', accounts=sponsors)
