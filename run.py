"""Used to define App"""
from aiohttp import web
from controllers.operations import AgentCrud, SystemCrud

URL = '/CrudOperations'

def get_app():
    """
    @description - Used to create database session and calls HTTP methods
    @returns - returns web app
    """

    app = web.Application(debug=True)
    app.router.add_route("*", URL + "/{uuid}", AgentCrud, name="agent_view")
    app.router.add_route("*", URL + "/agent", AgentCrud, name="agent")
    app.router.add_route("*", URL + "/system", SystemCrud, name="system")

    return app

if __name__ == '__main__':
    web.run_app(get_app())
