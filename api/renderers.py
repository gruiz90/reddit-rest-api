from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data and 'error' in data:
            response_data = data
        else:
            response_data = {'data': data}
        # call super to render the response
        response = super(CustomJSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )

        return response
