from workers import WorkerEntrypoint, Response
from collections import namedtuple
import json

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

        code = statusOk.code
        msg = statusOk.message

        return Response(
            json.dumps({
                "article": "Modern world imbalanced with nature?"
            }),
            status=code,
            status_text=msg,
            headers={
                "Content-Type": "application/json"
            }
        )