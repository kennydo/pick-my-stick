import json
import mimetypes

import tornado.web
from tornado.httpclient import (
    AsyncHTTPClient,
    HTTPRequest,
)
from tornado.httputil import url_concat


URL_PREFIX = 'https://wakaba.hanekawa.net/pickermysticker'


class PackListHandler(tornado.web.RequestHandler):
    def get(self):
        slack_response_url = self.get_query_argument('slack_response_url', default='')
        pack_ids = self.application.sticker_store.list_pack_ids()
        self.write("Hello, here are the packs I know:<br />")
        for pack_id in pack_ids:
            pack_url = url_concat(URL_PREFIX + '/packs/' + pack_id, {
                'slack_response_url': slack_response_url,
            })
            self.write("<a href='{pack_url}'>{pack_id}</a><br />".format(pack_url=pack_url, pack_id=pack_id))


class PackHandler(tornado.web.RequestHandler):
    def get(self, pack_id: str):
        slack_response_url = self.get_query_argument('slack_response_url', default='')
        sticker_ids = self.application.sticker_store.list_sticker_ids(pack_id)
        self.write("Here are the sticker IDs for pack {0}:<br />".format(pack_id))
        for sticker_id in sticker_ids:
            send_sticker_url = url_concat(URL_PREFIX + '/packs/' + pack_id + '/stickers/' + sticker_id + '/send', {
                'slack_response_url': slack_response_url,
            })
            self.write("<a href='{send_sticker_url}'>{sticker_id}</a><br />".format(send_sticker_url=send_sticker_url, sticker_id=sticker_id))


class SendStickerHandler(tornado.web.RequestHandler):
    def get(self, pack_id: str, sticker_id: str):
        slack_response_url = self.get_query_argument('slack_response_url', default='')
        sticker_path = self.application.sticker_store.get_sticker_path_by_id(pack_id, sticker_id)

        http_client = AsyncHTTPClient()


        body = {
            'attachments': [
                {
                    "text": "Pack {pack_id} sticker {sticker_id}".format(pack_id=pack_id, sticker_id=sticker_id),
                    "image_url": URL_PREFIX + '/packs/' + pack_id + '/stickers/' + sticker_id,
                },
            ]
        }

        slack_request = HTTPRequest(
            slack_response_url,
            method='POST',
            headers={
                'Content-Type': 'application/json',
            },
            body=json.dumps(body),
        )
        http_client.fetch(slack_request)

        self.write("Sending sticker to slack!")
        self.write(json.dumps(body))


class StickerHandler(tornado.web.RequestHandler):
    def get(self, pack_id: str, sticker_id: str):
        sticker_path = self.application.sticker_store.get_sticker_path_by_id(pack_id, sticker_id)

        mime_type, encoding = mimetypes.guess_type(sticker_path)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        with open(sticker_path, 'rb') as f:
            self.write(f.read())


class SlashCommandHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_query_argument('token', default='')
        response_url = self.get_query_argument('response_url', default='')

        pack_url = url_concat(
            URL_PREFIX + '/packs',
            {
                'slack_response_url': response_url,
            }
        )

        immediate_response = {
            'response_type': 'ephemeral',
            'text': 'Click <{pack_url}|here> to pick a sticker'.format(pack_url=pack_url),
            'unfurl_links': False,
        }

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(immediate_response))
