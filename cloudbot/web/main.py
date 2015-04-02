import cloudbot

from tornado import gen
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.platform.asyncio import AsyncIOMainLoop

from jinja2 import Environment, PackageLoader

wi = None


def get_template_env():
    env = Environment(loader=PackageLoader('cloudbot.web'))
    return env


def get_application():
    app = Application([
        (r'/', TestHandler),
        (r"/s/(.*)", StaticFileHandler, {"path": "./cloudbot/web/static"}),
    ])
    return app


class TestHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        template = wi.env.get_template('basic.html')
        args = {
            'bot_name': wi.config.get('bot_name', 'CloudBot'),
            'bot_version': cloudbot.__version__,
            'heading': 'Placeholder Page',
            'text': 'Lorem ipsum!'
        }
        self.write(template.render(**args))


class WebInterface():
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config.get('web', {})

        self.port = self.config.get('port', 8090)
        self.address = self.config.get('address', '0.0.0.0')

        self.env = get_template_env()

        self.app = None

        global wi
        wi = self

        # Install tornado IO loop.
        AsyncIOMainLoop().install()

    def start(self):
        """ Starts the CloudBot web application """
        self.app = get_application()
        self.app.listen(self.port, address=self.address)