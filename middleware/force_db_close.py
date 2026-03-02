from django.db import connections


class ForceDBConnectionCloseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Before request: close previous connection
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()

        response = self.get_response(request)

        # After request: close specific conn
        for conn in connections.all():
            conn.close()

        return response
