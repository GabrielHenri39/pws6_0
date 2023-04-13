import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def password_is_valid(request, password, confirm_password):
    """
    Verifica se a senha é válida.

    Parâmetros:
    request -- O objeto de requisição do Django
    password -- A senha a ser validada
    confirm_password -- A confirmação da senha

    Retorna:
    True se a senha for válida, False caso contrário
    """

    if len(password.strip()) < 8:
        messages.add_message(request, constants.ERROR,
                             'Sua senha deve conter 8 ou mais caracteres')
        return False

    if not password.strip() == confirm_password:
        messages.add_message(request, constants.ERROR,
                             'As senhas não coincidem!')
        return False

    if not re.search(r'[A-Z]', password.strip()):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém letras maiúsculas')
        return False

    if not re.search(r'[a-z]', password.strip()):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém letras minúsculas')
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.strip()):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém caracteres especiais')
        return False

    return True


def email_html(path_template: str, assunto: str, destinatarios: list, **kwargs) -> bool:
    """
    Envia um email em formato HTML.

    Parâmetros:
    path_template -- O caminho para o modelo HTML
    assunto -- A linha de assunto do email
    destinatarios -- Uma lista de endereços de email para enviar o email
    kwargs -- Quaisquer argumentos de palavra-chave a serem usados no modelo

    Retorna:
    True se o email for enviado com sucesso, False caso contrário
    """
    try:
        html_content = render_to_string(path_template, kwargs)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            assunto, text_content, settings.EMAIL_HOST_USER, destinatarios)

        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return False
