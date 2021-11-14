from io import BytesIO
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf.pisa import pisaDocument
import uuid




def save_pdf(context:dict):
    '''
           save pdf file
    '''
    template = get_template('invoice.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisaDocument(BytesIO(html.encode("UTF-8")), result)
    file_name = 'Invoice'+str(uuid.uuid4()) + '.pdf'

    try:
        with open(str(settings.BASE_DIR) + f'/public/static/{file_name}','wb+') as output:
            pdf = pisaDocument(BytesIO(html.encode("UTF-8")), output)

    except Exception as e:
        print(e)

    if pdf.err:
        return False
    else:
        return file_name, True