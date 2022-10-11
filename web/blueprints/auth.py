
from flask        import Blueprint, redirect, request
from flask_login  import current_user, login_user, UserMixin
from urllib.parse import quote
from zenora       import APIClient
from lib.Config        import Configuration
from lib.DatabaseLayer import DatabaseLayer
from lib.objects       import User

# Required vars
app_auth = Blueprint('app_auth', __name__, url_prefix="/auth")
conf     = Configuration()
dbl      = DatabaseLayer()

# Discord OAUTH
_REDIRECT_URI_ = f"{conf.web_url}/auth/discord/callback"
_D_OAUTH_URL_  = f"https://discord.com/api/oauth2/authorize?client_id={conf.discord_bot_id}&redirect_uri={quote(_REDIRECT_URI_)}&response_type=code&scope=identify"
d_oauth = APIClient(conf.discord_bot_key, client_secret=conf.discord_bot_secret)

class UserNotFoundError(Exception):
    pass

class AppUser(UserMixin):
    def __init__(self, id=None, discord_id=None, display_name=None):
        print(id, discord_id, display_name)
        # Try to get the user:
        user = None
        if id:           user = dbl.users.get_by_id(id)
        elif discord_id: user = dbl.users.get_by_discord_id(discord_id)
        # Create discord user if not exist
        if discord_id and not user:
            user = User(discord_id=discord_id, image_url=None, preferred_language_id=1)
            try:
                id = dbl.users.add(user)
                print(f"User with Discord ID {id} added")
                user.id = id
                print(user); print(type(user))
            except Exception as e:
                user = None
                print(f"Couldn't add user with Discord ID {id}. Reason: {e}")

        # create user
        if user:
            self.id           = user.id
            self.display_name = user.charter_name or display_name
            self.discord_id   = user.discord_id
            self.charter_name = user.charter_name
            self.image_url    = user.image_url
            self.email        = user.email
            self.about        = user.about
            self.pref_diff    = user.preferred_difficulty
            self.pref_lang    = user.preferred_language
        else:
            raise UserNotFoundError()

    @classmethod
    def get(self, id=None, discord_id=None, display_name=None):
        try:
            return self(id, discord_id, display_name)
        except UserNotFoundError:
            return None


def load_user(id):
    if isinstance(id, str):
        try:
            id = str(id)
        except:
            id = None
    return AppUser.get(id=id, discord_id=None, display_name=None)


@app_auth.route('/discord', methods=['GET'])
def discord_login():
    return redirect(_D_OAUTH_URL_)


@app_auth.route('/discord/callback', methods=['GET'])
def oauth_callback():
    code = request.args["code"]
    access_token = d_oauth.oauth.get_access_token(
                     code, redirect_uri=_REDIRECT_URI_).access_token
    bearer  = APIClient(access_token, bearer=True)
    account = bearer.users.get_current_user()
    user    = AppUser.get(id=None, discord_id=account.id, display_name=None)
    if user:
        login_user(user)
    return redirect('/profile')
