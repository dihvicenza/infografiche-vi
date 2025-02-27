from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html


from source.content import *
from source.functions import prepare_data, make_graph, app_content

####################
# PARAMETRI INIZIALI
####################
app_list = ["viirs", "ghm", "pvout"]

####################
# IMPLEMENTAZIONE
####################

# Aprire il dataset e fare pre-elaborazione
bd_viirs = body[app_list[0]]
bd_ghm = body[app_list[1]]
bd_pvout = body[app_list[2]]

csv_path_viirs = Path.cwd() / "data" / f"stats_{app_list[0]}.csv"
csv_path_ghm = Path.cwd() / "data" / f"stats_{app_list[1]}.csv"
csv_path_pvout = Path.cwd() / "data" / f"stats_{app_list[2]}.csv"

df_viirs = prepare_data(csv_path_viirs)
df_vi_viirs = df_viirs["df_vi"]
df_100k_viirs = df_viirs["df_100k"]
df_reg_viirs = df_viirs["df_reg"]

df_ghm = prepare_data(csv_path_ghm)
df_vi_ghm = df_ghm["df_vi"]
df_100k_ghm = df_ghm["df_100k"]
df_reg_ghm = df_ghm["df_reg"]

df_ghm = prepare_data(csv_path_pvout)
df_vi_pvout = df_ghm["df_vi"]
df_100k_pvout = df_ghm["df_100k"]
df_reg_pvout = df_ghm["df_reg"]

#########
# WEB APP
#########

# Google Fonts
ext_scripts = [{"src": "https://kit.fontawesome.com/798fa6dddc.js",
                "crossorigin": "anonymous"}]
ext_stylesheets = [
        {"href": "https://fonts.gstatic.com", "rel": "preconnect"},
        {"href": "https://fonts.googleapis.com/css2?family=Roboto+Condensed:"
                 "wght@300;400;700&family=Roboto:wght@300;400;700&display=swap",
         "rel": "stylesheet"}
]

app = dash.Dash(name=__name__,
                title="InnovationLab Vicenza | Web App per il Vicentino sulla base di Open Data Geospaziali",
                update_title="Caricamento...",
                assets_folder="static",
                assets_url_path="static",
                meta_tags=[
                        # A description for search engines
                        {
                                "name": "description",
                                "content": "Web app del progetto InnovationLab Vicenza."
                        },
                        # For IE, use the latest renderer available (e.g. Edge)
                        {
                                "http-equiv": "X-UA-Compatible",
                                "content": "IE=edge"
                        },
                        # A tag necessary for "true" mobile support.
                        {
                                "name": "viewport",
                                "content": "width=device-width, initial-scale=1.0"
                        }
                ],
                external_stylesheets=ext_stylesheets,
                external_scripts=ext_scripts,
                # avoid an exception, which warns us that we might be doing something wrong
                suppress_callback_exceptions=True
                )

# Grafici

fig_vi_viirs = make_graph(df_vi_viirs, "Comuni in provincia di Vicenza", "Brillanza", "nW/cm²·sr")
fig_100k_viirs = make_graph(df_100k_viirs, "Comuni italiani con più di 100000 abitanti", "Brillanza", "nW/cm²·sr")
fig_reg_viirs = make_graph(df_reg_viirs, "Capoluoghi regionali", "Brillanza", "nW/cm²·sr")

fig_vi_ghm = make_graph(df_vi_ghm, "Comuni in provincia di Vicenza", "Indice gHM", "")
fig_100k_ghm = make_graph(df_100k_ghm, "Comuni italiani con più di 100000 abitanti", "Indice gHM", "")
fig_reg_ghm = make_graph(df_reg_ghm, "Capoluoghi regionali", "Indice gHM", "")

fig_vi_pvout = make_graph(df_vi_pvout, "Comuni in provincia di Vicenza", "Potenziale solare fotovoltaico annuo", "kWh/m²")
fig_100k_pvout = make_graph(df_100k_pvout, "Comuni italiani con più di 100000 abitanti", "Potenziale solare fotovoltaico annuo", "kWh/m²")
fig_reg_pvout = make_graph(df_reg_pvout, "Capoluoghi regionali", "Potenziale solare fotovoltaico annuo", "kWh/m²")

# App content
web_app_title = "Web App - InnovationLab Vicenza"

app_header = html.Div(
        children=[
                html.H1([html.I(className="fa fa-laptop"), " ", web_app_title]),
                html.Div(children=[
                        html.Img(alt="Logo dell'InnovationLab Vicenza",
                                 src="static/img/logo-innovationlab.png",
                                 className="img-center")],
                        style={"width": "100%", "text-align": "center"}),
                html.Div(className="", children=[
                dcc.Markdown(bando),
                dcc.Markdown(children="![Logo InnovationLab Vicenza](static/img/logos.png)",
                             className="img-logo"),
                dcc.Markdown(className="right-align",
                             children=">A cura del [Digital Innovation Hub Vicenza]"
                                      "(https://digitalinnovationhubvicenza.it/)")
                        ]),
                html.Hr()
        ]
)

app.layout = html.Div([
    dcc.Location(id="url", refresh=True),
    html.Div(id="page-content", children=[])
])

not_found_page = html.Div([
        html.Div(className="container", children=[
                html.H1([html.I(className="fa fa-laptop"),
                         " ",
                         "Web App - InnovationLab Vicenza"]),
                html.Div(className="h2 warning", children=[
                        "Errore: Pagina non trovata",
                        html.Br(),
                        "Sembra che non ci sia nulla a questo indirizzo."
                ]),
                dcc.Markdown(className="central-align",
                             children="Torna alla [Pagina Iniziale](/).")
        ])
])

index_page = html.Div(className="container", children=[
        app_header,

        html.Div(className="gallery",
                 children=[
                        dcc.Link(html.Img(src="static/img/italy-night-200px.jpg",
                                          alt="Inquinamento luminoso"),
                                 href="/inquinamento-luminoso"),
                        html.Div("Inquinamento luminoso", className="desc")
                ]
        ),

        html.Div(className="gallery",
                 children=[
                         dcc.Link(html.Img(src="static/img/fotovoltaici-tetto-200px.jpg",
                                           alt="Potenziale fotovoltaico"),
                                  href="/fotovoltaico"),
                         html.Div("Potenziale fotovoltaico", className="desc")
                 ]
                 ),

        html.Div(className="gallery",
                 children=[
                         dcc.Link(
                             html.Img(src="static/img/vicenza-300px.jpg",
                                      alt="Pressione antropica"),
                             href="/pressione-antropica"),
                         html.Div("Pressione antropica", className="desc")
                 ]
                 ),
        html.Div(className="homepage fade-in")
])

viirs_page = app_content(bd_viirs, fig_vi_viirs, fig_100k_viirs, fig_reg_viirs)
ghm_page = app_content(bd_ghm, fig_vi_ghm, fig_100k_ghm, fig_reg_ghm)
pvout_page = app_content(bd_pvout, fig_vi_pvout, fig_100k_pvout, fig_reg_pvout)


# Fill the page content
@app.callback(dash.dependencies.Output("page-content", "children"),
              [dash.dependencies.Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return index_page
    elif pathname == "/inquinamento-luminoso":
        return viirs_page
    elif pathname == "/pressione-antropica":
        return ghm_page
    elif pathname == "/fotovoltaico":
        return pvout_page
    else:
        return not_found_page


application = app.server
if __name__ == '__main__':
    application.run(port=80, debug=False)
