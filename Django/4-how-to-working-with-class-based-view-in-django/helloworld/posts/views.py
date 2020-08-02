from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class PostList(TemplateView):
    template_name = 'post_list.html'

    def get_context_data(self):
        context = {
            'title': 'Post overview',
            'description': 'A little list of all the post we got from the database.'
        }

        return context


class PostDetail(View):
    def get(self, request, number):
        return render(request, 'post_detail.html', {
            'number': number
        })
