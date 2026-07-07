from workers import WorkerEntrypoint, Response
from collections import namedtuple
import json
import requests
from bs4 import BeautifulSoup

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
        
        links = self.GetNcscContent
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
            for i, article in enumerate(links):
                articles[i] = article


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
    
    def GetNcscContent():
        response = requests.get("https://www.ncsc.gov.uk/section/keep-up-to-date/reports-advisories")
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.find('li', class_="pl-fl-sm")
        links = []
        if content:
            for link in content.find_all('a'):
                links.append(link)
        else:
            return links
        
        return links
        