from workers import WorkerEntrypoint, Response, fetch
from collections import namedtuple
import json
from html.parser import HTMLParser

Status = namedtuple("Status", ["code", "message"])

errBadRequest = Status(400, "Bad Request")
errUnprocessableEntity = Status(422, "Unprocessable Entity")
errInternalServer = Status(500, "Internal Server Error")
errNotFound = Status(404, "Not Found")
statusOk = Status(200, "OK")


class Default(WorkerEntrypoint):

    async def fetch(self, request):
        if request.method != "GET":
            code = errBadRequest.code
            msg = errBadRequest.message

            return Response(
                json.dumps({"error": msg}),
                status=code,
                status_text=msg,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        links = await GetNcscContent()
        if not links:
            
            code = errInternalServer.code
            msg = errInternalServer.message

            return Response(
                json.dumps({"error": msg}),
                status=code,
                status_text=msg,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        elif links:

            code = statusOk.code
            msg = statusOk.message

            articles = {}
            for i in range(0<len(links)):
                articles[i] = links[i]


            return Response(
                json.dumps({
                    "articles": articles
                }),
                status=code,
                status_text=msg,
                headers={
                    "Content-Type": "application/json"
                }
            )
    



class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_target_li = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "li":
            classes = attrs.get("class", "")
            if "pl-fl-sm" in classes.split():
                self.in_target_li = True

        elif self.in_target_li and tag == "a":
            self.links.append(attrs.get("href"))

    def handle_endtag(self, tag):
        if tag == "li" and self.in_target_li:
            self.in_target_li = False


async def GetNcscContent():
    response = await fetch(
        "https://www.ncsc.gov.uk/section/keep-up-to-date/reports-advisories"
    )

    html = await response.text()

    parser = LinkExtractor()
    parser.feed(html)

    return parser.links
        