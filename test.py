# coding=utf-8
from dataviz import Dataviz
from altair import Chart, load_dataset, X, Y

df = load_dataset('seattle-weather')

dataviz = Dataviz("Seattle Weather")

overview_chart = Chart(df).mark_bar(stacked='normalize').encode(
    X('date:T', timeUnit='month'),
    Y('count(*):Q'),
    color='weather',
)

dataviz.add("commented", title="Overview", charts=[overview_chart],
            comment= "Lorem ipsum dolor sit amet, cum pertinacia definitionem an. His ne oratio facilis voluptatum, nam lorem putant qualisque ad. Mea in affert nostrum. Mea cu ignota adipiscing. Omnis mnesarchum vix cu, omnes impedit democritum nec te. Malorum urbanitas consectetuer ei eam, no sea paulo tollit detracto."
            )

chart_a = Chart(df).mark_bar().encode(
    X('precipitation', bin=True),
    Y('count(*):Q')
)

chart_b = Chart(df).mark_line().encode(
    X('date:T', timeUnit='month'),
    Y('average(precipitation)')
)

chart_c = Chart(df).mark_line().encode(
    X('date:T', timeUnit='month'),
    Y('average(temp_max)'),
)

dataviz.add("titled", title="Precipitations", charts=[chart_a, chart_b, chart_c])


dataviz.serve()