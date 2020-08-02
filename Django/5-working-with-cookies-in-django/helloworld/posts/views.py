from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def set_cookie_demo_page(request):
    response = render(request, 'set-cookie-page.html')

    response.set_cookie('demo-cookie', 'this cookie set from set-cookie-page', max_age=5)

    return response


class PostList(TemplateView):
    template_name = 'post_list.html'

    def get_context_data(self):
        post_list = [{
            'id': 1,
            'title': 'Post sample 1'
        }, {
            'id': 2,
            'title': 'Post sample 2'
        }, {
            'id': 3,
            'title': 'Post sample 3'
        }, {
            'id': 4,
            'title': 'Post sample 4'
        }]

        context = {
            'title': 'Post overview',
            'description': 'A little list of all the post we got from the database.',
            'posts': post_list,
            'cookie_data': self.request.COOKIES['demo-cookie'] if 'demo-cookie' in self.request.COOKIES else ''
        }

        return context


class PostDetail(TemplateView):
    template_name = 'post_detail.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(PostDetail, self).render_to_response(context, **response_kwargs)
        response.set_cookie('last-visit-post-id', context['number'])

        return response
