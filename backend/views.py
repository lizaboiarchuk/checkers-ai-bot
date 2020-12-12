import asyncio
import logging

from aiohttp import web

from .game import Game, ForbiddenMoveError, MoveIsNotPossible


class Views:
    def __init__(self):
        self._game = Game()

    @staticmethod
    def _prepare_response(data):
        return web.json_response({
            'status': 'success',
            'data': data
        })

    @staticmethod
    async def health_check(_request):
        return web.json_response({'status': 'healthy'})

    async def connect(self, request):
        if self._game.is_started():
            raise web.HTTPBadRequest(text='Game has already been started')

        try:
            team_name = request.query['team_name']
        except KeyError:
            raise web.HTTPBadRequest(
                text='team_name query parameter is missing'
            )

        logging.info(f'{team_name} connected')
        response = self._game.add_player(team_name)

        while not self._game.is_started():
            await asyncio.sleep(0.1)

        return self._prepare_response(response)

    async def game(self, _request):
        return self._prepare_response(self._game.json)

    async def move(self, request):
        if not self._game.is_started() or self._game.is_finished():
            raise web.HTTPBadRequest(text='You cannot make move right now')

        try:
            header = request.headers["Authorization"]

        except KeyError as exc:
            raise web.HTTPUnauthorized(
                headers={"WWW-Authenticate": "Token"}
            ) from exc

        token = header.split()[1]
        try:
            body = await request.json()
            move = body['move']

        except KeyError:
            raise web.HTTPBadRequest(
                text='move parameter is missing'
            )

        try:
            self._game.move(token, move)
            return self._prepare_response('successful move')

        except ForbiddenMoveError:
            raise web.HTTPForbidden(
                text='invalid token for current player move'
            )
        except MoveIsNotPossible as e:
            raise web.HTTPBadRequest(
                text=str(e)
            )

    def configure(self, app):
        app.router.add_get(
            '/health_check', self.health_check, name='health_check'
        )
        app.router.add_get(
            '/game', self.game, name='get_game'
        )
        app.router.add_post(
            '/game', self.connect, name='connect_to_the_game'
        )
        app.router.add_post(
            '/move', self.move, name='make_game_move'
        )
