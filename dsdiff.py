import bottle
import hashlib
from base64 import b64encode
from lxml import etree

def linebreaks(string):
    return bottle.html_escape(string).replace('\n', '<br>')

@bottle.route('/xml', method='POST')
def x():
    h = hashlib.md5()
    body = bottle.request.body.read()
    h.update(body)
    digest = b64encode(h.digest()).decode('utf-8')

    with open(f'temp/{digest}.xml', 'wb') as f:
        f.write(body)

    return digest

@bottle.route('/<filename>/xml', method='GET')
def xml_get(filename):
    bottle.response.headers['Content-Type'] = 'text/xml'
    with open(f'temp/{filename}.xml') as f:
        return f.read()

@bottle.route('/<filename>/html', method='GET')
def html_get(filename):
    tree = etree.parse(f'temp/{filename}.xml')
    changes = []

    for prop in tree.findall('.//Property'):
        path = tree.getpath(prop).split('/')
        result = []
        for i in range(1, len(path) + 1):
            subpath = '/'.join(path[:i])
            name = tree.xpath(f"{subpath}/@name")
            if name:
                tag = tree.xpath(subpath)[0].tag
                result.append(f'{name[0]} ({tag})')
        breadcrumb = ' > '.join(result)

        change = prop.get('changetype')
        if change == 'Change':
            changes.append({'path': breadcrumb,
                            'left': prop.find('Was').text,
                            'right': prop.find('Now').text})
        elif change == 'Remove':
            changes.append({'path': breadcrumb,
                            'left': 'Removed',
                            'right': ''})
        else:
            print(etree.tostring(prop))

    tpl = bottle.SimpleTemplate(name='table.tpl', escape_func=linebreaks)
    return tpl.render(file=filename, changes=changes)

bottle.run(host='localhost', port=8080, reloader=True)