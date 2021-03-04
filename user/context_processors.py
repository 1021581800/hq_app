from .forms import LoginForm
#公共映射
def login_modal_form(request):
    return {'login_modal_form': LoginForm()}