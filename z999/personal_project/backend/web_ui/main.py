# Import app config
from web_ui.app_config import app, session

from engines.hosts import get_hosts, add_host
from engines.forms import SearchForm
from utils.tools import match_regex, print_exception


from flask import request, render_template, abort

import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    res_hosts = []
    # get the current date and time
    now = datetime.datetime.now()
    hosts_states = get_hosts()
    form = SearchForm()
    if request.method == "POST":
        name = form.name.data
        res_hosts = [ v for v in hosts_states if match_regex(name, v["hostname"]) ]
    else:
        res_hosts = hosts_states
    if len(res_hosts) > 0:
        return render_template('index.html', hosts=res_hosts, now=now, request=request, 
                               form=form)
    return render_template('no_host.html')


@app.route('/host/<hostname>', methods=['POST'])
def host(hostname):
    try:
        res_dict = request.get_json()
        add_host(hostname, res_dict)
        return "i am ok", 200
    except Exception as e:
        print_exception(request.path, repr(e))
        return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def show_exception_page(e):
    return render_template('500.html'), 500
