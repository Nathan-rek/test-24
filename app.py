from flask import Flask , send_from_directory
from flask_flatpages import FlatPages
from flask import render_template
import os

FLATPAGES_EXTENSION = '.md'
FLATPAGES_AUTO_RELOAD = True

app = Flask(__name__) 
app.config['APPLICATION_ROOT'] = '/myproject'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLATPAGES_MARKDOWN_EXTENSIONS = ['extra']
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {
        'linenums': 'True'
    }
}



app.config.from_object(__name__)
pages = FlatPages(app)
application = app
pages.get('foo')



def Liste_cat(): #fonction qui parcour tout les pages
    articles = (p for p in pages if 'published' in p.meta) # Liste de tout les articles (pages = FlatPages(app)) si il y a Published dans les meta 
    catList = []
    for a in articles: # pour chacun des articles
        catList.append(a.meta['cat']) #dés qu'il y a une categorie on va l'ajouter a la liste
    catList = list(dict.fromkeys(catList)) # retirer les doublons
    return catList 

def imagelist(articlename):
    dir_path = os.path.dirname(os.path.realpath(articlename))+'/pages/' #
    gallery_path = os.path.join(dir_path, articlename)
    if os.path.exists(gallery_path):
        images = [f for f in os.listdir(gallery_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif') or f.endswith('.svg')]
        return gallery_path ,images
    else:
        return None, None


@app.route('/') #
def index():
    # Articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    latest = sorted(articles, reverse=True, # faire une liste acronologique
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()  # variable qui stock la liste des categories
    return render_template('index.html', articles=latest , catList=catList  ) # renvoi au client une mise en page avec une liste d'article et de categories

@app.route('/<path:path>')
def page(path):
    page = pages.get_or_404(path)
    catList = Liste_cat()
    g_path, imgs = imagelist(path)
    if imgs:
        return render_template('single.html', page=page ,catList=catList  , g_path=g_path, imgs = imgs)
    else :
        return render_template('single.html', page=page ,catList=catList)

@app.route('/info')
def info():
    page = pages.get_or_404('info')
    catList = Liste_cat()
    return render_template('staticpage.html', page=page , catList=catList)

@app.route('/cat/<catname>') #
def catPage(catname):
    articles = (p for p in pages if 'published' in p.meta and 'cat' in p.meta and p.meta['cat']==catname )
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()
    return render_template('index.html', articles=latest , catList=catList  )

@app.route('/author/<path:authorname>')
def authorPage(authorname):
    author_names = authorname.split('+')
    articles = [p for p in pages if 'published' in p.meta and 'author' in p.meta and p.meta['author'] in author_names]
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    catList = Liste_cat()
    return render_template('index.html', articles=latest , catList=catList)


@app.route('/tags/<path:tags>')
def tagPage(tags):
    tag_names = tags.split(',')
    articles = [p for p in pages if 'published' in p.meta and 'tags' in p.meta and any(tag in p.meta['tags'] for tag in tag_names)]
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
    catList = Liste_cat()
    tag_links = {tag: f"/tags/{tag}" for tag in tag_names} # Ajouter cette ligne pour créer un dictionnaire de liens pour chaque tag
    return render_template('index.html', articles=latest, catList=catList, tag_links=tag_links) # Ajouter la variable tag_links pour être utilisée dans le template




@app.route('/pages/<path:path>')
def serve_pages(path):
    return send_from_directory('pages', path)


@app.errorhandler(404)
def page_not_found(e):
        # note that we set the 404 status explicitly
            return "NOPE NOTHING HERE plz leave now 🛸"

if __name__ == "__main__":
        app.run(host='0.0.0.0')