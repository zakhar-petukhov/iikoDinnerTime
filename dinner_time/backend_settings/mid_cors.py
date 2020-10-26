from django.utils.deprecation import MiddlewareMixin


class CrossOriginAccessControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
        response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, Access-Control-Allow-Origin, Authentication"
        response['Access-Control-Allow-Origin'] = "*"
        return response
