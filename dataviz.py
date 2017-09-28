# coding=utf-8
from abc import ABCMeta, abstractmethod
from flask import Flask, render_template, Response
from jinja2 import Environment
import sass
import os


class DatavizElement:
    __metaclass__ = ABCMeta

    @abstractmethod
    def html(self):
        return ""

    @abstractmethod
    def js(self):
        return ""

    def render(self):
        self.rendered_html = self.html()
        self.rendered_js = self.js()


class DatavizTitle(DatavizElement):
    def __init__(self, text):
        self.text = text

    def html(self):
        return "<h1>%s</h1>" % self.text

    def js(self):
        return ""


class DatavizGraph(DatavizElement):
    def __init__(self, graph, html_id):
        self.graph = graph
        self.html_id = html_id

    def html(self):
        # return "<div id='%s'></div>" % self.html_id
        return "<div class='chart'><img src='charts/%s.svg'></div>" % self.html_id

    def js(self):
        # res = "render_graph('#%s', %s);" % (self.html_id, self.graph.to_json())
        # return res
        return ""

    def save(self):
        self.graph.savechart('dataviz-out/charts/%s.svg' % self.html_id)


class DatavizSection(DatavizElement):
    def __init__(self, template_path, args):
        self.args = args
        self.template_path = template_path

    def html(self):
        with open(self.template_path) as f:
            return Environment().from_string(f.read()).render(self.args)

    def js(self):
        return ""


class Dataviz(object):
    def __init__(self, title):
        self.title = title

        self.sections = []
        self.graphs = []

        self.next_id = 1

    def add_title(self, text):
        self.sections.append(DatavizTitle(text))

    def _add_graph(self, graph):
        html_id = "viz_%d" % self.next_id
        self.next_id += 1

        tmp = DatavizGraph(graph, html_id)
        self.graphs.append(tmp)
        return tmp

    def add(self, template, **args):
        template_path = "section_templates/%s.html" % template

        if "charts" in args:
            args["charts"] = [self._add_graph(chart) for chart in args["charts"]]

        self.sections.append(DatavizSection(template_path, args))

    def to_html(self):
        for g in self.graphs:
            g.save()
            g.render()

        for s in self.sections:
            s.render()

        with open("templates/template.html") as f:
            return Environment().from_string(f.read()).render(**self.__dict__)

    def render(self):
        if not os.path.exists("dataviz-out/charts"):
            os.makedirs("dataviz-out/charts")

        with open("dataviz-out/index.html", "w") as f:
            f.write(self.to_html())

    def serve(self):
        self.render()

        app = Flask(__name__, static_folder="dataviz-out", static_url_path="")

        @app.route("/style.css")
        def style():
            with open("style.scss") as f:
                res = sass.compile(string=f.read())
                return Response(res, mimetype='text/css')

        @app.route('/')
        def hello_world():
            return app.send_static_file("index.html")

        app.run(port=8080)

