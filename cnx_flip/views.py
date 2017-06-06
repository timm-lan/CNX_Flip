from pyramid.view import view_config

@view_config(route_name='home', renderer = 'templates/index.html.jinja2')
def my_view(request):
    return {'project': 'cnx_flip'}

@view_config(route_name='add_card', renderer = 'templates/success.html.jinja2')
def success_add_card_view(request):
    return {'project': 'cnx_flip'}


# @view_config(route_name='generate_ajax_data', renderer='json')
# def my_ajax_view(request):
#     return {'message': "Hello"}
# 
# @view_config(route_name='home', renderer='templates/mytemplate.jinja2')
# def my_view(request):
#     return {'project': 'cnx_flip'}
